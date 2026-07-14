from dataclasses import dataclass


@dataclass
class Startup:
    id: int
    name: str
    sector: str
    stage: str
