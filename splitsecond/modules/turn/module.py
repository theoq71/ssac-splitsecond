"""Turn module: approach to the wall, the turn itself, and the push-off.

Metrics (from the team meeting):
  turn_type          "flip" or "open"
  turn_in_time_s     time from the 5 m mark to wall contact
  turn_out_time_s    time from wall contact back out to the 5 m mark
  turn_time_s        turn_in + turn_out
  wall_contact_s     time feet (or hands, for open turns) spend on the wall
  push_off_speed_mps speed right after leaving the wall

Key frames worth recording: "turn_in", "wall_contact", "wall_leave", "turn_out".

Extra options this module reads: none yet.
"""

from __future__ import annotations

from typing import Any

from splitsecond.core.types import Result
from splitsecond.core.video import Clip
from splitsecond.modules.base import AnalysisModule


class TurnModule(AnalysisModule):
    name = "turn"
    description = "Flip and open turns"
    owner = ""
    metric_keys = (
        "turn_type",
        "turn_in_time_s",
        "turn_out_time_s",
        "turn_time_s",
        "wall_contact_s",
        "push_off_speed_mps",
    )

    def analyze(self, clip: Clip, options: dict[str, Any]) -> Result:
        result = self.empty_result()

        # TODO: replace this placeholder with real analysis.
        result.notes.append("turn: not implemented yet")
        return result
