# Fusion 360 CAD Modeling Strategy — Umbrella Dryer V2

> Created: 2026-09-22  
> Base: `docs/HARDWARE.md`, `docs/BOM.md`, `model/README.md`, `docs/SYSTEM-ARCHITECTURE.md`  
> All dimensions below are extracted directly from these docs or marked with `[PLACEHOLDER]` when not specified.

---

## 1. Coordinate System Recommendation

```
       Y (up)
       │
       │
       ▼
       ○──────────→ X (long axis of chamber, 2200mm)
      /
     /
    Z (depth axis, 800mm)
```

**Origin placement:** Bottom-left-front corner of the **chamber interior** (left end of the long axis, floor level).

| Axis | Direction | Range |
|---|---|---|
| X | Long axis (station row direction) | 0 → 2200 mm |
| Y | Vertical (up) | 0 → 1300 mm |
| Z | Depth axis | 0 → 800 mm |

**Station center positions (X-axis):**

| Station | X center | Z center | Y hub height |
|---|---|---|---|
| Station 1 | 350 mm | 400 mm | ~300 mm |
| Station 2 | 1050 mm | 400 mm | ~300 mm |
| Station 3 | 1750 mm | 400 mm | ~300 mm |

> 700mm pitch is center-to-center; 350mm from each end gives 700mm spacing with 350mm margin on both ends.

---

## 2. Component-Level Model Tree

```
UmbrellaDryerV2 (Root Assembly)
├── _PARAMETERS (Fusion 360 named parameters)
├── Frame (External / Top-level assembly)
│   ├── Base_Rail_Long_X (2×, top + bottom)
│   ├── Base_Rail_Z (2× left, 2× right)
│   ├── Vertical_Pillar (×4, at corners)
│   ├── Top_Frame (outer rectangle 2200×800)
│   ├── Top_Frame_Mid_Support (intermediate cross members)
│   └── Floor_Grid / Sloped_Floor (drainage slope)
├── Station_01 (1 of 3 — parametric, reuse via pattern)
│   ├── Motor_Plate (100×80×6mm aluminum)
│   │   ├── SGM370_Motor_Mount_Holes
│   │   └── Pillow_Block_Mount_Holes
│   ├── Shafts
│   │   ├── Main_Shaft (6mm × 300mm SS)
│   │   ├── Coupling_Motor (6×8mm rigid)
│   │   └── Coupling_Hub (PETIYOUZA 6mm flange)
│   ├── Bearings
│   │   └── UCP06_Pillow_Block (×2 per station, per docs)
│   ├── PTC_Heater (diymore 12V 100W, ~60×42×60mm [confirmed])
│   │   ├── Heater_Mount_Bracket (×3)
│   │   └── Heater_Air_Guide (optional deflector)
│   ├── Blower (AVC 80×80×38mm, ×3)
│   │   ├── Blower_Mount_Frame
│   │   └── Blower_Duct
│   ├── Umbrella_Hub_Mount
│   │   └── Umbrella_Holder (custom geometry)
│   └── Drip_Tray
├── Station_02 (same as Station_01, X+700)
├── Station_03 (same as Station_01, X+1400)
├── Electronics_Enclosure
│   ├── Enclosure_Box
│   ├── Mega_Brush_Hole
│   ├── SSR_Mount_Space (×7: 4×40A + 3×10A)
│   ├── Buck_Converter_Space
│   └── Terminal_Bar_Space
├── Battery_Compartment
│   ├── Battery_Base
│   ├── Battery_Retainer
│   └── Charger_Space
├── Door / Cover (front opening)
│   └── Door_Seal
└── Sensors
    ├── DHT22_Mount (mid-chamber)
    └── DS18B20_Mount (heater airstream)
```

---

## 3. Parameter Table

All values below are **Fusion 360 Sketched Parameters** (Manage → Parameters).

### 3a. Global Parameters

| Name | Value | Unit | Source | Notes |
|---|---|---|---|---|
| `CHAMBER_W` | 2200 | mm | HARDWARE §5 | Confirmed |
| `CHAMBER_D` | 800 | mm | HARDWARE §5 | Confirmed |
| `CHAMBER_H` | 1300 | mm | HARDWARE §5 | Confirmed |
| `STATION_PITCH` | 700 | mm | model/README | Confirmed |
| `NUM_STATIONS` | 3 | — | Design req | Confirmed |
| `UMBRELLA_HUB_H` | 300 | mm | model/README | Approximate (`~300mm`) |
| `CLEARANCE_SIDE` | 75 | mm | HARDWARE §5 | Confirmed |
| `CLEARANCE_BETWEEN` | 50 | mm | HARDWARE §5 | Confirmed |

