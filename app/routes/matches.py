from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.match import FitMatch, Thesis
from app.models.startup import Startup
from app.services.matching_service import compute_match_score

matches_bp = Blueprint("matches", __name__, url_prefix="/api/v1")


@matches_bp.post("/thesis")
@jwt_required()
def upsert_thesis():
    data = request.get_json(silent=True) or {}
    try:
        investor_id = int(data.get("investor_id", Thesis.query.count() + 1))
    except (TypeError, ValueError):
        return jsonify({"error": "investor_id must be an integer"}), 400
    data["investor_id"] = investor_id
    thesis = db.session.get(Thesis, investor_id)
    if thesis:
        thesis.data = data
    else:
        thesis = Thesis(investor_id=investor_id, data=data)
        db.session.add(thesis)
    db.session.commit()
    return jsonify(thesis.to_dict()), 201


@matches_bp.get("/thesis/<int:investor_id>")
@jwt_required()
def get_thesis(investor_id: int):
    thesis = db.session.get(Thesis, investor_id)
    if not thesis:
        return jsonify({"error": "Thesis not found"}), 404
    return jsonify(thesis.to_dict()), 200


@matches_bp.get("/matches/for-investor/<int:investor_id>")
@jwt_required()
def matches_for_investor(investor_id: int):
    results = FitMatch.query.filter_by(investor_id=investor_id).all()
    return jsonify([m.to_dict() for m in results]), 200


@matches_bp.get("/matches/for-startup/<int:startup_id>")
@jwt_required()
def matches_for_startup(startup_id: int):
    results = FitMatch.query.filter_by(startup_id=startup_id).all()
    return jsonify([m.to_dict() for m in results]), 200


@matches_bp.get("/matches/<int:match_id>/rationale")
@jwt_required()
def get_rationale(match_id: int):
    match = db.session.get(FitMatch, match_id)
    if not match:
        return jsonify({"error": "Match not found"}), 404
    return jsonify((match.data or {}).get("rationale", {})), 200


@matches_bp.post("/matches/recompute")
@jwt_required()
def recompute_matches():
    FitMatch.query.delete()
    matches = []
    for thesis in Thesis.query.all():
        for startup in Startup.query.all():
            computed = compute_match_score(startup.to_dict(), thesis.to_dict())
            match = FitMatch(investor_id=thesis.investor_id, startup_id=startup.id, data=computed)
            db.session.add(match)
            matches.append(match)
    db.session.commit()
    return jsonify([m.to_dict() for m in matches]), 200
