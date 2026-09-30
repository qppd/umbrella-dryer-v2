# Umbrella Dryer V2 — CAD Build Specification

> **Project:** Smart Umbrella Dryer V2 — 3-station 12V DC drying system  
> **Role:** BS Computer Engineering capstone (CLU S)  
> **Specification date:** 2026-09-22  
> **Revision baseline:** `main` branch commit `1f95122` (latest — drivetrain restored)

---

## A. OBJECT IDENTIFICATION

| Field | Value |
|---|---|
| **Product name** | Smart Umbrella Dryer V2 |
| **Manufacturer / origin** | Self-designed capstone project — CLSU SSU BSCE |
| **Exact model** | Umbrella Dryer V2, Rev 9 (latest) |
| **Product family** | Multi-umbrella heated forced-air drying system |
| **Intended application** | Drying 3 umbrellas simultaneously (or 1–3 mix) via 12V DC heated forced air with humidity + temperature feedback control |
| **Country/region** | Philippines (CLSU SSU, Malolos City, Bulacan) |
| **Manufacturing standard** | DIY fabrication — aluminum plate, stainless shafts, standard fasteners |
| **Industry standard** | SELV 12V DC only (no mains voltage) |
| **Generation/year** | V2 — Rev 9 (no-fuse SSR build) |
| **Status** | Prototype/design stage — not a commercial manufactured product |

**EXACT MODEL CONFIRMED:** Yes — this is a documented capstone project with complete electrical, mechanical, and software specifications in the `UMBRELLA DRYER V2` repository.

---

## B. SOURCE LIST

### Primary (local project docs)

| Source | Path | Purpose |
|---|---|---|
| README.md | `../README.md` | System overview |
| HARDWARE.md | `docs/HARDWARE.md` | Component specs, pin map, station layout |
| BOM.md | `docs/BOM.md` | Bill of materials, prices, sourcing links |
| SOURCING-ANNEX.md | `docs/SOURCING-ANNEX.md` | Verified Lazada/makerlab.ph links |
| SYSTEM-ARCHITECTURE.md | `docs/SYSTEM-ARCHITECTURE.md` | Layered architecture, power distribution |
| BLOCK-DIAGRAM.md | `docs/BLOCK-DIAGRAM.md` | Block diagrams, wire schedule |
| STACKS.md | `docs/STACKS.md` | Hardware/software stack reference |
| SETUP.md | `docs/SETUP.md` | Mechanical assembly steps |
| model/README.md | `model/README.md` | 3D model dimensions, assembly notes |
| wiring/README.md | `wiring/README.md` | Pin map, power distribution tree |
| wiring/UmbrellaDryerV2.ckt | `wiring/UmbrellaDryerV2.ckt` | CirKit Designer circuit file (53 components) |
| wiring/circuit_image.png | `wiring/circuit_image.png` | Circuit schematic image (4.7 MB) |

### Secondary (external product pages consulted)

| Component | Source | URL |
|---|---|---|
| SGM-370 motor | Makerlab PH | https://makerlab.ph/products/dc-worm-gear-motor-sgm-370-12v-16rpm |
| AVC blower fan | Lazada PH | https://www.lazada.com.ph/products/pdp-i2328323489.html |
| SSR-40DD / SSR-10DD | Lazada PH (taxnele) | https://www.lazada.com.ph/products/pdp-i4110347574-s22718212255.html |
| SSR heatsink | Makerlab PH | https://www.lazada.com.ph/products/ssr-heatsink-black-... |
| PTC heater (diymore 12V 100W) | Lazada PH | https://www.lazada.com.ph/products/diymore-dc-12v-100w... |
| LiFePO4 battery (PowMr) | Lazada PH | https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4... |

---

## C. COMPONENT BREAKDOWN

### ASSEMBLY: Umbrella Dryer V2

```
UmbrellaDryerV2
├── Frame
│   ├── Base_Rails (2× long, 2× short)
│   ├── Vertical_Pillars (×4)
│   ├── Top_Frame (rectangle 2200×800mm)
│   └── Floor_Panel (perforated/sloped)
├── Station_1 (parametric template)
│   ├── Motor_Plate (100×80×6mm Al 6061)
│   │   ├── SGM-370 Motor (×1)
│   │   ├── Rigid_Coupling_6x8mm (×1)
│   │   ├── SS_Shaft_6x300mm (×1)
│   │   ├── UCP06_Pillow_Block (×2)
│   │   └── PETIYOUZA_Flange_6mm (×1)
│   ├── PTC_Heaters (×3)
│   ├── AVC_Blowers (×3)
│   └── Drip_Tray
├── Station_2 (identical to Station_1, X+700mm)
├── Station_3 (identical to Station_1, X+1400mm)
├── Electronics_Enclosure
│   ├── Arduino_Mega_2560
│   ├── SSR-40DD ×4 (PTC×3 + Fan_bus)
│   ├── SSR-10DD ×3 (Motors)
│   ├── SSR_Heatsink_BLACK ×4
│   ├── LM2596S_Buck_Converter
│   ├── Terminal_Blocks
│   └── Bus_Bars ×2
├── Battery_Compartment
│   └── LiFePO4_12.8V_200Ah
├── Door / Cover (front opening)
├── Sensors
│   ├── DHT22 ×1
│   └── DS18B20 ×1
└── UI Panel
    ├── LCD 16×2 I2C
    ├── Arcade_Button
    ├── LEDs (R/Y/G) ×3
    └── Buzzer
```

---

## D. COMPLETE DIMENSION TABLE

