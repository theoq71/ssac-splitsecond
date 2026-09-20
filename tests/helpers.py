"""Shared test helpers. Every module test file imports from here.

Tests are written with unittest so they run with either command:
    python -m pytest
    python -m unittest
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from splitsecond.core.types import Result  # noqa: E402
from splitsecond.core.video import ArrayClip, Clip, VideoFileClip, blank_frame  # noqa: E402
from splitsecond.modules.base import AnalysisModule  # noqa: E402


def moving_dot_clip(frames: int = 60, fps: float = 30.0, width: int = 320, height: int = 180) -> ArrayClip:
    """An in-memory clip with a bright dot moving left to right. Fast, no disk."""
    images = []
    for index in range(frames):
        frame = blank_frame(width, height, (120, 80, 20))
        x = int(20 + (width - 40) * index / max(1, frames - 1))
        frame[height // 2 - 5 : height // 2 + 5, max(0, x - 5) : x + 5] = (255, 255, 255)
        images.append(frame)
    return ArrayClip(images, fps=fps)


def synthetic_file_clip(seconds: float = 3.0) -> VideoFileClip | None:
    """The cartoon sprint written to a temp file, or None if this machine cannot encode video."""
    from tools.make_sample_clip import make_clip

    folder = tempfile.mkdtemp(prefix="splitsecond_")
    try:
        path = make_clip(os.path.join(folder, "sprint.mp4"), seconds=seconds)
    except RuntimeError:
        return None
    return VideoFileClip(path)


class ModuleContractTest:
    """Mix this into your module's test file next to unittest.TestCase and set `module_class`.

        class DiveModuleContractTest(ModuleContractTest, unittest.TestCase):
            module_class = DiveModule

    It checks the things every module must get right regardless of what the
    analysis does. Add your own tests next to it for the actual metrics.
    """

    module_class: type[AnalysisModule] | None = None

    def setUp(self) -> None:
        assert self.module_class is not None, "set module_class"
        self.module = self.module_class()
        self.clip: Clip = moving_dot_clip()

    def test_has_name_and_metric_keys(self) -> None:
        self.assertTrue(self.module.name, "module needs a name")
        self.assertTrue(self.module.metric_keys, "module needs at least one metric key")
        self.assertEqual(len(set(self.module.metric_keys)), len(self.module.metric_keys), "duplicate metric keys")

    def test_is_registered(self) -> None:
        from splitsecond.modules import MODULES

        self.assertIs(MODULES.get(self.module.name), self.module_class)

    def test_returns_complete_result(self) -> None:
        result = self.module.run(self.clip, {})
        self.assertIsInstance(result, Result)
        self.assertEqual(result.module, self.module.name)
        for key in self.module.metric_keys:
            self.assertIn(key, result.metrics)

    def test_key_frames_are_inside_clip(self) -> None:
        result = self.module.run(self.clip, {})
        for label, index in result.key_frames.items():
            self.assertTrue(0 <= index < self.clip.frame_count, f"key frame '{label}' = {index} is outside the clip")

    def test_result_is_json_serializable(self) -> None:
        import json

        json.dumps(self.module.run(self.clip, {}).to_dict())

    def test_accepts_course_options(self) -> None:
        for course in ("SCY", "SCM", "LCM"):
            self.module.run(self.clip, {"course": course, "start_s": 0.5})
