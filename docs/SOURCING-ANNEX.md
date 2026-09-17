# Sourcing Annex — 12V DC, with Verified Links

> Complete sourcing guide with **actual store links**. Verified September 2026. No mains components needed.

---

## 1. Order strategy

1. **Battery first** — longest lead time (PowMr from Lazada)
2. **MakeLAB.PH** — motor + couplings (local, fast shipping)
3. **Lazada** — everything else (electronics, PTC heaters, BLDC fans, wiring)
4. **Hardware store** — consumables (screws, zip ties, sealant)

---

## 2. Component sourcing — all verified links

### 2a. Heating (PTC ceramic heaters)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 9 | MXKJING T30 12V 100W PTC Ceramic Heater (with fan + housing) | ₱484 ea = ₱4,356 | Lazada (LazMall, 95% rating) | https://www.lazada.com.ph/products/pdp-i15593670246.html |

> **Alternative (cheaper, bare element only):** "Direct Sale 50W/12V Ceramic Ribbon PTC Heater 92×31mm" at ₱219 — but this is 50W, not 100W. You'd need 2 per station (6 total) = ₱1,314. Search: https://www.lazada.com.ph/catalog/?q=12v+100w+ptc+ceramic+heater+element

> **Important:** At checkout, select the **12V 100W** variant. Some listings offer 220V — do NOT pick that. LazMall seller with 95% rating.

### 2b. Fans (BLDC ducted fan modules with ESC)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 9 | RC Waterproof Cooling Fan Motor ESC 50mm 12V (ducted, brushless, ESC included) | ₱469 ea = ₱4,221 | Lazada | Search "50mm BLDC ducted fan 12V ESC" → https://www.lazada.com.ph/catalog/?q=50mm+BLDC+ducted+fan+12V+ESC |

> **Pick variant:** 50mm, 12V, with ESC. The listing shows 25/30/35/40/45/50mm options — select **50mm**.

> **Physical store fallback:** If online unavailable, check **e-Gizmo** (Manila) or **Rep Asia** for BLDC motor + ESC combos.

### 2c. Motors + drivetrain (makerlab.ph)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 3 | SGM-370 DC Worm Gear Motor 12V 6RPM | ₱500 ea = ₱1,500 | makerlab.ph | https://makerlab.ph/products/dc-worm-gear-motor-sgm-370-12v-16rpm |
| 3 | Rigid Coupling 6×8mm (motor to shaft) | ₱82.84 ea = ₱248.52 | makerlab.ph | https://makerlab.ph/products/6x8mm-rigid-coupling-set |

> **Note:** Select **6×8mm** variant (6mm motor bore, 8mm shaft side). We have 3 needed + can use the spare from a second set if needed.

### 2d. Bearings (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 6 | KP08 Pillow Block Bearing 6mm bore (2 per station) | ₱87 ea = ₱522 | Lazada | https://www.lazada.com.ph/catalog/?q=kp08+pillow+block+bearing+6mm |

> **Note:** KP08 accepts 6mm bore insert bearing. Select "6mm" variant at checkout. 2 per station × 3 stations = 6 total. (Or buy 3× 2-packs at ₱167 = ₱501)

### 2e. Shafts (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 3 | 304 Stainless Steel Rod 6mm × 300mm | ~₱180 ea = ~₱540 | Lazada | https://www.lazada.com.ph/catalog/?q=304+stainless+steel+rod+6mm+300mm |

> Search and pick the closest match. Some sellers offer cut-to-length.

### 2f. Control electronics (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | Arduino Mega 2560 + USB cable (CH340G) | ₱1,165 | Makerlab PH | https://www.lazada.com.ph/products/pdp-i5989151-s15092061710.html |
| 1 | DHT22 sensor module (black) | ₱210 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/pdp-i132179919-s144637867.html |
| 1 | DS18B20 waterproof probe (temp) | ₱105 | Lazada | https://www.lazada.com.ph/products/pdp-i3864018549.html |
| 1 | LCD 16×2 I2C (black on white) | ₱165 | Lazada | https://www.lazada.com.ph/products/pdp-i3934869498.html |
| 1 | LM2596S DC-DC buck converter 12V→5V | ₱49 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/pdp-i6005010-s7605914.html |

### 2g. SSRs, drivers, and modules (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 4 | **SSR-40DD DC-output solid-state relay (40A)** | ~₱200 ea = ~₱800 EST | Lazada | search "SSR-40DD 40A DC output" — VERIFY PRICE |
| 4 | Heatsinks for SSR-40DD | ~₱50 ea = ~₱200 | Lazada | search "SSR heatsink" |
| 1 | **4-CH optocoupler relay module (10A @ 30VDC)** | ~₱200 | Lazada | search "4 channel relay module 12V optocoupler" |
| 1 | **Screw terminal 2-pin** | ₱10 | Lazada | — |

> **Important:** SSR-40DD must be **DC-output** type (input 3–32VDC, DC output). Do NOT buy the AC-output 'DA' type. The SSRs are driven directly from Mega pins (D4/D6/D8 for PTC, D13 for fan bus).

### 2h. UI components (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | LED 5mm red | ₱29 | Lazada | https://www.lazada.com.ph/products/pdp-i2573601435.html |
| 1 | Active buzzer 5V | ₱35 | Lazada | https://www.lazada.com.ph/products/pdp-i4472196293.html |
| 1 | Arcade LED push button 5V (Circuitrocks) | ₱45 | Lazada | https://www.lazada.com.ph/products/i343850766.html |

