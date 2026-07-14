from dataclasses import dataclass


@dataclass
class Reputation:
    user_id: int
    score: float
