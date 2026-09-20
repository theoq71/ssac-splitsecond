"""Shared data types every module uses.

Keep this file small and stable. If you need to change something here,
talk to the team first, because every module depends on it.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Segment:
    """A time window inside a clip, in seconds. end_s of None means 'to the end'."""

    start_s: float = 0.0
    end_s: float | None = None


@dataclass
class Result:
    """What a module hands back after analyzing a clip.

    metrics    - the numbers the coach cares about. Keys are defined by each
                 module's metric_keys. A value of None means 'not measured'.
    key_frames - frame indexes for important moments (e.g. "entry", "breakout"),
                 so the web page can later show those frames to the coach.
    notes      - short human-readable remarks, warnings, or confidence hints.
    """

    module: str
    metrics: dict[str, Any] = field(default_factory=dict)
    key_frames: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "module": self.module,
            "metrics": dict(self.metrics),
            "key_frames": dict(self.key_frames),
            "notes": list(self.notes),
        }
