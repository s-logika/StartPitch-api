from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self) -> dict:
        return {**(self.data or {}), "id": self.id}
