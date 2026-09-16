# Umbrella Dryer V2 — Bill of Materials (Rev 8, canonical)

> **Design:** 12V DC-only system. Each umbrella station has 3× PTC heaters (100W each), 3× BLDC fans, and 1× worm gear motor. Battery-powered with 2× 200Ah LiFePO4 in parallel. **40A automotive relays** control PTC heaters (NPN-driven), **optocoupler module** controls worm motors, **ESC PWM** controls BLDC fans.
>
> **Rev 8 changes:** Main fuse upgraded to 50A ANL; PTC relays upgraded to 40A automotive (4×); per-station PTC fuses 30A; thermal fuse 130°C per heater (9×); kill switch upgraded to 50A disconnect; LCD I2C on pins 20/21.

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
| 2 | **LiFePO4 12.8V 200Ah w/ BMS 200A (PowMr)** | Parallel bank, 400Ah, 5,120Wh; **ORDER FIRST** | ~₱8,900 ea = ~₱17,800 |
| 1 | **LiFePO4 charger 14.6V 20A** | Recharge ≈ 10h; verify 14.6V output; never lead-acid | ~₱2,000–2,700 |

### 3b. DC power distribution

| Fuse | Rating | Protects |
|---|---|---|
| Main | **50A ANL** | Total DC bus (one station at a time ≈ 36A) |
| Disconnect | **50A battery disconnect switch** | Manual kill — replaces old 10A DC rocker |
| Station PTC 1 | **30A** | 3× PTC heaters station 1 (~25A) |
| Station PTC 2 | **30A** | 3× PTC heaters station 2 |
| Station PTC 3 | **30A** | 3× PTC heaters station 3 |
| Fan bus | **30A** | 9× BLDC fans (~28.8A) |
| Motor 1 | **3A** | 1× SGM-370 motor |
| Motor 2 | **3A** | 1× SGM-370 motor |
| Motor 3 | **3A** | 1× SGM-370 motor |
| Logic | **3A** | Mega + sensors + buck |

> Wire: 8 AWG battery main, 10 AWG heater/fan branches, 18 AWG motor, 20 AWG logic, 22 AWG signals. All stranded copper. Fuses on the + side only.

### 3c. High-current relay switching (12V DC)

| Channel | Pin | Relay type | Load | Current | Active level |
|---|---|---|---|---|---|
| PTC Station 1 | D4 | 40A automotive + 2N2222 | 3× PTC heaters | ~25A | HIGH = ON |
| Motor Station 1 | D5 | Optocoupler module ch1 | SGM-370 | ~0.8A | LOW = ON |
| PTC Station 2 | D6 | 40A automotive + 2N2222 | 3× PTC heaters | ~25A | HIGH = ON |
| Motor Station 2 | D7 | Optocoupler module ch2 | SGM-370 | ~0.8A | LOW = ON |
| PTC Station 3 | D8 | 40A automotive + 2N2222 | 3× PTC heaters | ~25A | HIGH = ON |
| Motor Station 3 | D9 | Optocoupler module ch3 | SGM-370 | ~0.8A | LOW = ON |
| Fan bus | D13 | 40A automotive + 2N2222 | 9× ESCs (all fans) | ~28.8A | HIGH = ON |

> **NPN driver components per automotive relay (4×):** 2N2222 + 1 kΩ base resistor + 10 kΩ base-to-GND pull-down + 1N4007 flyback diode across coil.

### 3d. BLDC fan control — ESCs

| Channel | ESC Signal Pin | Function | ESC Input |
|---|---|---|---|
| ESC 1 | D10 | Station 1 BLDC fans (3 in parallel) | 12V from fan bus relay |
| ESC 2 | D11 | Station 2 BLDC fans (3 in parallel) | 12V from fan bus relay |
| ESC 3 | D12 | Station 3 BLDC fans (3 in parallel) | 12V from fan bus relay |

> ESCs must be armed on startup (write 1000 µs for 2s, then throttle position). Use the Servo library for PWM generation.

### 3e. Safety (12V DC)

