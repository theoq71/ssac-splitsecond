"""Reading video frames.

Modules never open files themselves. They receive a Clip and ask it for
frames. That is what lets the same module code run on a real .MOV from a
phone, on a synthetic test clip, or on a handful of frames built in a test.

Two implementations:
  VideoFileClip - backed by a file on disk, read with OpenCV.
  ArrayClip     - backed by a list of numpy arrays already in memory (tests).
"""

from __future__ import annotations

import os
from typing import Iterator

import cv2
import numpy as np

Frame = np.ndarray  # H x W x 3, BGR, uint8 (OpenCV's default layout)


class Clip:
    """Base class. Subclasses fill in fps, frame_count, width, height and _read()."""

    fps: float = 0.0
    frame_count: int = 0
    width: int = 0
    height: int = 0
    path: str = ""

    @property
    def duration_s(self) -> float:
        return self.frame_count / self.fps if self.fps else 0.0

    def time_to_frame(self, t_s: float) -> int:
        index = int(round(t_s * self.fps))
        return max(0, min(index, self.frame_count - 1))

    def frame_to_time(self, index: int) -> float:
        return index / self.fps if self.fps else 0.0

    def frame_at(self, index: int) -> Frame:
        if index < 0 or index >= self.frame_count:
            raise IndexError(f"frame {index} out of range 0..{self.frame_count - 1}")
        return self._read(index)

    def frames(self, start_s: float = 0.0, end_s: float | None = None, step: int = 1) -> Iterator[tuple[int, float, Frame]]:
        """Yield (frame_index, time_s, frame) for the window [start_s, end_s]."""
        first = self.time_to_frame(start_s)
        last = self.frame_count - 1 if end_s is None else self.time_to_frame(end_s)
        for index in range(first, last + 1, max(1, step)):
            yield index, self.frame_to_time(index), self._read(index)

    def _read(self, index: int) -> Frame:
        raise NotImplementedError

    def close(self) -> None:
        pass

    def __enter__(self) -> "Clip":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path or 'memory'}, {self.width}x{self.height}, {self.fps:.2f} fps, {self.frame_count} frames)"


class VideoFileClip(Clip):
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.path = path
        self._cap = cv2.VideoCapture(path)
        if not self._cap.isOpened():
            raise ValueError(f"OpenCV could not open {path}")
        self.fps = float(self._cap.get(cv2.CAP_PROP_FPS)) or 30.0
        self.frame_count = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._next_index = 0

    def _read(self, index: int) -> Frame:
        # Sequential reads are cheap; seeking is slow, so only seek when needed.
        if index != self._next_index:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            self._next_index = index
        ok, frame = self._cap.read()
        if not ok:
            raise IOError(f"could not read frame {index} of {self.path}")
        self._next_index = index + 1
        return frame

    def close(self) -> None:
        self._cap.release()


class ArrayClip(Clip):
    def __init__(self, frames: list[Frame], fps: float = 30.0, path: str = ""):
        if not frames:
            raise ValueError("ArrayClip needs at least one frame")
        self._frames = frames
        self.fps = float(fps)
        self.frame_count = len(frames)
        self.height, self.width = frames[0].shape[:2]
        self.path = path

    def _read(self, index: int) -> Frame:
        return self._frames[index]


def open_clip(path: str) -> Clip:
    """Open a video file. Later this can grow to handle multi-camera folders."""
    return VideoFileClip(path)


def blank_frame(width: int = 640, height: int = 360, color: tuple[int, int, int] = (0, 0, 0)) -> Frame:
    """A solid-color frame, handy for tests and for the synthetic sample clip."""
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = color
    return frame