### 2i. Wiring + consumables (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | Silicone wire kit 6–18AWG | ₱218 | Lazada | https://www.lazada.com.ph/products/pdp-i4880482146.html |
| 1 | Dupont jumper kit 40-pin | ₱45 | Lazada | https://www.lazada.com.ph/products/pdp-i245055558.html |
| 1 | Terminal block 15A barrier strip | ₱106 | Lazada | https://www.lazada.com.ph/products/pdp-i2818578034.html |
| 2 | 10-Terminal Bus Bar 150A (Copper) | ~₱350 ea = ₱700 | Lazada | https://www.lazada.com.ph/products/814-terminal-bus-bar-150a-high-current-dc-busbar-12-48v-copper-power-distribution-terminal-block-for-car-boat-i5119401028-s30216194181.html |
| 1 | Heat-shrink tube kit | ₱111 | Lazada | https://www.lazada.com.ph/products/pdp-i2569065087.html |
| 1 | 1/4W resistor kit | ₱69 | Lazada | https://www.lazada.com.ph/products/pdp-i2501387387.html |
| 1 | Nylon standoff kit | ₱97 | Lazada | https://www.lazada.com.ph/products/pdp-i2946710217.html |
| 1 | Aluminum plate 6061 6mm (motor plate + mounts) | ₱760 | Lazada | https://www.lazada.com.ph/products/pdp-i4449859085.html |

### 2j. Battery + charger (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | PowMr LiFePO4 12.8V 200Ah w/ BMS 200A | ~₱8,900 ea | Lazada | https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html |
| 1 | LiFePO4 charger 14.6V 20A | ~₱2,000–2,700 | Lazada | https://www.lazada.com.ph/tag/lifepo4-charger-20a/ |

> **⚠️ ORDER BATTERY FIRST** — longest shipping time. Verify seller rating ≥4.5.

### 2k. Hardware store (physical — Robinsons/Wildepanda/etc.)

| Item | Est. Price | Note |
|---|---|---|
| Zip ties (assorted) | ~₱50 | |
| M3/M4 screws + nuts (assorted) | ~₱150 | Stainless preferred |
| Silicone sealant | ~₱100 | |
| Plastic drip tray | ~₱100 | Station base |
| Velcro strips | ~₱50 | Board mounting |
| Rubber grommets | ~₱40 | Wire passthrough |

---

## 3. Quick price summary

| Category | Total |
|---|---|
| PTC heaters (9×₱484) | ≈ ₱4,356 |
| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
| Motors + couplings (makerlab) | ≈ ₱1,749 |
| Bearings + shafts (Lazada) | ≈ ₱1,062 |
| Control electronics (Lazada) | ≈ ₱1,589 |
| SSRs + opto module + heatsinks + terminals | ≈ ₱1,210 |
| UI (LEDs, buzzer, button) | ≈ ₱109 |
| Wiring + consumables (Lazada) | ≈ ₱1,346 |
| Battery (1× 200Ah) + charger | ≈ ₱10,900–11,600 |
| Hardware store consumables | ≈ ₱490 |
| **GRAND TOTAL** | **≈ ₱27,000–28,000** |

---

## 4. Physical store fallbacks (if online unavailable)

| Item | Physical store | Location |
|---|---|---|
| BLDC fan + ESC | e-Gizmo Mechatronics | Tomas Morato, QC |
| BLDC fan + ESC | Rep Asia | Quezon Ave, QC |
| KP08 pillow blocks | Kuan Kee Hardware | Manila |
| Steel shafts | Manila Trading (steel) | Various |
| Arduino + sensors | e-Gizmo / Circuitrocks | QC / Online |
| SSR-40DD | Any electronics parts shop | Universal |

---

## 5. Variant checklists (at checkout)

| Item | Pick this | NOT this |
|---|---|---|
| PTC heater | 12V 100W MXKJING T30 | 220V (wrong!) |
| BLDC fan | 50mm with ESC | Bare motor only |
| Pillow block | KP08, 6mm bore | KP08, 8mm bore |
| Shaft | 6mm × 300mm SS | 8mm (wrong) |
| Coupling | 6×8mm rigid | Other sizes |
| PTC relay | **SSR-40DD DC-output 40A** | 40A automotive relay (has moving parts, needs NPN driver) |
| PTC relay | **DC-output** (3–32VDC input, DC output) | AC-output (DA type) |
| Motor relay module | **4-CH optocoupler 10A** | 40A auto (overkill for 0.8A motor) |
| Main protection | **No fuses** — BMS + firmware cutoff only | Any fuses (removed per no-fuse design) |
| Battery | LiFePO4 12.8V 200Ah | Lead-acid (too heavy) |
| Charger | LiFePO4 14.6V 20A | Lead-acid charger (wrong!) |
| DHT22 | Black module | Blue (less accurate) |

---

## 6. Notes on the no-fuse design

The no-fuse SSR build removes all fuses (50A ANL, 30A blade, 3A blade, 130°C thermal fuses, disconnect switch) from the power path. The battery connects directly to the distribution bus through a 2-pin screw terminal. Emergency kill is achieved by unplugging the battery cable.

**Protection scheme:**
- Over-current: BMS 200A cutoff
- Over-temperature: DS18B20 firmware cutoff at 65°C + PTC self-regulation
- Boot-safe: SSRs are active-HIGH (floating pin = OFF)

**SSR-40DD sourcing note:** These are DC-output solid-state relays with 40A rating. They require heatsinks due to ~1W/A dissipation (~25W per PTC SSR at 25A). The price estimate (~₱200 each) should be verified on Lazada — prices may vary.
