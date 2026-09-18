# Umbrella Dryer V2 — 3D Model

> This folder contains the 3D model of the umbrella dryer frame and station layout.

---

## Model overview

The 3D model shows:
- **3-station frame** — holds 3 umbrellas inverted for drying
- **Motor mounts** — SGM-370 worm gear motors on aluminum plates
- **Drivetrain** — per station: SGM-370 motor → rigid coupling 6×8mm → 6mm × 300mm shaft → UCP06 pillow block (shaft passes through the bearing's middle) → PETIYOUZA 6mm flange coupling → umbrella hub; all bolted to the aluminum plate
- **PTC heater placement** — 3× PTC ceramic heaters per station, positioned for airflow
- **AVC blower placement** — 3× 80mm blowers per station, positioned for air circulation
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
| Motor drivetrain | rigid coupling 6×8mm · 6mm × 300mm SS shaft · UCP06 pillow block (mid-shaft) · PETIYOUZA flange, 6mm bore (motor → shaft → hub) |
| PTC heater spacing | ≥ 30mm between elements (airflow gap) |
| Fan duct clearance | ≥ 10mm from umbrella fabric |
| Chamber internal W × D × H | 2200 × 800 × 1300mm |

---

## Assembly notes

1. Print or fabricate motor mount plates from aluminum.
2. Mount each SGM-370 motor directly onto its plate; align motor output shaft with umbrella hub.
3. Drivetrain per station, in order: rigid coupling 6×8mm on the motor output shaft, then the 6mm × 300mm shaft through the UCP06 pillow block (shaft centered in the bearing), then the PETIYOUZA 6mm flange coupling to the umbrella hub. Motor and pillow block share the aluminum plate.
4. Verify: spin by hand. Should rotate freely with no binding. Motor is self-locking.
5. Position AVC blowers to blow air across PTC heaters toward umbrella fabric.
6. Wire everything per [wiring/README.md](../wiring/README.md) and [HARDWARE.md](../HARDWARE.md).
