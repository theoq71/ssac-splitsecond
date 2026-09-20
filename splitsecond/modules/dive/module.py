"""Dive module: from the start signal to the swimmer entering the water.

Metrics (from the team meeting):
  reaction_time_s     time from start signal to first movement off the block
  flight_time_s       time from leaving the block to hands entering the water
  entry_distance_m    distance from the wall to the entry point
  entry_angle_deg     angle of the body relative to the water surface at entry
  entry_depth_m       how deep the swimmer goes right after entry (underwater camera)

Key frames worth recording: "start", "leave_block", "entry".

Extra options this module reads: none yet. Add them here when you need them.
"""

from __future__ import annotations

from typing import Any

from splitsecond.core.types import Result
from splitsecond.core.video import Clip
from splitsecond.modules.base import AnalysisModule


class DiveModule(AnalysisModule):
    name = "dive"
    description = "Start reaction, flight, and water entry"
    owner = ""
    metric_keys = (
        "reaction_time_s",
        "flight_time_s",
        "entry_distance_m",
        "entry_angle_deg",
        "entry_depth_m",
    )

    def analyze(self, clip: Clip, options: dict[str, Any]) -> Result:
        result = self.empty_result()

        # TODO: replace this placeholder with real analysis.
        # Example of walking the clip from the start signal:
        #   for index, t, frame in clip.frames(start_s=options["start_s"]):
        #       ...
        result.notes.append("dive: not implemented yet")
        return result
