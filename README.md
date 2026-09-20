# SSAC SplitSecond

Swim race video analyzer for the SSAC team. A coach films a swimmer, the app
breaks the race into phases and reports the numbers that matter: dive, underwater,
surface swimming, and turns.

The app is split into four modules, one per race phase, so each of us can build
and test our own part without waiting on anyone else. A shared core handles
video reading, the result format, the command line, and (later) the web page.

## Layout

    run.py                     command line runner
    splitsecond/
      core/
        video.py               Clip: reads frames from a file or from memory
        types.py               Result and Segment, the shared data types
        report.py              text and JSON output
      modules/
        base.py                AnalysisModule, the contract every module follows
        __init__.py            MODULES registry (add your module here)
        dive/                  start reaction, flight, entry
        underwater/            underwater phase, kicks, breakout
        swim/                  stroke count, tempo, speed, splits
        turn/                  flip and open turns
    tests/
      helpers.py               shared test clips and the contract test
      test_core.py             tests for the shared pieces
      test_<module>.py         one test file per module, owned by that module's builder
    tools/make_sample_clip.py  makes a cartoon clip so you can run code before real footage exists
    samples/                   put video clips here (ignored by git)
    results/                   JSON output lands here (ignored by git)

## Setup (once)

    ./setup.sh                 Mac or Linux
    setup.bat                  Windows

This creates a `.venv` folder and installs OpenCV, numpy and pytest into it.
Afterwards, activate it in each new terminal:

    source .venv/bin/activate      Mac or Linux
    .venv\Scripts\activate         Windows

On a Mac you can also double-click `Run Tests.command`, which does the setup
if needed and then runs the whole test suite.

## Running

    python tools/make_sample_clip.py                     make samples/synthetic_sprint.mp4
    python run.py --list                                 show the modules
    python run.py dive samples/synthetic_sprint.mp4      run one module
    python run.py dive,turn clip.mov --start 1.2         run two modules, start signal at 1.2 s
    python run.py all clip.mov --course LCM --json results/clip.json

Options: `--start` (time of the start signal in the clip), `--course` (SCY, SCM
or LCM; sets the pool length), `--lane`, and `-o key=value` for anything extra
your module needs.

## Testing

    python -m pytest                     everything
    python -m pytest tests/test_dive.py  just your module
    python -m unittest                   works too, no pytest needed

Every module gets the same contract tests for free (from `tests/helpers.py`):
it is registered, it returns a Result with every metric key, key frames are
inside the clip, and the output can be saved as JSON. Those must stay green.
Then add your own tests for the real numbers.

## Building your module

1. Open `splitsecond/modules/<yours>/module.py`. Put your name in `owner`.
2. The docstring lists the metrics from the team meeting. Those are the keys
   in `metric_keys`; keep them, and add more if you need them.
3. Write `analyze(self, clip, options)`. Start with `self.empty_result()`,
   fill in `result.metrics`, `result.key_frames` and `result.notes`, return it.
4. Get frames with `clip.frames(start_s=..., end_s=..., step=...)`, which yields
   `(frame_index, time_s, frame)`. Frames are numpy arrays in OpenCV's BGR layout.
   `clip.fps`, `clip.width`, `clip.height`, `clip.time_to_frame()` and
   `clip.frame_to_time()` are there too.
5. Read settings from `options`: `pool_length_m`, `course`, `start_s`, `lane`,
   `swimmer_box`. Never hard-code a pool length.
6. Helper functions go in your module's folder. Anything two modules both need
   goes in `splitsecond/core/` after a quick chat with the team.
7. Run `python -m pytest tests/test_<yours>.py` and
   `python run.py <yours> samples/synthetic_sprint.mp4` until you like the numbers.

## Ground rules

- Do not commit video files. `samples/` and `results/` are git-ignored.
- Do not change `core/types.py` or `modules/base.py` on your own; everyone
  depends on them.
- A module must never crash the whole run. If you cannot measure something,
  leave it `None` and say why in `result.notes`.
- Units: metres, seconds, degrees, strokes per minute. Yards get converted at
  the edges, not inside modules.
