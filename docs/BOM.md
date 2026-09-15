# Umbrella Dryer V2 — Bill of Materials — 12V DC System

> **Design:** 12V DC-only system — no mains, no inverter, no RCD. Each umbrella station has 3× PTC heaters (100W each), 3× BLDC fans, and 1× worm gear motor. Battery-powered with 2× 200Ah LiFePO4 in parallel. Relays control PTC heaters and motors; ESCs control BLDC fans via PWM.

---

## 1. Control (logic)

| Qty | Part | Notes | Price | Source |
|---|---|---|---|---|
| 1 | Arduino Mega 2560 + USB cable | CH340G — Makerlab PH | ₱1,165 | Lazada — Makerlab PH |
| 1 | DHT22 temperature + humidity sensor module | one per umbrella station | ₱210 | Lazada — Makerlab PH |
| 1 | DS18B20 waterproof (probe + long lead) | attached near heaters | ₱105 | (258), 6K sold |
| 1 | 16×2 LCD I2C (black on white OK) | addresses 0x27/0x3F; I2C only | ₱165 | (241), 2K sold |

## 2. Power conversion — 12V DC

| Qty | Part | Notes | Price |
|---|---|---|---|
| 1 | LM2596S DC-DC buck converter | 12V→5V for Mega + sensors; set to 5.0V before connecting | ₱49 | Lazada — Makerlab PH |

## 3. Power supply — 12V DC

### 3a. Battery bank + charging

| Qty | Part | Notes | Price |
|---|---|---|---|
| 2 | **LiFePO4 12.8V 200Ah w/ BMS 200A (PowMr)** | parallel bank, 5,120Wh; ORDER FIRST | ~₱8,900 ea = ~₱17,800 |
| 1 | **LiFePO4 charger 14.6V 20A** | recharge ≈ 10h; verify 14.6V output + LiFePO4 mode; never lead-acid | ~₱2,000–2,700 EST |

### 3b. DC power distribution

12V DC-only system: battery → 25A main fuse → DC rocker → station distribution.

| Fuse | Rating | Protects |
|---|---|---|
| Main | 25A | total DC bus |
| Station PTC | 10A ×3 | 3× PTC heaters per station (25A total, 10A fuse per heater group) |
| Station Motor | 3A ×3 | 1× worm gear motor per station |
| Station Fan | 15A ×3 | 3× BLDC fans per station (9.7A total, 15A fuse per fan bus) |
| Logic | 3A | Mega + sensors + buck |

> Wire: 14 AWG main feed (battery to distribution), 16 AWG station feed, 18 AWG motors, 20 AWG logic. All stranded copper. Fuses on the + side only (negative is common ground).

### 3c. High-current relay switching (12V DC)

Relays switch 12V DC loads directly. No SSR needed — DC switching is straightforward.

| Channel | Pin | Function | Current |
|---|---|---|---|
| 1A | D4 | PTC heaters group A (Station 1 + Station 2 heaters) | ~16.7A |
| 1B | D5 | PTC heaters group B (Station 3 heaters + spare) | ~8.3A |
| 2A | D6 | Worm motor Station 1 | ~0.8A stall |
| 2B | D7 | Worm motor Station 2 | ~0.8A stall |
| 3A | D8 | Worm motor Station 3 | ~0.8A stall |
| 3B | D9 | BLDC fan power bus (all 9 fans) | ~9.7A |

> **Relay modules:** Use 2× 2-CH relay modules (for PTC heaters and worm motors) + 1× 12V 40A automotive relay (for BLDC fan power bus). The automotive relay handles the higher fan bus current.

### 3d. BLDC fan control — ESCs

Each BLDC fan is controlled by an ESC (Electronic Speed Controller). ESCs receive PWM signals from the Mega and switch 12V DC power to the brushless motors.

| Channel | ESC Signal Pin | Function | ESC Input |
|---|---|---|---|
| ESC 1 | D10 | Station 1 BLDC fans (3 in parallel) | 12V from fan bus relay |
| ESC 2 | D11 | Station 2 BLDC fans (3 in parallel) | 12V from fan bus relay |
| ESC 3 | D12 | Station 3 BLDC fans (3 in parallel) | 12V from fan bus relay |

> **ESC wiring:** 3 wires — black (GND), red (VCC 12V), white/orange (PWM signal from Mega). ESCs must be armed on startup (write 0 for 2s, then throttle position). Use the Servo library for PWM generation.

