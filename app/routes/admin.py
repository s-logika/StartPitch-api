from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models.audit_log import AuditLog

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


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
    log = AuditLog(event="verification_approved", data={"user_id": user_id})
    db.session.add(log)
    db.session.commit()
    return jsonify({"approved": True, "user_id": user_id}), 200


@admin_bp.get("/audit-logs")
@jwt_required()
def audit_logs():
    if not _is_admin():
        return jsonify({"error": "Forbidden"}), 403
    return jsonify([log.to_dict() for log in AuditLog.query.all()]), 200


@admin_bp.post("/moderation/<int:content_id>/flag")
@jwt_required()
def flag_content(content_id: int):
    if not _is_admin():
        return jsonify({"error": "Forbidden"}), 403
    log = AuditLog(event="content_flagged", data={"content_id": content_id})
    db.session.add(log)
    db.session.commit()
    return jsonify({"flagged": True, "content_id": content_id}), 200