### 3b. Mechanical Parameters (Per Station)

| Name | Value | Unit | Source | Notes |
|---|---|---|---|---|
| `MOTOR_PLATE_W` | 100 | mm | model/README | Confirmed |
| `MOTOR_PLATE_D` | 80 | mm | model/README | Confirmed |
| `MOTOR_PLATE_T` | 6 | mm | model/README | Confirmed |
| `SHAFT_LEN` | 300 | mm | model/README | Confirmed |
| `SHAFT_DIA` | 6 | mm | model/README | Confirmed |
| `COUPLING_MOTOR` | 6 | mm | BOM §5 | Motor bore |
| `COUPLING_SHAFT` | 8 | mm | BOM §5 | Shaft bore |
| `PILLOW_BLOCK_TYPE` | UCP06 | — | BOM §5 | Confirmed part number |
| `PILLOW_BLOCK_BORE` | 6 | mm | BOM §5 | Confirmed |
| `FLANGE_COUPLING_BORE` | 6 | mm | BOM §5 | PETIYOUZA, confirmed |
| `PTC_CLEARANCE_MIN` | 50 | mm | HARDWARE §3 | ≥ 5cm from wiring/sensors |
| `PTC_GAP_MIN` | 30 | mm | model/README | Between heater elements |
| `BLOWER_CLEARANCE_MIN` | 10 | mm | model/README | From umbrella fabric |

### 3c. Component Dimensions (Confirmed from BOM/HARDWARE)

| Part | Dimension | Source | Status |
|---|---|---|---|
| PTC heater (diymore 12V 100W) | ~60×42×60 mm | BOM §9 | Approximate (body only) |
| AVC blower (80×80×38mm) | 80×80×38 mm | BOM §4 / HARDWARE §2 | Confirmed |
| SGM-370 motor | See [1] | BOM §5 | External part — model as placeholder |
| SSR-40DD (LCTC) | ~40×24×22 mm | BOM §4 | Approximate (standard module) |
| SSR-10DD (LCTC) | ~28×18×14 mm | BOM §3 | Approximate (standard module) |
| SSR heatsink (BLACK) | 80×50×50 mm | BOM §4 | Confirmed |
| LM2596S buck | ~43×21×15 mm | BOM §4 | Approximate |
| Arduino Mega 2560 + terminal | 105×53×? mm | BOM §4 | Standard board |
| 16×2 LCD I2C | 80×36×12 mm | BOM §4 | Standard |
| LiFePO4 200Ah battery | `[PLACEHOLDER]` | BOM §7a | **Not in docs** — measure before modeling |
| DHT22 module | 15×25×? mm | BOM §4 | Approximate |
| DS18B20 probe | 12×Ø4×? mm | BOM §4 | Approximate |
| Arcade button (5V) | Ø22×? mm | BOM §4 | Approximate |

> **[1]** SGM-370 motor physical dimensions are NOT in the docs. Typical N20-style worm gear: ~37×57×37mm. Model as `[PLACEHOLDER]` and replace when you have the datasheet.

### 3d. Assumed Placeholders (NOT confirmed — verify before machining)

| Parameter | Assumed Value | Reason |
|---|---|---|
| Frame rail profile | 20×40mm square tube | Typical for 2.2m span |
| Frame wall thickness | 1.5 mm | Light-weight aluminum |
| Floor panel thickness | 2 mm | Perforated sheet or mesh |
| Door material | 5mm polycarbonate sheet | Translucent, lightweight |
| Drip tray depth | 30 mm | Below floor level |
| Drip tray width | 150 mm | Under each station |
| Electronics enclosure size | 120×80×50 mm | Needs measurement |
| Battery compartment size | `[PLACEHOLDER]` | Battery physical dims unknown |
| Chamber wall material | 3mm aluminum sheet | Lightweight, corrosion-resistant |
| Pillar spacing | 700mm (aligned with stations) | Matches station pitch |

---

