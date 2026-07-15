from app.extensions import db


class DealRoom(db.Model):
    __tablename__ = "deal_rooms"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False, default=dict)
    documents = db.Column(db.JSON, nullable=False, default=list)
    access_logs = db.Column(db.JSON, nullable=False, default=list)

    def to_dict(self) -> dict:
        return {
            **(self.data or {}),
            "id": self.id,
            "documents": self.documents or [],
            "access_logs": self.access_logs or [],
        }
