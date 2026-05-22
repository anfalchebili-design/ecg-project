from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """تشفير كلمة المرور"""
    return generate_password_hash(password)

def verify_password(stored_password, provided_password):
    """التحقق من صحة كلمة المرور العادية مقارنة بالمشفرة"""
    return check_password_hash(stored_password, provided_password)