### 3e. Safety (12V DC)

- 25A main fuse on battery positive.
- Per-station fuses: 10A (PTC heaters), 3A (motor), 15A (BLDC fans), 3A (logic).
- DS18B20 cutoff if chamber exceeds 65 °C: firmware cuts PTC relays + ESCs.
- Appliance thermal fuse on each PTC heater cluster (80 °C cutoff, non-resettable).
- DC rocker switch kills all12V loads.
- Battery BMS protects against over-discharge, over-charge, short circuit.
- No mains voltage anywhere in the system — no RCD needed.

---

## 4. Station peripherals

| Qty | Part | Notes | Price |
|---|---|---|---|
| 3 | **2-Channel 12V relay module w/ optocoupler** | 10A @ 30VDC per channel — one module per station (2 channels: PTC + motor) | ₱103 ea = ₱309 |
| 1 | **12V 40A automotive relay** | BLDC fan power bus — one relay powers all 9 fans | ~₱80 EST |
| 3 | **DC 12V BLDC fan module w/ ESC** | 50mm ducted fan, 12V, ~3.2A each — 3 fans per station wired in parallel on one ESC | ~₱470 ea = ~₱1,410 |
| 3 | **12V 100W PTC heater element** | self-regulating ceramic — 3 per station, wired in parallel | ~₱280 ea = ~₱840 |
| 1 | 16×2 I2C LCD | UI display | ₱165 |
| 1 | 5 mm LEDs — red, yellow, green | status indicators | ₱29 |
| 1 | Active buzzer 5 V | audible alert | ₱35 |
| 1 | Arcade LED push button (5 V) | start button (Circuitrocks) | ₱45 |
| 2 | DC rocker switch 12 V 10 A | labeled "DC" (battery kill) | ₱72 |
| 1 | Screw terminal 2-pin | battery in | ₱10 |
| 1 | Screw terminal 3-pin | sensor | ₱10 |

---

## 5. Motor & Drive — 3× worm stations

3× SGM-370 12V 6RPM (14 kg·cm, ~0.2A rated / ~0.8A stall, 6mm shaft, self-locking) — one per umbrella, ≥4.6× torque margin per station, per-station 3A fuse isolation. Driven by **2-CH relay modules** (channels 2A, 2B, 3A): coils from the buck 5V rail, Mega drives only the optocoupler LEDs.

Mechanical: 3× 6mm × 300mm 304 SS shafts · 6× KP08 · 3× 6×8 rigid couplings · fabricated holders.

Listings: makerlab.ph motors ×3 in one order.

---

## 6. Sensors

| Qty | Part | Notes | Price |
|---|---|---|---|
| 1 | DHT22 sensor module | Chamber humidity — one sensor, shared across all 3 stations | ₱210 |
| 1 | DS18B20 waterproof | Chamber temperature probe — mounted near PTC heaters | ₱105 |

---

## 7. UI

| Qty | Part | Notes | Price |
|---|---|---|---|
| 1 | 16×2 LCD I2C | Displays status, humidity, temperature, station states | ₱165 |
| 3 | 5mm LEDs (red, yellow, green) | Station status indicators | ₱29 |
| 1 | Active buzzer 5V | Alert on cycle complete / fault | ₱35 |
| 1 | Arcade LED push button (5V) | Start button (Circuitrocks) | ₱45 |
| 2 | DC rocker switch 12V 10A | Labeled "DC" (battery kill) | ₱72 |

---

## 8. Thermal design (12V DC)

| Item | Spec |
|---|---|
| Heat source | 9× PTC ceramic heaters, 12V 100W each = 900W total (300W per station) |
| PTC behavior | Self-regulating: resistance rises with temperature → current drops → auto-limits at set point (~200°C element temp) |
| Heating method | PTC elements radiate + convect heat into drying chamber; BLDC fans circulate warm air around umbrellas |
| Temperature target | 40–60°C chamber air (safe for nylon/polyester umbrella fabric) |
| Temperature sensing | DS18B20 waterproof probe in chamber air-path |
| Over-temperature protection | (1) DS18B20 software cutoff at 65°C → firmware cuts PTC relays + ESCs; (2) Appliance thermal fuse 80°C on each PTC cluster (non-resettable); (3) PTC self-regulation limits element temperature |
| Cooling | 3× BLDC fans per station circulate air; chamber is not sealed (vented) |

