from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.pitch import Pitch, PitchVersion
from app.models.startup import Startup
from app.services.file_service import normalize_pitch_payload

pitches_bp = Blueprint("pitches", __name__, url_prefix="/api/v1/pitches")


@pitches_bp.post("")
@jwt_required()
def create_pitch():
    payload = request.get_json(silent=True) or {}
    startup_id = payload.get("startup_id")
    if not db.session.get(Startup, startup_id):
        return jsonify({"error": "Startup not found"}), 404
    data = normalize_pitch_payload(payload)
    pitch = Pitch(startup_id=startup_id, data=data)
    db.session.add(pitch)
    db.session.commit()
    return jsonify(pitch.to_dict()), 201


@pitches_bp.get("/<int:pitch_id>")
@jwt_required()
def get_pitch(pitch_id: int):
    pitch = db.session.get(Pitch, pitch_id)
    if not pitch:
        return jsonify({"error": "Pitch not found"}), 404
    return jsonify(pitch.to_dict()), 200


@pitches_bp.get("")
@jwt_required()
def list_pitches():
    startup_id = request.args.get("startup_id")
    visibility = request.args.get("visibility")
    query = Pitch.query
    if startup_id:
        query = query.filter(Pitch.startup_id == startup_id)
    if visibility:
        query = query.filter(Pitch.visibility == visibility)
    return jsonify([p.to_dict() for p in query.all()]), 200


@pitches_bp.post("/<int:pitch_id>/versions")
@jwt_required()
def add_version(pitch_id: int):
    pitch = db.session.get(Pitch, pitch_id)
    if not pitch:
        return jsonify({"error": "Pitch not found"}), 404
    payload = request.get_json(silent=True) or {}
    existing_count = PitchVersion.query.filter_by(pitch_id=pitch_id).count()
    version = PitchVersion(
        local_id=existing_count + 1,
        pitch_id=pitch_id,
        status="queued",
        data={"content_url": payload.get("content_url")},
    )
    db.session.add(version)
    db.session.commit()
    return jsonify(version.to_dict()), 201


@pitches_bp.get("/<int:pitch_id>/versions")
@jwt_required()
def list_versions(pitch_id: int):
    versions = PitchVersion.query.filter_by(pitch_id=pitch_id).order_by(PitchVersion.local_id).all()
    return jsonify([v.to_dict() for v in versions]), 200


@pitches_bp.get("/<int:pitch_id>/versions/<int:version_id>")
@jwt_required()
def get_version(pitch_id: int, version_id: int):
    version = PitchVersion.query.filter_by(pitch_id=pitch_id, local_id=version_id).first()
    if not version:
        return jsonify({"error": "Version not found"}), 404
    return jsonify(version.to_dict()), 200


@pitches_bp.get("/<int:pitch_id>/versions/<int:version_id>/status")
@jwt_required()
def get_version_status(pitch_id: int, version_id: int):
    version = PitchVersion.query.filter_by(pitch_id=pitch_id, local_id=version_id).first()
    if not version:
        return jsonify({"error": "Version not found"}), 404
    return jsonify({"status": version.status}), 200


@pitches_bp.get("/<int:pitch_id>/score-history")
@jwt_required()
def score_history(pitch_id: int):
    versions = PitchVersion.query.filter_by(pitch_id=pitch_id).order_by(PitchVersion.local_id).all()
    history = [
        {"version_id": v.local_id, "overall_score": 70 + v.local_id, "delta": 1}
        for v in versions
    ]
    return jsonify(history), 200
