# blender-mcp — knowledge digest
> Pinned to ahujasid/blender-mcp @ 6641189231ca (read 2026-07-19). Claims below are true of THIS sha.
> (Full sha: `6641189231caf3752302ae20591bc87fda85fc4e`; pyproject version 1.6.0; addon `bl_info` version (1, 2), min Blender (3, 0, 0).)

## What it is
BlenderMCP connects an MCP client (Claude Desktop/Code, Cursor, VS Code) to a live Blender session so the LLM can inspect and manipulate scenes directly. Two pieces: a Python MCP server (`uvx blender-mcp`) and a Blender addon (`addon.py`) that runs a TCP socket server inside Blender. Through it an agent can read scene/object info, take viewport screenshots, create/modify/delete objects and materials, run arbitrary `bpy` Python, and pull assets from Poly Haven / Sketchfab or generate them via Hyper3D Rodin / Hunyuan3D.

## Architecture map
- **Split**: `src/blender_mcp/server.py` (MCP server, FastMCP, stdio to the client) ↔ `addon.py` (Blender addon, socket server on `localhost:9876` by default, listens with `socket.listen(1)`).
- **Command flow**: MCP tool call → server sends JSON `{"type": <command>, "params": {...}}` over TCP → addon's `execute_command` dispatches to a handler dict → executes on Blender's **main thread** via `bpy.app.timers.register` → JSON `{"status", "result"|"message"}` back. 180 s socket timeout on both sides; server keeps one persistent global connection (`get_blender_connection()`), reconnecting on failure.
- **Key MCP tools** (`@mcp.tool()` in server.py): `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, `execute_blender_code` (→ addon `execute_code`, which `exec()`s the string with `{"bpy": bpy}` and returns captured stdout), Poly Haven (`get_polyhaven_categories/search/download`, `set_texture`, `get_polyhaven_status`), Sketchfab (`search/preview/download`, status), Hyper3D Rodin (`generate_hyper3d_model_via_text/images`, `poll_rodin_job_status`, `import_generated_asset`, status), Hunyuan3D (`generate`, `poll`, `import`, status). Also an `@mcp.prompt()` `asset_creation_strategy` that tells the LLM: screenshot before/after, prefer asset libraries over scripting, check `world_bounding_box` after imports.
- Addon-side integration handlers are only registered when the corresponding checkbox (`blendermcp_use_polyhaven` / `_hyper3d` / `_sketchfab` / `_hunyuan3d`) is enabled in the Blender UI.
- Config: env vars `BLENDER_HOST` (default `localhost`) and `BLENDER_PORT` (default `9876`) on the server side; API keys via addon Preferences or `BLENDERMCP_SKETCHFAB_API_KEY`, `BLENDERMCP_HYPER3D_API_KEY`, `BLENDERMCP_HUNYUAN3D_SECRET_ID/SECRET_KEY/API_URL`.

## How to drive it
Prereqs: Blender ≥ 3.0, Python ≥ 3.10, uv installed via the **official installer** (`brew install uv` on Mac; not `pip install uv`).

Claude Code (their exact command):
```bash
claude mcp add blender uvx blender-mcp
```

Claude Desktop — `claude_desktop_config.json` (Settings > Developer > Edit Config):
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blender-mcp"]
        }
    }
}
```

Their recommended hardened variant (pins Python, avoids conda/pyenv interpreters):
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["--python", "3.11", "blender-mcp"],
            "env": { "UV_PYTHON_PREFERENCE": "only-managed" }
        }
    }
}
```

Addon install: download `addon.py` from the repo → Blender: Edit > Preferences > Add-ons > Install… → enable "Interface: Blender MCP". Then in the 3D View sidebar (press N) open the **BlenderMCP** tab → optionally enable Poly Haven → click **Connect to Claude**. Do NOT run `uvx blender-mcp` manually in a terminal — the client launches it over stdio.

## Design-anything fit
- blender-mcp is an **execution backbone**, not a design brain: LLM plans → drives Blender via MCP → we export STL/glTF and run `ready_gate` / `scene_gate` on the result.
- There is **no dedicated export tool** at this sha — export goes through `execute_blender_code` with `bpy` export operators (e.g. `bpy.ops.wm.stl_export`, `bpy.ops.export_scene.gltf`). Gate inputs are therefore produced by code we author, which keeps them deterministic.
- Parametric-source-first still applies: our parametric source (script/params) remains the artifact of record; blender-mcp EXECUTES compositions (scene assembly, asset placement, material/lighting passes, screenshot-verified iteration), it does not replace parametric generation. `execute_blender_code` is exactly the channel to run our generated `bpy` source.
- Its built-in `asset_creation_strategy` prompt biases toward downloading library/AI-generated assets over scripting — for design-anything we invert that priority for gated geometry, and use asset integrations only for context/dressing.
- `get_viewport_screenshot` gives a cheap visual-verification loop before the machine gates run.

## Gotchas
- **Security**: `execute_blender_code` runs arbitrary Python via `exec()` inside Blender with no sandboxing — their README says use with caution and ALWAYS save work first. The addon socket has no auth; it binds localhost:9876 by default, but `BLENDER_HOST` supports remote hosts — never expose the port beyond trusted networks (exposure risk is our inference; the no-auth fact is from the code).
- **Headless Blender does not work**: the server's timeout message states that under `blender -b` commands never execute (handlers run via `bpy.app.timers` which need the GUI event loop); use a GUI or `xvfb-run -a blender`.
- **Version/env pins**: `requires-python >=3.10`; deps `mcp[cli]>=1.3.0`, `httpx>=0.27.0`. They recommend `--python 3.11` + `UV_PYTHON_PREFERENCE=only-managed` to dodge conda/pyenv/wheel issues; stale failures need `uv cache clean blender-mcp && uvx --refresh blender-mcp`. The repo `.python-version` does not affect `uvx`.
- **Platform/PATH**: GUI-launched clients don't inherit terminal PATH → `spawn uvx ENOENT`; use the absolute `uvx` path, or on Windows `"command": "cmd", "args": ["/c", "uvx", "blender-mcp"]`; fully quit and relaunch the client after config changes. Windows needs `~\.local\bin` added to user PATH. pipx fallback exists for locked-down machines.
- **Only run ONE MCP server instance** (Cursor OR Claude Desktop, not both).
- **Telemetry is ON by default**: with the addon consent box checked it collects anonymized prompts, code snippets, and screenshots. Disable fully with `DISABLE_TELEMETRY=true` in the server env. For design-anything satellites, set this.
- Upgrades require replacing `addon.py` in Blender AND re-adding the MCP server to the client.
- Timeouts on complex ops are expected; their fix is "break requests into smaller steps". First command after connect sometimes fails, then works (their README).
- Hyper3D free-trial key (`vibecoding`, hardcoded in addon.py) has a daily generation cap.
- Addon `bl_info` version (1, 2) lags the PyPI package (1.6.0) — the two components version independently; whether every PyPI release matches the repo HEAD addon is UNVERIFIED.

## Verify
Minimal end-to-end check per their docs: (1) install addon + enable it, (2) add the MCP server to the client config, (3) in Blender sidebar click "Connect to Claude", (4) confirm the client shows the Blender MCP tools (hammer icon in Claude Desktop), (5) ask: **"Create a sphere and place it above the cube"** (their example) and see it appear in the viewport. A stricter design-anything variant: `get_scene_info` → `execute_blender_code` creating a primitive → `get_viewport_screenshot` to visually confirm — this exact 3-step sequence is our composition, not in their docs (UNVERIFIED as a documented flow, but each tool is documented).
