# Seamly2D — knowledge digest
> Pinned to FashionFreedom/Seamly2D @ dacc5600e29f (read 2026-07-19). Claims below are true of THIS sha.

## What it is
Open-source (GPLv3+) parametric patternmaking CAD for garments — "patternmaking software to democratize fashion" — for Windows 10/11, macOS 12–26, and Linux (Flatpak/AppImage). Drafting is formula-driven: every point/line/curve is defined by expressions over body measurements and variables, so one pattern file regenerates itself for any body. Qt 6.8.3 / C++ desktop app; heritage is a fork of Valentina (authors list still credits the Valentina lineage).

## Architecture map
- Two apps in one repo (`src/app/`):
  - **Seamly2D** (`src/app/seamly2d`) — the pattern drafting/layout app. Pattern files: **`.sm2d`** (XML; current schema v0.7.4, XSDs in `src/libs/ifc/schema/pattern/`). Legacy Valentina `.val` extension still recognized.
  - **SeamlyMe** (`src/app/seamlyme`) — the measurement manager. **`.smis`** = individual measurements (schema v0.3.4), **`.smms`** = multi-size/graded measurements (schema v0.4.5). Legacy `.vit`/`.vst` recognized. All formats are XML validated against bundled XSDs with version-upgrade converters (`src/libs/ifc/xml/*converter*`).
- Formula/variable system: `src/libs/qmuparser` (Qt fork of muParser) evaluates expressions; `src/libs/vpatterndb` holds the variable table — measurement variables, custom variables (user-defined, prefixed `@` per `CustomMSign` in `src/libs/ifc/ifcdef.cpp`), and auto-generated internals (`Line_A_B`, `AngleLine_`, `Spl_`, `Arc_`, `Radius…`, curve control lengths).
- Export/geometry libs: `vlayout` (piece nesting/layout), `vdxf` (bundled libdxfrw; AAMA/ASTM layer logic in `vdxfengine.cpp`), `vgeometry`, `vobj`, `ifc` (XML/schemas, xerces-c).

## How to drive it
- **Install (their docs, `.github/README.md`)**: Windows x64/ARM64 zips, macOS zip (Apple Silicon + Intel), Linux AppImage or Flatpak `io.seamly.seamly2d` from Flathub — all from GitHub Releases latest. Build-from-source (`.github/README-DEVELOPER.md`): Qt 6.8.3 + qmake (`qmake && make -j$(nproc) && sudo make install`; use `qmake6` where qmake is Qt5). `pdftops` (poppler/Xpdf) required for PS/EPS export.
- **Workflow**: SeamlyMe → create/save measurements (.smis or .smms) → Seamly2D → draft blocks as formula-defined geometry referencing measurement names → add pattern pieces (seam allowance, notches, grainline) → layout/nest → export.
- **Export formats** (`LayoutExportFormat` in `src/libs/vmisc/def.h`): SVG, PDF, tiled PDF, PNG/JPG/BMP/PPM/TIF, OBJ, PS, EPS, and DXF in flat + **AAMA** + ASTM variants across DXF versions R10→AC1027 (AutoCAD 2013). AAMA export is fully implemented (piece outline/draw/intcut/notch/grainline/text layers per `vdxfengine.h`, binary DXF optional).
- **Headless/CLI**: Seamly2D has a batch export mode (`src/app/seamly2d/core/vcmdexport.cpp`): `--basename`, `--destination`, `--mfile <measurements>`, `--format <N>`, `--binarydxf`, `--exportOnlyDetails`, gradation size/height, page size/margin options — i.e. scriptable measurements-in → pattern-out.

## Design-anything fit
- Their model IS our P5/pattern-as-function: a `.sm2d` file is a deterministic function from a measurement file to drafted geometry — same measurements + same file = same pattern. Validates our principle with 10+ years of production survival (Valentina→Seamly lineage).
- Interop path: our `dxf_aama.py` and `pattern_gate` speak DXF-AAMA; Seamly2D emits AAMA DXF with standard layer semantics (outline/cut/notch/grainline/text), so gates can verify Seamly2D output, and our generated AAMA DXF should load in downstream tools alongside theirs. UNVERIFIED: exact AAMA layer-number mapping matches our reader — confirm with a round-trip test.
- The CLI export mode enables a satellite pipeline: generate/patch `.sm2d` + `.smis` XML programmatically, invoke Seamly2D headless, gate the DXF.

## Gotchas
- **ASTM DXF is enumerated but NOT implemented**: `ExportApparelLayout` hits `Q_UNREACHABLE(); // For now not supported` for all ASTM variants (`src/app/seamly2d/mainwindowsnogui.cpp:417-427`), and the export dialog strips ASTM entries. Use AAMA.
- File formats are versioned XML with converters; old files auto-upgrade on open but files saved by newer schema (pattern v0.7.4) won't open in older builds. Legacy `.val/.vit/.vst` supported read-side.
- PS/EPS export silently needs a `pdftops` binary next to (or findable by) the app; on Win/mac you must copy `pdftops.exe` into the build dir per their docs.
- Qt 6.8.3 is the pinned toolchain; Arch-like distros need `qmake6` (Qt5 `qmake` produces a broken Makefile — `make distclean` then redo).
- OBJ export is compiled out in release builds (`#ifdef V_NO_ASSERT` removes it — "Temporarily unavailable").
- User wiki manual and developer wiki are flagged "needs updating" by their own README; treat wiki claims as stale, prefer repo docs.

## Verify
- `seamly2d --version` / `seamlyme --version` (or launch GUI: Help > About shows version). UNVERIFIED: exact `--version` output format.
- Functional check: create a minimal `.smis` in SeamlyMe, draft a rectangle block in Seamly2D from two measurement names, export SVG and DXF-AAMA; confirm files appear and the DXF opens (or passes our pattern_gate).
- Headless check: `seamly2d --basename test --destination /tmp --mfile m.smis --format <N> pattern.sm2d` produces the export without GUI interaction.