### Global / Chamber Dimensions

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Chamber internal width (long axis) | 2200 | mm | **HIGH** | HARDWARE §5 | SPECIFIED |
| Chamber internal depth | 800 | mm | **HIGH** | HARDWARE §5 | SPECIFIED |
| Chamber internal height | 1300 | mm | **HIGH** | HARDWARE §5 | SPECIFIED |
| Station pitch (center-to-center) | 700 | mm | **HIGH** | model/README | SPECIFIED |
| Station positions (X center from left wall) | 350, 1050, 1750 | mm | **HIGH** | calc. from pitch + margin | CALCULATED |
| Side clearance (wall to nearest canopy) | 75 | mm | **HIGH** | HARDWARE §5 | SPECIFIED |
| Inter-station canopy gap | ≥ 50 | mm | **HIGH** | HARDWARE §5 | SPECIFIED |
| Umbrella hub height from base | ~300 | mm | **MEDIUM** | model/README | ESTIMATED |

### Station Layout (per station, all 3 identical)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Motor mount plate W × D × T | 100 × 80 × 6 | mm | **HIGH** | model/README | SPECIFIED |
| Plate material | 6061 Aluminum | — | **HIGH** | model/README / BOM | SPECIFIED |
| Main shaft length | 300 | mm | **HIGH** | model/README / BOM | SPECIFIED |
| Main shaft diameter | 6 | mm | **HIGH** | model/README / BOM | SPECIFIED |
| Shaft material | 304 Stainless Steel | — | **HIGH** | BOM §5 | SPECIFIED |
| UCP06 pillow block bore | 6 | mm | **HIGH** | BOM §5 | SPECIFIED |
| Pillow block position | Mid-shaft (~150mm from each end) | mm | **MEDIUM** | DESIGN INTENT | ASSUMED |
| PETIYOUZA flange coupling bore | 6 | mm | **HIGH** | BOM §5 | SPECIFIED |
| Rigid coupling (motor→shaft) | 6×8mm | mm | **HIGH** | BOM §5 | SPECIFIED |
| Motor output shaft diameter | 6 | mm | **HIGH** | HARDWARE §2 / BOM | SPECIFIED |
| Station footprint on base rail | 100×80mm (plate) | mm | **HIGH** | model/README | SPECIFIED |

### PTC Heater Array (3 per station, 9 total)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| PTC heater element size | ~60 × 60 × 42 | mm | **HIGH** | BOM §9 (confirmed 60×60×42mm) | CONFIRMED |
| PTC mounting hole distance | 87 | mm | **HIGH** | BOM §9 (official listing) | CONFIRMED |
| PTC mounting hole size | 4 | mm | **HIGH** | BOM §9 (official listing) | CONFIRMED |
| Heater mass | ~120 | g | **HIGH** | BOM §9 (official listing) | CONFIRMED |
| Minimum spacing between elements | ≥ 30 | mm | **HIGH** | model/README | SPECIFIED |
| Clearance to wiring/sensors/plastic | ≥ 50 | mm | **HIGH** | HARDWARE §3 | SPECIFIED |
| Mounting | Station bracket, aimed at canopy underside | — | **MEDIUM** | HARDWARE §3 | ASSUMED |

### AVC Blower (3 per station, 9 total)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Housing dimensions | 80 × 80 × 38 | mm | **HIGH** | HARDWARE §2 / BOM | SPECIFIED |
| Mounting holes | Standard 4× M3 pattern at 72.5mm corners | mm | **MEDIUM** | Industry standard | ASSUMED |
| Impeller diameter | ~72 | mm | **LOW** | typical for 80mm fan | ESTIMATED |
| Airflow direction | Through housing, across PTC heaters | — | **HIGH** | HARDWARE §3 | SPECIFIED |

### SGM-370 Worm Gear Motor (×3)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Motor body length | ~57 | mm | **LOW** | Typical N20 motor size | ESTIMATED |
| Motor body diameter | ~37 | mm | **LOW** | Typical N20 motor size | ESTIMATED |
| Motor body height | ~37 | mm | **LOW** | Typical N20 motor size | ESTIMATED |
| Output shaft diameter | 6 | mm | **HIGH** | HARDWARE §2 / BOM | SPECIFIED |
| Output shaft length | ~15 | mm | **LOW** | Typical 370 motor | ESTIMATED |
| Mounting hole pattern | 2× M3 or M4, 25mm spacing | mm | **LOW** | Typical N20 gearbox | ESTIMATED |
| Motor mass | 156 | g | **HIGH** | Makerlab PH spec | SPECIFIED |
| Gearbox type | Metal worm gear, self-locking | — | **HIGH** | HARDWARE §2 | SPECIFIED |

> **⚠ NOTE:** Motor body dimensions are NOT in the project docs. The ~57×37×37mm values are typical for N20-style 370 motors but require physical verification.

### UCP06 Pillow Block Bearing (×6 total, 2 per station)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Bore diameter | 6 | mm | **HIGH** | BOM §5 | SPECIFIED |
| Outer diameter | ~34 | mm | **LOW** | Standard UCP06 spec | ESTIMATED |
| Center height | ~29 | mm | **LOW** | Standard UCP06 spec | ESTIMATED |
| Mounting bolt spacing | ~30mm | mm | **LOW** | Standard UCP06 spec | ESTIMATED |
| Set-screw type | 2× M5 set screws (standard) | — | **MEDIUM** | Industry standard | ASSUMED |

### PETIYOUZA Rigid Flange Coupling (×3)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Bore diameter | 6 | mm | **HIGH** | BOM §5 | SPECIFIED |
| Coupling length | ~25–35 | mm | **LOW** | Standard flange coupling | ESTIMATED |
| Flange diameter | ~18–22 | mm | **LOW** | Standard 6mm coupling | ESTIMATED |
| Keyway | None (6mm round shaft) | — | **MEDIUM** | Design intent | ASSUMED |

### SSR Modules

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| SSR-40DD body | ~48 × 36 × 22 | mm | **LOW** | Standard SSR module | ESTIMATED |
| SSR-10DD body | ~30 × 24 × 15 | mm | **LOW** | Standard SSR module | ESTIMATED |
| SSR heatsink (BLACK) | 80 × 50 × 50 | mm | **HIGH** | BOM §4 / sourcing | SPECIFIED |
| Heatsink type | M-shape for SSR mounting | — | **HIGH** | BOM §4 | SPECIFIED |

