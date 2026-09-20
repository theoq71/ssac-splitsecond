"""Underwater module: from water entry to the breakout.

Metrics (from the team meeting):
  underwater_distance_m   distance covered before the head breaks the surface
  underwater_time_s       time spent underwater
  kick_count              number of dolphin kicks
  breakout_time_s         time from the start signal to the breakout
  breakout_speed_mps      speed at the moment of breakout
  breakout_slowdown_pct   how much the swimmer slowed down in the last kicks before breakout (0 if none)

Key frames worth recording: "entry", "first_kick", "breakout".

Extra options this module reads: none yet.
"""

from __future__ import annotations

from typing import Any

from splitsecond.core.types import Result
from splitsecond.core.video import Clip
from splitsecond.modules.base import AnalysisModule


class UnderwaterModule(AnalysisModule):
    name = "underwater"
    description = "Underwater phase and breakout"
    owner = ""
    metric_keys = (
        "underwater_distance_m",
        "underwater_time_s",
        "kick_count",
        "breakout_time_s",
        "breakout_speed_mps",
        "breakout_slowdown_pct",
    )

    def analyze(self, clip: Clip, options: dict[str, Any]) -> Result:
        result = self.empty_result()

        # TODO: replace this placeholder with real analysis.
        result.notes.append("underwater: not implemented yet")
        return result