## 4. Critical Dimensions & Constraints

### 4a. Chamber Envelope (fixed)

```
Outer envelope: 2200 × 800 × 1300 mm (internal)
Wall thickness: assume 10mm → outer: 2220 × 820 × 1320 mm
```

### 4b. Station Layout (X-axis)

```
[Left wall] 350mm [Station 1 center] 700mm [Station 2 center] 700mm [Station 3 center] 350mm [Right wall]
              ←──────── CHAMBER_W (2200mm) ────────→
```

### 4c. Vertical Stack (per station, Y-axis from floor)

```
Y=0      ── Floor
Y=30     ── Drip tray bottom
Y=60     ── Drip tray top
Y=100    ── Shaft centerline (hub height ~300mm — adjust based on actual shaft mount)
Y=300    ── Umbrella hub center (half-open canopy apex)
Y=420    ── Canopy edge (r≈650/2≈325mm radius, half-open ~650mm projected)
Y=500    ── PTC heater row (below canopy, blowing upward)
Y=560    ── AVC blower row (behind PTC, blowing across)
Y=700    ── Top frame
Y=1300   ── Chamber top (roof)
```

> **Note:** Y=100–560 are assumed. Verify by measuring actual PTC + blower + shaft mount when components arrive.

### 4d. Heat & Airflow Clearance

| Clearance | Min | Source |
|---|---|---|
| PTC → wiring/sensors | ≥ 50 mm | HARDWARE §3 |
| PTC element spacing | ≥ 30 mm | model/README |
| Blower → umbrella fabric | ≥ 10 mm | model/README |
| Station-to-station gap | ≥ 50 mm | HARDWARE §5 |

---

## 5. Assembly Joints (Fusion 360 Constraints)

### 5a. Station Assembly (per station, internal)

| Component A | Component B | Joint Type | Constraint |
|---|---|---|---|
| `SGM370_Motor` | `Motor_Plate` | Insert | Motor body centered on plate |
| `Coupling_Motor` | `SGM370_Motor` shaft | Insert | Coaxial, flush |
| `Main_Shaft` | `Coupling_Motor` | Insert | Coaxial |
| `Main_Shaft` | `UCP06_Pillow_Block` (×2) | Insert | Shaft through bearing ID |
| `UCP06_Pillow_Block` | `Motor_Plate` | coincident | Bottom face on plate |
| `Coupling_Hub` | `Main_Shaft` end | Insert | Coaxial |
| `Umbrella_Hub_Mount` | `Coupling_Hub` | Insert | Coaxial |
| `PTC_Heater` (×3) | `Heater_Mount_Bracket` | Angle | Facing canopy underside |
| `AVC_Blower` (×3) | `Blower_Mount_Frame` | Angle | Blowing toward PTC → canopy |
| `Drip_Tray` | `Station_Base` | Coincident | Below shaft level |

### 5b. Frame Assembly

| Component A | Component B | Joint Type | Constraint |
|---|---|---|---|
| `Base_Rail_Long_X` | `Base_Rail_Z` (left) | T-joint | Corner |
| `Base_Rail_Long_X` | `Base_Rail_Z` (right) | T-joint | Corner |
| `Vertical_Pillar` | `Base_Rail` | Tee | Perpendicular |
| `Top_Frame` | `Vertical_Pillar` | Tee | Perpendicular |
| `Top_Frame_Mid_Support` | `Base_Rail` | T-joint | Spanning X or Z |
| `Station_01_Base` | `Base_Rail_Long_X` | Angle | At X=350 |
| `Station_02_Base` | `Base_Rail_Long_X` | Angle | At X=1050 |
| `Station_03_Base` | `Base_Rail_Long_X` | Angle | At X=1750 |

### 5c. Electronics Enclosure Mount

| Component A | Component B | Joint Type | Constraint |
|---|---|---|---|
| `Electronics_Enclosure` | `Frame_Pillar` | Angle | Side-mounted, accessible |
| `Battery_Compartment` | `Frame_Base` | Coincident | Bottom of chamber |
| `DHT22_Mount` | `Chamber_Wall` (mid) | Angle | Mid-chamber, away from direct airflow |
| `DS18B20_Mount` | `Heater_Air_Guide` | Angle | In heated airstream path |

---

## 6. Measurement Priorities

### 6a. Must Measure Before Modeling (critical path)