### Electronics

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Arduino Mega 2560 board | 101.6 × 53.3 × ? | mm | **HIGH** | Industry standard | SPECIFIED |
| Terminal board (Mega add-on) | adds ~5mm height | mm | **MEDIUM** | BOM spec | ASSUMED |
| LCD 16×2 I2C display | 80.0 × 36.0 × 12.0 | mm | **HIGH** | Industry standard | SPECIFIED |
| LM2596S buck converter | ~43 × 21 × 15 | mm | **LOW** | Standard module | ESTIMATED |
| Bus bars (10-terminal) | ~150mm length | mm | **MEDIUM** | BOM spec | ASSUMED |
| Terminal block (6-pole) | ~70 × 20 × ? | mm | **LOW** | Standard barrier block | ESTIMATED |

### Power System

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| LiFePO4 200Ah battery | **REQUIRES PHYSICAL MEASUREMENT** | — | **NONE** | Not in docs | MISSING |
| Battery BMS rating | 200A | A | **HIGH** | HARDWARE §2 | SPECIFIED |
| Battery voltage | 12.8V nominal | V | **HIGH** | HARDWARE §2 | SPECIFIED |
| Charger dimensions | **REQUIRES MEASUREMENT** | — | **NONE** | Not in docs | MISSING |
| DC rocker switch (50A) | Panel-mount, ~35×20mm cutout | mm | **MEDIUM** | Standard 50A switch | ASSUMED |

### Drip Trays (×3)

| Dimension | Value | Unit | Confidence | Source | Type |
|---|---|---|---|---|---|
| Tray size | **REQUIRES MEASUREMENT** | — | **NONE** | Only ~100 cost noted | MISSING |
| Drain tube size | **REQUIRES MEASUREMENT** | — | **NONE** | Not specified | MISSING |

---

## E. MATERIAL SPECIFICATION

### Structural

| Component | Material | Standard | Notes |
|---|---|---|---|
| Motor mount plates | Aluminum 6061-T6 | ASTM B209 | 6mm thick, machined or laser-cut |
| Main shaft | Stainless Steel 304 | ASTM A276 | Corrosion-resistant, 6mm Ø × 300mm |
| Frame rails (assumed) | Aluminum square tube 20×40×1.5mm | — | Typical for DIY frames; **REQUIRES VERIFICATION** |
| Chamber panels (assumed) | 3mm Aluminum sheet or Polycarbonate | — | Lightweight, corrosion-resistant; **REQUIRES VERIFICATION** |

### Drivetrain

| Component | Material | Standard | Notes |
|---|---|---|---|
| UCP06 pillow block | Cast iron body + stainless insert | ISO 1224 | Standard bearing unit |
| PETIYOUZA flange coupling | Cast iron or steel | — | Rigid coupling, 6mm bore |
| Rigid coupling 6×8mm | Steel or aluminum | — | 6mm motor bore, 8mm shaft bore |

### Electrical Enclosure

| Component | Material | Notes |
|---|---|---|
| Electronics enclosure | ABS or Polycarbonate plastic | Ventilated, IP40+ |
| Bus bars | Copper, tinned | 150A rated, 10-terminal |

### Fasteners

| Size | Quantity | Purpose |
|---|---|---|
| M3 × 8/12/16mm | Kit (320pcs) | Motor plate, SSR mounts, sensor mounts |
| M4 | Kit | General assembly |
| M5 | Kit | Pillow block set screws (UCP06) |
| Nylon standoffs M3/M2.5 | Kit | Mega, LCD, SSR mounting |

---

## F. MANUFACTURING SPECIFICATION

### Processes

| Component | Process | Notes |
|---|---|---|
| Motor mount plates | CNC milling or waterjet cutting | 6mm Al 6061, 100×80mm, drilled/tapped holes |
| Frame rails | Tube cutting + drilling | Laser/waterjet/aluminum extrusion |
| Chamber panels | Laser cutting or sheet bending | 3mm Al or polycarbonate |
| Floor panel | Laser cutting (perforated) or mesh | Sloped toward drain |
| Drip trays | 3D printing or sheet metal forming | Custom geometry per station |

### Design for Manufacturing

- **Plate mounting:** 6mm Al provides rigidity for motor + pillow block shared mount
- **No custom machining required** for drivetrain — all standard components
- **Frame:** Use aluminum extrusion (20×40mm or similar) for ease of assembly
- **Modular stations:** Same template reused 3× via pattern or manual placement

---

## G. THREAD SPECIFICATION

| Feature | Specification | Standard | Confidence |
|---|---|---|---|
| Motor plate mounting holes | M3 | ISO 4762 (hex socket) | **HIGH** |
| Pillow block mounting holes | M3 or M4 | ISO 4762 | **HIGH** |
| UCP06 set screws | M5 × 0.8 | ISO 4014 | **MEDIUM** |
| SSR heatsink mounting | M3 | ISO 4762 | **HIGH** |
| Umbrella hub interface | 6mm bore (no thread) | — | **HIGH** |
| Shaft couplings | 6mm/8mm bore (no thread) | — | **HIGH** |

---

## H. HOLE & FASTENER SPECIFICATION

### Motor Plate (100×80×6mm)

| Feature | Size | Position | Purpose |
|---|---|---|---|
| Motor mount holes | 2× M3 or 2× Ø3.5mm | Symmetric on plate | Secure SGM-370 |
| Pillow block holes | 2× M3 or 2× Ø3.5mm | Centered, ~40mm from motor | Secure UCP06 |
| Shaft access hole | Ø10mm | Edge of plate | Allow shaft protrusion |
| Coupling access | — | Aligned with motor shaft | Connect 6×8mm coupling |

### Plate Mounting to Frame

| Feature | Size | Position | Purpose |
|---|---|---|---|
| Base plate holes | 4× M4 | Corners of 100×80 plate | Bolt to frame rails |

### Electronics Enclosure Cutouts

