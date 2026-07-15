from app.extensions import db


class Reputation(db.Model):
    __tablename__ = "reputations"

    user_id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False, default=0)
    ratings = db.Column(db.JSON, nullable=False, default=list)

    def to_dict(self) -> dict:
        return {"user_id": self.user_id, "score": self.score, "ratings": self.ratings or []}
