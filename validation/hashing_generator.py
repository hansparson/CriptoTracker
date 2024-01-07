import hashlib
import os

class HashingModels():
    @staticmethod
    def hash_password(password):
        signature_key_pass = os.getenv("PASSWORD_KEY_VALIDATION")
        if isinstance(signature_key_pass, str):
            salt = signature_key_pass.encode('utf-8')  # Mengonversi string ke dalam bytes
        else:
            salt = signature_key_pass  # Jika sudah dalam bentuk bytes, gunakan langsung
        
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        hashed_password_hex = hashed_password.hex()
        
        return hashed_password_hex