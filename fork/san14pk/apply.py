#!/usr/bin/env python3
"""Materialize the independently maintained experimental game profile for the APK build."""
from pathlib import Path
import shutil, subprocess, sys
here = Path(__file__).resolve().parent
root = here.parents[1]
title = '0100CD4012DCA000'
source = here / 'dm/games' / title
target = root / 'dm/games' / title
release = root / 'peanuts/release-titles.txt'
if target.exists() or title in release.read_text().split():
    raise SystemExit('Profile already exists upstream; review it before enabling the fork patch.')
shutil.copytree(source, target)
old = release.read_text()
release.write_text(old.rstrip() + '\n' + title + '\n')
subprocess.run([sys.executable, str(root/'peanuts/scripts/games_catalog.py'), '--refresh'], cwd=root, check=True)
print('Added experimental San14PK 1.1.1 profile; no upstream source was changed permanently.')
