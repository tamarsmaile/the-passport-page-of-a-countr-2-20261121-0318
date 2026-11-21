#!/usr/bin/env python3
"""the-passport-page-of-a-countr-2-20261121-0318 entry.

The deliverable is the bundled passport-spread image, entry.png: a
1024x1024 PNG of an open passport spread for the invented Republic of
Veskara, drawn procedurally (see ../render.py). This program only copies
it to the output directory (stdlib only, no network).
"""
import os
import shutil

out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")
shutil.copyfile(src, os.path.join(out, "entry.png"))
