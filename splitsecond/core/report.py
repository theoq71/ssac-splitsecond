"""Turning Results into something a person can read.

For now: plain text for the terminal and JSON for saving. The future web
page will build on the same to_dict() output.
"""

from __future__ import annotations

import json
from typing import Any

from splitsecond.core.types import Result


def format_value(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def to_text(results: list[Result]) -> str:
    lines: list[str] = []
    for result in results:
        lines.append(f"[{result.module}]")
        width = max((len(key) for key in result.metrics), default=0)
        for key, value in result.metrics.items():
            lines.append(f"  {key.ljust(width)}  {format_value(value)}")
        if result.key_frames:
            frames = ", ".join(f"{label}={index}" for label, index in result.key_frames.items())
            lines.append(f"  key frames: {frames}")
        for note in result.notes:
            lines.append(f"  note: {note}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def to_json(results: list[Result], clip_path: str = "") -> str:
    payload = {"clip": clip_path, "results": [result.to_dict() for result in results]}
    return json.dumps(payload, indent=2)
