from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

voice_bp = Blueprint("voice", __name__, url_prefix="/api/v1/voice")


@voice_bp.post("/navigate")
@jwt_required()
def navigate():
    data = request.get_json(silent=True) or {}
    return jsonify({"intent": data.get("intent"), "status": "stub"}), 200


@voice_bp.post("/pitch-submission")
@jwt_required()
def voice_pitch_submission():
    data = request.get_json(silent=True) or {}
    return jsonify({"transcript": data.get("transcript"), "status": "queued"}), 202