- 50A ANL main fuse + 50A battery disconnect switch
- Per-station fuses: 30A (PTC heaters), 3A (motor), 30A (fan bus), 3A (logic)
- DS18B20 cutoff if chamber exceeds 65 °C: firmware cuts all relays + ESCs
- **130 °C one-shot thermal fuse on each PTC heater (9×)** — non-resettable
- PTC self-regulation: resistance rises with temperature, auto-limits
- Battery BMS protects against over-discharge, over-charge, short circuit
- No mains voltage anywhere — no RCD needed

---

## 4. Station peripherals

| Qty | Part | Notes | Price |
|---|---|---|---|
| 4 | **12V 40A automotive relay (5-pin SPDT)** | 3× PTC switching + 1× fan bus; coil driven via 2N2222 | ~₱80 ea = ~₱320 |
| 1 | **4-CH optocoupler relay module (10A @ 30VDC)** | 3 channels used for worm motors (ch1–3); ch4 spare | ~₱200 |
| 9 | **DC 12V BLDC fan module w/ ESC** | 50mm ducted, 12V, ~3.2A each — 3 fans per station wired in parallel on one ESC | ~₱470 ea = ~₱4,230 |
| 9 | **12V 100W PTC heater element (MXKJING T30)** | Self-regulating ceramic — 3 per station | ~₱484 ea = ~₱4,356 |
| 9 | **130 °C / 10A one-shot thermal fuse** | One per PTC heater in its + lead | ~₱15 ea = ~₱135 |
| 4 | **2N2222 NPN transistor (TO-92)** | PTC relay + fan bus drivers | ~₱5 ea = ~₱20 |
| 4 | **1 kΩ resistor (¼W)** | NPN base resistors | from kit |
| 4 | **10 kΩ resistor (¼W)** | NPN base pull-downs | from kit |
| 4 | **1N4007 diode** | Flyback across each automotive relay coil | from kit |
| 1 | 16×2 I2C LCD | UI display | ₱165 |
| 3 | 5 mm LEDs — red, yellow, green | Status indicators | ₱29 |
| 1 | Active buzzer 5 V | Audible alert | ₱35 |
| 1 | Arcade LED push button (5 V) | Start button | ₱45 |
| 1 | 50A battery disconnect switch | Main kill switch | ~₱150 EST |
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
| Over-temperature | (1) DS18B20 firmware cutoff at 65°C (2) 130°C thermal fuse per heater (3) PTC self-regulation |
| Cooling | 3× BLDC fans per station; chamber is vented |

---

## 7. Capacity verification

### 7a. Mechanical — per-station torque — PASS
≤3 kg·cm per station vs 14 kg·cm → ≥4.6× margin; KP08 >90× load margin; 6 RPM gentle; self-locking hold.

### 7b. Thermal — PASS
300W per station with BLDC fan circulation → 40–60°C chamber; DS18B20 + thermal fuse + PTC self-regulation = triple over-temp protection.

### 7c. Electrical — 12V DC — PASS

| Subsystem | Voltage | Current (one station) | Protection |
|---|---|---|---|
| PTC heaters (3× 100W) | 12V | 25A | 30A fuse per station + 130°C thermal fuse per heater |
| BLDC fans (3× 3.2A) | 12V | 9.6A | 30A fan bus fuse |
| Worm motor | 12V | 0.8A | 3A fuse |
| Mega + sensors | 5V | 0.1A | 3A fuse |
| **Total (one station)** | | **~36A** | **50A main fuse** |

### 7d. Battery runtime — corrected for LiFePO4 usable capacity

> **Usable capacity ≠ nameplate.** LiFePO4 should be cycled at 80% DoD for rated cycle
> life, and the bank should still meet spec at 90% capacity (end-of-life margin):
> **usable = 400 Ah × 0.80 × 0.90 ≈ 288 Ah** (≈ 3.5 kWh at 12V).

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

**Runtime on the 400 Ah bank (288 Ah usable):**

