#!/usr/bin/env python3
"""SOLMARA — "The Poster for a Place That Isn't There" (make.fun).

The program writes one image to /output/entry.png: a vintage art-deco
travel poster for Solmara, an invented coastal city where two suns set
through a great natural stone arch over a violet sea. White-and-gold
terraces cascade down rose cliffs; lantern boats drift on the water.
The place name SOLMARA is set in large cream serif capitals across
the upper sky, and it is the only text in the picture.

The poster is stored in this repository as entry.png (JPEG bytes,
1024x1024, 221,232 bytes — inside the competition's 1 MiB cap). This
program copies it to the grader's output directory and verifies the
copy: same bytes, JPEG magic, and within the size limit. Standard
library only, no network, deterministic — every run writes the same
bytes, so repeated grading runs are byte-identical by construction.

Drand anchor for this entry: round 34146529, anchor commit
62111377084a99a692de4d5cc7497e8e80977a7f (fetched after the
competition opened at 2026-11-21T05:39:00Z; see .makefun/freshness.json).
The anchor proves the repository was started inside the entry window.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"

# The poster as shipped in this repository: JPEG bytes, 1024 by 1024.
EXPECTED_SHA256 = "de044e8e16804b1c0bcbd6785bc720cef21c41ece0111664d577976d523f5336"
EXPECTED_BYTES = 221232
MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8\xff"


def _fail(message: str) -> "SystemExit":
    print(f"solmara: error: {message}", file=sys.stderr)
    return SystemExit(1)


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        raise _fail(f"{SOURCE_NAME} missing next to {Path(__file__).name}")

    data = source.read_bytes()
    if len(data) != EXPECTED_BYTES:
        raise _fail(
            f"{SOURCE_NAME} is {len(data)} bytes, expected {EXPECTED_BYTES}"
        )
    if not data.startswith(JPEG_MAGIC):
        raise _fail(f"{SOURCE_NAME} is not a JPEG (bad magic bytes)")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise _fail(f"{SOURCE_NAME} failed its sha256 check")
    if len(data) > MAX_BYTES:
        raise _fail(f"{SOURCE_NAME} exceeds the 1 MiB limit")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    shutil.copyfile(source, target)

    written = target.read_bytes()
    if written != data:
        raise _fail(f"{target} does not match {SOURCE_NAME} after copy")
    print(f"solmara: wrote {target} ({len(written)} bytes, 1024x1024 JPEG)")


if __name__ == "__main__":
    main()
