# 3D simulation

**Input:** scene description, sensor data → **Output:** simulation-ready worlds (USD), physics-valid scenes.

## The stack (evidence-ranked)
- **World models:** NVIDIA Cosmos 3 (open omnimodel) + Isaac Lab 3.0 on Newton physics; HunyuanWorld-1.0 (open).
- **Scene graph:** OpenUSD — the presumptive digital-twin standard (AOUSD Core Spec 1.0 → ISO).
- **Capture → sim:** COLMAP (the 10-year default) → 3DGS for real-time representation.
- **Agent bridge:** blender-mcp (24k★) — LLM → Blender → exportable scene.

## Governing principles
- **P6 hot-swap the AI layer** — the neural-representation layer churned once already (NeRF→3DGS in 3 years); bet the pipeline on USD/COLMAP, not on any one model.
- **True scale is non-negotiable** — a simulation world that isn't dimensionally true poisons everything downstream (robotics, daylight, ergonomics).
- **Maker ≠ checker** — generated scenes get validated by independent physics sanity checks, not by the generator's own confidence.

## Ready gate — scene gate v0.1 (`pipeline/scene_gate.py`)
glTF structure · poly budget · true scale in meters (the units-bug catcher) · collision present. Roadmap: USD validity, gravity declaration, physics settle-test probe.
