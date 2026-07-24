from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.massage import Message
from app.services.notification_service import send_notification

messages_bp = Blueprint("messages", __name__, url_prefix="/api/v1/messages")


@messages_bp.post("")
@jwt_required()
def create_message():
    data = request.get_json(silent=True) or {}
    message = Message(data=data)
    db.session.add(message)
    db.session.commit()
    recipient_id = data.get("to")
    if recipient_id:
        send_notification(int(recipient_id), "You have a new message.")
    return jsonify(message.to_dict()), 201


@messages_bp.get("")
@jwt_required()
def list_messages():
    thread_with = request.args.get("thread_with")
    deal_room_id = request.args.get("deal_room_id")
    results = [m.to_dict() for m in Message.query.all()]
    if thread_with:
        results = [m for m in results if str(m.get("to")) == thread_with or str(m.get("from")) == thread_with]
    if deal_room_id:
        results = [m for m in results if str(m.get("deal_room_id")) == deal_room_id]
    return jsonify(results), 200
