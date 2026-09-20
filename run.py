"""Command line runner.

    python run.py dive samples/synthetic_sprint.mp4
    python run.py dive,turn clip.mov --start 1.2 --course LCM
    python run.py all clip.mov --json results/clip.json
    python run.py --list

Each boy runs only his own module while building it. `all` runs every
registered module in order and is what the web page will eventually call.
"""

from __future__ import annotations

import argparse
import os
import sys

from splitsecond.core.report import to_json, to_text
from splitsecond.core.video import open_clip
from splitsecond.modules import MODULES, get_module, module_names


def parse_option(text: str) -> tuple[str, object]:
    """Turn 'key=value' into a typed (key, value) pair."""
    if "=" not in text:
        raise argparse.ArgumentTypeError(f"expected key=value, got '{text}'")
    key, raw = text.split("=", 1)
    for convert in (int, float):
        try:
            return key, convert(raw)
        except ValueError:
            pass
    return key, raw


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SSAC SplitSecond swim video analyzer")
    parser.add_argument("modules", nargs="?", help="module name, comma list, or 'all'")
    parser.add_argument("clip", nargs="?", help="path to a video file")
    parser.add_argument("--list", action="store_true", help="show the registered modules and exit")
    parser.add_argument("--start", type=float, default=0.0, help="time of the start signal in the clip, seconds")
    parser.add_argument("--course", default="SCY", choices=["SCY", "SCM", "LCM"], help="pool course (default SCY)")
    parser.add_argument("--lane", type=int, default=None, help="lane of the swimmer of interest")
    parser.add_argument("--option", "-o", action="append", default=[], type=parse_option, metavar="KEY=VALUE",
                        help="extra option passed to the modules; repeatable")
    parser.add_argument("--json", metavar="FILE", help="also write the results as JSON to FILE")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        for name, cls in MODULES.items():
            owner = f" (owner: {cls.owner})" if cls.owner else ""
            print(f"{name:12} {cls.description}{owner}")
        return 0

    if not args.modules or not args.clip:
        parser.error("need a module name and a clip path (or --list)")

    names = module_names() if args.modules == "all" else [name.strip() for name in args.modules.split(",")]
    options = {"start_s": args.start, "course": args.course, "lane": args.lane}
    options.update(dict(args.option))

    results = []
    with open_clip(args.clip) as clip:
        print(f"clip: {clip}")
        for name in names:
            module = get_module(name)
            results.append(module.run(clip, options))

    print(to_text(results))

    if args.json:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as handle:
            handle.write(to_json(results, clip_path=args.clip))
        print(f"saved {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
