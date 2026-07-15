from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.deal_room import DealRoom

deal_rooms_bp = Blueprint("deal_rooms", __name__, url_prefix="/api/v1/deal-rooms")


@deal_rooms_bp.post("")
@jwt_required()
def create_deal_room():
    data = request.get_json(silent=True) or {}
    room = DealRoom(data=data, documents=[], access_logs=[])
    db.session.add(room)
    db.session.commit()
    return jsonify(room.to_dict()), 201


@deal_rooms_bp.get("/<int:room_id>")
@jwt_required()
def get_deal_room(room_id: int):
    room = db.session.get(DealRoom, room_id)
    if not room:
        return jsonify({"error": "Deal room not found"}), 404
    return jsonify(room.to_dict()), 200


@deal_rooms_bp.post("/<int:room_id>/nda/sign")
@jwt_required()
def sign_nda(room_id: int):
    room = db.session.get(DealRoom, room_id)
    if not room:
        return jsonify({"error": "Deal room not found"}), 404
    room.data = {**(room.data or {}), "nda_signed": True}
    db.session.commit()
    return jsonify({"room_id": room_id, "nda_signed": True}), 200


@deal_rooms_bp.post("/<int:room_id>/documents")
@jwt_required()
def add_document(room_id: int):
    room = db.session.get(DealRoom, room_id)
    if not room:
        return jsonify({"error": "Deal room not found"}), 404
    data = request.get_json(silent=True) or {}
    documents = list(room.documents or [])
    doc = {"id": len(documents) + 1, "name": data.get("name"), "url": data.get("url")}
    documents.append(doc)
    room.documents = documents
    db.session.commit()
    return jsonify(doc), 201


@deal_rooms_bp.get("/<int:room_id>/documents/<int:doc_id>/download")
@jwt_required()
def download_document(room_id: int, doc_id: int):
    room = db.session.get(DealRoom, room_id)
    if not room:
        return jsonify({"error": "Deal room not found"}), 404
    doc = next((d for d in (room.documents or []) if d["id"] == doc_id), None)
    if not doc:
        return jsonify({"error": "Document not found"}), 404
    access_logs = list(room.access_logs or [])
    access_logs.append({"event": "download", "doc_id": doc_id})
    room.access_logs = access_logs
    db.session.commit()
    return jsonify({"download_url": doc["url"]}), 200


@deal_rooms_bp.get("/<int:room_id>/access-logs")
@jwt_required()
def access_logs(room_id: int):
    room = db.session.get(DealRoom, room_id)
    if not room:
        return jsonify({"error": "Deal room not found"}), 404
    return jsonify(room.access_logs or []), 200
