from dataclasses import dataclass


@dataclass
class Mentor:
    id: int
    user_id: int
    expertise: str
