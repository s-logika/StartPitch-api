from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import bcrypt, db
from app.models.user import User


def get_user_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id: int) -> User | None:
    return db.session.get(User, user_id)


def register_user(email: str, password: str, role: str = "founder") -> dict:
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(email=email, password_hash=hashed, role=role)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def authenticate_user(email: str, password: str) -> User | None:
    user = get_user_by_email(email)
    if not user:
        return None
    if not bcrypt.check_password_hash(user.password_hash, password):
        return None
    return user


def issue_tokens(user: User) -> dict:
    claims = {"role": user.role, "email": user.email}
    access_token = create_access_token(identity=str(user.id), additional_claims=claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)
    return {"access_token": access_token, "refresh_token": refresh_token}
