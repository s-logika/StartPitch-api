from app.extensions import db


class EvaluationJob(db.Model):
    __tablename__ = "evaluation_jobs"

    id = db.Column(db.Integer, primary_key=True)
    pitch_version_id = db.Column(db.Integer, nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False, default="processing")
    data = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self) -> dict:
        return {
            **(self.data or {}),
            "id": self.id,
            "pitch_version_id": self.pitch_version_id,
            "status": self.status,
        }
