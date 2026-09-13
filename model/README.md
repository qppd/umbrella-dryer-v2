# 3D Model Views (Rev 6)

Engineering-style views of the drying chamber and its three motor stations, with measurements in millimeters.

**Status: to be produced in Fusion 360 (3D machine model) and Cirkit Designer (wiring/schematic).** Export PNGs into this folder when done. An earlier scripted-render attempt was removed for inaccuracy — use a real CAD tool. The decided dimensions below are the binding design record (see `HARDWARE.md` section 3 for the layout decision).

## Decided dimensions (all mm)

| Parameter | Value | Notes |
|---|---|---|
| Chamber internal W x D x H | 2200 x 800 x 1300 | Real chamber box; cut wall panels 2240 x 840 x 1340 (20 mm walls) |
| Legs | 100 | Floor panel top at z = 120 |
| Station pitch (X) | 700 | 3 stations, single row on the long axis |
| Motor (worm gear) | 115 x 40 x 36 | SGM-A58SW31ZY, 60 kg-cm, 16 RPM |
| Motor plate (6061) | 6 thick | Spans chamber top |
| Shaft | 8 dia x 300 long | 304 SS, ground |
| Coupling | 8 x 8, 25 long | Rigid clamp |
| Bearings | 2x KP08 per station | Near each shaft end |
| Canopy (half-open, projected) | 650 dia x 200 deep | Umbrellas dry half-open; fully-open commuter canopy is 950-1000 dia |
| Min canopy clearance | 50 (75 at walls, 50 between canopies) | Verified against the 2200 box |
| Floor slope | 3-5 degrees (4 deg = 28 mm drop) | To drain corner (+X, +Y) |
| Drain tube | 8 dia | Silicone, exits back wall to drip tray |
| Drip tray | 500 x 400 x 60 | 500 mL+ capacity |
| Heater-fans (2x 1500W PTC, 220V) | ~200 x 200 x 250 each (verify against the purchased unit) | Freestanding on chamber floor, zone away from the drain/drip path; factory cords out through grommets to plugs outside |
| Exhaust fan (12in Omni, 220V) | ~300 dia blade in rear-wall opening (verify) | Rear wall, ducted out; runs on the mains rocker (no Mega channel) |
| Door | 1600 x 1000 | Front wall, bottom 150 above inner floor, rotary latch |

## For the CAD work

- **Fusion 360:** model from the dimension table above — frame/walls, sloped floor + drain, 3 stations (motor plate, KP08 bearings, 8x300 shaft, coupling, half-open canopy), door + latch, legs, appliance placements. Parametric dimensions so the team can adjust after measuring the real heater-fans and fan.
- **Cirkit Designer:** follow `wiring/README.md` (master list) and `docs/BLOCK-DIAGRAM.md` (topology) — 3 domains kept separate: 220V AC (RCD -> rocker -> 10A fuses -> SSR-40DA x2 -> heater-fans; fan gang), 12V DC (battery -> DC rocker -> 25A -> 3A x3 -> motors; 3A -> buck), 5V logic (Mega, sensors, LCD, relay coils). Label D2-D13 + 20/21 as in the pin map.
- Target views: exploded, front, side, top, front-right, front-left - each fully dimensioned in mm.
- The single DHT22 (D2) and DS18B20 probe (D3) are chamber-wide sensors - one of each, not per station.
- The 12in exhaust fan has no Mega channel - do not draw a control wire to it (mains rocker only).

## Required views

exploded, front, side, top, front-right, front-left - each fully dimensioned in mm, exported as PNG into this folder.
