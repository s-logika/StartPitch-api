from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.ai_service import EVALUATION_JOBS, queue_evaluation

evaluations_bp = Blueprint("evaluations", __name__, url_prefix="/api/v1/evaluations")


@evaluations_bp.post("")
@jwt_required()
def create_evaluation():
    data = request.get_json() or {}
    job = queue_evaluation(data.get("pitch_version_id", 0))
    return jsonify(job), 202


@evaluations_bp.get("/jobs/<int:job_id>")
@jwt_required()
def get_job(job_id: int):
    job = EVALUATION_JOBS.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job), 200


@evaluations_bp.get("/<int:pitch_version_id>")
@jwt_required()
def get_evaluation(pitch_version_id: int):
    result = next(
        (job for job in EVALUATION_JOBS.values() if job.get("pitch_version_id") == pitch_version_id and job.get("status") == "done"),
        None,
    )
    if not result:
        return jsonify({"error": "Evaluation not ready"}), 404
    return jsonify(result), 200


@evaluations_bp.post("/<int:evaluation_id>/override")
@jwt_required()
def override_evaluation(evaluation_id: int):
    job = EVALUATION_JOBS.get(evaluation_id)
    if not job:
        return jsonify({"error": "Evaluation not found"}), 404
    data = request.get_json() or {}
    job["override"] = data
    return jsonify({"updated": True, "evaluation": job}), 200
