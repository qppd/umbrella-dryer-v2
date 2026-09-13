# 3D Model Views (Rev 4)

Engineering-style views of the drying chamber and its three motor stations, with measurements in millimeters. These are representative reference views for the build and the capstone paper — the paper does not fix chamber dimensions, so the sizes below are design targets that satisfy the verified clearances in `HARDWARE.md` section 3.

## Files

| File | View |
|---|---|
| `exploded-view.png` | Exploded assembly: motors, plate, shafts, bearings, holders, canopy, heater, fan, tray |
| `front-view.png` | Front elevation (-Y): chamber W/H, station pitch, shaft, canopy diameter |
| `side-view.png` | Side elevation (-X): chamber D/H, floor slope + drain, heater/fan placement |
| `top-view.png` | Plan: station layout on the X axis, pitch, canopy swing envelope |
| `front-right-view.png` | Axonometric from front-right |
| `front-left-view.png` | Axonometric from front-left |

## Dimension table (all mm, representative — adjust to your chamber)

| Parameter | Value | Notes |
|---|---|---|
| Chamber internal W x D x H | 1400 x 800 x 1200 | Fits 3 open canopies with clearance |
| Wall thickness | 20 | Panel material allowance |
| Station pitch (X) | 750 | 3 stations, equally spaced |
| Motor (worm gear) | 115 x 40 x 36 | SGM-A58SW31ZY, 60 kg-cm, 16 RPM |
| Motor plate (6061) | 6 thick | Spans chamber top |
| Shaft | 8 dia x 300 long | 304 SS, ground |
| Coupling | 8 x 8, 25 long | Rigid clamp |
| Bearings | 2x KP08 per station | Near each shaft end |
| Canopy (open) | 550 dia x 150 deep | Representative commuter umbrella |
| Min canopy clearance | 50 | Between canopies and to walls |
| Floor slope | 3-5 degrees | To drain corner |
| Drain tube | 8 dia | Silicone, to drip tray |
| Drip tray | 500 x 400 x 60 | 500 mL+ capacity |
| Heater (PTC 100 W) | 200 x 100 x 100 | Left wall, low |
| Circulation fan | 120 dia | Right wall, low |
| Heater center height | 150 | Above floor |

## Regenerating

The PNGs are generated from a single script so the whole set stays consistent when a dimension changes:

```bash
pip install matplotlib numpy
cd model
python generate_models.py
```

Edit the CONSTANTS block at the top of `generate_models.py` (chamber size, pitch, canopy diameter, etc.) and re-run — all six views update.

## Using these in the capstone paper

- Insert as Figures for the design chapter; caption each with its view name.
- The dimension table above doubles as the figure source note.
- If the team later fixes real chamber dimensions (available box, bought sheet sizes), update the constants and regenerate before the final paper print.