| Mode | Result |
|---|---|
| Quick cycles | ≈ **19 cycles (57 umbrellas)** per charge |
| Standard cycles | ≈ **8.8 cycles (26 umbrellas)** per charge |
| Continuous staged operation | ≈ **8.1 hours** (288 Ah ÷ 35.5A) |
| Standby | ≈ 24 days (288 Ah ÷ 0.5A) |

**Capacity requirement check — 2× 200Ah is adequate:**

| Daily scenario | Ah/day | Min bank required (÷ 0.72) |
|---|---|---|
| Capstone demo: 6 quick cycles (18 umb) | ≈ 91 Ah | 126 Ah |
| Typical rainy day: 10 quick cycles (30 umb) | ≈ 151 Ah | 210 Ah |
| Typical rainy day: 8 standard cycles (24 umb) | ≈ 263 Ah | 365 Ah |
| Heavy day: 12 standard cycles (36 umb, full-dry) | ≈ 395 Ah | 548 Ah |

> **Verdict:** 2× 200Ah (400 Ah) covers the capstone demo and typical mixed use with
> margin; a heavy all-standard day slightly exceeds one charge (charge overnight —
> ~14 h at 14.6 V / 20 A for a full 240 Ah recharge from typical-day depletion).
> C-rate is gentle: 0.09 C on the bank (0.18 C per pack), far below the 200A BMS limit.

---

## 8. Fuse plan

| Fuse | Rating | Location | Protects |
|---|---|---|---|
| Main | **50A ANL** | Battery positive, after disconnect switch | Total DC bus |
| Disconnect | **50A** | Battery positive, before main fuse | Manual kill |
| PTC Station 1 | **30A** | Station 1 PTC heater branch | 3× PTC heaters (~25A) |
| PTC Station 2 | **30A** | Station 2 PTC heater branch | 3× PTC heaters |
| PTC Station 3 | **30A** | Station 3 PTC heater branch | 3× PTC heaters |
| Motor Station 1 | **3A** | Station 1 motor branch | 1× worm motor |
| Motor Station 2 | **3A** | Station 2 motor branch | 1× worm motor |
| Motor Station 3 | **3A** | Station 3 motor branch | 1× worm motor |
| Fan Bus | **30A** | BLDC fan power bus | 9× BLDC fans |
| Logic | **3A** | Mega + sensors + buck | Logic subsystem |

---

## 9. Pin assignment (Mega 2560) — canonical

| Pin | Net | Direction | Function | Active level |
|---|---|---|---|---|
| D2 | DHT22_DATA | in | Chamber humidity + temp sensor | — |
| D3 | DS18B20_DATA | in | Heater-zone temperature probe | — |
| D4 | RELAY_PTC_1 | out | PTC heaters station 1 (40A auto relay via NPN) | HIGH = ON |
| D5 | RELAY_MOTOR_1 | out | Worm motor station 1 (opto module) | LOW = ON |
| D6 | RELAY_PTC_2 | out | PTC heaters station 2 (40A auto relay via NPN) | HIGH = ON |
| D7 | RELAY_MOTOR_2 | out | Worm motor station 2 (opto module) | LOW = ON |
| D8 | RELAY_PTC_3 | out | PTC heaters station 3 (40A auto relay via NPN) | HIGH = ON |
| D9 | RELAY_MOTOR_3 | out | Worm motor station 3 (opto module) | LOW = ON |
| D10 | ESC_1 | out (PWM) | ESC signal — station 1 BLDC fans | — |
| D11 | ESC_2 | out (PWM) | ESC signal — station 2 BLDC fans | — |
| D12 | ESC_3 | out (PWM) | ESC signal — station 3 BLDC fans | — |
| D13 | RELAY_FAN_BUS | out | Fan power bus (40A auto relay via NPN) | HIGH = ON |
| D14 | BTN_START | in | Arcade push button (INPUT_PULLUP) | LOW = pressed |
| D15 | LED_RED | out | Heating active | HIGH = ON |
| D16 | LED_YELLOW | out | Cycle running / cooling | HIGH = ON |
| D17 | LED_GREEN | out | Ready / done | HIGH = ON |
| D18 | BUZZER | out | Audible notification | HIGH = ON |
| 20 | SDA | I2C | LCD data | — |
| 21 | SCL | I2C | LCD clock | — |