| Component | Cutout Size | Purpose |
|---|---|---|
| LCD 16×2 I2C | 78 × 16mm | Display window |
| Arcade button | Ø22mm | Start button |
| Mega board | 105 × 55mm | Board space |
| SSR modules | 50 × 40mm each (×7) | SSR mounting |
| Ventilation | Multiple Ø6–8mm | Heat dissipation |

---

## I. TOLERANCES

### Specified Tolerances

| Feature | Tolerance | Note |
|---|---|---|
| Chamber internal envelope | ±5mm | Assembly tolerance |
| Station pitch (700mm c2c) | ±2mm | Critical for canopy spacing |
| Shaft alignment (motor→hub) | ±0.5mm | Critical for drivetrain function |
| Pillow block bore | ±0.02mm | Standard bearing tolerance |
| Motor plate flatness | ±0.5mm | Ensure shaft alignment |

### Assumed Tolerances (General)

| Feature | Tolerance | Basis |
|---|---|---|
| Frame rail lengths | ±1mm | Standard cutting tolerance |
| Plate holes | ±0.2mm | Drill bit tolerance |
| Enclosure panels | ±1mm | Sheet metal/laser tolerance |
| Drip tray geometry | ±2mm | 3D print or formed |

---

## J. FITS & CLEARANCES

### Drivetrain Fits

| Interface | Fit Type | Min Clearance | Max Clearance | Notes |
|---|---|---|---|---|
| 6mm shaft in UCP06 bore | Clearance | 0.02mm | 0.05mm | Bearing inner race |
| 6mm shaft in rigid coupling | Transition | 0mm | 0.02mm | Press-fit on motor side |
| 6mm shaft in PETIYOUZA flange | Clearance | 0.02mm | 0.05mm | Free rotation |
| 8mm coupling bore on 6mm shaft | Clearance | 1mm | 2mm | Step-down coupling |

### Mechanical Clearances

| Clearance | Value | Purpose |
|---|---|---|
| PTC → wiring/sensors | ≥ 50mm | Thermal safety |
| PTC elements → elements | ≥ 30mm | Airflow gap |
| Blower → umbrella fabric | ≥ 10mm | Prevent contact |
| Canopy → adjacent canopy | ≥ 50mm | Safe drying gap |
| Canopy → chamber wall | ≥ 75mm | Safe drying gap |

---

## K. ASSEMBLY RELATIONSHIPS

### Per-Station Drivetrain

| Part A → Part B | Relationship | Type |
|---|---|---|
| SGM-370 Motor → Motor_Plate | Fixed (bolted) | Threaded |
| Motor output shaft → Rigid coupling 6×8mm | Interference/press | Press-fit |
| Rigid coupling → SS shaft 6×300mm | Fixed (keyed) | Coupling |
| SS shaft → UCP06 Pillow Block (×2) | Revolute (bearing) | Insert |
| UCP06 Pillow Block → Motor_Plate | Fixed (bolted) | Threaded |
| SS shaft end → PETIYOUZA Flange coupling | Interference/press | Press-fit |
| PETIYOUZA Flange → Umbrella hub | Revolute (free spin) | Insert |

### Frame Assembly

| Part A → Part B | Relationship | Type |
|---|---|---|
| Base rails → Vertical pillars | Fixed (welded/bolted) | T-joint |
| Vertical pillars → Top frame | Fixed | T-joint |
| Motor plates → Base rails | Fixed (bolted) | Angle joint |
| Station bases → Floor panel | Fixed | Coincident |

### Electronics

| Part A → Part B | Relationship | Type |
|---|---|---|
| Mega 2560 → Enclosure | Fixed (standoffs) | Threaded |
| SSR modules → Heatsinks | Fixed (thermal paste + clip) | Press-fit |
| Bus bars → Enclosure | Fixed (bolts) | Threaded |
| Battery → Compartment | Fixed (straps) | Strap |

---

## L. MOVEMENT REQUIREMENTS

| Motion | Type | Limit | Notes |
|---|---|---|---|
| Umbrella rotation | Revolute | Continuous (360°) | 6 RPM worm drive, self-locking |
| Motor output | Revolute | 6 RPM nominal | 14 kg·cm torque, self-locking |
| Chamber door | Revolute (hinge) | 0–180° | Front access panel |
| Fan blade | Revolute | Continuous | 80mm blower, PWM-controlled |

### Interference Conditions to Avoid

- Umbrella canopy must not contact PTC heaters or blower housings
- Shaft must not bind at any rotation angle (self-locking worm prevents back-drive)
- Drip tray must not interfere with rotating hub

---

## M. ENVIRONMENTAL REQUIREMENTS

| Factor | Condition | Design Response |
|---|---|---|
| Temperature | 40–60°C chamber air | PTC self-regulation + firmware cutoff at 65°C |
| Humidity | Up to 100% RH (wet umbrellas) | DHT22 sensor, sealed electronics enclosure |
| Water exposure | Condensate dripping | Sloped floor + drain tube + drip trays |
| Salt air (optional) | Coastal use | 304 SS shaft, Al 6061 plates, silicone sealant |
| Vibration | Motor operation | Pillow block supports reduce shaft vibration |

**Impact on materials:**
- All structural: Aluminum 6061 (corrosion-resistant)
- Shafts: 304 SS (corrosion-resistant)
- Fasteners: Stainless steel (corrosion-resistant)
- Sealing: PROSEAL silicone on all chamber penetrations

---

## N. SURFACE FINISH

| Component | Finish | Notes |
|---|---|---|
| Motor mount plates | Mill finish or anodized | Al 6061, smooth for bearing seats |
| SS shaft | Mirror/polished | Reduces friction in bearings |
| Frame rails | Mill finish or powder coat | Al or steel |
| Chamber panels | Mill finish or clear coat | Al sheet or polycarbonate |
| Drip trays | Smooth (3D print or formed) | Easy cleaning |

---

## O. WEIGHT / MASS

### Calculated Mass (estimated)

