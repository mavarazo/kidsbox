from dataclasses import dataclass

@dataclass(order=True)
class Track:
    name: str
