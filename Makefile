# design-anything — agent-native interface. `make check` is CI's finish line.

PY := python3

.PHONY: check test validate gate demo readme readme-check clean

check: validate test readme-check gate  ## everything CI runs; exit 0 = green

test:
	$(PY) -m pytest tests/ -q

validate:
	$(PY) scripts/validate.py

readme:
	$(PY) scripts/build_readme.py

readme-check:
	$(PY) scripts/build_readme.py --check

gate: demo  ## the vertical slices must stay READY
	$(PY) pipeline/ready_gate.py /tmp/design-anything-planter.stl --min-feature 3.0
	$(PY) pipeline/construction_gate.py /tmp/design-anything-studio.json
	$(PY) pipeline/pattern_gate.py /tmp/design-anything-apron.json

demo:
	$(PY) examples/planter/generate.py /tmp/design-anything-planter.stl
	$(PY) examples/studio-flat/generate.py /tmp/design-anything-studio.json
	$(PY) examples/apron/generate.py /tmp/design-anything-apron.json

clean:
	rm -f /tmp/design-anything-planter.stl /tmp/design-anything-studio.json /tmp/design-anything-apron.json