1. **LiFePO4 200Ah battery physical dimensions** — determines battery compartment size and chassis base length
2. **SGM-370 motor mounting hole pattern** — needed for Motor_Plate cutout
3. **UCP06 pillow block outer dimensions** — needed for plate mount holes
4. **PETIYOUZA flange coupling dimensions** — needed for umbrella holder geometry
5. **SSR-40DD / SSR-10DD module dimensions** — needed for enclosure layout

### 6b. Should Verify After Components Arrive

6. **PTC heater physical size** — current spec says ~6×4.2×6cm but verify actual unit
7. **AVC blower mounting hole pattern** — 80×80mm frame, need screw spacing
8. **Arcade button diameter & mounting depth** — for enclosure panel cutout
9. **LCD 16×2 I2C bezel cutout** — 80×36mm standard, but verify

### 6c. Low Priority (can be refined iteratively)

10. Drip tray shape and slope angle
11. Door hinge type and seal profile
12. Internal wire routing channels
13. Grommet sizes for chamber wall penetrations

---

## 7. Modeling Workflow Recommendation

```
Phase 1 — Frame (1 day)
  ├─ Create sketch on XY plane at Y=0
  ├─ Extrude base rails (2200×800mm outline)
  ├─ Extrude 4 vertical pillars (1300mm tall)
  ├─ Extrude top frame rails
  ├─ Add mid-support cross members at 700mm intervals
  └─ Publish external references for station mounting points

Phase 2 — Station Template (1 day)
  ├─ Create one parametric station at X=350mm
  ├─ Model Motor_Plate (100×80×6mm) with constraint-driven hole patterns
  ├─ Model Main_Shaft (6×300mm) as cylinder — simple boolean
  ├─ Model UCP06 as cylinder with outer ring (use actual dims from #6a)
  ├─ Model 3× PTC heaters with 30mm gap spacing
  ├─ Model 3× AVC blowers with 10mm fabric clearance
  ├─ Model Drip_Tray with drainage slope
  └─ Test: move station to X=1050 and X=1750 — verify no overlap

Phase 3 — Electronics & Battery (0.5 day)
  ├─ Model Electronics_Enclosure with cutouts for Mega, SSRs, LCD, button
  ├─ Model Battery_Compartment sized to actual battery (#6a #1)
  └─ Position in frame assembly

Phase 4 — Door & Details (0.5 day)
  ├─ Front door (hinged or removable panel)
  ├─ Ventilation openings (top/bottom)
  └─ Wire grommets at chamber wall penetrations

Phase 5 — Design Review (0.5 day)
  ├─ Run interference check (especially PTC→wiring 50mm clearance)
  ├─ Verify all 3 stations fit within chamber envelope
  ├─ Check service access ( SSR swap, battery pull-out)
  └─ Export STEP for fabrication
```

---

## 8. Fusion 360 File Organization

```
UmbrellaDryerV2.f3d
├── Design: Frame
│   └── (all frame sketches + bodies)
├── Design: Station_Template
│   └── (motor plate, shaft, bearings, heaters, blowers, tray)
├── Design: Electronics
│   └── (enclosure, mounting brackets)
├── Design: Battery
│   └── (compartment, retainer)
├── Assembly: UmbrellaDryerV2
│   ├── Frame component (linked)
│   ├── Station_01 (linked, X=350)
│   ├── Station_02 (linked, X=1050)
│   ├── Station_03 (linked, X=1750)
│   ├── Electronics_Enclosure (linked)
│   └── Battery_Compartment (linked)
└── Sketches: Parameters
    └── (all named parameters defined here)
```

**Key tip:** Model the station **once** in its own design file, then reference it into the main assembly three times at different X positions. This way changing the station template auto-updates all 3 stations.

---

## 9. What Is NOT Invented (Strict Policy)

The following are intentionally **left as `[PLACEHOLDER]` or external parts** because their exact dimensions are not in any project doc:

- SGM-370 motor body dimensions (use external part import or placeholder box)
- LiFePO4 200Ah battery dimensions (must measure)
- SSR-40DD exact footprint (approximate, verify)
- Chassis wall/frame profile (assumed 20×40mm tube, but needs confirmation)
- Door mechanism (not specified in docs)
- Internal wire routing (will be determined during build)

These will be refined when components are received and measured.
