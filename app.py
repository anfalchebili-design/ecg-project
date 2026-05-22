from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, User, Patient
from utils import hash_password, verify_password
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'memoir.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------- REGISTER ----------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    if not data:
        return jsonify({"error": "empty data"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "user exists"}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hash_password(data['password'])
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "registered"}), 201


# ---------- LOGIN ----------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get('username')).first()

    if user and verify_password(user.password_hash, data.get('password')):
        return jsonify({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username
            }
        })

    return jsonify({"success": False}), 401


# ---------- PATIENT ----------
@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.json

    patient = Patient(
        full_name=data['full_name'],
        age=data['age'],
        gender=data['gender'],
        phone=data.get('phone', '')
    )

    db.session.add(patient)
    db.session.commit()

    return jsonify({"message": "saved"}), 201


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=10000)