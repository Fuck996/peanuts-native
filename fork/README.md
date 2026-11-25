# Fork overlays

This branch is based on the upstream 0.1.8 release. The source tree remains upstream
English. All fork UI mappings live in `zh-cn/`; the build-only adapter materializes
translations in a disposable checkout before packaging. Existing choice values and
route keys remain English, separately from the displayed Chinese labels. Unknown
labels fall back to English; update the TSV or catalog and run the tests to add coverage.
When updating upstream, merge upstream into the branch without merging generated
Java files. The overlay fails if core hooks cannot be found; review the hook script
when upstream changes those boundaries.

The San14PK profile lives separately in `san14pk/` and is optional. It targets
Chinese title 0100CD4012DCA000, update 1.1.1 (v786432). This is an experimental
import and requires device testing. Its apply script builds the catalogs on top
of the upstream release list without replacing it.

The branch-only Actions workflow creates an APK using the existing signing identity.
It fails closed if the signing certificate is absent or differs from the pinned
fingerprint. No APK is installed or published automatically.

Local check (fresh disposable checkout):
```sh
python fork/zh-cn/apply.py
python fork/zh-cn/test_catalog.py
python fork/zh-cn/test_routes.py
python fork/san14pk/apply.py
sh peanuts/scripts/check-profiles.sh $(cat peanuts/release-titles.txt)
```
