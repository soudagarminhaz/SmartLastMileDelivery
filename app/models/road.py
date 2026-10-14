from dataclasses import dataclass


@dataclass(frozen=True)
class Road:
    source: str
    destination: str
    distance: float