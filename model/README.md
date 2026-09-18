# Umbrella Dryer V2 — 3D Model

> This folder contains the 3D model of the umbrella dryer frame and station layout.

---

## Model overview

The 3D model shows:
- **3-station frame** — holds 3 umbrellas inverted for drying
- **Motor mounts** — SGM-370 worm gear motors on aluminum plates
- **Flange couplings** — 3× PETIYOUZA 6mm rigid flange couplings connect each SGM-370 output shaft directly to the umbrella hub (no separate shaft, no pillow blocks)
- **PTC heater placement** — 3× PTC ceramic heaters per station, positioned for airflow
- **BLDC fan placement** — 3× 50mm ducted fans per station, positioned for air circulation
- **Electronics enclosure** — Mega, SSR modules, buck converter
- **Battery compartment** — 1× LiFePO4 200Ah battery
- **Drip tray** — under each station for water collection

---

## File formats

| File | Use |
|---|---|
| `.step` / `.stp` | CAD interchange (Fusion 360, SolidWorks, FreeCAD) |
| `.stl` | 3D printing |
| `.f3d` | Fusion 360 native |

---

## Key dimensions

| Part | Dimension |
|---|---|
| Station spacing | **700mm** center-to-center |
| Umbrella hub height | ~300mm from base |
|| Motor mount plate | 100×80mm aluminum 6mm |
| Motor couplings | PETIYOUZA rigid flange, 6mm bore (motor shaft → umbrella hub) |
| PTC heater spacing | ≥ 30mm between elements (airflow gap) |
| Fan duct clearance | ≥ 10mm from umbrella fabric |
| Chamber internal W × D × H | 2200 × 800 × 1300mm |

---

## Assembly notes

1. Print or fabricate motor mount plates from aluminum.
2. Mount each SGM-370 motor directly onto its plate; align motor output shaft with umbrella hub.
3. Connect motor output shaft to umbrella hub using a 6mm-bore PETIYOUZA rigid flange coupling (no separate shaft, no pillow blocks).
4. Verify: spin by hand. Should rotate freely with no binding. Motor is self-locking.
5. Position BLDC fans to blow air across PTC heaters toward umbrella fabric.
6. Wire everything per [wiring/README.md](../wiring/README.md) and [HARDWARE.md](../HARDWARE.md).
