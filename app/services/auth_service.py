from typing import Dict

from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import bcrypt

USERS: Dict[str, dict] = {}


def register_user(email: str, password: str, role: str = "founder") -> dict:
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    user = {"id": len(USERS) + 1, "email": email, "password": hashed, "role": role}
    USERS[email] = user
    return {k: v for k, v in user.items() if k != "password"}


def authenticate_user(email: str, password: str) -> dict | None:
    user = USERS.get(email)
    if not user:
        return None
    if not bcrypt.check_password_hash(user["password"], password):
        return None
    return user


def issue_tokens(user: dict) -> dict:
    claims = {"role": user["role"], "email": user["email"]}
    access_token = create_access_token(identity=str(user["id"]), additional_claims=claims)
    refresh_token = create_refresh_token(identity=str(user["id"]), additional_claims=claims)
    return {"access_token": access_token, "refresh_token": refresh_token}
