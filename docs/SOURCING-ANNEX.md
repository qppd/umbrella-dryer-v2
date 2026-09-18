# Sourcing Annex — 12V DC, with Verified Links

> Complete sourcing guide with **actual store links**. Verified September 2026. No mains components needed.

---

## 1. Order strategy

1. **Battery first** — longest lead time (PowMr from Lazada)
2. **50A DC rocker switch** — main power disconnect, order with battery
3. **MakeLAB.PH** — motor + couplings (local, fast shipping)
3. **Lazada** — everything else (electronics, PTC heaters, blowers, wiring)
4. **Hardware store** — consumables (screws, zip ties, sealant)

---

## 2. Component sourcing — all verified links

### 2a. Heating (PTC ceramic heaters)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 9 | MXKJING T30 12V 100W PTC Ceramic Heater (with fan + housing) | ₱484 ea = ₱4,356 | Lazada (LazMall, 95% rating) | https://www.lazada.com.ph/products/pdp-i15593670246.html |

> **Alternative (cheaper, bare element only):** "Direct Sale 50W/12V Ceramic Ribbon PTC Heater 92×31mm" at ₱219 — but this is 50W, not 100W. You'd need 2 per station (6 total) = ₱1,314. Search: https://www.lazada.com.ph/catalog/?q=12v+100w+ptc+ceramic+heater+element

> **Important:** At checkout, select the **12V 100W** variant. Some listings offer 220V — do NOT pick that. LazMall seller with 95% rating.

### 2b. Main Power Disconnect

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | **50A 12V DC Heavy Duty Toggle Switch** | ~₱190 | Lazada | https://www.lazada.com.ph/catalog/?q=50A+12V+DC+heavy+duty+toggle+switch |

> **Purpose:** Manual main power disconnect. Installed between battery + and positive bus bar. Flip OFF to completely isolate battery from all loads.
> **Mounting:** Panel-mount, 2-pin SPST. Wire 8 AWG through switch.

### 2c. Fans (AVC blowers)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 9 | AVC Super High Speed Blower DC 12V 4.5A, 80×80×38mm | ₱330 ea = ₱2,970 | Lazada | https://www.lazada.com.ph/products/pdp-i2328323489.html |

> **Pick variant:** 12V 4.5A, 80mm. PWM-controlled directly from Mega. No ESC needed.
> **Physical store fallback:** If online unavailable, check **e-Gizmo** (Manila) or **Rep Asia** for similar blower fans.

### 2d. Motors + drivetrain (makerlab.ph)

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
| 1 | Arduino Mega 2560 + Terminal Board (CH340G) | ₱413 | Lazada | https://www.lazada.com.ph/products/mega-2560-16au-ch340g-based-on-arduino-arduino-mega-2560-terminal-board-i123143829-s20504057319.html |
| 1 | DHT22 sensor module | ₱220 | Lazada | https://www.lazada.com.ph/products/pdp-i132179919.html |
| 1 | DS18B20 temperature sensor module + terminal adapter + 3-pin cable (LEOOYI) | ₱141 | Lazada | https://www.lazada.com.ph/products/pdp-i4398946755-s24721782197.html |
| 1 | LCD 16×2 I2C (black on white) | ₱165 | Lazada | https://www.lazada.com.ph/products/1602-16x2-character-lcd-module-display-hd44780-with-i2c-i104139284-s1630402476.html |
| 1 | LM2596S DC-DC buck converter with 7-segment display | ₱155 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/pdp-i127879071-s137114729.html |

### 2g. SSRs, drivers, and modules (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 4 | **Solid State Relay taxnele 40A (DC-DC)** — SSR-40DD | ₱239.17 ea = ₱956.68 | Lazada (taxnele) | https://www.lazada.com.ph/products/pdp-i4110347574-s22718212255.html |
| 3 | **Solid State Relay taxnele 10A (DC-DC)** — SSR-10DD | ₱218.22 ea = ₱654.66 | Lazada (taxnele) | https://www.lazada.com.ph/products/pdp-i4110347574-s22718212255.html |
| 4 | **SSR Heatsink BLACK (Makerlab)** — 10A to 40A (80x50x50mm) | ₱110 ea = ₱440 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/ssr-heatsink-black-10a-to-40a-size80x50x50mm-ssr-heatsink-m-shape-small-type-heat-radiator-for-10a-to100a-size125x50x70mm-i3585835660-s18544712824.html |

> **Important:** SSR-40DD must be **DC-output** type (input 3–32VDC, DC output). Do NOT buy the AC-output 'DA' type. The SSRs are driven directly from Mega pins (D4/D6/D8 for PTC, D13 for fan bus).
> **Heatsink requirement:** 40A SSR at 25A draws ~25W dissipation. 40A SSR at fan bus (40.5A) draws ~40W — use larger heatsink or ensure good airflow.

