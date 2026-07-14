from dataclasses import dataclass


@dataclass
class FitMatch:
    id: int
    investor_id: int
    startup_id: int
    score: int