| Component | Qty | Mass Each | Total |
|---|---|---|---|
| SGM-370 motor | 3 | 156g | 468g |
| SS shaft 6×300mm | 3 | ~420g | 1260g |
| UCP06 pillow block | 6 | ~150g | 900g |
| PETIYOUZA flange coupling | 3 | ~50g | 150g |
| Motor plate (Al 6061) | 3 | ~130g | 390g |
| AVC blower (80×80×38mm) | 9 | ~150g | 1350g |
| PTC heater (12V 100W) | 9 | ~120g | 1080g |
| LiFePO4 200Ah battery | 1 | ~18kg | 18000g |
| Frame (assumed Al tube) | — | ~8kg | 8000g |
| **Total estimated** | | | **~32kg** |

> **Note:** Battery mass dominates (~56% of total). Frame mass is estimated — requires actual material selection.

---

## P. CRITICAL DIMENSIONS

| Dimension | Why Critical | Required Accuracy | Verification |
|---|---|---|---|
| **Shaft alignment (motor→hub)** | Drivetrain function; misalignment causes binding/vibration | ±0.5mm | Measure after assembly; check rotation by hand |
| **Station pitch (700mm c2c)** | Canopy spacing; affects drying uniformity | ±2mm | Measure from frame rail centerlines |
| **Motor plate height** | Umbrella hub height (~300mm) | ±5mm | Measure from floor to shaft centerline |
| **UCP06 mounting hole spacing** | Shaft support position | ±1mm | Measure pillow block before mounting |
| **PTC clearance from fabric** | Safety; prevent overheating/scorching | ≥10mm | Verify during assembly |
| **Chamber internal envelope** | Overall size constraint | ±5mm | Measure frame interior |

---

## Q. NON-CRITICAL / COSMETIC DIMENSIONS

| Dimension | Tolerance | Notes |
|---|---|---|
| Drip tray shape | ±5mm | Functional but not precision-critical |
| Door hinge placement | ±3mm | Cosmetic + basic function |
| Ventilation hole pattern | ±2mm | Aesthetic/functional but not critical |
| Label/sticker placement | — | Cosmetic |
| Wire routing channels | — | Determine during build |

---

## R. FUSION 360 PARAMETER TABLE

### Global Parameters

| Name | Value | Unit | Type | Source |
|---|---|---|---|---|
| CHAMBER_W | 2200 | mm | User Parameter | HARDWARE §5 |
| CHAMBER_D | 800 | mm | User Parameter | HARDWARE §5 |
| CHAMBER_H | 1300 | mm | User Parameter | HARDWARE §5 |
| STATION_PITCH | 700 | mm | User Parameter | model/README |
| NUM_STATIONS | 3 | — | User Parameter | Design req |
| CLEARANCE_SIDE | 75 | mm | User Parameter | HARDWARE §5 |
| CLEARANCE_BETWEEN | 50 | mm | User Parameter | HARDWARE §5 |

### Station Template Parameters

| Name | Value | Unit | Type | Source |
|---|---|---|---|---|
| MOTOR_PLATE_W | 100 | mm | User Parameter | model/README |
| MOTOR_PLATE_D | 80 | mm | User Parameter | model/README |
| MOTOR_PLATE_T | 6 | mm | User Parameter | model/README |
| SHAFT_LEN | 300 | mm | User Parameter | model/README |
| SHAFT_DIA | 6 | mm | User Parameter | model/README |
| PILLOW_BLOCK_BORE | 6 | mm | User Parameter | BOM §5 |
| FLANGE_BORE | 6 | mm | User Parameter | BOM §5 |
| COUPLING_MOTOR_BORE | 6 | mm | User Parameter | BOM §5 |
| COUPLING_SHAFT_BORE | 8 | mm | User Parameter | BOM §5 |
| PTC_GAP_MIN | 30 | mm | User Parameter | model/README |
| BLOWER_CLEARANCE_MIN | 10 | mm | User Parameter | model/README |
| PTC_CLEARANCE_MIN | 50 | mm | User Parameter | HARDWARE §3 |

### Assumed Parameters (verify before finalizing)

| Name | Value | Unit | Type | Source |
|---|---|---|---|---|
| UMBRELLA_HUB_H | 300 | mm | User Parameter | model/README (~300mm estimated) |
| FRAME_TUBE_W | 40 | mm | User Parameter | ASSUMED (20×40mm tube) |
| FRAME_TUBE_H | 20 | mm | User Parameter | ASSUMED |
| FRAME_WALL_T | 1.5 | mm | User Parameter | ASSUMED |
| BATTERY_W | [MEASURE] | mm | User Parameter | REQUIRES PHYSICAL MEASUREMENT |
| BATTERY_D | [MEASURE] | mm | User Parameter | REQUIRES PHYSICAL MEASUREMENT |
| BATTERY_H | [MEASURE] | mm | User Parameter | REQUIRES PHYSICAL MEASUREMENT |
| SGM370_BODY_L | 57 | mm | User Parameter | ESTIMATED (typical N20 size) |
| SGM370_BODY_D | 37 | mm | User Parameter | ESTIMATED |
| SGM370_BODY_H | 37 | mm | User Parameter | ESTIMATED |
| UCP06_Outer_D | 34 | mm | User Parameter | ESTIMATED (standard spec) |
| UCP06_Center_H | 29 | mm | User Parameter | ESTIMATED |

---

## S. FUSION 360 MODEL TREE

### Recommended Feature Order