---

## 9. Capacity verification

### 9a. Mechanical — per-station torque — PASS

≤3 kg·cm per station vs 14 kg·cm → ≥4.6× margin; KP08 >90× load margin; 6 RPM gentle; self-locking hold.

### 9b. Thermal — PASS

300W per station (3× 100W PTC) with BLDC fan circulation → 40–60°C chamber; DS18B20 + thermal fuse + PTC self-regulation = triple over-temp protection.

### 9c. Electrical — 12V DC — PASS

| Subsystem | Voltage | Current | Protection |
|---|---|---|---|
| PTC heaters (9× 100W) | 12V | 75A total (25A/station) | 10A fuses per heater group |
| BLDC fans (9× 3.2A) | 12V | 28.8A total (9.7A/station) | 15A fuse per fan bus |
| Worm motors (3× 0.8A stall) | 12V | 2.4A total (0.8A/station) | 3A fuse per motor |
| Mega + sensors | 5V (buck from 12V) | ~0.5A | 3A fuse |
| **Total (all stations active)** | **12V** | **≈106A** | **25A main fuse (staged operation)** |

> **Note:** With 3A motor fuses, the motor-stall current (0.8A) is well within fuse rating. The 25A main fuse allows 1 station active (~45A) at a time. Staged operation (one station at a time) keeps total draw within the25A main fuse + battery BMS limits.

### 9d. Battery runtime — PASS

| Mode | Load | Runtime |
|---|---|---|
| Wall mode (N/A — pure battery) | — | — |
| Battery: 1 station active | ~45A (300W PTC + 9.7W fans + 0.2W motor) | 200Ah ÷ 45A ≈ 4.4h |
| Battery: all 3 stations | ~106A | 200Ah ÷ 106A ≈ 1.9h |
| Typical cycle (1 station, 30 min) | ~45A × 0.5h = 22.5Ah | 200Ah ÷ 22.5Ah ≈ **8–9 cycles per charge** |

---

## 10. Fuse plan (12V DC)

| Fuse | Rating | Location | Protects |
|---|---|---|---|
| Main | 25A | Battery positive, near battery | Total DC bus |
| PTC Station 1 | 10A | Station 1 PTC heater bus | 3× PTC heaters (25A total, 10A per group) |
| PTC Station 2 | 10A | Station 2 PTC heater bus | 3× PTC heaters |
| PTC Station 3 | 10A | Station 3 PTC heater bus | 3× PTC heaters |
| Motor Station 1 | 3A | Station 1 motor branch | 1× worm motor |
| Motor Station 2 | 3A | Station 2 motor branch | 1× worm motor |
| Motor Station 3 | 3A | Station 3 motor branch | 1× worm motor |
| Fan Bus | 15A | BLDC fan power bus | 9× BLDC fans |
| Logic | 3A | Mega + sensors + buck | Logic subsystem |

> Wire gauges: 14 AWG battery-to-distribution, 16 AWG station feeds, 18 AWG motor/fan runs, 20 AWG logic.

---

## 11. Pin assignment (Mega 2560)

| Pin | Net | Direction | Function |
|---|---|---|---|
| D2 | DHT22_DATA | in | Chamber humidity sensor (one shared) |
| D3 | DS18B20_DATA | in | Chamber temperature probe |
| D4 | RELAY_PTC_A | out | PTC heaters group A (relay module 1, ch A) |
| D5 | RELAY_PTC_B | out | PTC heaters group B (relay module 1, ch B) |
| D6 | RELAY_MOTOR_1 | out | Worm motor station 1 (relay module 2, ch A) |
| D7 | RELAY_MOTOR_2 | out | Worm motor station 2 (relay module 2, ch B) |
| D8 | RELAY_MOTOR_3 | out | Worm motor station 3 (automotive relay) |
| D9 | RELAY_FAN_BUS | out | BLDC fan power bus (automotive relay) |
| D10 | ESC_1 | out (PWM) | ESC signal — station 1 BLDC fans |
| D11 | ESC_2 | out (PWM) | ESC signal — station 2 BLDC fans |
| D12 | ESC_3 | out (PWM) | ESC signal — station 3 BLDC fans |
| D13 | BTN_START | in | Arcade push button (active LOW) |
| D14 | V_SENSE | in | Battery voltage divider (optional) |
| A4 | SDA | I2C | LCD data |
| A5 | SCL | I2C | LCD clock |

