"""The contract every analysis module follows.

To build a module you subclass AnalysisModule, set the class attributes,
and implement analyze(). That is all the rest of the app needs.

    class DiveModule(AnalysisModule):
        name = "dive"
        description = "Start and entry"
        metric_keys = ("entry_distance_m", "entry_angle_deg")

        def analyze(self, clip, options):
            result = self.empty_result()
            ...look at clip.frames()...
            result.metrics["entry_distance_m"] = 3.4
            result.key_frames["entry"] = 41
            return result

Rules:
  - Do not open video files yourself. Use the Clip you are given.
  - Always return a Result whose metrics contain every key in metric_keys
    (None is fine for anything you could not measure).
  - Put warnings or "I am not sure" comments in result.notes instead of printing.
  - Read settings from `options` (see COMMON_OPTIONS); never hard-code the pool length.
"""

from __future__ import annotations

from typing import Any

from splitsecond.core.types import Result
from splitsecond.core.video import Clip

# Options every module can expect in the `options` dict. The CLI fills in the
# defaults; a module may read extra keys of its own (document them in its docstring).
COMMON_OPTIONS: dict[str, Any] = {
    "course": "SCY",          # SCY (25 yd), SCM (25 m) or LCM (50 m)
    "pool_length_m": 22.86,   # metres per length; the CLI sets this from `course`
    "start_s": 0.0,           # time in the clip when the race starts (horn / strobe)
    "lane": None,             # lane number of the swimmer of interest, if known
    "swimmer_box": None,      # (x, y, w, h) in pixels in the first frame, if the coach marked the swimmer
}

POOL_LENGTH_M = {"SCY": 22.86, "SCM": 25.0, "LCM": 50.0}


def fill_defaults(options: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(COMMON_OPTIONS)
    merged.update(options or {})
    if "pool_length_m" not in (options or {}):
        merged["pool_length_m"] = POOL_LENGTH_M.get(str(merged["course"]).upper(), merged["pool_length_m"])
    return merged


class AnalysisModule:
    name: str = ""
    description: str = ""
    owner: str = ""
    metric_keys: tuple[str, ...] = ()

    def analyze(self, clip: Clip, options: dict[str, Any]) -> Result:
        raise NotImplementedError(f"{type(self).__name__}.analyze is not written yet")

    def empty_result(self) -> Result:
        """A Result with every metric key present and set to None."""
        return Result(module=self.name, metrics={key: None for key in self.metric_keys})

    def run(self, clip: Clip, options: dict[str, Any] | None = None) -> Result:
        """What the CLI and tests call. Validates the result before handing it back."""
        result = self.analyze(clip, fill_defaults(options))
        if not isinstance(result, Result):
            raise TypeError(f"{self.name}.analyze must return a Result, got {type(result).__name__}")
        if result.module != self.name:
            raise ValueError(f"{self.name}.analyze returned a Result labelled '{result.module}'")
        missing = [key for key in self.metric_keys if key not in result.metrics]
        if missing:
            raise ValueError(f"{self.name}.analyze left out metrics: {missing}")
        return result
