# Umbrella Dryer V2 — Bill of Materials

> **Design:** 12V DC-only system. Each umbrella station has 3× PTC heaters (100W each), 3× BLDC fans, and 1× worm gear motor. Battery-powered with **1× 200Ah LiFePO4**. **DC-output SSR-40DD** control PTC heaters (direct-drive from Mega), **optocoupler module** controls worm motors, **ESC PWM** controls BLDC fans.

---

## 1. Control (logic)

| Qty | Part | Notes | Price | Source |
|---|---|---|---|---|
| 1 | Arduino Mega 2560 + USB cable | CH340G — Makerlab PH | ₱1,165 | Lazada — Makerlab PH |
| 1 | DHT22 temperature + humidity sensor module | Mount mid-chamber, away from air jets | ₱210 | Lazada — Makerlab PH |
| 1 | DS18B20 waterproof (probe + long lead) | Attached in heater airstream | ₱105 | Lazada |
| 1 | 16×2 LCD I2C (black on white OK) | I2C address 0x27 or 0x3F; **wire to Mega pins 20/21** | ₱165 | Lazada |

---

## 2. Power conversion — 12V DC

| Qty | Part | Notes | Price |
|---|---|---|---|
| 1 | LM2596S DC-DC buck converter | 12V→5V for Mega + sensors; **set to 5.00 V before connecting to Mega 5V pin** | ₱49 |

---

## 3. Power supply — 12V DC

### 3a. Battery bank + charging

| Qty | Part | Notes | Price |
|---|---|---|---|
| 1 | **LiFePO4 12.8V 200Ah w/ BMS 200A (PowMr)** | Single battery, 200Ah, 2,560Wh; **ORDER FIRST** | ~₱8,900 |
| 1 | **LiFePO4 charger 14.6V 20A** | Recharge ≈ 10h; verify 14.6V output; never lead-acid | ~₱2,000–2,700 |

### 3b. DC power distribution

|| Wire: 8 AWG battery main, 10 AWG heater/fan branches, 18 AWG motor, 20 AWG logic, 22 AWG signals. All stranded copper. No fuses, no disconnect switch in the circuit.

### 3c. High-current switching (12V DC)

| Channel | Pin | Relay type | Load | Current | Active level |
|---|---|---|---|---|---|
| PTC Station 1 | D4 | LCTC DC-DC SSR 40A (DC output) | 3× PTC heaters | ~25A | HIGH = ON |
|| Motor Station 1 | D5 | LCTC DC-DC SSR 10A (DC output) | SGM-370 | ~0.8A | HIGH = ON |
|| PTC Station 2 | D6 | LCTC DC-DC SSR 40A (DC output) | 3× PTC heaters | ~25A | HIGH = ON |
|| Motor Station 2 | D7 | LCTC DC-DC SSR 10A (DC output) | SGM-370 | ~0.8A | HIGH = ON |
|| PTC Station 3 | D8 | LCTC DC-DC SSR 40A (DC output) | 3× PTC heaters | ~25A | HIGH = ON |
|| Motor Station 3 | D9 | LCTC DC-DC SSR 10A (DC output) | SGM-370 | ~0.8A | HIGH = ON |
|| Fan bus | D13 | LCTC DC-DC SSR 40A (DC output) | 9× ESCs (all fans) | ~28.8A | HIGH = ON |

> **SSR direct drive:** All LCTC DC-DC SSR inputs connect directly to Mega pins. SSR input draws ≈10–20 mA at 5V — fine for direct drive. No additional components needed. Each SSR requires a heatsink (40A version: ~25W dissipation at 25A). Motor SSRs (10A): minimal dissipation at 0.8A.

### 3d. BLDC fan control — ESCs

| Channel | ESC Signal Pin | Function | ESC Input |
|---|---|---|---|
| ESC 1 | D10 | Station 1 BLDC fans (3 in parallel) | 12V from fan bus SSR |
| ESC 2 | D11 | Station 2 BLDC fans (3 in parallel) | 12V from fan bus SSR |
| ESC 3 | D12 | Station 3 BLDC fans (3 in parallel) | 12V from fan bus SSR |

> ESCs must be armed on startup (write 1000 µs for 2s, then throttle position). Use the Servo library for PWM generation.

### 3e. Safety (12V DC)

- No fuses in the circuit
- DS18B20 cutoff if chamber exceeds 65 °C: firmware cuts all SSRs + ESCs
- PTC self-regulation: resistance rises with temperature, auto-limits
- Battery BMS protects against over-discharge, over-charge, short circuit
- No mains voltage anywhere — no RCD needed

