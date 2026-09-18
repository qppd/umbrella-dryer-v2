# Umbrella Dryer V2 — Bill of Materials

| Design: | 12V DC-only system. Each umbrella station has 3× PTC heaters (100W each), 3× AVC 12V 4.5A blowers (PWM-controlled directly from Mega), and 1× worm gear motor. Battery-powered with **1× 200Ah LiFePO4**. **DC-output SSR-40DD** control PTC heaters (direct-drive from Mega), **LCTC DC-DC SSR 10A** controls worm motors (replaces optocoupler module), **Mega PWM** controls AVC blowers.

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
| 1 | **LiFePO4 charger 14.6V 20A** | VariCore alligator clip; CC/CV; LED indicator; never lead-acid | ~₱2,809 |

### 3b. DC power distribution

| From | To | Wire | Protection |
|---|---|---|---|
| Battery + | 50A DC Rocker Switch | 8 AWG | Manual disconnect |
| Rocker Switch + | 2-pin screw terminal (battery in) | 8 AWG | — |
| Battery − | 12V Negative Ground Bus Bar | 8 AWG | — |

> **No fuses, no ANL breakers.** Main power controlled by 50A DC rocker switch. Emergency kill = flip rocker OFF + unplug battery cable.

> **Wire:** 8 AWG battery main, 10 AWG heater/fan branches, 18 AWG motor, 20 AWG logic, 22 AWG signals. All stranded copper. No fuses. Main power disconnected via 50A DC rocker switch.

### 3c. High-current switching (12V DC)

| Channel | Pin | SSR type | Load | Current | Active level |
|---|---|---|---|---|---|
| PTC Station 1 | D4 | LCTC DC-DC SSR 40A (DC output) | 3× PTC heaters | ~25A | HIGH = ON |
| Motor Station 1 | D5 | LCTC DC-DC SSR 10A (DC output) | SGM-370 | ~0.8A | HIGH = ON |
| PTC Station 2 | D6 | LCTC DC-DC SSR 40A (DC output) | 3× PTC heaters | ~25A | HIGH = ON |
| Motor Station 2 | D7 | LCTC DC-DC SSR 10A (DC output) | SGM-370 | ~0.8A | HIGH = ON |
| PTC Station 3 | D8 | LCTC DC-DC SSR 40A (DC output) | 3× PTC heaters | ~25A | HIGH = ON |
| Motor Station 3 | D9 | LCTC DC-DC SSR 10A (DC output) | SGM-370 | ~0.8A | HIGH = ON |
| Fan bus | D13 | LCTC DC-DC SSR 40A (DC output) | 9× AVC blowers | ~40.5A | HIGH = ON |

> **SSR direct drive:** All LCTC DC-DC SSR inputs connect directly to Mega pins. SSR input draws ≈10–20 mA at 5V — fine for direct drive. No additional components needed. Each SSR requires a heatsink (40A version: ~25W dissipation at 25A; fan bus at 40.5A: ~40W dissipation). Motor SSRs (10A): minimal dissipation at 0.8A.

### 3d. Fan PWM control — AVC blowers

| Channel | Pin | Function | Load | Speed control |
|---|---|---|---|---|
| Fans Station 1 | D10 | PWM signal | 3× AVC blowers (parallel) | `analogWrite(D10, val)` 0–255 |
| Fans Station 2 | D11 | PWM signal | 3× AVC blowers (parallel) | `analogWrite(D11, val)` 0–255 |
| Fans Station 3 | D12 | PWM signal | 3× AVC blowers (parallel) | `analogWrite(D12, val)` 0–255 |

> AVC blowers accept PWM duty cycle directly from Mega pins (5V logic). No ESC needed. Full speed = analogWrite(D, 255). Each blower draws 4.5A at full speed.

### 3e. Safety (12V DC)

- No fuses in the circuit
- DS18B20 cutoff if chamber exceeds 65 °C: firmware cuts all SSRs + blower PWM
- PTC self-regulation: resistance rises with temperature, auto-limits
- Battery BMS protects against over-discharge, over-charge, short circuit
- No mains voltage anywhere — no RCD needed

---

## 4. Station peripherals

| Qty | Part | Notes | Price |
|---|---|---|---|
| 4 | Solid State Relay taxnele 40A (DC-DC) | SSR-40DD (3-32VDC input, 5-60VDC output); 3× PTC + 1× fan bus; direct-drive from Mega | ₱956.68 |
| 3 | Solid State Relay taxnele 10A (DC-DC) | SSR-10DD (3-32VDC input, 5-60VDC output); motor control | ₱654.66 |
| 4 | SSR Heatsink BLACK (80×50×50mm) | One per 40A SSR | ₱440 |
| 9 | AVC 12V DC blower fan | Super High Speed Blower, 80×80×38mm, PWM control, 4.5A each | ₱2,970 |
| 9 | 12V 100W PTC heater element (MXKJING T30) | Self-regulating ceramic — 3 per station | ₱4,356 |
| 1 | Screw terminal 2-pin | Battery in | ₱10 |
| 1 | Screw terminal 3-pin | Sensor | ₱10 |

