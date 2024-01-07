
import datetime
import os
import jwt

user_data = {
    "username": "john_doe",
    "email": "john_doe@example.com",
    "role": "user"
}

class TokenJWT(object):
    def __init__(self, data=None, token=None):
        self.secret_key = os.getenv("SERVER_KEY")
        self.expire_token = int(os.getenv("EXPIRE_TOKEN"))
        self.token = token
        self.data = data

    def create_jwt_token(self):
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.expire_token)
        data_to_encode = self.data.copy()
        data_to_encode['exp'] = expire_time
        jwt_token = jwt.encode(data_to_encode, self.secret_key, algorithm="HS256")
        return jwt_token

    def validate_jwt_token(self):
        try:
            decoded_token = jwt.decode(self.token, self.secret_key, algorithms=["HS256"])
            return decoded_token, None
        except jwt.ExpiredSignatureError:
            print("Token expired. Please generate a new token.")
            return False, "TOKEN_EXPIRED"
        except jwt.InvalidTokenError:
            print("Invalid token. Please provide a valid token.")
            return False, "INVALID_TOKEN"