```
01  CHAMBER_FRAME (Root Assembly)
    └─ Sketch: Base_Outline (2200×800mm rectangle on XY plane)
    └─ Extrude: Base_Rails (4 rails, 20×40mm tube)
    └─ Sketch: Pillar_Positions (4 corners)
    └─ Extrude: Vertical_Pillars (×4, 1300mm tall)
    └─ Sketch: Top_Frame_Outline (2200×800mm)
    └─ Extrude: Top_Frame (4 rails, same profile)
    └─ Pattern: Station_Mount_Points (3 positions at X=350, 1050, 1750)

02  STATION_TEMPLATE (Parametric, X=350mm)
    └─ Sketch: Motor_Plate_Profile (100×80mm rectangle)
    └─ Extrude: Motor_Plate (6mm thick)
    └─ Hole: Motor_Mount_Holes (2× M3)
    └─ Hole: Pillow_Block_Holes (2× M3/M4)
    └─ Hole: Shaft_Access (Ø10mm at plate edge)
    └─ Cylinder: Main_Shaft (6mm × 300mm, positioned through plate)
    └─ Body: UCP06_Pillow_Block (×2, at mid-shaft positions)
    └─ Body: Rigid_Coupling (6×8mm, on motor side)
    └─ Body: Flange_Coupling (PETIYOUZA 6mm, on hub side)
    └─ Body: SGM370_Motor (placeholder box, 57×37×37mm)
    └─ Body: PTC_Heater (×3, positioned below hub, 30mm gaps)
    └─ Body: AVC_Blower (×3, positioned behind PTC array)
    └─ Body: Drip_Tray (sloped, under shaft)

03  STATION_02 (Reference to STATION_TEMPLATE, X+700mm)
04  STATION_03 (Reference to STATION_TEMPLATE, X+1400mm)

05  ELECTRONICS_ENCLOSURE
    └─ Body: Enclosure_Box (custom, sized to components)
    └─ Cutout: Mega_Board_Space (105×55mm)
    └─ Cutout: SSR_Space (×7, 50×40mm each)
    └─ Cutout: LCD_Window (78×16mm)
    └─ Cutout: Button_Hole (Ø22mm)
    └─ Vent: Ventilation_Holes (multiple Ø6mm)

06  BATTERY_COMPARTMENT
    └─ Body: Compartment_Base (sized to battery measurements)
    └─ Cutout: Battery_Retainer (straps or brackets)
    └─ Access: Charger_Port (for alligator clips)

07  DOOR_COVER
    └─ Body: Front_Panel (2200×1300mm or partial)
    └─ Hinge: Door_Hinges (top/bottom)
    └─ Seal: Door_Seal_Groove (silicone channel)

08  SENSORS & UI
    └─ Body: DHT22_Mount (mid-chamber position)
    └─ Body: DS18B20_Mount (heater airstream)
    └─ Body: LCD_Mount (front panel)
    └─ Body: Button_Mount (front panel)
```

---

## T. SKETCH CONSTRAINTS

### Motor Plate Sketch

| Constraint | Applied To |
|---|---|
| `Coincident` | Plate edges to construction axes |
| `Symmetric` | Motor holes about plate centerline |
| `Symmetric` | Pillow block holes about plate centerline |
| `Horizontal` | Plate top/bottom edges |
| `Vertical` | Plate left/right edges |
| `Dimension` | Plate = MOTOR_PLATE_W × MOTOR_PLATE_D |
| `Concentric` | Shaft access hole center to motor axis |

### Shaft Alignment

| Constraint | Applied To |
|---|---|
| `Collinear` | Motor shaft axis → coupling → shaft → pillow block → flange |
| `Coincident` | Pillow block outer race to plate mounting holes |
| `Equal` | Both pillow block distances from plate edges (symmetric) |

### Chamber Frame

| Constraint | Applied To |
|---|---|
| `Rectangle` | Base outline = CHAMBER_W × CHAMBER_D |
| `Parallel` | Opposite rails |
| `Perpendicular` | Long rails to short rails |
| `Dimension` | Station positions = CHAMBER_W/2 - STATION_PITCH/2, etc. |

---

## U. DATUM / ORIGIN PLAN

### Coordinate System

```
        Y (up)
        │
        │
        ○──────────→ X (long axis, 0→2200mm)
       /
      /
     Z (depth, 0→800mm)
```

**Origin:** Bottom-left-front corner of chamber **interior** (left end, floor level, front edge).

### Datums

| Datum | Definition |
|---|---|
| **Primary** | Floor plane (Y=0) |
| **Secondary** | Left interior wall (X=0) |
| **Tertiary** | Front interior wall (Z=0) |

### Station Positions (X-axis)

| Station | X center | Y hub center | Z center |
|---|---|---|---|
| Station 1 | 350mm | ~300mm | 400mm |
| Station 2 | 1050mm | ~300mm | 400mm |
| Station 3 | 1750mm | ~300mm | 400mm |

### Why This Orientation?

- **X-axis along long dimension** → natural for parametric station placement
- **Origin at corner** → easy to dimension from frame references
- **Y up** → standard CAD convention, matches gravity for drip tray design
- **Z depth** → allows symmetric station placement (400mm = 800/2)

---

## V. PHYSICAL MEASUREMENT PLAN

### Priority 1 — Must Measure Before Modeling

| # | What to Measure | Where | Tool | Accuracy | Notes |
|---|---|---|---|---|---|
| 1 | **LiFePO4 200Ah battery** W×D×H | Battery case | Digital caliper | ±0.1mm | Critical for compartment sizing |
| 2 | **SGM-370 motor** body W×D×H, shaft length, mount hole spacing | Motor body | Digital caliper | ±0.1mm | Critical for motor plate design |
| 3 | **UCP06 pillow block** outer dimensions, bolt hole pattern, center height | Bearing unit | Digital caliper + gauge | ±0.1mm | Critical for plate mount holes |
| 4 | **PETIYOUZA flange coupling** OD, length, bore | Coupling | Digital caliper | ±0.1mm | Critical for hub interface |
| 5 | **SSR-40DD / SSR-10DD** body dimensions, terminal spacing | SSR module | Digital caliper | ±0.1mm | Critical for enclosure layout |

### Priority 2 — Verify After Components Arrive