> D4/D5: active-LOW relay channels with 10 kΩ pull-ups to 5V (boot-safe OFF). D6–D9: active-LOW relay channels. D10–D12: ESC PWM signals (use Servo library for 50Hz PWM). D13: internal pull-up, active-LOW button.

---

## 12. Compatibility matrix

| Subsystem | Voltage | Margin | Pin/Channel | Status |
|---|---|---|---|---|
| Mega 2560 | 5V (buck from 12V) | 4.3× buck | LM2596S | PASS |
| DHT22 | 3.3–5V | OK direct | D2 | PASS |
| DS18B20 | 3.3–5V (parasitic or VCC) | OK direct | D3 | PASS |
| LCD I2C | 5V | direct from buck | A4/A5 | PASS |
| 2× 2-CH relay modules | 5V coil | coils from buck rail | D4–D8 | PASS |
| Automotive relay (fan bus) | 12V coil | direct from battery | D9 (via transistor) | PASS |
| PTC heaters 12V 100W | 12V | 25A main, 10A per group | D4/D5 via relays | PASS |
| BLDC fans 12V | 12V | 15A fan bus fuse | D9 (relay) + D10–D12 (ESC) | PASS |
| Worm motors 12V | 12V | ≥4.6× torque, 3A fuse | D6–D8 | PASS |
| 2× LiFePO4 200Ah | 12.8V nominal | BMS 200A ×2 | 25A main fuse | PASS |
| LM2596S | 12.8→5V | 4.3× | — | PASS |

---

## 13. BOM line-item table (Lazada + makerlab)

