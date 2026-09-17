# Umbrella Dryer V2 — 3D Model

> This folder contains the 3D model of the umbrella dryer frame and station layout.

---

## Model overview

The 3D model shows:
- **3-station frame** — holds 3 umbrellas inverted for drying
- **Motor mounts** — SGM-370 worm gear motors on aluminum plates
- **Shaft alignment** — 6mm shafts through KP08 pillow blocks, connected via rigid couplings
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
| Motor mount plate | 100×80mm aluminum 6mm |
| Shaft length | 300mm (6mm diameter) |
| Pillow block centers | ~250mm apart |
| PTC heater spacing | ≥ 30mm between elements (airflow gap) |
| Fan duct clearance | ≥ 10mm from umbrella fabric |
| Chamber internal W × D × H | 2200 × 800 × 1300mm |

---

## Assembly notes

1. Print or fabricate motor mount plates from aluminum.
2. Bolt KP08 pillow blocks to frame rails.
3. Insert shafts through pillow blocks, connect to motors via rigid couplings.
4. Mount PTC heaters on heat-resistant brackets (ceramic standoffs).
5. Position BLDC fans to blow air across PTC heaters toward umbrella fabric.
6. Wire everything per [wiring/README.md](../wiring/README.md) and [HARDWARE.md](../HARDWARE.md).