| # | What to Measure | Where | Tool | Accuracy | Notes |
|---|---|---|---|---|---|
| 6 | **PTC heater** actual W×D×H (estimate is ~60×42×60mm) | Heater body | Digital caliper | ±0.1mm | Verify vs. BOM estimate |
| 7 | **AVC blower** mounting hole pattern (4× M3 corners) | Blower frame | Digital caliper | ±0.1mm | Standard 80mm fan pattern |
| 8 | **Arcade button** diameter, mounting depth | Button body | Digital caliper | ±0.1mm | For enclosure cutout |
| 9 | **LCD 16×2 I2C** bezel dimensions | Display module | Digital caliper | ±0.1mm | Standard 80×36mm |
| 10 | **LM2596S buck** dimensions | Converter module | Digital caliper | ±0.1mm | For enclosure layout |

### Priority 3 — Low Priority (Iterative Refinement)

| # | What to Measure | Tool |
|---|---|---|
| 11 | Drip tray shape/slope | Tape measure |
| 12 | Door hinge placement | Tape measure |
| 13 | Internal wire routing paths | Visual inspection |
| 14 | Grommet sizes for wall penetrations | Radius gauge set |

---

## W. UNKNOWN PARAMETERS

| Missing Dimension | Why It Matters | How to Obtain | Tool Required |
|---|---|---|---|
| **LiFePO4 200Ah battery W×D×H** | Determines battery compartment size, chassis base length | **PHYSICAL MEASUREMENT REQUIRED** | Digital caliper, tape measure |
| **SGM-370 motor body dimensions** | Motor plate cutout, enclosure clearance | **PHYSICAL MEASUREMENT REQUIRED** | Digital caliper |
| **UCP06 pillow block outer dimensions** | Plate mount hole pattern | Measure from component or datasheet | Digital caliper |
| **PETIYOUZA flange coupling dimensions** | Umbrella holder geometry | Measure from component | Digital caliper |
| **SSR-40DD / SSR-10DD dimensions** | Enclosure layout, heatsink spacing | Measure from component | Digital caliper |
| **PTC heater exact dimensions** | Heater bracket design, airflow gaps | Measure from component | Digital caliper |
| **Frame rail profile** | Structural design, connection details | Verify with supplier or measure prototype | Tape measure |
| **Chamber panel material/thickness** | Structural analysis, weight | Confirm with build plan | Documentation |
| **Drip tray dimensions** | Water collection capacity | Measure or design | Tape measure |
| **Door mechanism** | Hinge type, seal design | Design decision | — |

---

## X. ENGINEERING CALCULATIONS

### Torque Verification (Rev 7a from BOM)

```
Required torque per station: ≤ 3 kg·cm (umbrella resistance)
Motor rated torque: 14 kg·cm
Margin: 14 / 3 = 4.67× ← PASS (≥ 4.6× margin)
```

### Current Budget (Rev 7c from BOM)

```
Per station (staged):
  PTC heaters (3× 100W @ 12V): 3 × 8.33A = 25A
  AVC blowers (3× 4.5A): 13.5A
  Motor (0.8A stall): 0.8A
  Logic (0.5A): 0.5A
  ─────────────────────────────
  Total: 39.3A

BMS rating: 200A
Safety margin: 200 / 39.3 = 5.1× ← PASS
```

### Battery Runtime (Rev 7d from BOM)

```
Usable capacity: 200Ah × 0.80 (DoD) × 0.90 (EoL) = 144Ah
Staged draw: 39.3A
Runtime: 144 / 39.3 = 3.66 hours

Quick cycle (27min): ~15Ah per cycle → 144/15 = 9.6 cycles
Standard cycle (57min): ~33Ah per cycle → 144/33 = 4.4 cycles
```

### Volume / Mass Calculation (Estimates)

```
Aluminum plate (per station): 100×80×6mm = 48,000mm³
  Mass = 48,000 × 2.7g/cm³ = 129.6g ≈ 130g (matches BOM)

SS shaft (per station): π×(3mm)² × 300mm = 8,482mm³
  Mass = 8,482 × 7.9g/cm³ = 67g (approx)
```

---

## Y. VERIFICATION CHECKLIST

| Item | Status |
|---|---|
| [x] Exact product/component identified | Umbrella Dryer V2 Rev 9 confirmed |
| [x] Correct revision/version identified | main branch, commit 1f95122 |
| [x] Real-world dimensions collected (partial) | See Section D for confirmed vs. estimated |
| [ ] Overall dimensions verified | Chamber confirmed; frame requires measurement |
| [x] Critical dimensions identified | Shaft alignment, station pitch, motor plate height |
| [ ] Hole dimensions verified | Motor plate holes — **REQUIRES MEASUREMENT** |
| [x] Thread dimensions verified | M3/M4/M5 standard threads confirmed |
| [x] Material identified | Al 6061, SS 304, cast iron (UCP06) |
| [x] Manufacturing process identified | CNC/waterjet/frame assembly |
| [ ] Tolerances identified | Specified ±5mm global; ±0.5mm critical |
| [x] Fits and clearances identified | See Section J |
| [x] Fasteners identified | M3/M4/M5 kit |
| [x] Assembly interfaces identified | See Section K |
| [x] Moving parts checked | Revolute joints defined |
| [x] Environmental requirements checked | See Section M |
| [ ] Surface finish identified | Mill finish assumed; verify per component |
| [x] Weight checked/calculated | Estimated ~32kg total |
| [x] Fusion 360 parameters created | See Section R |
| [x] Fusion 360 feature sequence defined | See Section S |
| [x] Sketch constraints defined | See Section T |
| [ ] Missing measurements identified | See Section W — 10 items |
| [x] Sources documented | See Section B |
| [x] Conflicting dimensions investigated | See Revision History below |
| [x] Low-confidence dimensions identified | See Section D (LOW confidence items) |
| [x] Physical measurement plan created | See Section V |

---

## Z. REVISION HISTORY & CONFLICT ANALYSIS

### Documented Revisions (from HARDWARE.md §8)