---

## 5. Motor & Drive — 3× worm stations

3× SGM-370 12V 6RPM (14 kg·cm, ~0.2A rated / ~0.8A stall, 6mm output shaft, self-locking) — one per umbrella.

Mechanical (per station): **SGM-370 DC worm gear motor → rigid coupling (6×8mm) → 6mm × 300mm SS shaft → UCP06 pillow block (shaft passes through the bearing's middle) → PETIYOUZA rigid flange coupling (6mm bore) → umbrella hub.** Motor and pillow block bolted to the 6mm aluminum plate mount.

---

## 6. Thermal design (12V DC)

| Item | Spec |
|---|---|
| Heat source | 9× PTC ceramic heaters, 12V 100W each = 900W total (300W per station) |
| PTC behavior | Self-regulating: resistance rises with temperature → current drops → auto-limits |
| Heating method | PTC elements radiate + convect heat; AVC blowers circulate warm air |
| Temperature target | 40–60°C chamber air |
| Temperature sensing | DHT22 (humidity) mid-chamber + DS18B20 (temp) in heater airstream |
| Over-temperature | (1) DS18B20 firmware cutoff at 65°C (2) PTC self-regulation |
| Cooling | 3× AVC blowers per station; chamber is vented |

---

## 7. Capacity verification

### 7a. Mechanical — per-station torque — PASS
≤3 kg·cm per station vs 14 kg·cm → ≥4.6× margin; drivetrain: motor → rigid coupling → shaft through UCP06 pillow block → flange coupling to hub; 6 RPM gentle; self-locking hold.

### 7b. Thermal — PASS
300W per station with AVC blower circulation → 40–60°C chamber; DS18B20 + PTC self-regulation = dual over-temp protection.

### 7c. Electrical — 12V DC — PASS

| Subsystem | Voltage | Current (one station) | Protection |
|---|---|---|---|
| PTC heaters (3× 100W) | 12V | 25A | BMS 200A + PTC self-regulation |
| AVC blowers (3× 4.5A) | 12V | 13.5A | BMS 200A |
| Worm motor | 12V | 0.8A | BMS 200A |
| Mega + sensors | 5V | 0.1A | BMS 200A |
| **Total (one station)** | | **~39.3A** | **BMS 200A** |

### 7d. Battery runtime — 1× 200Ah LiFePO4

> **Usable capacity ≠ nameplate.** LiFePO4 should be cycled at 80% DoD for rated cycle
> life, and the battery should still meet spec at 90% capacity (end-of-life margin):
> **usable = 200 Ah × 0.80 × 0.90 ≈ 144 Ah** (≈ 1.73 kWh at 12V).

Load profile (staged, one station at a time):

| Phase | Draw | Notes |
|---|---|---|
| PREHEAT / DRY (active station) | ~39.3A | 3 PTC (25A) + 3 blowers (13.5A) + motor (0.8A) + logic (0.5A) |
| COOL | ~14A | Blowers (13.5A) + logic (0.5A) |
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
| Continuous staged operation | ≈ **3.7 hours** (144 Ah ÷ 39.3A) |
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
| D10 | PWM_FAN_1 | out (PWM) | Blower PWM — station 1 AVC blowers | — |
| D11 | PWM_FAN_2 | out (PWM) | Blower PWM — station 2 AVC blowers | — |
| D12 | PWM_FAN_3 | out (PWM) | Blower PWM — station 3 AVC blowers | — |
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
| 9 | **AVC 12V DC blower fan** | Super High Speed Blower, 80×80×38mm, PWM control, 4.5A | ₱330 ea = ₱2,970 | Lazada | https://www.lazada.com.ph/products/pdp-i2328323489.html |
| 3 | Worm gear motor SGM-370 | 12V 6RPM 14 kg·cm | ₱500 ea = ₱1,500 | makerlab.ph | https://makerlab.ph/products/dc-worm-gear-motor-sgm-370-12v-16rpm |
| 4 | Solid State Relay taxnele 40A (DC-DC) | SSR-40DD (3-32VDC input, 5-60VDC output) | ₱239.17 ea = ₱956.68 | Lazada | https://www.lazada.com.ph/products/pdp-i4110347574-s22718212255.html |
| 4 | SSR Heatsink BLACK (Makerlab) | BLACK 10A to 40A (Size: 80x50x50mm) | ₱110 ea = ₱440 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/ssr-heatsink-black-10a-to-40a-size80x50x50mm-ssr-heatsink-m-shape-small-type-heat-radiator-for-10a-to100a-size125x50x70mm-i3585835660-s18544712824.html |
| 3 | Solid State Relay taxnele 10A (DC-DC) | SSR-10DD (3-32VDC input, 5-60VDC output) | ₱218.22 ea = ₱654.66 | Lazada | https://www.lazada.com.ph/products/pdp-i4110347574-s22718212255.html |
| 1 | LM2596S Buck Converter (w/ display) | 12V→5V with 7-segment voltmeter display | ₱155 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/pdp-i127879071-s137114729.html |
| 1 | **Arduino Mega 2560 + Terminal Board** | CH340G + screw terminal board | ₱413 | Lazada | https://www.lazada.com.ph/products/mega-2560-16au-ch340g-based-on-arduino-arduino-mega-2560-terminal-board-i123143829-s20504057319.html |
| 1 | **DHT22 sensor module** | humidity + temp, 3-pin | ₱220 | Lazada | https://www.lazada.com.ph/products/pdp-i132179919.html |
| 1 | **DS18B20 temperature sensor module** | LEOOYI, 3-pin cable + pluggable terminal adapter | ₱141 | Lazada | https://www.lazada.com.ph/products/pdp-i4398946755-s24721782197.html |
| 1 | LCD 16×2 I2C | display | ₱165 | Lazada | https://www.lazada.com.ph/products/1602-16x2-character-lcd-module-display-hd44780-with-i2c-i104139284-s1630402476.html |
| 1 | **DC Rocker Switch 50A 12V** | Main power disconnect (heavy duty toggle) | ~₱190 | Lazada | https://www.lazada.com.ph/catalog/?q=50A+12V+DC+heavy+duty+toggle+switch |
| 3 | **PETIYOUZA Rigid Flange Coupling 6mm** | 6mm bore — shaft end → umbrella hub | ~₱107 ea = ~₱321 | Lazada | https://www.lazada.com.ph/products/petiyouza-coupler-hardware-power-transmission-parts-r11-rigid-flange-coupling-iron-motor-guide-shaft-diy-metal-coupling-i4018785636-s21726441085.html |
| 3 | Rigid shaft coupling 6×8mm | motor output shaft → shaft | ₱82.84 ea (pack of 3) = ₱249 | Lazada | https://www.lazada.com.ph/products/pdp-i245055558.html |
| 3 | 304 SS shaft 6mm × 300mm | shaft — passes through the UCP06 pillow block middle | ~₱180 ea = ~₱540 | Lazada | https://www.lazada.com.ph/catalog/?q=304+stainless+steel+rod+6mm+300mm |
| 3 | **UCP06 pillow block bearing (6mm bore)** | holds the shaft mid-span, absorbs radial load | ₱87 ea = ₱522 | Lazada | https://www.lazada.com.ph/catalog/?q=ucp06+pillow+block+bearing+6mm |
| 1 | LED 5mm (R/Y/G) | status | ₱29 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/5mm-led-diode-assorted-colors-i144137387-s166391718.html |
| 1 | Active buzzer 5V | alarm | ₱35 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/active-alarm-buzzer-driver-module-high-current-blue-i3474748260-s17874906532.html |
| 1 | Arcade LED push button 5V | start | ₱45 | Circuitrocks | https://www.lazada.com.ph/products/i343850766.html |
| 1 | Silicone wire kit 6–18AWG | gauges | ₱218 | Lazada | https://www.lazada.com.ph/products/pdp-i4880482146.html |
| 2 | **Model 1007 Tinned Copper Wire Kit** (COLOR 01 + COLOR 02) | 18/20/22/24 AWG, 5-color spool — logic + signal wiring | ₱385 ea = ₱770 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/model-1007-18awg-20awg-22-awg-24awg-tinned-copper-wire-5-color-spool-i3154761672-s17328234744.html |
| 1 | **Terminal block 15A barrier 6-pole** | 5V rail distribution (buck out → Mega/DHT22/DS18B20/LCD/button) | ~₱132 | Lazada | https://www.lazada.com.ph/products/terminal-block-15a-25a-45a-60a-80a-100a-600v-barrier-3-poles-to-12-poles-vat-included-prices-i2818578034.html |
| 2 | 10-Terminal Bus Bar 150A (Copper) | Main 12V (+ & -) bus rails | ~₱120 ea = ₱240 | Lazada | https://www.lazada.com.ph/products/814-terminal-bus-bar-150a-high-current-dc-busbar-12-48v-copper-power-distribution-terminal-block-for-car-boat-i5119401028-s30216194181.html |
| 1 | Heat-shrink tube kit | insulation | ₱111 | Lazada | https://www.lazada.com.ph/products/pdp-i2569065087.html |
| 1 | **1/4W 1% Metal Film Resistor Kit** 600pcs | 47Ω/220Ω/1K/10K/47K/68K/100K/220K/1M (20ea each) | ₱220 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/14w-resistance-1-metal-film-resistor-assorted-kit-each-20-total-600pcs-47-ohms-220-1k-10k-47k-68k-100k-220k-1m-i118492390-s122930341.html |
| 1 | **Nylon Standoff Kit M3/M2.5** | M3x6+6mm×30 + M3x10+6mm×20 + M2.5x6+6mm×20 — covers Mega, LCD, SSR mounts | ₱97 | Lazada | https://www.lazada.com.ph/products/pdp-i2946710217.html |
| 1 | Aluminum plate 6061 6mm | motor plate + mounts | ₱760 | Lazada | https://www.lazada.com.ph/products/pdp-i4449859085.html |
| 1 | LiFePO4 12.8V 200Ah w/ BMS 200A | battery | ~₱8,900 | Lazada (PowMr) | https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html |
| 1 | **VariCore 14.6V 20A Smart LiFePO4 Charger** | Alligator clip variant; CC/CV; LED red/green; 110-240V input | ~₱2,809 | Lazada | https://www.lazada.com.ph/products/varicore-146v-20a-smart-lifepo4-battery-charger-110-220v-4s-12v-high-power-charger-for-lithium-iron-phosphate-i5375251271-s32167681050.html |
| 1 | **Zip ties 100pcs nylon UV-resistant** | Heavy duty, 3-tooth buckle — wire bundling | ~₱84 | Lazada | https://www.lazada.com.ph/products/100pcs-heavy-duty-nylon-cable-zip-ties-uv-resistant-multipurpose-i4164586303.html |
| 1 | **Screws M3/M4/M5 stainless 320pcs kit** | M3 8/12/16mm + M4 + washers/nuts — Mega, plate, chamber mounts | ~₱298 | Lazada | https://www.lazada.com.ph/products/320pcs-380pcs-stainless-steel-screws-bolts-nuts-kit-m3-m4-m5-hex-socket-fasteners-assortment-set-anti-loosening-washers-gaskets-diy-home-furniture-auto-repair-hardware-tool-cod-ready-stock-ph-i15532367775.html |
| 1 | **PROSEAL silicone sealant (clear)** | 100% RTV, waterproof, weather-resistant — seam sealing | ~₱199 | Lazada | https://www.lazada.com.ph/products/proseal-silicone-sealant-clear-white-black-brown-i4013402307.html |
| 1 | **Rubber grommets 180pcs (8 sizes)** | Wire passthrough / chamber wall penetrations | ~₱249 | Lazada | https://www.lazada.com.ph/products/same-day-shipping-180pcs-rubber-grommet-assortment-contain-8-popular-sizes-gasket-firewall-hole-plug-set-electrical-wire-gasket-kit-for-car-high-quality-cyb-rubber-grommet-i3692147637.html |
| 1 | Zip ties, screws, sealant, grommets | consumables — hardware-store bulk alternative to the 4 online items above | ~₱490 | hardware | — |

---

## 10. Cost summary

| Category | Estimate |
|---|---|
| PTC heaters (9×₱484) | ≈ ₱4,356 |
| AVC blowers (9×₱330) | ≈ ₱2,970 |
| Motors + drivetrain + mounts (3× SGM-370, couplings 6×8mm, 3× shafts, 3× UCP06 pillow blocks, 3× PETIYOUZA flange, 6mm aluminum plate) | ≈ ₱3,892 |
| taxnele SSR 40A (4×₱239) + SSR 10A (3×₱218) + SSR Heatsink BLACK (4×₱110) | ≈ ₱2,051 |
| Control electronics (Mega w/ terminal board ₱413, DHT22 ₱220, DS18B20 ₱141, LCD ₱165, LM2596S ₱155, resistor kit ₱220) | ≈ ₱1,314 |
| Battery (1× 200Ah) + charger | ≈ ₱11,700–12,200 |
| UI (LEDs, buzzer, button) | ≈ ₱109 |
| Wiring, connectors, consumables | ≈ ₱2,400 |
| DC Rocker Switch 50A | ~₱190 |
| **TOTAL** | **≈ ₱29,000** (₱28,700–29,300 with price swings) |
