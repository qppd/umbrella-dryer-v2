# 3D Model Views (Rev 5)

Engineering-style views of the drying chamber and its three motor stations, with measurements in millimeters.

**Status: to be produced.** The auto-generated renders that previously lived here were removed — they were not accurate enough to use as build or paper references. The decided dimensions below are the binding design record (see `HARDWARE.md` section 3 for the layout decision).

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
| Heater-fans (2x 1500W PTC, 220V) | freestanding appliances | Chamber floor, designated zone away from the drain/drip path; factory cords out through grommets to plugs outside |
| Exhaust fan (12in Omni, 220V) | 12-in blade in rear-wall opening | Rear wall, ducted out; runs on the mains rocker (no Mega channel) |
| Door | 1600 x 1000 | Front wall, bottom 150 above inner floor, rotary latch |

## Required views (still to be drawn properly)

exploded, front, side, top, front-right, front-left - each fully dimensioned in mm.

Recommended: draw these in a real CAD tool (FreeCAD, Fusion 360, SolidWorks) or have the team sketch them by hand from the table above, then export PNG here. A scripted mesh renderer cannot be trusted for dimensioned drawings without visual checking, which is why the previous set was pulled.
