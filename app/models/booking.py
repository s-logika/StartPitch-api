from dataclasses import dataclass


@dataclass
class Booking:
    id: int
    mentor_id: int
    user_id: int
    status: str
