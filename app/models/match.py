from app.extensions import db


class Thesis(db.Model):
    __tablename__ = "theses"

    investor_id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self) -> dict:
        return {**(self.data or {}), "investor_id": self.investor_id}


class FitMatch(db.Model):
    __tablename__ = "fit_matches"

    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, nullable=False, index=True)
    startup_id = db.Column(db.Integer, nullable=False, index=True)
    data = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self) -> dict:
        return {
            **(self.data or {}),
            "id": self.id,
            "investor_id": self.investor_id,
            "startup_id": self.startup_id,
        }