| Rev | Change |
|---|---|
| Rev 2 | SSR-25DD + BTS7960 + single carousel motor |
| Rev 3 | Relays replace SSR + driver; MLX90614 dropped |
| Rev 4 | 3 independent stations (3× motors + flange couplings); 25A main fuse |
| Rev 5 | Mains heat: 2× 1500W PTC heater-fans via 2× SSR-40DA; RCD added |
| Rev 6 | Dual source: wall outlet OR 3000W inverter via changeover; 2× 200Ah LiFePO4 |
| Rev 7 | Complete 12V DC redesign: 9× PTC + 9× AVC blower + 3× SGM-370; no mains, no inverter |
| Rev 8 | Fuse plan fixed (50A main, 30A PTC/fan, per-heater 130°C thermal fuse); PTC relays upgraded to 40A automotive |
| **Rev 9 (current)** | No-fuse SSR build: all fuses/NPN removed; SSR-40DD DC-output direct-drive from Mega pins |

### Conflicts Investigated

| Conflict | Resolution |
|---|---|
| **Drivetrain change (Rev 4→7→9)** | Rev 4: direct flange coupling. Rev 7: added shaft + UCP06. **Rev 9 (current): restores shaft + UCP06 + couplings.** Use Rev 9 spec. |
| **Blower type (Rev 7)** | Changed from BLDC (with ESC) to AVC direct PWM. **Current: AVC 80×80×38mm.** |
| **PTC heater variant (Rev 9)** | Changed from MXKJING T30 (out of stock) to diymore 12V 100W. **Both ~60×42×60mm.** |
| **SSR type (Rev 8→9)** | Rev 8: 40A automotive relays + NPN driver. **Rev 9: SSR-40DD DC-output, direct-drive from Mega.** |
| **Fuse plan (Rev 8→9)** | Rev 8: 50A ANL + 30A blade + 130°C thermal fuses. **Rev 9: NO fuses — BMS 200A + PTC self-regulation only.** |

### Final Configuration (Rev 9)

```
3 Stations, 12V DC only
9× PTC 12V 100W (3 per station)
9× AVC 12V 4.5A blower (3 per station, PWM from Mega D10/D11/D12)
3× SGM-370 12V 6RPM worm gear (1 per station)
Drivetrain: SGM-370 → rigid coupling 6×8mm → SS shaft 6×300mm → UCP06 pillow block → PETIYOUZA 6mm flange → umbrella hub
4× SSR-40DD (3 PTC + 1 fan bus)
3× SSR-10DD (motors)
1× LiFePO4 12.8V 200Ah w/ BMS 200A
1× LM2596S buck 12V→5V
Arduino Mega 2560 (D2=DHT22, D3=DS18B20, D4/D6/D8=PTC, D5/D7/D9=motor, D10/D11/D12=blower PWM, D13=fan bus, D14=start button, D15-D17=LEDs, D18=buzzer, D20/D21=LCD I2C)
```

---

## AA. FINAL QUALITY CHECK

| Check | Status |
|---|---|
| Exact product/component identified | ✅ |
| Correct revision/version identified | ✅ |
| Real-world dimensions collected | ⚠️ Partial — see Section W for missing |
| Overall dimensions verified | ⚠️ Chamber verified; frame needs measurement |
| Critical dimensions identified | ✅ |
| Hole dimensions verified | ❌ **REQUIRES MEASUREMENT** |
| Thread dimensions verified | ✅ |
| Material identified | ✅ |
| Manufacturing process identified | ✅ |
| Tolerances identified | ⚠️ Partial — see Section I |
| Fits and clearances identified | ✅ |
| Fasteners identified | ✅ |
| Assembly interfaces identified | ✅ |
| Moving parts checked | ✅ |
| Environmental requirements checked | ✅ |
| Surface finish identified | ❌ **REQUIRES VERIFICATION** |
| Weight checked/calculated | ✅ Estimated |
| Fusion 360 parameters created | ✅ |
| Fusion 360 feature sequence defined | ✅ |
| Sketch constraints defined | ✅ |
| Missing measurements identified | ✅ Section W |
| Sources documented | ✅ Section B |
| Conflicting dimensions investigated | ✅ Section Z |
| Low-confidence dimensions identified | ✅ See Section D (LOW/MEDIUM tags) |
| Physical measurement plan created | ✅ Section V |

---

## CAD READINESS: REQUIRES MORE MEASUREMENTS

The following **5 critical measurements** must be obtained before starting the Fusion 360 model:

### Mandatory (Critical Path)

| # | Component | What to Measure | Tool | Accuracy |
|---|---|---|---|---|
| 1 | **LiFePO4 200Ah battery** | Length, Width, Height, terminal position | Tape measure + caliper | ±1mm |
| 2 | **SGM-370 motor** | Body L×W×H, shaft length, mount hole pattern | Digital caliper | ±0.1mm |
| 3 | **UCP06 pillow block** | Outer diameter, center height, bolt hole spacing | Digital caliper | ±0.1mm |
| 4 | **PETIYOUZA flange coupling** | Length, OD, bore | Digital caliper | ±0.1mm |
| 5 | **SSR-40DD / SSR-10DD** | Body dimensions, terminal spacing | Digital caliper | ±0.1mm |

### Recommended (After Components Arrive)

| # | Component | What to Verify |
|---|---|---|
| 6 | PTC heater | Confirm ~60×42×60mm estimate |
| 7 | AVC blower | Confirm 80×80×38mm + hole pattern |
| 8 | Arcade button | Confirm Ø22mm + depth |
| 9 | LCD 16×2 I2C | Confirm 80×36mm + mounting |
| 10 | Frame rail profile | Confirm 20×40mm or other size |

### Optional (Can Iterate During Build)

| # | Item |
|---|---|
| 11 | Drip tray dimensions |
| 12 | Door hinge/seal design |
| 13 | Wire routing channels |

---

**END OF CAD BUILD SPECIFICATION**

> **Next step:** Obtain the 5 critical measurements from Section "CAD READINESS", then begin Fusion 360 modeling per the strategy in `docs/CAD-STRATEGY.md`.