### 2h. UI components (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | LED 5mm red | ₱29 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/5mm-led-diode-assorted-colors-i144137387-s166391718.html |
| 1 | Active buzzer 5V | ₱35 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/active-alarm-buzzer-driver-module-high-current-blue-i3474748260-s17874906532.html |
| 1 | Arcade LED push button 5V (Circuitrocks) | ₱45 | Lazada | https://www.lazada.com.ph/products/i343850766.html |

### 2i. Wiring + consumables (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | Silicone wire kit 6–18AWG | ₱218 | Lazada | https://www.lazada.com.ph/products/pdp-i4880482146.html |
| 2 | **Model 1007 Tinned Copper Wire Kit** (COLOR 01 + COLOR 02) | 18/20/22/24 AWG wire, 5-color spool | ₱385 ea = ₱770 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/model-1007-18awg-20awg-22-awg-24awg-tinned-copper-wire-5-color-spool-i3154761672-s17328234744.html |
| 1 | Terminal block 15A barrier (6-pole) | 5V rail distribution | ₱132 | Lazada | https://www.lazada.com.ph/products/terminal-block-15a-25a-45a-60a-80a-100a-600v-barrier-3-poles-to-12-poles-vat-included-prices-i2818578034.html |
|| 2 | 10-Terminal Bus Bar 150A (Copper) | ~₱120 ea = ₱240 | Lazada | https://www.lazada.com.ph/products/814-terminal-bus-bar-150a-high-current-dc-busbar-12-48v-copper-power-distribution-terminal-block-for-car-boat-i5119401028-s30216194181.html |
|| 1 | Heat-shrink tube kit | ₱111 | Lazada | https://www.lazada.com.ph/products/pdp-i2569065087.html |
|| 1 | **1/4W 1% Metal Film Resistor Kit** 600pcs | 47Ω/220Ω/1K/10K/47K/68K/100K/220K/1M — pull-ups | ₱220 | Lazada (Makerlab PH) | https://www.lazada.com.ph/products/14w-resistance-1-metal-film-resistor-assorted-kit-each-20-total-600pcs-47-ohms-220-1k-10k-47k-68k-100k-220k-1m-i118492390-s122930341.html |
|| 1 | **Nylon Standoff Kit M3/M2.5** | M3x6+6mm×30 + M3x10+6mm×20 + M2.5x6+6mm×20 — Mega/LCD/SSR mounts | ₱97 | Lazada | https://www.lazada.com.ph/products/pdp-i2946710217.html |
| 1 | Aluminum plate 6061 6mm (motor plate + mounts) | ₱760 | Lazada | https://www.lazada.com.ph/products/pdp-i4449859085.html |

### 2j. Battery + charger (Lazada)

| Qty | Item | Price | Store | Link |
|---|---|---|---|---|
| 1 | PowMr LiFePO4 12.8V 200Ah w/ BMS 200A | ~₱8,900 ea | Lazada | https://h5.lazada.com.ph/products/powmr-12v-200ah-lifepo4-battery-lithium-battery-built-in-bms-6000-deep-cycles-rechargeable-solar-battery-i5047514166.html |
| 1 | VariCore 14.6V 20A Smart LiFePO4 Charger (alligator clip variant) | ~₱2,809 | Lazada | https://www.lazada.com.ph/products/varicore-146v-20a-smart-lifepo4-battery-charger-110-220v-4s-12v-high-power-charger-for-lithium-iron-phosphate-i5375251271-s32167681050.html |

> **⚠️ ORDER BATTERY FIRST** — longest shipping time. Verify seller rating ≥4.5.

### 2k. Cable management & consumables

| Qty | Item | Spec | Price | Store | Link |
|---|---|---|---|---|---|
| 1 | **Zip ties** 100pcs nylon, UV-resistant, heavy duty | 3-tooth buckle; wire bundling | ~₱84 | Lazada | https://www.lazada.com.ph/products/100pcs-heavy-duty-nylon-cable-zip-ties-uv-resistant-multipurpose-i4164586303.html |
| 1 | **Screw kit** M3/M4/M5 stainless steel 320pcs | M3 8/12/16mm screws + nuts + washers; Mega/plate/chamber mounts | ~₱298 | Lazada | https://www.lazada.com.ph/products/320pcs-380pcs-stainless-steel-screws-bolts-nuts-kit-m3-m4-m5-hex-socket-fasteners-assortment-set-anti-loosening-washers-gaskets-diy-home-furniture-auto-repair-hardware-tool-cod-ready-stock-ph-i15532367775.html |
| 1 | **PROSEAL silicone sealant (clear)** | 100% RTV, waterproof/weather-resistant; seam sealing | ~₱199 | Lazada | https://www.lazada.com.ph/products/proseal-silicone-sealant-clear-white-black-brown-i4013402307.html |
| 1 | **Rubber grommets** 180pcs, 8 sizes | Wire passthrough / chamber wall penetrations | ~₱249 | Lazada | https://www.lazada.com.ph/products/same-day-shipping-180pcs-rubber-grommet-assortment-contain-8-popular-sizes-gasket-firewall-hole-plug-set-electrical-wire-gasket-kit-for-car-high-quality-cyb-rubber-grommet-i3692147637.html |
| 1 | Plastic drip tray | Station base | ~₱100 | hardware | — |
| 1 | Velcro strips | Board mounting | ~₱50 | hardware | — |

