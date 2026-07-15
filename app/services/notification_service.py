from app.extensions import db
from app.models.notification import Notification


def send_notification(user_id: int, message: str) -> dict:
    item = Notification(user_id=user_id, message=message, read=False)
    db.session.add(item)
    db.session.commit()
    return item.to_dict()