---

## 10. BOM line-item table (Lazada + makerlab)

| Qty | Part | Spec | Price | Seller | URL / note |
|---|---|---|---|---|---|
| 9 | PTC ceramic heater MXKJING T30 | 12V 100W | ₱484 ea = ₱4,356 | Lazada (LazMall) | https://www.lazada.com.ph/products/pdp-i15593670246.html |
| 9 | BLDC fan module 50mm 12V w/ ESC | 12V ~3.2A | ₱469 ea = ₱4,221 | Lazada | search "50mm BLDC ducted fan 12V ESC" |
| 9 | Thermal fuse 130°C / 10A | One-shot | ~₱15 ea = ~₱135 | Lazada | search "thermal fuse 130C 10A" |
| 3 | Worm gear motor SGM-370 | 12V 6RPM 14 kg·cm | ₱500 ea = ₱1,500 | makerlab.ph | https://makerlab.ph/products/dc-worm-gear-motor-sgm-370-12v-16rpm |
| 4 | 40A automotive relay 5-pin SPDT | 12V 40A | ~₱80 ea = ~₱320 | Lazada | search "12v 40a automotive relay" |
| 1 | 4-CH optocoupler relay module | 10A @ 30VDC | ~₱200 | Lazada | search "4 channel relay module 12V optocoupler" |
| 4 | 2N2222 NPN transistor (TO-92) | — | ~₱5 ea = ~₱20 | Lazada | search "2n2222 transistor" |
| 4 | 1N4007 diode | flyback | from kit | Lazada | — |
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
| 1 | 50A battery disconnect switch | main kill | ~₱150 | Lazada | search "50a battery disconnect switch" |
| 1 | Dupont jumper kit 40-pin | logic | ₱45 | Circuitrocks | — |
| 1 | Terminal block 15A barrier | DC distribution | ₱106 | Lazada | — |
| 1 | Silicone wire kit 6–18AWG | gauges | ₱218 | Lazada | — |
| 1 | Heat-shrink tube kit | insulation | ₱111 | Lazada | — |
| 1 | 1/4W resistor kit | pull-ups, limiters | ₱69 | Lazada | — |
| 1 | Automotive blade fuse kit (3A–25A + 30A + 50A) | DC fuses | ~₱200 | Lazada | search "automotive blade fuse kit assortment" |
| 1 | ANL fuse holder + 50A fuse | main fuse | ~₱80 | Lazada | search "ANL fuse holder 50A" |
| 1 | Aluminum plate 6061 6mm | motor plate | ₱760 | Lazada | — |
| 2 | LiFePO4 12.8V 200Ah w/ BMS 200A | battery | ~₱8,900 ea = ~₱17,800 | Lazada (PowMr) | — |
| 1 | LiFePO4 charger 14.6V 20A | recharge | ~₱2,000–2,700 | Lazada | — |
| 1 | Zip ties, screws, sealant, grommets | consumables | ~₱490 | hardware | — |

---

## 11. Cost summary

| Category | Estimate |
|---|---|
| PTC heaters (9×₱484) | ≈ ₱4,356 |
| Thermal fuses (9×₱15) | ≈ ₱135 |
| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
| Motors + shafts + bearings + couplings | ≈ ₱3,028 |
| Automotive relays (4×₱80) + opto module | ≈ ₱520 |
| NPN driver components (4×2N2222 + resistors + diodes) | ≈ ₱40 |
| Control electronics (Mega, sensors, LCD, buck) | ≈ ₱1,589 |
| Battery bank (2× 200Ah) + charger | ≈ ₱19,800–20,500 |
| Disconnect switch + fuses + fuse holders | ≈ ₱430 |
| UI (LEDs, buzzer, button) | ≈ ₱109 |
| Wiring, connectors, consumables | ≈ ₱1,800–2,200 |
| **TOTAL** | **≈ ₱36,000–37,000** |