---

## 4. Station peripherals

| Qty | Part | Notes | Price |
|---|---|---|---|
|| 4 | **LCTC DC-DC SSR 40A** | DC input (3-32VDC) → DC output, 40A rated; 3× PTC + 1× fan bus; direct-drive from Mega | ~₱344 ea = ~₱1,376 |
|| 3 | **LCTC DC-DC SSR 10A** | DC input (3-32VDC) → DC output, 10A rated; motor control (replaces optocoupler module) | ~₱164 ea = ~₱492 |
| 9 | **DC 12V BLDC fan module w/ ESC** | 50mm ducted, 12V, ~3.2A each — 3 fans per station wired in parallel on one ESC | ~₱470 ea = ~₱4,230 |
| 9 | **12V 100W PTC heater element (MXKJING T30)** | Self-regulating ceramic — 3 per station | ~₱484 ea = ~₱4,356 |
|| 4 | Heatsinks for SSR-40A | ~₱50 ea | ~₱200 |
| 1 | 16×2 I2C LCD | UI display | ₱165 |
| 3 | 5 mm LEDs — red, yellow, green | Status indicators | ₱29 |
| 1 | Active buzzer 5 V | Audible alert | ₱35 |
| 1 | Arcade LED push button (5 V) | Start button | ₱45 |
| 1 | Screw terminal 2-pin | Battery in | ₱10 |
| 1 | Screw terminal 3-pin | Sensor | ₱10 |

---

## 5. Motor & Drive — 3× worm stations

3× SGM-370 12V 6RPM (14 kg·cm, ~0.2A rated / ~0.8A stall, 6mm shaft, self-locking) — one per umbrella.

Mechanical: 3× 6mm × 300mm 304 SS shafts · 6× KP08 pillow block bearings · 3× 6×8 rigid couplings · fabricated holders.

---

## 6. Thermal design (12V DC)

| Item | Spec |
|---|---|
| Heat source | 9× PTC ceramic heaters, 12V 100W each = 900W total (300W per station) |
| PTC behavior | Self-regulating: resistance rises with temperature → current drops → auto-limits |
| Heating method | PTC elements radiate + convect heat; BLDC fans circulate warm air |
| Temperature target | 40–60°C chamber air |
| Temperature sensing | DHT22 (humidity) mid-chamber + DS18B20 (temp) in heater airstream |
| Over-temperature | (1) DS18B20 firmware cutoff at 65°C (2) PTC self-regulation |
| Cooling | 3× BLDC fans per station; chamber is vented |

---

## 7. Capacity verification

### 7a. Mechanical — per-station torque — PASS
≤3 kg·cm per station vs 14 kg·cm → ≥4.6× margin; KP08 >90× load margin; 6 RPM gentle; self-locking hold.

### 7b. Thermal — PASS
300W per station with BLDC fan circulation → 40–60°C chamber; DS18B20 + PTC self-regulation = dual over-temp protection.

### 7c. Electrical — 12V DC — PASS

| Subsystem | Voltage | Current (one station) | Protection |
|---|---|---|---|
| PTC heaters (3× 100W) | 12V | 25A | BMS 200A + PTC self-regulation |
| BLDC fans (3× 3.2A) | 12V | 9.6A | BMS 200A |
| Worm motor | 12V | 0.8A | BMS 200A |
| Mega + sensors | 5V | 0.1A | BMS 200A |
| **Total (one station)** | | **~36A** | **BMS 200A** |

### 7d. Battery runtime — 1× 200Ah LiFePO4

> **Usable capacity ≠ nameplate.** LiFePO4 should be cycled at 80% DoD for rated cycle
> life, and the battery should still meet spec at 90% capacity (end-of-life margin):
> **usable = 200 Ah × 0.80 × 0.90 ≈ 144 Ah** (≈ 1.73 kWh at 12V).

Load profile (staged, one station at a time):

| Phase | Draw | Notes |
|---|---|---|
| PREHEAT / DRY (active station) | ~35.5A | 3 PTC (25A) + 3 fans full (9.6A) + motor (0.2A) + logic (0.4A) + idle ESCs (0.3A) |
| COOL | ~10.3A | Fans only |
| Standby | ~0.5A | Sensors + LCD |

Energy per drying cycle (3 umbrellas per cycle):