| Qty | Part | Spec | Price | Seller (rating) | URL / note |
|---|---|---|---|---|---|
| 9 | **PTC ceramic heater 12V 100W** (MXKJING T30 — PTC + fan + housing) | self-regulating, 12V DC, constant temp | ₱484 ea = ₱4,356 | Lazada — MXKJING T30 (LazMall) | https://www.lazada.com.ph/products/pdp-i15593670246.html |
| 9 | **BLDC fan module 12V w/ ESC** (50mm ducted, waterproof) | 50mm, ~3.2A, ESC included | ₱469 ea = ₱4,221 | Lazada — RC Waterproof Cooling Fan | https://www.lazada.com.ph/catalog/?q=50mm+BLDC+ducted+fan+12V+ESC |
| 3 | Worm gear motor SGM-370 12V 6RPM | 14 kg·cm, self-locking — one per station | ₱500 ea = ₱1,500 | makerlab.ph (site) | https://makerlab.ph/products/dc-worm-gear-motor-sgm-370-12v-16rpm |
| 3 | 304 SS shaft 6mm × 300mm | ground finish | ~₱180 ea = ~₱540 | Lazada — search "304 stainless steel rod 6mm 300mm" | https://www.lazada.com.ph/catalog/?q=304+stainless+steel+rod+6mm+300mm |
| 6 | KP08 pillow block bearing | 6mm bore insert — select KP08 + 6mm | ₱87 ea = ₱522 | Lazada | https://www.lazada.com.ph/catalog/?q=kp08+pillow+block+bearing+6mm |
| 2 | Rigid coupling set (use 6×8) | 3 needed + spare | ₱82.84 ea = ₱165.68 | (185), 408 sold | https://www.lazada.com.ph/products/pdp-i2734273953.html |
| 1 | Arduino Mega 2560 + USB cable | CH340G | ₱1,165 | Makerlab PH (98%) | https://www.lazada.com.ph/products/pdp-i5989151-s15092061710.html |
| 1 | DHT22 sensor module | humidity | ₱210 | Makerlab PH | https://www.lazada.com.ph/products/pdp-i132179919-s144637867.html |
| 1 | DS18B20 waterproof | temp probe | ₱105 | (258), 6K sold | https://www.lazada.com.ph/products/pdp-i3864018549.html |
| 1 | LCD 16×2 I2C | black on white | ₱165 | (241), 2K sold | https://www.lazada.com.ph/products/pdp-i3934869498.html |
| 6 | Single-channel relay (5V/12V, 10A, optocoupler) | PTC heater switching | ₱49 ea = ₱294 | Makerlab PH (14.6K sold) | https://www.lazada.com.ph/products/pdp-i100047427-s100061336.html |
| 1 | 12V 40A automotive relay | BLDC fan power bus, 5-pin SPDT | ~₱80 | Lazada | https://www.lazada.com.ph/catalog/?q=12v+40a+automotive+relay |
| 1 | LM2596S buck converter | 12V→5V | ₱49 | Makerlab PH (4.5K sold) | https://www.lazada.com.ph/products/pdp-i6005010-s7605914.html |
| 1 | LED 5mm red | station indicator | ₱29 | (325), 3.4K sold | https://www.lazada.com.ph/products/pdp-i2573601435.html |
| 1 | Active buzzer 5V | alarm | ₱35 | (163) | https://www.lazada.com.ph/products/pdp-i4472196293.html |
| 1 | Arcade LED push button 5V | start (Circuitrocks) | ₱45 | Circuitrocks | https://www.lazada.com.ph/products/i343850766.html |
| 2 | DC rocker switch 12V 10A | labeled "DC" | ₱72 | Unnicoco (97%) | https://www.lazada.com.ph/products/pdp-i2808878488.html |
| 1 | Dupont jumper kit 40-pin | logic hookups | ₱45 | Circuitrocks | https://www.lazada.com.ph/products/pdp-i245055558.html |
| 1 | Terminal block 15A barrier | DC distribution | ₱106 | Laguna | https://www.lazada.com.ph/products/pdp-i2818578034.html |
| 1 | Silicone wire kit 6–18AWG | 14 main, 16 station, 18 motor/fan, 20 logic | ₱218 | 6.2K sold | https://www.lazada.com.ph/products/pdp-i4880482146.html |
| 1 | Heat-shrink tube kit | insulation | ₱111 | (461), 30K sold | https://www.lazada.com.ph/products/pdp-i2569065087.html |
| 1 | 1/4W resistor kit | pull-ups, LED limiting | ₱69 | (108), 2K sold | https://www.lazada.com.ph/products/pdp-i2501387387.html |
| 1 | Nylon standoff kit | board mounting | ₱97 | (252) | https://www.lazada.com.ph/products/pdp-i2946710217.html |
| 2 | **LiFePO4 12.8V 200Ah w/ BMS 200A (PowMr)** | parallel bank, 5,120Wh — ORDER FIRST | ~₱8,900 ea = ~₱17,800 | PowMr, 4.8 (22) | https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html |
| 1 | **LiFePO4 charger 14.6V 20A** | recharge ≈ 10 h | ~₱2,000–2,700 EST | Lazada (435 rated, 4.8) | https://www.lazada.com.ph/tag/lifepo4-charger-20a/ |
| 1 | Aluminum plate 6061 6mm | motor plate + mounts | ₱760 | (52) | https://www.lazada.com.ph/products/pdp-i4449859085.html |
| 1 | Zip ties, M3/M4 screws, sealant, drip tray, velcro, grommets | consumables | ~₱490 | hardware | (any order) |
| 1 | Automotive blade fuse kit (3A, 10A, 15A, 20A, 25A) | DC fuse assortment | ~₱150 | Lazada | https://www.lazada.com.ph/catalog/?q=automotive+blade+fuse+kit+assortment |

---

## 14. Cost summary (12V DC)

| Category | Estimate |
|---|---|
| PTC heaters (9×₱484, MXKJING T30) | ≈ ₱4,356 |
| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
| Motors + shafts + bearings + couplings | ≈ ₱3,032 |
| Control electronics (Mega, sensors, LCD, relays, ESC, buck) | ≈ ₱1,653 |
| Battery bank (2× 200Ah) + 20A charger | ≈ ₱19,800–20,500 |
| UI (LEDs, buzzer, button, rockers) | ≈ ₱356 |
| Wiring, fuses, chassis, consumables | ≈ ₱1,800–2,200 |
| **TOTAL** | **≈ ₱34,900–35,600** |

| **Savings vs previous mains-based design:** ≈₱4,800–9,200 — eliminated inverter (₱5,500–8,500), mains wiring, RCD, changeover switch, ANL kit. PTC heater assemblies cost more than bare elements but include fan+housing.

---

## Appendix A — Shopping checklists

