# Share guide for BA-SE438

Hi BA-SE438 — this branch contains the Lingrow app and everything needed to run and inspect it.

Short summary
- Project: Lingrow (simple Python/tkinter app to show a mockup and provide writing suggestions)
- Location: top-level files: `main.py`, `README.md`, `scripts/`, `assets/`, `icons/`

How to run locally
1. Open a terminal and go to the project folder (example):
   ```bash
   cd "/Users/ashlcarm18/Computer sciencie /CAC"
   ```
2. (Optional) Use the provided helper script to create a venv and run:
   ```bash
   ./run.sh
   ```
   This script will create a `.venv` (if missing), install Pillow optionally, and run `main.py`.

3. Or run directly with system Python 3:
   ```bash
   python3 main.py
   ```

Dependencies
- The app uses only the Python standard library for a basic run. For better image support and scaling, install Pillow:
  ```bash
  pip install pillow
  ```
- Optional: `cairosvg` + system `cairo` if you want SVG -> PNG conversion for icons. Not required for the demo.

Files of interest
- `main.py` — main GUI app (tkinter). Key areas: nav drawing, `load_nav_icons`, `build_home`, `open_write_popup`.
- `assets/lingrow_logo.png` — generated pink logo (displayed in the app header).
- `icons/` — small icons used by the bottom navigation (generated if missing).
- `scripts/generate_assets.py` — helper that generates example icons and the logo with Pillow.
- `run.sh` — helper script to create/.venv and run the app.

Notes for the video / collaborator
- The UI is simple and made for demos. If you want a perfect visual match to the Canva mockup, tell me and I can adjust fonts, spacing, and colors.
- If the app shows a busy spinner when moving the window, try running from a terminal so we can capture any error messages. I removed a problematic overlay in the nav to avoid blocking clicks.

If you want me to add BA-SE438 as a GitHub collaborator automatically, I can't modify GitHub permissions from here — you'll need to add them in the repository Settings → Manage access, or give me a GitHub token. Otherwise, they can clone the repo and use the branch created here.

Branch: `share-with-BA-SE438`

Happy to help with a short README clip for the video explaining how to run and what to show on screen.

-- Lingrow team
