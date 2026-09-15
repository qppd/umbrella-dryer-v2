# Smart Umbrella Dryer — Component & Material Validation (Rev 6)

**Revision 6 — design change from Rev 5:** dual-source power with a **changeover switch** — the 220V loads (2× 1500W PTC heater-fans, 12" Omni exhaust fan) run either from the **wall outlet** or from a **single 3000W pure sine inverter** fed by the **2× 200Ah LiFePO4 battery bank** — never both. The changeover switch grounds the inverter's remote pin in wall-outlet mode (inverter OFF, zero idle draw); in battery mode the inverter supplies the RCD and everything downstream unchanged. The Mega senses the mode (D14) and applies the battery-mode economy rule (battery mode never enters stage 2 — one heater + fan ≈ 2.1kW, within the 3000W inverter).

## Study Overview

**Title:** Smart Umbrella Dryer: Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control

**Key Requirements:**
1. Dry **3 umbrellas** simultaneously (any 1–3 mix per cycle)
2. Energy-efficient operation (sensor-based control; battery-backed control and rotation)
3. Smart/automated control via sensors
4. Safe operating temperatures for umbrella materials

---

## 1. Microcontroller — Arduino Mega 2560

| Parameter | Value |
|---|---|
| Processor | ATmega2560 |
| Digital I/O | 54 (15 PWM) |
| Flash / SRAM | 256 KB / 8 KB |
| I2C | SDA=20, SCL=21 |

**v6 pin audit:** 2 SSR inputs (D4/D5) + 3 motor relay channels (D6/D7/D8) + 3 LEDs + buzzer + button + LCD I2C + 2 sensors + mode input (D14) ≈ **11 digital + 2 I2C** — far inside capacity. The exhaust fan has **no** Mega channel (mains rocker). COMPATIBLE

**Powering the Mega:** buck 5V → 5V pin only (never the DC jack; never mains anything).

Listing: `makerlab.ph/products/mega-2560-r3-with-usb-cable-compatible-with-arduino-do-not-supply-with-12v-on-dc-jack` — ₱1,199

---

## 2. Power — two selectable sources, three domains

### 2a. 12V battery bank — motors + control + (via inverter) 220V loads in battery mode

2× PowMr LiFePO4 12.8V 200Ah parallel (5,120Wh, 200A BMS each → 400A aggregate). Worst-case DC draw in battery mode: inverter 188A steady (~210A surge, stage 1: heater 1 + fan ≈ 2.05kW) + 3 motors at stall 10.5A + logic ~0.8A ≈ **221A peak → 1.8× BMS margin**. In wall-outlet mode: ≈ 11.3A peak.

**DC fuse plan (v6):** 25A main · 3A ×3 station branches · 3A logic · **250A ANL on the inverter feed (1/0 AWG, ≤ 1 m)** · 4 AWG battery links. Wire: 16 AWG main/logic feed, 18 AWG stations, 22 AWG logic.

**Charging:** 14.6V 20A LiFePO4 charger → ~10 h recharge from 80% depth. Keep the FOXSUR 6A as the backup/top-off charger.

### 2b. Source selection — changeover switch (the Rev 6 core idea)

A 2-position changeover (transfer) switch feeds the RCD from **either** the wall outlet **or** the inverter output — never both. In wall-outlet mode, the switch's second pole grounds the inverter's **remote/enable pin** through its supplied mode jumper, so the inverter is fully OFF with zero idle draw; in battery mode the pin is released and the inverter runs.

Wall outlet → changeover position A —↘
Inverter output → changeover position B —↗ **RCD/GFCI** → mains rocker (2-gang) → per-branch **10A fuses** → loads

Mega D14 senses the position via the switch's auxiliary contact (LOW = wall-outlet mode). Mode rules: battery mode never enters stage 2 (heater 1 + exhaust fan stay ≤ 2050W on the 3000W inverter — 68%); battery mode adds inverter idle 20–30W to the consumption math.

### 2c. 220V AC domain — heat + exhaust fan (source-agnostic downstream)

| Branch | Load | Current @220V | Switch |
|---|---|---|---|
| Heater 1 | 1500W PTC heater-fan | 6.8A | SSR-40DA #1 (D4) |
| Heater 2 | 1500W PTC heater-fan | 6.8A | SSR-40DA #2 (D5) |
| Exhaust | 12" Omni fan | ~1.5–2.5A | mains rocker gang (no SSR) |

Note: the exhaust fan runs whenever its mains rocker gang is ON in either source mode — that is stage 1 airflow, and it is intentional (air must move whenever heat can).

---

## 3. Heating — 2× 1500W PTC heater-fans (220V) via Fotek SSR-40DA

### 3a. Why the SSR-40DA (AC type) is now the CORRECT Fotek part

Rev 2–4 banned the DA type because a TRIAC cannot turn off a **DC** load. The new heaters are **AC** loads — exactly what the DA type is built for: current crosses zero 100×/second, so the SSR switches off cleanly. Never use the DD type here.

| Parameter | Value | Design check |
|---|---|---|
| Output | 24–380VAC, 40A | 220V heaters — correct type |
| Rated current | 40A | 5.9× the 6.8A heater |
| Surge | 600A-class | PTC inrush covered |
| Input | 3–32VDC, ~12mA | direct Mega pin (D4/D5), 10kΩ pull-down to hold OFF at boot |
| Dissipation | ≈ 1.0–1.6V × 6.8A ≈ **7–10W each** | **heatsink mandatory** — mount inside the grounded metal box with thermal paste |
| Control | slow time-proportional (2–5s period) | zero-cross DA switches at mains zero-crossings; do not fast-PWM |

### 3b. Staged heater control (the energy-efficient scheme)

| Stage | State | Use |
|---|---|---|
| Stage 0 | both OFF | idle / complete |
| Stage 1 | heater 1 duty-cycled (2–5s period) from humidity error | normal drying, holds 40–60C |
| Stage 2 | heater 1 steady ON + heater 2 duty-cycled | wet 3-umbrella load / pull-down |
| Cutoff | both OFF (latched) | DS18B20 > 65C, or humidity target met |

Appliances keep their **built-in thermostats + thermal cutoffs** — a fourth protection layer behind DS18B20, the RCD, and the branch fuses.

### 3c. Thermal verification (3000W staged)

| Quantity | Value |
|---|---|
| Water for 3 umbrellas | 90–300g typical (450g soaked worst case) |
| Evaporation energy | 57–188Wh (283Wh worst) |
| Effective delivered heat | ~2100–2500W (two blowers + exhaust exchange) |
| **Cycle time** | **≈ 15–25 min typical · ~30–45 min soaked** (humidity auto-stop) |
| Chamber air temp | 40–60C held by staging; DS18B20 cutoff 65C |

30× the heat plus forced air exchange is far beyond the old 100W loop — cycle time is now limited by moisture transport, not energy. The energy-efficiency claim shifts to **control efficiency**: heaters never run dry (humidity staging + auto-shutoff), which is where duty cycling still saves real power. In battery mode, staging is also what keeps the inverter inside its rating and the BMS budget — stage 2 is disabled by firmware (D14 mode input).

### 3d. Inverter — 1× pure sine 3000W, 12V DC → 220V AC 60Hz

| Parameter | Value | Design check |
|---|---|---|
| Type | **pure sine wave** — mandatory | the exhaust fan is an AC induction motor; modified sine overheats it |
| Rating | **3000W continuous** (6000W-class surge) | battery-mode stage-1 load = heater 1 (1500W) + fan (~550W) ≈ 2050W = **68%** — comfortable headroom; stage 2 exists in wall mode only |
| Input | 12V DC | matches the battery bank |
| Output | 220VAC 60Hz | matches the appliances |
| Efficiency | ~88–90% | see the battery-mode energy math in §10 |
| Idle draw | ~20–30W | grounded remote pin in wall-outlet mode = 0W |
| Remote pin | remote/enable via the supplied mode jumper | grounded by the changeover's second pole in wall-outlet mode |
| DC input | **1/0 AWG feed, ≤ 1 m, 250A ANL fuse** | 188A steady / 210A surge at full stage-1 load |
| Why one inverter | two high-power inverters cannot be paralleled (wavephase mismatch) — and one 3000W is cheaper than two 2000W | firmware keeps battery mode in stage 1 |

**Never backfeed:** the inverter output appears only on changeover position B. In wall-outlet mode its remote pin is grounded — the inverter is off — so the RCD is fed solely by the wall outlet. Two sources on one RCD input would destroy the inverter and backfeed the street.

---

## 4. Sensors — DHT22 + DS18B20

| Sensor | Role | Interface | Status |
|---|---|---|---|
| DHT22 (AM2302) | Chamber humidity — stage control + auto-shutoff | 1-wire, D2 | Required — ₱69 |
| DS18B20 waterproof | Heater-zone air temp — over-temp cutoff | 1-Wire, D3 + 4.7kΩ | Required — ₱105 |

I2C carries only the LCD. MLX90614 remains removed.

---

## 5. Motor & Drive — 3× worm stations

3× SGM-A58SW31ZY 12V 16RPM (60 kg·cm, 1.2A rated / 3.5A stall, 8mm shaft, self-locking) — one per umbrella, ≥20× torque margin per station, per-station 3A fuse isolation. Driven by **2× 2-CH relay modules** (3 of 4 channels used): coils from the buck 5V rail, Mega drives only the optocoupler LEDs.

Mechanical: 3× 8mm × 300mm 304 SS shafts · 6× KP08 · 3× 8×8 rigid couplings · fabricated holders.

Listings: makerlab.ph motors ×3 in one order; JGY370 not acceptable.

---

## 6. Voltage Regulation — LM2596S

Logic load: Mega 0.2A + sensors + LCD + LEDs + buzzer + 3 relay coils (0.21A) ≈ **0.7A** — 4.3× margin on 3A.

---

## 7. Water Management — PASSIVE

Sloped floor (3–5°) → drain tube → drip tray (100–300mL/cycle; 500mL tray). With fast drying, condensate arrives sooner — check the tray fill after the first cycles and size up if needed.

---

## 8. User Interface

- LCD 16×2 I2C (0x27/0x3F) — status, humidity, stage
- LEDs green/yellow/red; buzzer; start button (INPUT_PULLUP)
- **Two labeled rockers: MAINS (AC domain) and DC (battery domain)** — the mains rocker is the manual kill for a fail-short SSR

---

## 9. THREE-UMBRELLA CAPACITY VERIFICATION (Rev 5)

### 9a. Mechanical — per-station torque — PASS
≤3 kg·cm per station vs 60 kg·cm → ≥20× margin; KP08 >90× load margin; 16 RPM gentle; self-locking hold.

### 9b. Thermal — PASS (see 3c)
15–45 min cycles; staged 1500W heaters; 40–60C held; quadruple over-temp protection (appliance thermostat, DS18B20 cutoff, branch fuse, RCD).

### 9c. Electrical — split domains — PASS

| Domain | Worst case | Protection | Margin |
|---|---|---|---|
| AC | 15.6A via the changeover — from the wall outlet (grid mode) or from the inverter (battery mode) | RCD 30mA + 10A branch fuses + breaker upstream | branch fuses sized to wire |
| 12V | ≈ 221A peak in battery mode (inverter 210A surge + 3 stalls + logic — stalls do not coincide with full heater duty); ≈ 11.3A in wall mode | 200A BMS ×2 + 250A ANL inverter fuse + 25A main + 3A branches | 1.8× peak (firmware caps battery mode at stage 1) |
| 5V | ~0.7A | 3A branch, buck 3A | 4.3× |

---

## 10. Energy & Runtime (Rev 5 story)

| Item | Value |
|---|---|
| Wall-outlet mode: energy per 3-umbrella cycle | ≈ **0.6–1.0 kWh** (staged control; auto-shutoff prevents dry running) |
| Wall-outlet mode: cost per cycle | ≈ ₱7–12 at ₱12/kWh |
| Battery mode: usable AC energy | 5,120Wh × 80% DoD × 88% inverter eff ≈ **3,600Wh** |
| Battery mode: stage 1-only cycle | ≈ 0.4–0.6 kWh → **~6–8 cycles per charge** (firmware caps battery mode at stage 1 via D14) |
| Full-heat cycles | wall mode only (stage 2 = 3.4kW exceeds the battery-mode cap) |
| Motors + control | ~14W — days of autonomy on either source |
| Inverter idle | 0W in wall-outlet mode (remote pin grounded by the changeover); 20–30W in battery mode |

**Honest framing for the paper:** absolute energy per cycle is higher than the 12V design (bigger heaters dry much faster); the efficiency contribution of the controller is **eliminating idle/dry heating** via humidity staging and auto-shutoff. The changeover adds **source flexibility**: full performance from the grid, or grid-independent operation from the battery bank with a firmware-enforced economy cap.

---

## 11. System Block Diagram

```mermaid
flowchart TB
    subgraph SRC["220V source selection"]
        OUT["Wall outlet 220V"]
        INV["3000W pure sine inverter<br/>remote pin grounded in wall mode"]
        CHO["Changeover switch 2P<br/>A: wall / B: inverter"]
    end
    subgraph AC["220V AC domain (source-agnostic downstream)"]
        RCD["RCD/GFCI"]
        MSW["Mains rocker 2-gang"]
        MF1["10A fuse line 1"]
        MF2["10A fuse line 2"]
        SSR1["SSR-40DA 1 - D4"]
        SSR2["SSR-40DA 2 - D5"]
        H1["1500W PTC heater-fan 1"]
        H2["1500W PTC heater-fan 2"]
        EFAN["12in Omni exhaust fan"]
    end
    subgraph DC["12V DC domain"]
        BAT["2x LiFePO4 12.8V 200Ah parallel<br/>BMS 200A each"]
        IFUSE["ANL fuse 250A x2"]
        DSW["DC rocker"]
        F1["Fuse 25A main"]
        FA["3A st1"] 
        FB["3A st2"]
        FC["3A st3"]
        FL["3A logic"]
        BUCK["LM2596S buck 5V"]
    end
    RM["2x 2-CH relay - D6 st1 / D7 st2 / D8 st3"]
    M1["Worm motor 1"]
    M2["Worm motor 2"]
    M3["Worm motor 3"]
    MEGA["Arduino Mega 2560"]
    DHT["DHT22 - D2"]
    DS["DS18B20 - D3"]
    LCD["LCD I2C - 20/21"]
    HMI["LEDs D9-D11 + buzzer D12 + button D13"]

    OUT --> CHO
    INV --> CHO
    CHO --> RCD
    RCD --> MSW
    MSW --> MF1 --> SSR1 --> H1
    MSW --> MF2 --> SSR2 --> H2
    MSW --> EFAN
    BAT --> IFUSE --> INV
    MEGA -. "mode sense D14" .-> CHO
    MEGA -. "DC inputs" .-> SSR1
    MEGA -. "DC inputs" .-> SSR2
    BAT --> DSW --> F1
    F1 --> FA --> M1
    F1 --> FB --> M2
    F1 --> FC --> M3
    F1 --> FL --> BUCK --> MEGA
    MEGA --> RM
    RM --> M1
    RM --> M2
    RM --> M3
    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA --> HMI
    HMI -- "start" --> MEGA
```

---

## 12. Compatibility Matrix (v6)

| Component | Domain | Margin | Interface | Verdict |
|---|---|---|---|---|
| Arduino Mega 2560 | 5V buck | pin fit 11+2 | SSR inputs + opto LEDs + sensors + D14 mode sense | PASS |
| Fotek SSR-40DA ×2 | 220VAC out / 3–32VDC in | 5.9× per heater | Mega D4/D5, 10kΩ pull-downs, heatsinked | PASS |
| 1500W PTC heater-fans ×2 | 220VAC | 6.8A each | SSR output + plug/socket | PASS |
| Omni 12" exhaust fan | 220VAC | ~2A on 10A branch | mains rocker (no SSR) | PASS |
| 1× 3000W pure sine inverter | 12V→220V | 2050W stage-1 load vs 3000W (68%) | remote-pin interlock + 250A ANL feed | PASS |
| 2P changeover switch 63A | 220VAC | 2.3× branch current | wall A / inverter B → RCD; D14 aux | PASS (source interlock) |
| RCD/GFCI + mains kit | 220VAC | life-safety | — | PASS (mandatory) |
| 3× worm motors | 12V | ≥20× torque | relay channels D6–D8 | PASS |
| 2× 2-CH relay boards | 12V contacts | 2.9× at stall | opto LEDs, coils on 5V rail | PASS |
| LiFePO4 200Ah ×2, BMS 200A ea | 12V | 1.8× peak battery mode; unlimited wall mode | 4 AWG links + 250A ANL inverter feed | PASS |
| LM2596S | 12.8→5V | 4.3× | — | PASS |
| DHT22 / DS18B20 | 5V | mA | D2 / D3 | PASS |
| LCD + LEDs + buzzer + button | 5V | — | I2C + digital | PASS |
| Gravity drain + tray | — | — | passive | PASS |

---

## 13. Safety Validation (v6) — dual source

| Hazard | Mitigation | Status |
|---|---|---|
| **Two sources on one bus (new)** | 2P changeover — breaks before makes; inverter remote pin grounded in wall mode; interlock drill in SETUP before first heat | interlocked |
| **Inverter overload / DC wiring fault (new)** | 3000W vs 2050W stage-1 load; firmware stage-1 cap in battery mode; 250A ANL; 1/0 AWG short runs; BMS 200A ×2 | managed |
| **Electric shock** | RCD/GFCI 30mA + grounded metal box + earthed frame and chassis + plugs accessible | primary control |
| **SSR fail-short (heater stuck ON, AC)** | Mains rocker kill + 10A branch fuse + appliance thermostat + DS18B20 cutoff + RCD | five layers |
| Over-temperature | Appliance thermostat → DS18B20 65C latched cutoff → PTC self-regulation | triple |
| SSR overheating | 7–10W each on heatsink, thermal paste, closed box | managed |
| Overcurrent | 10A branches (AC), 25A main + 3A branches (DC) | fused everywhere |
| Battery overdischarge | BMS | yes |
| Station jam | per-station 3A fuse + self-locking worm | isolated |
| Fire | PTC elements (no open coil) + RCD + fuses | low |
| Water | gravity drain + tray; liquids away from the electrical box | managed |
| Mains in chamber | **No mains terminals or joints inside the chamber** — only the appliances' factory cords pass through grommets to accessible plugs outside; appliance zone on the floor, away from the drain/drip path | by design |

---

## 14. Bill of Materials — Itemized (Rev 5)

> **Sourcing policy:** Makerlab PH first → trusted Lazada sellers. Motors + Fotek SSRs from makerlab.ph website; appliances and mains kit from Lazada/hardware. Prices verified 2026-09-12 unless marked EST (re-check at checkout). Backup listings and seller reasoning: `SOURCING-ANNEX.md`.

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | Arduino Mega 2560 R3 | ATmega2560 | ₱1,215 / ₱1,265 w/ USB | Makerlab PH, 4.8 (331), 2.4K sold | https://www.lazada.com.ph/products/pdp-i5989151.html |
| 2 | **Fotek SSR-40DA (AC output)** | 40A, 3–32VDC in, 24–380VAC out — NOT DD | ₱160 ea = ₱320 | Makerlab PH (site) | https://makerlab.ph/products/fotek-solid-state-relay-module-ssr-40da |
| 2 | **1500W PTC industrial heater-fan, 220V** | portable heater-fan w/ thermostat + thermal cutoff | ₱1,395.35 ea = ₱2,790.70 | Lazada listing | https://www.lazada.com.ph/products/portable-industrial-electric-heater-fan-commercial-thermostat-air-warm-heater-blower-radiator-office-garage-air-fan-i4902069326-s28572024789.html |
| 1 | **Omni industrial exhaust fan w/ grill, wall-mount** | **select 12-inch variant** (listing spans 12/14/16) | ~₱1,000–1,500 EST | Omni official Lazada | https://www.lazada.com.ph/products/omni-industrial-exhaust-fan-w-grill-wall-mounted-12-inch-14-inch-16-inch-i4020672066-s21738898500.html |
| 2 | 2-CH relay module 5V, optocoupler, low-level trigger | 10A@30VDC — 3 motor channels + spare | ₱89 ea = ₱178 | Bulacan, (330), 2.5K sold | https://www.lazada.com.ph/products/pdp-i100047444.html |
| 1 | DHT22 module | select "DHT22 Black" | ₱69 | FU-LABS 98% | https://www.lazada.com.ph/products/pdp-i4888079786.html |
| 1 | DS18B20 waterproof 3m | +4.7kΩ pull-up | ₱105 | Circuitrocks | https://www.lazada.com.ph/products/pdp-i111662523.html |
| 1 | LCD 16×2 w/ I2C | 0x27/0x3F | ₱165 | Makerlab PH | https://www.lazada.com.ph/products/pdp-i104139284.html |
| 1 | 5mm LED kit 10pc | G/Y/R status | ₱29 | (433), 3.0K sold | https://www.lazada.com.ph/products/pdp-i3105641040.html |
| 1 | Active buzzer module | cycle alert | ₱35 | Makerlab PH | https://www.lazada.com.ph/products/pdp-i3474748260.html |
| 1 | Tactile buttons 12mm ×10 | start/reset | ₱79 | Makerlab PH | https://www.lazada.com.ph/products/pdp-i118682689.html |
| 1 | Rocker switch 16A 4-pin (DC side) | battery control-side switching | ₱72 | Unnicoco | https://www.lazada.com.ph/products/pdp-i2272943066.html |
| 1 | Rocker/double-gang mains switch + plate (AC side) | 2-gang, 10A+, flush type | ~₱150–300 EST | hardware / Lazada | (add at checkout) |
| 1 | LM2596S buck w/ display | 12.8→5V 3A | ₱155 | Makerlab PH | https://www.lazada.com.ph/products/pdp-i127879071.html |
| 1 | RCD/GFCI outlet or breaker | 30mA class — MANDATORY | ~₱800–1,500 EST | hardware / Omni / Philex | (add at checkout) |
| 1 | Grounded metal electrical box + DIN/plate | houses SSRs, fuses, terminals | ~₱300–600 EST | hardware | (add at checkout) |
| 1 | Heatsink profile for SSRs (2 pc or 1 shared) | ≥100×100mm contact each | ~₱150–300 EST | Lazada "SSR heatsink" | (add at checkout) |
| 1 | 2.0mm² (14 AWG eq.) 3-core wire + plug/socket set | mains branches | ~₱400–700 EST | hardware / Lazada | (add at checkout) |
| 1 | **Pure sine inverter 3000W, 12V→220V 60Hz, remote pin** | MUST be pure sine (induction fan); verify continuous (not surge) rating | ~₱5,500–8,500 EST | Lazada "local stock pure sine inverter 3000W" | (add at checkout) |
| 1 | **Changeover switch 2P 63A** (wall / inverter → RCD) | break-before-make; second pole grounds the inverter remote in wall mode + D14 sense | ~₱300–800 EST | hardware / Lazada | (add at checkout) |
| 1 | **ANL fuse kit 250A + holder + 1/0 AWG inverter cable + 4 AWG battery links + lugs** | one 250A fuse on the inverter feed, ≤ 1 m runs | ~₱500–1,000 EST | Lazada "ANL fuse kit 250A" / "1/0 welding cable" | (add at checkout) |
| 3 | Worm gear motor SGM-A58SW31ZY 12V 16RPM | 60 kg·cm, self-locking — one per station | ₱1,249 ea = ₱3,747 | makerlab.ph (site) | https://makerlab.ph/products/dc-worm-gear-motor-sgm-a58sw31zys-12v-16rpm-80rpm-sgm-370-12v-40rpm-160rpm-dc-motor |
| 3 | 304 SS shaft 8mm × 300mm | ground finish | ₱222.40 ea = ₱667.20 | (19), 77 sold | https://www.lazada.com.ph/products/pdp-i4473127402.html |
| 3 | KP08 pillow block 2-pc set | 8mm bore — select KP08 | ₱310/set = ₱930 | Bulacan | https://www.lazada.com.ph/products/pdp-i5039609084.html |
| 2 | Rigid coupling set (use 8×8) | 3 needed + spare | ₱82.84 ea = ₱165.68 | (185), 408 sold | https://www.lazada.com.ph/products/pdp-i2734273953.html |
| 1 | Silicone wire kit 6–18AWG | 16 main/logic, 18 stations, 22 logic | ₱218 | 6.2K sold | https://www.lazada.com.ph/products/pdp-i4880482146.html |
| 1 | Dupont jumper kit 40-pin | logic hookups | ₱45 | Circuitrocks | https://www.lazada.com.ph/products/pdp-i245055558.html |
| 1 | Terminal block 15A barrier | DC distribution | ₱106 | Laguna | https://www.lazada.com.ph/products/pdp-i2818578034.html |
| 1 | Heat-shrink kit | splices | ₱111 | Toolstar | https://www.lazada.com.ph/products/pdp-i1085866956.html |
| 1 | Resistor kit 300pc | 220Ω LED, 4.7kΩ DS18B20, 10kΩ pull-ups | ₱69 | (73) | https://www.lazada.com.ph/products/pdp-i4888115298.html |
| 1 | Nylon standoff kit | board mounting | ₱97 | (252) | https://www.lazada.com.ph/products/pdp-i2946710217.html |
| 2 | **LiFePO4 12.8V 200Ah w/ BMS 200A (PowMr)** | parallel bank, 5,120Wh — feeds inverter + DC; ORDER FIRST | ~₱8,900 ea = ~₱17,800 | PowMr, 4.8 (22) | https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html |
| 1 | **LiFePO4 charger 14.6V 20A** | recharge ≈ 10 h — verify 14.6V output + LiFePO4 mode; never lead-acid | ~₱2,000–2,700 EST | Lazada (435 rated, 4.8) | https://www.lazada.com.ph/tag/lifepo4-charger-20a/ |
| 1 | Blade fuse kit 100pc + 1 panel holder | 25A main, 3A ×4 | ₱122.53 + ₱25 | (5022) | https://www.lazada.com.ph/products/pdp-i4214903852.html + https://www.lazada.com.ph/products/pdp-i2502994973.html |
| 1 | Aluminum plate 6061 6mm | motor plate + mounts | ₱760 | (52) | https://www.lazada.com.ph/products/pdp-i4449859085.html |
| 1 | Zip ties, M3/M4 screws, sealant, drip tray, velcro, grommets | consumables | ~₱490 | hardware | (any order) |

### Cart totals (Rev 6)

| Group | Subtotal |
|---|---|
| Electronics (Mega, SSR ×2, relays, sensors, UI, buck) | ≈ ₱2,572 |
| Mains kit (RCD, box, heatsinks, 2.0mm² wire, plug/socket, AC rocker, changeover) | ≈ ₱3,200–3,700 EST |
| Appliances (2× heater-fan ₱2,791 + Omni 12" ~₱1,200 EST) | ≈ ₱3,990 |
| Power conversion (1× pure sine inverter 3000W) | ≈ ₱5,500–8,500 EST |
| Battery bank (2× 200Ah) + 20A charger | ≈ ₱19,800–20,500 |
| Drivetrain (3 stations) | ≈ ₱5,510 |
| Wiring, fuses (incl. 250A ANL kit), chassis, consumables | ≈ ₱2,700–3,300 |
| **TOTAL** | **≈ ₱43,600–48,100** (≈ +₱23,000 vs Rev 5 — inverter, 200Ah bank, 20A charger, changeover, ANL kit) |

## Rev-6 order notes

1. **Inverter: pure sine, continuous rating ≥ 3000W, 12V, 60Hz, remote/enable pin.** Many "4000W" listings are surge-only or modified sine — check the fine print; the exhaust fan is an induction motor.
2. **Never parallel the two sources.** The changeover switch is the only path to the RCD. In wall mode the inverter remote pin is grounded (inverter OFF). Test the interlock drill in SETUP before the first heated cycle.
3. **Inverter sizing:** 3000W **continuous** (many listings are surge-only). Battery mode is stage-1-only by firmware — heater 1 + fan ≈ 2.05kW = 68%. Stage 2 (3.4kW) is wall-mode only.
4. **SSR type: DA (AC output) only.** The DD type cannot switch these AC heaters. Double-check the marking before wiring: SSR-40DA.
5. **Mains work must follow the RCD + grounded-box + earthing rules** in `wiring/README.md` — when in doubt, have a licensed electrician wire the AC side.
6. **Heaters and exhaust fan are appliances with plugs** — keep plugs accessible; unplug before chamber service.
7. The 12" Omni listing spans 12/14/16-inch variants — **select 12-inch**.
8. Battery still has the ~60-day lead time — order first, as always.
9. DHT22: select the "DHT22 Black" ₱69 variant.

---

## 15. Pin Map (v6 final)

| Pin | Connection |
|---|---|
| D2 | DHT22 data |
| D3 | DS18B20 data (+4.7kΩ pull-up) |
| D4 | SSR-40DA #1 input — heater-fan 1 (staged base) |
| D5 | SSR-40DA #2 input — heater-fan 2 (boost) |
| D6 | Relay #1 ch1 — station 1 motor |
| D7 | Relay #1 ch2 — station 2 motor |
| D8 | Relay #2 ch1 — station 3 motor |
| D9 / D10 / D11 | Green / Yellow / Red LED (220Ω) |
| D12 | Buzzer |
| D13 | Start button (INPUT_PULLUP) |
| D14 | in — source mode sense from the changeover aux contact (LOW = wall-outlet mode; INPUT_PULLUP internally) |
| 20 / 21 | LCD I2C |
| — | 10kΩ pull-downs on D4/D5 (SSR inputs, active-HIGH — hold OFF at boot); 10kΩ pull-ups on D6–D8 to relay VCC (active-LOW boards) |
| — | Mains rocker + RCD + 10A fuses: AC domain (no Mega channel) |
| — | DC rocker + 25A main: battery domain |

---

## 16. Final Verdict (Rev 6)

### THE v6 SYSTEM IS COMPATIBLE AND CAN DRY 3 UMBRELLAS PER CYCLE — IN 15–45 MINUTES FROM THE WALL OUTLET OR THE BATTERY BANK, WITH CHANGEOVER-SELECTED POWER

- 2× 1500W heater-fans staged by humidity, switched by SSR-40DAs (correct AC Fotek type) with five over-temp/shock protection layers.
- Dual source via a 2P changeover: wall outlet (full performance, stage 1+2) or one 3000W pure sine inverter on the 2× 200Ah bank (grid-independent, stage 1 capped by firmware).
- Battery mode budget: inverter 188A steady / 210A surge + stalls 10.5A + logic ≈ 221A peak vs 400A BMS aggregate (1.8×) — and firmware stage-1 capping keeps the inverter at 68% continuous.
- The exhaust fan has no Mega channel; it follows the mains rocker in either source mode (stage 1 airflow is intentional).
- All-12V inside the chamber; the AC box stays closed, earthed, and RCD-protected; the changeover is the single point where the two sources meet — and they never meet electrically.

*Paper figure updates for Rev 6: Fig 11/12 (heater chain → SSR-40DAs + source selection), block diagram (SRC domain), safety chapter (changeover interlock, inverter DC feed), energy chapter (two-mode consumption).*

---

# Appendix A — Printable Shopping Checklist (Rev 6)

### Order sequence
1. FIRST: 2× PowMr 200Ah batteries (pre-order ~60 days)
2. SECOND: 3× motors + 2× SSR-40DA (makerlab.ph, one order)
3. THIRD: 3000W pure sine inverter + changeover switch (verify continuous rating)
4. Everything else (Lazada + hardware)

### Variant picking
| Item | Select |
|---|---|
| DHT22 | "DHT22 Black" (₱69) |
| Omni fan | 12-inch variant |
| Pillow blocks | KP08 |
| Steel shaft | 8mm × 300mm |
| SSR | **SSR-40DA** (AC) — never DD for these heaters |
| Inverter | pure sine, **3000W continuous**, 12V, 60Hz, remote pin |
| Charger | 14.6V output, LiFePO4 mode, ≥ 20A |

### Cart A — makerlab.ph website
- [ ] 3× Worm gear motor SGM-A58SW31ZY 12V **16RPM** = ₱3,747
- [ ] 2× Fotek **SSR-40DA** = ₱320

### Cart B — Lazada PH
- [ ] Arduino Mega 2560 R3 — ₱1,215
- [ ] 2× PTC industrial heater-fan 1500W 220V — ₱2,790.70 — https://www.lazada.com.ph/products/portable-industrial-electric-heater-fan-commercial-thermostat-air-warm-heater-blower-radiator-office-garage-air-fan-i4902069326-s28572024789.html
- [ ] Omni 12" exhaust fan — ~₱1,000–1,500 (12-inch variant) — https://www.lazada.com.ph/products/omni-industrial-exhaust-fan-w-grill-wall-mounted-12-inch-14-inch-16-inch-i4020672066-s21738898500.html
- [ ] 2× 2-CH relay module — ₱178
- [ ] DHT22 Black — ₱69 · DS18B20 — ₱105 · LCD I2C — ₱165 · LEDs — ₱29 · buzzer — ₱35 · buttons — ₱79 · DC rocker — ₱72 · buck — ₱155
- [ ] 3× shaft 8×300 — ₱667.20 · 3× KP08 sets — ₱930 · 2× coupling sets — ₱165.68
- [ ] Silicone wire — ₱218 · dupont — ₱45 · terminal block — ₱106 · heat-shrink — ₱111 · resistors — ₱69 · standoffs — ₱97
- [ ] 2× PowMr 200Ah — ORDER FIRST — https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html
- [ ] LiFePO4 charger 20A — ~₱2,000–2,700 — https://www.lazada.com.ph/tag/lifepo4-charger-20a/
- [ ] Blade fuse kit + holder — ₱147.53 · aluminum plate — ₱760

### Cart C — hardware (mains kit + consumables)
- [ ] RCD/GFCI outlet or breaker (30mA)
- [ ] Grounded metal electrical box + plate
- [ ] 2-gang mains rocker + plate
- [ ] **Changeover switch 2P 63A** (wall / inverter)
- [ ] 2.0mm² 3-core wire + plug/socket set
- [ ] 2× SSR heatsink profile
- [ ] **ANL fuse kit 250A ×2 + holders; 2AWG inverter wire, 4AWG battery links, lugs**
- [ ] Zip ties, M3/M4 screws, silicone sealant, drip tray, velcro, grommets (~₱490)

### Sign-off before checkout
- [ ] SSRs marked **DA**, not DD
- [ ] Inverter: **pure sine**, **3000W continuous** (not surge), 12V, 60Hz, remote pin present
- [ ] Changeover switch on the list — never direct-wire both sources
- [ ] Omni fan is the 12-inch variant
- [ ] Battery pre-order confirmed, ordered first
- [ ] RCD + grounded box on the list (non-negotiable)
- [ ] DHT22 Black / KP08 / 8×300 variants picked
- [ ] Prices re-verified at checkout
