# 3D Model Views (Rev 4)

Engineering-style views of the drying chamber and its three motor stations, with measurements in millimeters. These match the decided Rev 4 chamber (see `HARDWARE.md` section 3): umbrellas dry **half-open** (projected diameter 650 mm), three stations in a row inside a 2200 x 800 x 1300 mm internal chamber — the smallest realistic box that keeps the 50 mm canopy clearance rule.

## Accuracy guarantees (v2 generator)

- **Front / side / top are true-scale 2D orthographic drawings** plotted in exact millimeter coordinates — distances on the drawing are proportional to real distances (equal-aspect axes, red dimension lines with arrows and ticks).
- **Layout assertions run before every render**: wall clearance ≥ 50 mm, canopy-to-canopy ≥ 50 mm, canopy rim height, heater/fan wall fit, coupling bore match (8=8), door vs opening, tray footprint. The script refuses to output images if any check fails — the drawing cannot silently lie.
- **Correct part geometry**: cylindrical shafts/couplings (not boxes), 8-rib canopy section, heater with outlet grille, fan with blades and ring, drain grommet + tube exiting the back wall to the tray, floor slope wedge (4 degrees = 28 mm drop), door with rotary latch, leveling legs.
- The exploded view lifts each assembly group along Z by fixed offsets and labels every part with its real spec.

## Files

| File | View |
|---|---|
| `exploded-view.png` | Exploded assembly: motors, plate, shafts, bearings, holders, canopy, heater, fan, tray |
| `front-view.png` | Front elevation (-Y): chamber W/H, station pitch, shaft, canopy diameter |
| `side-view.png` | Side elevation (-X): chamber D/H, floor slope + drain, heater/fan placement |
| `top-view.png` | Plan: station layout on the X axis, pitch, canopy swing envelope |
| `front-right-view.png` | Axonometric from front-right |
| `front-left-view.png` | Axonometric from front-left |

## Dimension table (all mm, decided Rev 4 — change only with a re-run of the clearance check)

| Parameter | Value | Notes |
|---|---|---|
| Chamber internal W x D x H | 2200 x 800 x 1300 | Real chamber box; cut wall panels 2240 x 840 x 1340 (20 mm walls) |
| Wall thickness | 20 | Panel material allowance |
| Station pitch (X) | 700 | 3 stations, single row on the long axis |
| Motor (worm gear) | 115 x 40 x 36 | SGM-A58SW31ZY, 60 kg-cm, 16 RPM |
| Motor plate (6061) | 6 thick | Spans chamber top |
| Shaft | 8 dia x 300 long | 304 SS, ground |
| Coupling | 8 x 8, 25 long | Rigid clamp |
| Bearings | 2x KP08 per station | Near each shaft end |
| Canopy (half-open, projected) | 650 dia x 200 deep | Umbrellas dry half-open; fully-open commuter canopy is 950-1000 dia |
| Min canopy clearance | 50 (75 at walls, 50 between canopies) | Verified against the 2200 box |
| Floor slope | 3-5 degrees | To drain corner |
| Drain tube | 8 dia | Silicone, to drip tray |
| Drip tray | 500 x 400 x 60 | 500 mL+ capacity |
| Heater (PTC 100 W) | 200 x 100 x 100 | Left wall, low |
| Circulation fan | 120 dia | Right wall, low |
| Heater center height | 220 | Bottom edge 50 clear of the floor (legs 100 + floor panel 20 raise the inner floor to z=120) |

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
