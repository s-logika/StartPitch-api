from dataclasses import dataclass


@dataclass
class Message:
    id: int
    from_user_id: int
    to_user_id: int
    content: str