> **Notes:** The 4 cable-management items (zip ties, screws, sealant, grommets) are all orderable online at ~₱830 total. If you prefer, the hardware store (Robinsons/Wildepanda) sells the same bulk at ~₱490 — pick whichever is cheaper after shipping.

---

## 3. Quick price summary

| Category | Total |
|---|---|
| PTC heaters (9×₱484) | ≈ ₱4,356 |
| AVC blowers (9×₱330) | ≈ ₱2,970 |
| Motors + couplings (makerlab) | ≈ ₱1,749 |
| Bearings + shafts (Lazada) | ≈ ₱1,062 |
| Control electronics (Lazada) | ≈ ₱1,984 |
| SSRs (taxnele) + heatsinks + terminals | ≈ ₱2,051 |
| UI (LEDs, buzzer, button) | ≈ ₱109 |
| Wiring + consumables (Lazada) | ≈ ₱2,500 |
| DC Rocker Switch 50A | ~₱190 |
| Battery (1× 200Ah) + charger | ≈ ₱11,700–12,200 |
| Hardware store consumables | ≈ ₱490 |
| **GRAND TOTAL** | **≈ ₱29,600–29,900** |

---

## 4. Physical store fallbacks (if online unavailable)

| Item | Physical store | Location |
|---|---|---|
| AVC blower fans | e-Gizmo Mechatronics | Tomas Morato, QC |
| KP08 pillow blocks | Kuan Kee Hardware | Manila |
| Steel shafts | Manila Trading (steel) | Various |
| Arduino + sensors | e-Gizmo / Circuitrocks | QC / Online |
| SSR-40DD | Any electronics parts shop | Universal |

---

## 5. Variant checklists (at checkout)

| Item | Pick this | NOT this |
|---|---|---|
| PTC heater | 12V 100W MXKJING T30 | 220V (wrong!) |
| Blower fan | AVC 12V 4.5A, 80mm, PWM | BLDC with ESC (different control) |
| Pillow block | KP08, 6mm bore | KP08, 8mm bore |
| Shaft | 6mm × 300mm SS | 8mm (wrong) |
| Coupling | 6×8mm rigid | Other sizes |
| PTC relay | **SSR-40DD DC-output 40A** | 40A automotive relay (has moving parts, needs NPN driver) |
| PTC relay | **DC-output** (3–32VDC input, DC output) | AC-output (DA type) |
| Motor relay | **SSR-10DD DC-output 10A** | 40A auto (overkill for 0.8A motor) |
| Main protection | **No fuses** — BMS + firmware cutoff only | Any fuses (removed per no-fuse design) |
| Battery | LiFePO4 12.8V 200Ah | Lead-acid (too heavy) |
| Charger | LiFePO4 14.6V 20A | Lead-acid charger (wrong!) |
| DHT22 | Module (black) | Blue (less accurate) |
| DS18B20 | Module + terminal adapter + 3-pin cable | Waterproof probe (harder to wire) |
| Mega | With terminal board | Bare board (more wiring work) |

---

## 6. Notes on the no-fuse design

The no-fuse SSR build removes all fuses (50A ANL, 30A blade, 3A blade, 130°C thermal fuses) from the power path. The battery connects to the distribution bus through a **50A DC rocker switch** (main power disconnect) then a 2-pin screw terminal. Emergency kill = flip rocker OFF + unplug the battery cable.

**Protection scheme:**
- Over-current: BMS 200A cutoff
- Over-temperature: DS18B20 firmware cutoff at 65°C + PTC self-regulation
- Boot-safe: SSRs are active-HIGH (floating pin = OFF)

**SSR-40DD sourcing note:** These are DC-output solid-state relays with 40A rating. They require heatsinks due to ~1W/A dissipation (~25W per PTC SSR at 25A, ~40W per fan bus SSR at 40.5A). The price estimate (~₱200 each) should be verified on Lazada — prices may vary.

**Fan bus SSR rating note:** The fan bus SSR-40DD handles 40.5A (9 × 4.5A). This is at the upper limit of the 40A rating. Ensure the heatsink is properly mounted with thermal paste, and consider that under sustained full load the SSR may approach its maximum dissipation. The SSR-40DD has a 40A rating at 25°C ambient — derating may be needed at higher temperatures.