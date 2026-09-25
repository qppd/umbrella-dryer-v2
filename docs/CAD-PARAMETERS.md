# Fusion 360 Parameter Quick Reference

> Copy these directly into Fusion 360 → Manage → Parameters.
> Green = confirmed from docs | Amber = approximate | Red = placeholder — measure before build

## Global

| Name | Value | Unit | Source | Status |
|---|---|---|---|---|
| CHAMBER_W | 2200 | mm | HARDWARE §5 | ✅ Confirmed |
| CHAMBER_D | 800 | mm | HARDWARE §5 | ✅ Confirmed |
| CHAMBER_H | 1300 | mm | HARDWARE §5 | ✅ Confirmed |
| STATION_PITCH | 700 | mm | model/README | ✅ Confirmed |
| NUM_STATIONS | 3 | — | Design req | ✅ Confirmed |
| CLEARANCE_SIDE | 75 | mm | HARDWARE §5 | ✅ Confirmed |
| CLEARANCE_BETWEEN | 50 | mm | HARDWARE §5 | ✅ Confirmed |

## Station

| Name | Value | Unit | Source | Status |
|---|---|---|---|---|
| MOTOR_PLATE_W | 100 | mm | model/README | ✅ Confirmed |
| MOTOR_PLATE_D | 80 | mm | model/README | ✅ Confirmed |
| MOTOR_PLATE_T | 6 | mm | model/README | ✅ Confirmed |
| SHAFT_LEN | 300 | mm | model/README | ✅ Confirmed |
| SHAFT_DIA | 6 | mm | model/README | ✅ Confirmed |
| COUPLING_MOTOR | 6 | mm | BOM §5 | ✅ Confirmed |
| COUPLING_SHAFT | 8 | mm | BOM §5 | ✅ Confirmed |
| PILLOW_BLOCK_TYPE | UCP06 | — | BOM §5 | ✅ Confirmed |
| PILLOW_BLOCK_BORE | 6 | mm | BOM §5 | ✅ Confirmed |
| FLANGE_BORE | 6 | mm | BOM §5 | ✅ Confirmed |
| PTC_GAP | 30 | mm | model/README | ✅ Confirmed |
| PTC_CLEARANCE | 50 | mm | HARDWARE §3 | ✅ Confirmed |
| BLOWER_CLEARANCE | 10 | mm | model/README | ✅ Confirmed |
| UMBRELLA_HUB_H | 300 | mm | model/README | 🟡 Approximate (~300mm) |
| SGM370_W | 37 | mm | BOM §5 | 🔴 Placeholder (typical N20) |
| SGM370_H | 57 | mm | BOM §5 | 🔴 Placeholder (typical N20) |
| SGM370_D | 37 | mm | BOM §5 | 🔴 Placeholder (typical N20) |

## Components

| Name | Value | Unit | Source | Status |
|---|---|---|---|---|
| AVC_W | 80 | mm | BOM §4 | ✅ Confirmed |
| AVC_D | 80 | mm | BOM §4 | ✅ Confirmed |
| AVC_H | 38 | mm | BOM §4 | ✅ Confirmed |
| PTC_W | 60 | mm | BOM §9 | ✅ Confirmed (60×60×42) |
| PTC_D | 60 | mm | BOM §9 | ✅ Confirmed |
| PTC_H | 42 | mm | BOM §9 | ✅ Confirmed (thickness) |
| PTC_MOUNT_HOLE_DIST | 87 | mm | BOM §9 | ✅ Confirmed (mounting holes) |
| PTC_MOUNT_HOLE_SIZE | 4 | mm | BOM §9 | ✅ Confirmed (Ø) |
| SSR40_W | 40 | mm | BOM §4 | 🟡 Approx (standard) |
| SSR40_D | 24 | mm | BOM §4 | 🟡 Approx (standard) |
| SSR40_H | 22 | mm | BOM §4 | 🟡 Approx (standard) |
| SSR10_W | 28 | mm | BOM §3 | 🟡 Approx (standard) |
| SSR10_D | 18 | mm | BOM §3 | 🟡 Approx (standard) |
| SSR10_H | 14 | mm | BOM §3 | 🟡 Approx (standard) |
| HEATSINK_W | 80 | mm | BOM §4 | ✅ Confirmed |
| HEATSINK_D | 50 | mm | BOM §4 | ✅ Confirmed |
| HEATSINK_H | 50 | mm | BOM §4 | ✅ Confirmed |
| BUCK_W | 43 | mm | BOM §4 | 🟡 Approx |
| BUCK_D | 21 | mm | BOM §4 | 🟡 Approx |
| BUCK_H | 15 | mm | BOM §4 | 🟡 Approx |
| MEGA_W | 105 | mm | BOM §4 | ✅ Standard board |
| MEGA_D | 53 | mm | BOM §4 | ✅ Standard board |
| LCD_W | 80 | mm | BOM §4 | ✅ Standard 16×2 |
| LCD_D | 36 | mm | BOM §4 | ✅ Standard 16×2 |
| BATTERY_W | — | mm | BOM §7a | 🔴 MEASURE FIRST |
| BATTERY_D | — | mm | BOM §7a | 🔴 MEASURE FIRST |
| BATTERY_H | — | mm | BOM §7a | 🔴 MEASURE FIRST |

## Frame (assumed)

| Name | Value | Unit | Source | Status |
|---|---|---|---|---|
| RAIL_PROFILE_W | 40 | mm | Assumed | 🟡 Typical |
|| RAIL_PROFILE_H | 20 | mm | Assumed | 🟡 Typical |
|| RAIL_THICKNESS | 1.5 | mm | Assumed | 🟡 Typical |
|| WALL_THICKNESS | 10 | mm | Assumed | 🟡 For outer envelope |
|| DOOR_THICKNESS | 5 | mm | Assumed | 🟡 Polycarbonate |
|| DOOR_LOCK_TYPE | Solenoid lock 12VDC (Makerlab) | — | BOM §4 | ✅ Confirmed (fail-secure) |
|| REED_SWITCH_TYPE | Magnetic Door Reed Switch Set NO/NC (Makerlab) | — | BOM §4 | ✅ Confirmed (NO contacts) |
|| TRAY_DEPTH | 30 | mm | Assumed | 🟡 Design choice |
