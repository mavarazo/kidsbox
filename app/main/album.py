from dataclasses import dataclass, field
from typing import List

from app.main.track import Track


@dataclass
class Album:
    name: str
    artwork: str
    tracks: List[Track]
