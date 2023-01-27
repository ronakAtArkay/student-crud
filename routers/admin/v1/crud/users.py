import json
import traceback

import bcrypt
from fastapi import HTTPException, Response, status
from jwcrypto import jwk, jwt
from sqlalchemy import or_
from sqlalchemy.orm import Session

from config import config
from libs.utils import _create_password, generate_id, now
from models import UserModel
from routers.admin.v1.schemas import ChangePassword, UserBase, UserUpdate


def get_token(user_id, email):
    claims = {"id": user_id, "email": email, "time": str(now())}

    # create a signed token with generated key
    key = jwk.JWK(**config["jwt_key"])
    Token = jwt.JWT(header={"alg": "HS256"}, claims=claims)
    Token.make_signed_token(key)

    # Furher encrypt the token with the same key

    encrypted_token = jwt.JWT(
        header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=Token.serialize()
    )
    encrypted_token.make_encrypted_token(key)
    token = encrypted_token.serialize()
    return token


def verify_token(db: Session, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    else:
        try:
            key = jwk.JWK(**config["jwt_key"])
            ET = jwt.JWT(key=key, jwt=token)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            claims = ST.claims
            claims = json.loads(claims)
            db_user = get_user_by_id(db, id=claims["id"])
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        elif db_user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return db_user


def sign_in(db: Session, user: UserBase):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif db_user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    hashed = db_user.password
    hashed = bytes(hashed, "utf-8")
    password = bytes(user.password, "utf-8")
    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_user.token = get_token(db_user.id, db_user.email)
    return db_user


def get_user_by_id(db: Session, id: str):
    return db.query(UserModel).filter(UserModel.id == id).first()


def get_user_by_email(db: Session, email: str):
    return (
        db.query(UserModel)
        .filter(UserModel.email == email, UserModel.is_deleted == False)
        .first()
    )


def add_user(db: Session, user: UserBase):
    _id = generate_id()
    id = _id
    user = user.dict()
    email = user["email"]
    db_user = get_user_by_email(db, email=email)
    password = user["password"]
    user["password"] = _create_password(password)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already registerd"
        )
    db_user = UserModel(id=id, **user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


def get_user(db: str, id: str):
    db_user = get_user_by_id(db, id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return db_user


def get_user_list(
    start: int, limit: int, sort_by: str, order: str, search: str, db: Session
):
    query = db.query(UserModel).filter(UserModel.is_deleted == False)

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(or_(UserModel.email.like(text)))

    if sort_by == "email":
        if order == "desc":
            query = query.order_by(UserModel.email.desc())
        else:
            query = query.order_by(UserModel.email)

    else:
        if order == "desc":
            query = query.order_by(UserModel.created_at.desc())
        else:
            query = query.order_by(UserModel.created_at)

    result = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": result}
    return data


def get_all_users(db: Session):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.is_deleted == False)
        .order_by(UserModel.email)
        .all()
    )
    return db_user


# def change_password(id : str, user: ChangePassword, db: Session):
#     password = _create_password(user.old_password)
#     db_user = db.query(UserModel).filter(UserModel.id == id, UserModel.is_deleted == False)
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     db_password = db_user.filter(UserModel.password == password).first()
#     print(db_password)
#     if db_password is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inccorect password")
#     db_password.password = _create_password(user.new_password)
#     db.commit()
#     return "passowrd is updated"


def change_password(id: str, user: ChangePassword, db: Session):
    db_user = get_user_by_id(db=db, id=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    hashed = db_user.password
    hashed = bytes(hashed, "utf-8")
    password = bytes(user.old_password, "utf-8")
    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inccorect old password"
        )
    db_user.password = _create_password(user.new_password)
    db_user.updated_at = now()
    db.commit()
    return "password change successfully"


def update_user(id: str, user: UserUpdate, db: Session):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.id == id, UserModel.is_deleted == False)
        .first()
    )
    print(db_user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    db_user.email = user.email
    db_user.updated_at = now()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(id: str, db: Session):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.id == id, UserModel.is_deleted == False)
        .first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    db_user.is_deleted = True
    db_user.updated_at = now()
    db.commit()
    return
