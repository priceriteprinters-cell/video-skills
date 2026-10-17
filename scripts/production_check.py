#!/usr/bin/env python3
"""Production-readiness checks: placeholder/debug text scan, missing local assets, black frames.

Usage:
  production_check.py scan PATH [PATH ...]
  production_check.py blackframes VIDEO [--min-duration 0.3]
Exit code 0 = clean, 1 = findings, 2 = usage/tool error.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEXT_EXT = {".tsx", ".ts", ".jsx", ".js", ".html", ".css", ".json", ".md", ".txt",
            ".srt", ".vtt", ".ass", ".py", ".svg", ".yaml", ".yml"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", ".cache"}

PLACEHOLDER_PATTERNS = [
    (r"lorem\s+ipsum", "placeholder copy"),
    (r"dolor\s+sit\s+amet", "placeholder copy"),
    (r"your\s+(text|title|headline|logo|name)\s+here", "placeholder copy"),
    (r"insert\s+(title|text|image|logo|name)", "placeholder copy"),
    (r"placeholder", "placeholder marker"),
    (r"\b(TODO|FIXME|XXX|HACK)\b", "developer note"),
    (r"\bTBD\b", "unfinished content"),
    (r"\bdummy\s+(text|content|data|image)\b", "dummy content"),
    (r"via\.placeholder\.com|placehold\.(co|it)|picsum\.photos|dummyimage\.com", "placeholder image service"),
    (r"\bdebug(ger)?\s*(overlay|label|mode)\b", "debug overlay"),
]
COMPILED = [(re.compile(p, re.IGNORECASE if "TODO" not in p and "TBD" not in p else 0), why)
            for p, why in PLACEHOLDER_PATTERNS]
ASSET_REF = re.compile(r"""["'(]((?:\./|\.\./|/)?[\w\-./]+\.(?:png|jpe?g|webp|gif|svg|mp3|wav|m4a|mp4|woff2?|ttf|otf))["')]""",
                       re.IGNORECASE)


def iter_files(paths):
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in TEXT_EXT and not (set(f.parts) & SKIP_DIRS):
                    yield f


def scan_text(text: str):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rx, why in COMPILED:
            m = rx.search(line)
            if m:
                findings.append({"line": lineno, "issue": why, "match": m.group(0)})
    return findings


def missing_assets(path: Path, text: str, roots):
    out = []
    for m in ASSET_REF.finditer(text):
        ref = m.group(1)
        if ref.startswith(("http", "//")):
            continue
        candidates = [path.parent / ref] + [r / ref.lstrip("/") for r in roots]
        if not any(c.exists() for c in candidates):
            out.append({"issue": "missing local asset", "match": ref})
    return out


def cmd_scan(args) -> int:
    invalid = [str(p) for raw in args.paths if not (p := Path(raw)).is_file() and not p.is_dir()]
    if invalid:
        print(json.dumps({"error": "Input paths must exist as files or directories", "paths": invalid}), file=sys.stderr)
        return 2
    roots = [Path(p) for p in args.paths if Path(p).is_dir()]
    roots += [r / "public" for r in roots]
    report = []
    scanned = 0
    for f in iter_files(args.paths):
        if f.name == Path(__file__).name:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            print(json.dumps({"error": str(exc), "file": str(f)}), file=sys.stderr)
            return 2
        scanned += 1
        items = scan_text(text)
        if f.suffix.lower() not in {".md", ".txt", ".srt", ".vtt"}:
            items += missing_assets(f, text, roots)
        for it in items:
            it["file"] = str(f)
            report.append(it)
    if not scanned:
        print(json.dumps({"error": "No readable text inputs were scanned"}), file=sys.stderr)
        return 2
    print(json.dumps({"findings": report, "count": len(report), "scanned_files": scanned}, indent=2))
    return 1 if report else 0


def parse_blackdetect(stderr: str):
    rx = re.compile(r"black_start:([\d.]+)\s+black_end:([\d.]+)\s+black_duration:([\d.]+)")
    return [{"start": float(a), "end": float(b), "duration": float(c)} for a, b, c in rx.findall(stderr)]


def cmd_blackframes(args) -> int:
    if not Path(args.video).is_file():
        print("Video input must be an existing file", file=sys.stderr)
        return 2
    if not math.isfinite(args.min_duration) or args.min_duration <= 0:
        print("Minimum duration must be finite and greater than zero", file=sys.stderr)
        return 2
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found", file=sys.stderr)
        return 2
    try:
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-xerror", "-i", args.video, "-map", "0:v:0", "-vf",
             f"blackdetect=d={args.min_duration}:pix_th=0.10", "-an", "-f", "null", "-"],
            capture_output=True, text=True)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if proc.returncode != 0:
        print(json.dumps({"error": "FFmpeg video decoding failed", "returncode": proc.returncode,
                          "details": proc.stderr[-4000:]}), file=sys.stderr)
        return 2
    spans = parse_blackdetect(proc.stderr)
    print(json.dumps({"black_spans": spans, "count": len(spans)}, indent=2))
    return 1 if spans else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("paths", nargs="+")
    b = sub.add_parser("blackframes")
    b.add_argument("video")
    b.add_argument("--min-duration", type=float, default=0.3)
    args = ap.parse_args(argv)
    return cmd_scan(args) if args.cmd == "scan" else cmd_blackframes(args)


if __name__ == "__main__":
    sys.exit(main())
