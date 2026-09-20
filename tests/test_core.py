import json
import unittest

from tests.helpers import ArrayClip, blank_frame, moving_dot_clip, synthetic_file_clip
from splitsecond.core.report import to_json, to_text
from splitsecond.core.types import Result
from splitsecond.modules import MODULES, get_module, module_names
from splitsecond.modules.base import fill_defaults


class ClipTests(unittest.TestCase):
    def test_array_clip_timing(self) -> None:
        clip = moving_dot_clip(frames=90, fps=30.0)
        self.assertEqual(clip.frame_count, 90)
        self.assertAlmostEqual(clip.duration_s, 3.0)
        self.assertEqual(clip.time_to_frame(1.0), 30)
        self.assertEqual(clip.time_to_frame(99.0), 89)
        self.assertAlmostEqual(clip.frame_to_time(45), 1.5)

    def test_frames_window(self) -> None:
        clip = moving_dot_clip(frames=60, fps=30.0)
        indexes = [index for index, _, _ in clip.frames(start_s=1.0, end_s=1.5)]
        self.assertEqual(indexes, list(range(30, 46)))
        stepped = [index for index, _, _ in clip.frames(step=10)]
        self.assertEqual(stepped, [0, 10, 20, 30, 40, 50])

    def test_frame_shape(self) -> None:
        clip = ArrayClip([blank_frame(64, 32)], fps=25)
        self.assertEqual(clip.frame_at(0).shape, (32, 64, 3))
        self.assertEqual((clip.width, clip.height), (64, 32))
        with self.assertRaises(IndexError):
            clip.frame_at(1)

    def test_file_clip_reads_like_array_clip(self) -> None:
        clip = synthetic_file_clip(seconds=2.0)
        if clip is None:
            self.skipTest("no video encoder available")
        with clip:
            self.assertGreater(clip.frame_count, 30)
            self.assertAlmostEqual(clip.fps, 30.0, places=1)
            frame = clip.frame_at(10)
            self.assertEqual(frame.shape[2], 3)
            count = sum(1 for _ in clip.frames(start_s=0.0, end_s=1.0))
            self.assertEqual(count, 31)


class OptionTests(unittest.TestCase):
    def test_pool_length_follows_course(self) -> None:
        self.assertAlmostEqual(fill_defaults({"course": "LCM"})["pool_length_m"], 50.0)
        self.assertAlmostEqual(fill_defaults({"course": "SCM"})["pool_length_m"], 25.0)
        self.assertAlmostEqual(fill_defaults({})["pool_length_m"], 22.86)
        self.assertAlmostEqual(fill_defaults({"course": "SCY", "pool_length_m": 23.0})["pool_length_m"], 23.0)


class RegistryTests(unittest.TestCase):
    def test_all_modules_registered(self) -> None:
        self.assertEqual(module_names(), ["dive", "underwater", "swim", "turn"])
        for name, cls in MODULES.items():
            self.assertEqual(cls.name, name)

    def test_unknown_module(self) -> None:
        with self.assertRaises(KeyError):
            get_module("nope")


class ReportTests(unittest.TestCase):
    def test_text_and_json(self) -> None:
        result = Result(module="demo", metrics={"a": 1.234, "b": None}, key_frames={"x": 3}, notes=["hi"])
        text = to_text([result])
        self.assertIn("[demo]", text)
        self.assertIn("1.23", text)
        self.assertIn("x=3", text)
        payload = json.loads(to_json([result], clip_path="c.mov"))
        self.assertEqual(payload["clip"], "c.mov")
        self.assertEqual(payload["results"][0]["metrics"]["b"], None)


class CliTests(unittest.TestCase):
    def test_list(self) -> None:
        import run

        self.assertEqual(run.main(["--list"]), 0)

    def test_run_all_on_synthetic_file(self) -> None:
        import run

        clip = synthetic_file_clip(seconds=1.0)
        if clip is None:
            self.skipTest("no video encoder available")
        path = clip.path
        clip.close()
        self.assertEqual(run.main(["all", path, "--course", "SCY"]), 0)


if __name__ == "__main__":
    unittest.main()
