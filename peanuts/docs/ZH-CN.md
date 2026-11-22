# Simplified Chinese interface

Fork-only branch: `zh-cn/android`. The app name remains **Peanuts Native**.

The Android interface follows the current locale: Simplified Chinese for a
Simplified Chinese locale, English otherwise. This does not change a game's
language setting. Game names, files, mod names, raw diagnostics, controller
button names and the saved preference keys keep their original values.
Unknown labels use the original English.

The catalog is under `android/app/src/main/java/dev/peanuts/i18n/`, split by
launcher, settings, build and in-game overlay. Upstream-facing calls only
translate display text. Do not translate stored values, protocol tokens, or
diagnostics. Rebuild the app to pick up catalog changes.

Keep the fork's `main` synchronized with upstream; merge updates from that
branch into `zh-cn/android`, not the other way round. Check the launcher,
per-game pages, controller navigation, and in-game panel before shipping.
Use a separate test build when playing archived saves or testing drivers.

For a separately installed test build, use the existing Peanuts build setup
and pass `-PnxApp=peanuts -PnxAppId=peanutszh`. The visible label remains
`Peanuts Native`; the package and data directory are separate from the
official app. Do not uninstall the official app to resolve a signature
mismatch.
