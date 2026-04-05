# py-elastica-plotter

![Screenshot - alt](/screenshot.png "")

Open-source Python deflection curve plotter based on Leonhard Euler and Jakob Bernoulli theory for elastic lines.

> **In memory of prof. Ryszard Pęcherski, who requested the app a while ago.**

## Requirements:
- Python 3.8+
- [uv](https://docs.astral.sh/uv/)

## Run:

```
uv run app.py
```

Then open the URL shown in the terminal (default: http://localhost:7860).

## Current version:
v2.0

## Changes in v2.0:
- Migrated from Python 2.7 / Tkinter to Python 3 / Gradio web UI
- Removed Pillow dependency (no longer needed)
- Migrated to [uv](https://docs.astral.sh/uv/) for dependency management
- Updated all dependencies to current versions

## Future ideas:
- Add stress curve
- Pack into single executable
- Add force quiver
- Allow data export

## Authors:
##### Aleksandra Manecka - theoretical analysis
##### Piotr Bomba - coding
##### under supervision of prof. Ryszard Pęcherski
