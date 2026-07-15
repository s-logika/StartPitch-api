from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.services.auth_service import get_user_by_id

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users_bp.get("/me")
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict(include_profile=False)), 200


@users_bp.patch("/me")
@jwt_required()
def patch_me():
    user_id = get_jwt_identity()
    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json(silent=True) or {}
    user.profile = {**(user.profile or {}), **data}
    db.session.commit()
    return jsonify({"updated": True, "profile": user.profile}), 200


@users_bp.get("/<int:user_id>/profile-completeness")
@jwt_required()
def profile_completeness(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    profile = user.profile or {}
    fields = ["name", "bio", "role"]
    filled = sum(1 for field in fields if profile.get(field) or getattr(user, field, None))
    score = int((filled / len(fields)) * 100)
    return jsonify({"user_id": user_id, "score": score}), 200