### Cart A — makerlab.ph website
- [ ] 3× Worm gear motor SGM-370 12V **6RPM** = ₱1,500

### Cart B — Lazada PH
- [ ] ⚠️ 2× PowMr 200Ah — ORDER FIRST — ₱17,800 — https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html
- [ ] LiFePO4 charger 20A — ~₱2,000–2,700 — https://www.lazada.com.ph/tag/lifepo4-charger-20a/
- [ ] 9× PTC heater CHLOCH BAG 12V 100W — ₱4,995 — https://www.lazada.com.ph/products/i2649138541.html (select 12V 100W variant!)
- [ ] 9× BLDC fan 50mm 12V w/ ESC — ₱4,221 — https://www.lazada.com.ph/catalog/?q=50mm+BLDC+ducted+fan+12V+ESC (select 50mm variant)
- [ ] Aluminum plate 6mm — ₱760 — https://www.lazada.com.ph/products/pdp-i4449859085.html
- [ ] 6× single-channel relay — ₱294 — https://www.lazada.com.ph/products/pdp-i100047427-s100061336.html
- [ ] 1× automotive relay 40A — ~₱80 — https://www.lazada.com.ph/catalog/?q=12v+40a+automotive+relay
- [ ] DHT22 — ₱210 · DS18B20 — ₱105 · LCD I2C — ₱165 · buck — ₱49 — links in §13
- [ ] LEDs — ₱29 · buzzer — ₱35 · arcade button — ₱45 · DC rocker — ₱72 — links in §2h
- [ ] 3× shaft 6×300 SS — ~₱540 — https://www.lazada.com.ph/catalog/?q=304+stainless+steel+rod+6mm+300mm
- [ ] 6× KP08 pillow block 6mm bore — ₱522 — https://www.lazada.com.ph/catalog/?q=kp08+pillow+block+bearing+6mm
- [ ] Silicone wire — ₱218 · dupont — ₱45 · terminal block — ₱106 · heat-shrink — ₱111 · resistors — ₱69 · standoffs — ₱97 — links in §2i
- [ ] Automotive fuse kit — ~₱150 — https://www.lazada.com.ph/catalog/?q=automotive+blade+fuse+kit+assortment

### Cart C — hardware
- [ ] Zip ties, M3/M4 screws, sealant, drip tray, velcro, grommets — ~₱490

### Variant picking (at checkout — exact SKUs matter)
| Item | Pick this |
|---|---|
| DHT22 | Makerlab PH module (₱210) |
| Pillow blocks | KP08 with 6mm bore insert |
| Steel shaft | 6mm × 300mm |
| PTC heater | 12V 100W MXKJING T30 (verify 12V variant, NOT 220V) |
| BLDC fan | 50mm ducted fan with ESC, 12V (verify ESC included) |
| Automotive relay | 12V 40A, 5-pin SPDT |
| Relay modules | 2-CH 10A optocoupler (active-LOW) |

### Sign-off checklist (before ordering)
- [ ] DHT22 Black / KP08 6mm bore / 6×300 SS variants picked
- [ ] PTC heaters verified as 12V MXKJING T30 (not 220V)
- [ ] BLDC fans include ESC (not bare motor only)
- [ ] Battery pre-order confirmed, ordered first
- [ ] Prices re-verified at checkout

---

## Rev-7 order notes

1. **Design:** 12V DC-only system. No mains voltage, no inverter, no RCD. Simpler, safer, cheaper.
2. **Heating:** 9× PTC ceramic heaters (12V 100W) — 3 per station, self-regulating. No SSR needed — relays switch 12V DC directly.
3. **Fans:** 9× BLDC ducted fan modules with ESC — 3 per station. ESCs receive PWM from Mega (Servo library, 50Hz). One automotive relay powers all fans (fan bus).
4. **Motors:** 3× SGM-370 worm gear (14 kg·cm, 6 RPM) — one per umbrella, self-locking. Relays switch 12V DC.
5. **Battery:** 2× 200Ah LiFePO4 in parallel (5,120Wh). Typical cycle: 1 station, 30 min → 22.5Ah per cycle → 8–9 cycles per charge.
6. **Fuse plan:** 25A main, 10A per PTC group, 3A per motor, 15A per fan bus, 3A logic.
7. **Safety:** DS18B20 cutoff + thermal fuse + PTC self-regulation. No mains = no electrocution risk.
