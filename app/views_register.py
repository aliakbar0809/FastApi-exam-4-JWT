from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_config import get_my_db
from app.auth.auth_bearer import JWTBearer,decode_jwt
from app.auth.auth_helpers import sign_jwt
from app.helpers import *
from app.models import *
from app.scheme import *

auth = APIRouter()




def get_current_user(payload, db: Session):
    user_id = payload["user_id"]
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@auth.post("/register")
async def register_user(user: UserSchema, db: Session = Depends(get_my_db)):
    exist = db.query(UserModel).filter(UserModel.email == user.email).first()
    if exist:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@auth.post("/login")
async def login_user(user: LoginSchema, db: Session = Depends(get_my_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = sign_jwt(db_user.id, db_user.role.value)
    return token



@auth.post("/logout")
async def logout_user(token: str = Depends(JWTBearer(return_token=True)),db: Session = Depends(get_my_db)):
    blacklisted = TokenBlacklistModel(token=token)
    db.add(blacklisted)
    db.commit()
    return {"message": "Successfully logged out"}
