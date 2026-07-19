# design-anything — agent-native interface. `make check` is CI's finish line.

PY := python3

.PHONY: check test validate gate demo readme readme-check clean

check: validate test readme-check graph-check satellites-check gate ainative  ## everything CI runs; exit 0 = green

ainative:  ## self-audit: a regression in HOW the repo operates fails CI
	$(PY) scripts/ainative.py

test:
	$(PY) -m pytest tests/ -q

validate:
	$(PY) scripts/validate.py

readme:
	$(PY) scripts/build_readme.py
	$(PY) scripts/build_graph.py

readme-check:
	$(PY) scripts/build_readme.py --check

graph-check:
	$(PY) scripts/build_graph.py --check

graph:
	$(PY) scripts/build_graph.py

satellites-check:
	$(PY) scripts/satellites.py build --check

satellites:
	$(PY) scripts/satellites.py build

satellites-sync:  ## network; weekly workflow or on demand — never in check
	$(PY) scripts/satellites.py sync
	$(PY) scripts/satellites.py build

gate: demo  ## the vertical slices must stay READY
	$(PY) pipeline/ready_gate.py /tmp/design-anything-planter.stl --min-feature 3.0
	$(PY) pipeline/construction_gate.py /tmp/design-anything-studio.json
	$(PY) pipeline/pattern_gate.py /tmp/design-anything-apron.json
	$(PY) pipeline/scene_gate.py /tmp/design-anything-arena.gltf
	$(PY) pipeline/dxf_aama.py /tmp/design-anything-apron.json /tmp/design-anything-apron.dxf /tmp/design-anything-studio.ifc /tmp/design-anything-fitspec.json /tmp/design-anything-temple.stl /tmp/design-anything-pen.stl /tmp/design-anything-apron-spec.json
	$(PY) pipeline/ifc_export.py /tmp/design-anything-studio.json /tmp/design-anything-studio.ifc
	$(PY) pipeline/bodyfit_gate.py /tmp/design-anything-fitspec.json
	$(PY) pipeline/ready_gate.py /tmp/design-anything-pen.stl --min-feature 3.0
	$(PY) pipeline/garmentcode_export.py /tmp/design-anything-apron.json /tmp/design-anything-apron-spec.json

demo:
	$(PY) examples/planter/generate.py /tmp/design-anything-planter.stl
	$(PY) examples/studio-flat/generate.py /tmp/design-anything-studio.json
	$(PY) examples/apron/generate.py /tmp/design-anything-apron.json
	$(PY) examples/arena/generate.py /tmp/design-anything-arena.gltf
	$(PY) examples/eyewear/generate.py /tmp/design-anything-fitspec.json /tmp/design-anything-temple.stl
	$(PY) examples/pen-holder/generate.py /tmp/design-anything-pen.stl

clean:
	rm -f /tmp/design-anything-planter.stl /tmp/design-anything-studio.json /tmp/design-anything-apron.json /tmp/design-anything-arena.gltf /tmp/design-anything-apron.dxf /tmp/design-anything-studio.ifc /tmp/design-anything-fitspec.json /tmp/design-anything-temple.stl
