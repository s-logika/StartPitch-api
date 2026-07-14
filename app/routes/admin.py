from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

AUDIT_LOGS: list[dict] = []


def _is_admin() -> bool:
    claims = get_jwt()
    return claims.get("role") == "admin"


@admin_bp.get("/verifications/pending")
@jwt_required()
def pending_verifications():
    if not _is_admin():
        return jsonify({"error": "Forbidden"}), 403
    return jsonify([]), 200


@admin_bp.post("/verifications/<int:user_id>/approve")
@jwt_required()
def approve_verification(user_id: int):
    if not _is_admin():
        return jsonify({"error": "Forbidden"}), 403
    AUDIT_LOGS.append({"event": "verification_approved", "user_id": user_id})
    return jsonify({"approved": True, "user_id": user_id}), 200


@admin_bp.get("/audit-logs")
@jwt_required()
def audit_logs():
    if not _is_admin():
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(AUDIT_LOGS), 200


@admin_bp.post("/moderation/<int:content_id>/flag")
@jwt_required()
def flag_content(content_id: int):
    if not _is_admin():
        return jsonify({"error": "Forbidden"}), 403
    AUDIT_LOGS.append({"event": "content_flagged", "content_id": content_id})
    return jsonify({"flagged": True, "content_id": content_id}), 200
