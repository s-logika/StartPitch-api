from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.notification_service import NOTIFICATIONS

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")


@notifications_bp.get("")
@jwt_required()
def list_notifications():
    user_id = get_jwt_identity()
    results = [n for n in NOTIFICATIONS if str(n["user_id"]) == str(user_id)]
    return jsonify(results), 200


@notifications_bp.patch("/<int:notification_id>/read")
@jwt_required()
def mark_read(notification_id: int):
    item = next((n for n in NOTIFICATIONS if n["id"] == notification_id), None)
    if not item:
        return jsonify({"error": "Notification not found"}), 404
    item["read"] = True
    return jsonify(item), 200
