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
# Game-specific runtime default, validated on RP Duo: disable automatic
# audio-follow for San14PK to prevent crackling and dropouts. The launcher
# still applies user environment overrides afterwards.
activity = root / 'android/app/src/main/java/dev/nxnative/android/GameActivity.java'
java = activity.read_text()
anchor = '        Profile prof = Profile.of(id);\n        ScreenMode.env(this, id, env);'
replacement = (
    '        Profile prof = Profile.of(id);\n'
    '        if ("' + title + '".equalsIgnoreCase(id)) env.add("PN_AUDIO_FOLLOW=0"); // San14PK audio compatibility\n'
    '        ScreenMode.env(this, id, env);'
)
if java.count(anchor) != 1:
    raise SystemExit('San14PK audio default anchor changed upstream; review before applying.')
patched = java.replace(anchor, replacement, 1)
assert patched.count('PN_AUDIO_FOLLOW=0') == 1
activity.write_text(patched)
shutil.copytree(source, target)
old = release.read_text()
release.write_text(old.rstrip() + '\n' + title + '\n')
subprocess.run([sys.executable, str(root/'peanuts/scripts/games_catalog.py'), '--refresh'], cwd=root, check=True)
print('Added experimental San14PK 1.1.1 profile; audio-follow disabled by default for this title only.')
