from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.notification import Notification

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")


@notifications_bp.get("")
@jwt_required()
def list_notifications():
    user_id = get_jwt_identity()
    results = Notification.query.filter_by(user_id=int(user_id)).all()
    return jsonify([n.to_dict() for n in results]), 200


@notifications_bp.patch("/<int:notification_id>/read")
@jwt_required()
def mark_read(notification_id: int):
    item = db.session.get(Notification, notification_id)
    if not item:
        return jsonify({"error": "Notification not found"}), 404
    item.read = True
    db.session.commit()
    return jsonify(item.to_dict()), 200
