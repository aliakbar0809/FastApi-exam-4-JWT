import time 


import jwt
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(token:str):
    return {"access_token":token}

def sign_jwt(user_id: str, role: str):
    payload = {"user_id": user_id, "role": role, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}

def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded["expires"] < time.time():
            return None
        return decoded
    except Exception as e:
        print("decode error:", e)
        return None