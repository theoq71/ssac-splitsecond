"""Make a small synthetic clip so a module can be run before real footage exists.

    python tools/make_sample_clip.py                 -> samples/synthetic_sprint.mp4
    python tools/make_sample_clip.py out.mp4 --seconds 12 --fps 30

The clip is a top-down cartoon of one length: a pool, lane lines, a start
signal flash at t = 1.0 s, a "swimmer" blob that leaves the wall, travels
underwater (darker, no splash) for a while, then swims on the surface with a
splash pulse at a fixed stroke rate, and touches the far wall near the end.
Nothing about it is realistic; it only gives the code something to chew on.
"""

from __future__ import annotations

import argparse
import os

import cv2
import numpy as np

WATER = (170, 120, 40)   # BGR
WALL = (200, 200, 200)
LANE = (40, 40, 200)
SWIMMER = (60, 200, 230)
SPLASH = (255, 255, 255)

START_S = 1.0        # start signal
UNDERWATER_S = 3.0   # seconds underwater after the start
STROKE_RATE_SPM = 50


def draw_frame(t: float, width: int, height: int, seconds: float) -> np.ndarray:
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = WATER
    cv2.rectangle(frame, (0, 0), (30, height), WALL, -1)
    cv2.rectangle(frame, (width - 30, 0), (width, height), WALL, -1)
    for y in range(0, height, height // 6):
        cv2.line(frame, (30, y), (width - 30, y), LANE, 2)

    if START_S <= t < START_S + 0.1:
        cv2.rectangle(frame, (0, 0), (width, height), SPLASH, 12)

    race_t = t - START_S
    if race_t >= 0:
        progress = min(1.0, race_t / (seconds - START_S - 0.5))
        x = int(30 + progress * (width - 60))
        y = height // 2
        underwater = race_t < UNDERWATER_S
        color = tuple(int(c * 0.6) for c in SWIMMER) if underwater else SWIMMER
        cv2.ellipse(frame, (x, y), (28, 12), 0, 0, 360, color, -1)
        if not underwater:
            phase = ((race_t - UNDERWATER_S) * STROKE_RATE_SPM / 60.0) % 1.0
            if phase < 0.25:
                cv2.circle(frame, (x + 10, y - 18), 8, SPLASH, -1)
    return frame


def make_clip(path: str, seconds: float = 10.0, fps: float = 30.0, width: int = 640, height: int = 360) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        path = os.path.splitext(path)[0] + ".avi"
        writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError("OpenCV could not open a video writer on this machine")
    total = int(seconds * fps)
    for index in range(total):
        writer.write(draw_frame(index / fps, width, height, seconds))
    writer.release()
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=os.path.join("samples", "synthetic_sprint.mp4"))
    parser.add_argument("--seconds", type=float, default=10.0)
    parser.add_argument("--fps", type=float, default=30.0)
    args = parser.parse_args()
    written = make_clip(args.path, args.seconds, args.fps)
    print(f"wrote {written}")


if __name__ == "__main__":
    main()
