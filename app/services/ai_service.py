from concurrent.futures import ThreadPoolExecutor
from time import sleep

from flask import current_app

from app.extensions import db
from app.models.evaluation import EvaluationJob

executor = ThreadPoolExecutor(max_workers=2)


def _run_evaluation(app, job_id: int, pitch_version_id: int) -> None:
    sleep(2)
    with app.app_context():
        job = db.session.get(EvaluationJob, job_id)
        if not job:
            return
        job.status = "done"
        job.data = {
            "score": {
                "market": 78,
                "team": 82,
                "traction": 70,
                "financials": 73,
                "defensibility": 76,
                "clarity": 80,
                "overall": 76.5,
            },
            "feedback": {
                "market": [
                    {
                        "claim": "Large target segment",
                        "evidence_snippet_from_pitch": "Addressing mid-sized SaaS firms",
                        "verdict": "reasonable",
                    }
                ]
            },
        }
        db.session.commit()


def queue_evaluation(pitch_version_id: int) -> dict:
    job = EvaluationJob(pitch_version_id=pitch_version_id, status="processing", data={})
    db.session.add(job)
    db.session.commit()
    app = current_app._get_current_object()
    executor.submit(_run_evaluation, app, job.id, pitch_version_id)
    return job.to_dict()