| Cycle type | Duration | Energy | Per umbrella |
|---|---|---|---|
| Quick (surface dry, light rain) | 10 min preheat + 15 min dry + 2 min cool ≈ 27 min | ≈ 15 Ah (≈ 182 Wh) | ≈ 5 Ah |
| Standard (fully soaked) | 10 min preheat + 45 min dry + 2 min cool ≈ 57 min | ≈ 33 Ah (≈ 395 Wh) | ≈ 11 Ah |

> 45 min staged DRY gives each umbrella 15 min of direct heat — the same 300 W × 15 min
> dose as the original non-staged 15-min cycle.

**Runtime on the 200 Ah battery (144 Ah usable):**

| Mode | Result |
|---|---|
| Quick cycles | ≈ **9.6 cycles (~29 umbrellas)** per charge |
| Standard cycles | ≈ **4.4 cycles (~13 umbrellas)** per charge |
| Continuous staged operation | ≈ **4.1 hours** (144 Ah ÷ 35.5A) |
| Standby | ≈ 12 days (144 Ah ÷ 0.5A) |

**Capacity requirement vs daily scenarios:**

| Daily scenario | Ah/day | Min battery required (÷ 0.72) |
|---|---|---|
| Capstone demo: 6 quick cycles (18 umb) | ≈ 91 Ah | 126 Ah |
| Typical rainy day: 10 quick cycles (30 umb) | ≈ 151 Ah | 210 Ah |
| Typical rainy day: 8 standard cycles (24 umb) | ≈ 263 Ah | 365 Ah |
| Heavy day: 12 standard cycles (36 umb, full-dry) | ≈ 395 Ah | 548 Ah |

> **Verdict:** 1× 200Ah covers the capstone demo (18 umbrellas) with ~40% margin.
> For busy days, recharge between sessions — a full 0→100% recharge takes ~7–9 h at
> 14.6 V / 20 A (real-world CC/CV taper), or top up overnight.
> C-rate is gentle: 0.18 C at full staged draw, far below the 200A BMS limit.
>
> **Expansion path:** battery wiring supports adding a second 200Ah pack in parallel later (bank becomes 400Ah / 288 Ah usable) with no other changes.

---

## 8. Pin assignment (Mega 2560)

| Pin | Net | Direction | Function | Active level |
|---|---|---|---|---|
| D2 | DHT22_DATA | in | Chamber humidity + temp sensor | — |
| D3 | DS18B20_DATA | in | Heater-zone temperature probe | — |
| D4 | SSR_PTC_1 | out | PTC heaters station 1 (LCTC DC-DC SSR 40A) | HIGH = ON |
| D5 | SSR_MOTOR_1 | out | Worm motor station 1 (LCTC DC-DC SSR 10A) | HIGH = ON |
| D6 | SSR_PTC_2 | out | PTC heaters station 2 (LCTC DC-DC SSR 40A) | HIGH = ON |
| D7 | SSR_MOTOR_2 | out | Worm motor station 2 (LCTC DC-DC SSR 10A) | HIGH = ON |
| D8 | SSR_PTC_3 | out | PTC heaters station 3 (LCTC DC-DC SSR 40A) | HIGH = ON |
| D9 | SSR_MOTOR_3 | out | Worm motor station 3 (LCTC DC-DC SSR 10A) | HIGH = ON |
| D10 | ESC_1 | out (PWM) | ESC signal — station 1 BLDC fans | — |
| D11 | ESC_2 | out (PWM) | ESC signal — station 2 BLDC fans | — |
| D12 | ESC_3 | out (PWM) | ESC signal — station 3 BLDC fans | — |
| D13 | SSR_FAN_BUS | out | Fan power bus (LCTC DC-DC SSR 40A) | HIGH = ON |
| D14 | BTN_START | in | Arcade push button (INPUT_PULLUP) | LOW = pressed |
| D15 | LED_RED | out | Heating active | HIGH = ON |
| D16 | LED_YELLOW | out | Cycle running / cooling | HIGH = ON |
| D17 | LED_GREEN | out | Ready / done | HIGH = ON |
| D18 | BUZZER | out | Audible notification | HIGH = ON |
| 20 | SDA | I2C | LCD data | — |
| 21 | SCL | I2C | LCD clock | — |

---

## 9. BOM line-item table (Lazada + makerlab)

