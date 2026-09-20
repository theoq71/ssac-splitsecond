"""Swim module: the surface swimming between breakout and the wall.

Metrics (from the team meeting):
  stroke_count          strokes taken in the length
  stroke_rate_spm       tempo, strokes per minute
  distance_per_stroke_m metres travelled per stroke
  avg_speed_mps         average surface speed
  splits_s              dict of time at each marker, e.g. {"15m": 7.1, "25m": 12.6}
  tempo_by_lap          list of stroke rate per length, in order
  tempo_change_pct      percent change of tempo from first length to last (negative = slowed down)

Key frames worth recording: "breakout", "finish", plus one per split marker.

Extra options this module reads: none yet.
"""

from __future__ import annotations

from typing import Any

from splitsecond.core.types import Result
from splitsecond.core.video import Clip
from splitsecond.modules.base import AnalysisModule


class SwimModule(AnalysisModule):
    name = "swim"
    description = "Stroke count, tempo, speed and splits"
    owner = ""
    metric_keys = (
        "stroke_count",
        "stroke_rate_spm",
        "distance_per_stroke_m",
        "avg_speed_mps",
        "splits_s",
        "tempo_by_lap",
        "tempo_change_pct",
    )

    def analyze(self, clip: Clip, options: dict[str, Any]) -> Result:
        result = self.empty_result()

        # TODO: replace this placeholder with real analysis.
        result.notes.append("swim: not implemented yet")
        return result