| Qty | Part | Spec | Price | Seller | URL / note |
|---|---|---|---|---|---|
| 9 | PTC ceramic heater MXKJING T30 | 12V 100W | ₱484 ea = ₱4,356 | Lazada (LazMall) | https://www.lazada.com.ph/products/pdp-i15593670246.html |
| 9 | BLDC fan module 50mm 12V w/ ESC | 12V ~3.2A | ₱469 ea = ₱4,221 | Lazada | search "50mm BLDC ducted fan 12V ESC" |
| 3 | Worm gear motor SGM-370 | 12V 6RPM 14 kg·cm | ₱500 ea = ₱1,500 | makerlab.ph | https://makerlab.ph/products/dc-worm-gear-motor-sgm-370-12v-16rpm |
|| 4 | LCTC DC-DC SSR 40A | Input 3–32VDC, DC output, 40A, heatsink required | ~₱344 ea = ~₱1,376 | Lazada | https://www.lazada.com.ph/products/pdp-i5107319917-s30094632906.html |
|| 4 | Heatsinks for SSR-40A | For ~25W dissipation per SSR | ~₱50 ea = ~₱200 | Lazada | search "SSR heatsink" |
|| 3 | LCTC DC-DC SSR 10A | Input 3–32VDC, DC output, 10A | ~₱164 ea = ~₱492 | Lazada | same seller, select 10A variant |
| 1 | LM2596S buck converter | 12V→5V | ₱49 | Makerlab PH | — |
| 1 | Arduino Mega 2560 + USB | CH340G | ₱1,165 | Makerlab PH | — |
| 1 | DHT22 module | humidity | ₱210 | Makerlab PH | — |
| 1 | DS18B20 waterproof probe | temp | ₱105 | Lazada | — |
| 1 | LCD 16×2 I2C | display | ₱165 | Lazada | — |
| 3 | 304 SS shaft 6mm × 300mm | — | ~₱180 ea = ~₱540 | Lazada | — |
| 6 | KP08 pillow block 6mm bore | — | ₱87 ea = ₱522 | Lazada | — |
| 2 | Rigid coupling 6×8mm | — | ₱82.84 ea = ~₱166 | Lazada | — |
| 1 | LED 5mm (R/Y/G) | status | ₱29 | Lazada | — |
| 1 | Active buzzer 5V | alarm | ₱35 | Lazada | — |
| 1 | Arcade LED push button 5V | start | ₱45 | Circuitrocks | — |
| 1 | Silicone wire kit 6–18AWG | gauges | ₱218 | Lazada | — |
| 1 | Dupont jumper kit 40-pin | logic | ₱45 | Circuitrocks | — |
| 1 | Terminal block 15A barrier | Existing terminal block (unchanged) | ₱106 | Lazada | — |
| 2 | 10-Terminal Bus Bar 150A (Copper) | Main 12V (+ & -) bus rails | ~₱350 ea = ₱700 | Lazada | https://www.lazada.com.ph/products/814-terminal-bus-bar-150a-high-current-dc-busbar-12-48v-copper-power-distribution-terminal-block-for-car-boat-i5119401028-s30216194181.html |
| 1 | Heat-shrink tube kit | insulation | ₱111 | Lazada | — |
| 1 | 1/4W resistor kit | pull-ups | ₱69 | Lazada | — |
| 1 | Aluminum plate 6061 6mm | motor plate | ₱760 | Lazada | — |
| 1 | LiFePO4 12.8V 200Ah w/ BMS 200A | battery | ~₱8,900 | Lazada (PowMr) | — |
| 1 | LiFePO4 charger 14.6V 20A | recharge | ~₱2,000–2,700 | Lazada | — |
| 1 | Zip ties, screws, sealant, grommets | consumables | ~₱490 | hardware | — |

---

## 10. Cost summary

| Category | Estimate |
||---|---|
|| PTC heaters (9×₱484) | ≈ ₱4,356 |
|| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
|| Motors + shafts + bearings + couplings | ≈ ₱3,028 |
|| LCTC DC-DC SSR 40A (4×₱344) + SSR 10A (3×₱164) + heatsinks | ≈ ₱2,068 |
|| Control electronics (Mega, sensors, LCD, buck) | ≈ ₱1,589 |
|| Battery (1× 200Ah) + charger | ≈ ₱10,900–11,600 |
|| UI (LEDs, buzzer, button) | ≈ ₱109 |
|| Wiring, connectors, consumables | ≈ ₱1,500–1,900 |
|| **TOTAL** | **≈ ₱27,600–28,100** |
