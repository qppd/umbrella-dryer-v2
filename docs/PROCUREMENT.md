# PROCUREMENT — Verified Component Sourcing (Lazada PH)

**Project:** Smart Umbrella Dryer (PUP Santa Maria, BS CpE capstone)
**Sourcing policy:** Makerlab PH first — verified trusted Lazada store (98% seller rating, 845.6K items sold, 10-Year Store, Bulacan). Items Makerlab doesn't carry → trusted third-party sellers with high rating/sold counts only.
**Prices verified:** 2026-09-12 (Lazada prices move — re-check before ordering)
**Rev 4 quantities:** 3× worm gear motors (one per umbrella station) · 1× 30A heater relay + 2× 2-CH relay modules (replace Rev 2's SSR + BTS7960) · 3× shafts / bearing sets / couplings · 25A main fuse · MLX90614 removed from the design.

## ✅ All components sourced

### Controller & drivers

**Arduino Mega 2560 R3 — ₱1,215 (Makerlab PH)**
- Listing: Mega 2560 R3 Board based on Arduino® | ⭐4.8 (331) | 2.4K sold
- URL: https://www.lazada.com.ph/products/pdp-i5989151.html
- Variant: ₱1,215 = "no cable" · ₱1,265 = with USB cable

**LM2596S Buck Converter w/ 7-seg display — ₱155 (Makerlab PH)**
- Listing: DC-DC Buck Converter with 7 Segment Display LM2596S | ⭐4.8 (264) | 1.3K sold
- URL: https://www.lazada.com.ph/products/pdp-i127879071.html
- Backup (plain, ₱49, ⭐4.8 (494), 4.5K sold): https://www.lazada.com.ph/products/pdp-i6005010.html

### Heater & power path

**1-Channel 30A Relay Module w/ optocoupler — ₱113 (heater switching)**
- Listing: 1-Channel 30A Relay Module Optocoupler Isolation 5V | (14) | 99 sold
- URL: https://www.lazada.com.ph/products/pdp-i5037406294.html
- 3.6× margin vs the 8.3A heater. ⚠️ Contacts are 30VDC-rated — never use on mains AC. Slow duty cycling only (2–5s period); no fast PWM.

**2-Channel Relay Module 5V w/ optocoupler, low-level trigger — ₱89 ea ×2 (3 motors + fan)**
- Listing: 2 Channel Relay Module 5V Optocoupler Low Level Trigger | (330) | 2.5K sold | Bulacan
- URL: https://www.lazada.com.ph/products/pdp-i100047444.html
- Qty 2 → 4 channels: 3 worm-motor stations (1 ch each) + 1 circulation fan. Coils fed from the LM2596S 5V rail; Mega drives only the optocoupler LEDs.
- Replaces Rev 2's SSR-25DD + BTS7960 (~₱1,850 saved) — all loads are on/off only.

**PTC Air Heater 12V w/ fan — ₱546.67 (PTCYIDU, 99%)** ⚠️ wattage flag
- Listing: PTCYIDU PTC Fan Heater Thermostatic | ⭐4.9 (39) | 2.6K sold | QC
- URL: https://www.lazada.com.ph/products/pdp-i2108420762.html
- ⚠️ **12V variants are 70W / 100W — no 120W variant.** Take the 100W (cycle runs ~20% longer; re-run thermal numbers, or run two 70W in parallel).
- Backup (50W 12V ₱271.23): https://www.lazada.com.ph/products/pdp-i3070436162.html

**120mm 12V Cooling Fan — ₱54 (Allan Head, 97%)**
- Listing: Allan 12V Fan 120mm Case Cooling Fan | ⭐4.7 (760) | 627.5K store sold
- URL: https://www.lazada.com.ph/products/pdp-i1022138302.html

**LiFePO4 Battery 12.8V 30Ah w/ BMS (PowMr)** ⚠️ pre-order flag
- Listing: PowMr 12.8V 30AH LiFePO4 Battery Built-in BMS | 152.9K store sold
- URL: https://www.lazada.com.ph/products/pdp-i4660631878.html
- PDP-verified: **LiFePO4 chemistry, 12.8V, 30Ah, BMS** ✓. ExpertPower 35Ah (paper's choice) is NOT on Lazada PH — this PowMr 30Ah is the best local equivalent (spec re-check: 30Ah = ~4 cycles/charge instead of 5).
- ⚠️ Price varies by promo — check PDP. Scout noted a **pre-order / ship-in-60-days flag** — confirm stock before committing, or order early.

**Blade fuses + holder — ₱122.53 + ₱25**
- Fuses: 100pcs Car Blade Fuse Assortment 2-35A w/ box | ⭐4.9 (5022) | 14.3K sold — needs **25A main, 15A heater, 3A ×3 motor stations, 3A logic** — https://www.lazada.com.ph/products/pdp-i4214903852.html
- Holders: 2× 15A Panel-Mount Fuse Holder | ₱25 ea · 131 sold · (13) · Bulacan (Makerlab listing) — https://www.lazada.com.ph/products/pdp-i2502994973.html — heater branch + main; motor-branch 3A fuses use inline holders from the assortment.

**Rocker Switch 16A — ₱72 (Unnicoco, 97%)** ⚠️ DC derating
- Listing: Unnicoco 16A 250VAC / 20A 125VAC Rocker Switch 4 Pins | 111.4K store sold
- URL: https://www.lazada.com.ph/products/pdp-i2272943066.html
- ⚠️ Rating is AC. At 12V DC, arcing is worse — derate ~50%. **Recommended wiring: rocker switches the control side (SSR input + driver enable), NOT the full 15A load.** If you must switch full load, size up or use the SSR as the power switch.

### Sensors

**DHT22 Temp/Humidity Sensor — ₱69 (FU-LABS, 98%)**
- Listing: DHT11/DHT22 Digital Temperature and Humidity Sensor | ⭐5.0 (34) | 549 sold
- URL: https://www.lazada.com.ph/products/pdp-i4888079786.html
- Variant: **"DHT22 Black" module = ₱69** (default PDP shows ₱239 bare-probe variant). Makerlab website also sells DHT22 (₱200) — FU-LABS module is cheaper.

**DS18B20 Waterproof Sensor — ₱105 (Circuitrocks)**
- Listing: Waterproof One Wire Sensor DS18B20 3 Meters | (24) | 325 sold | Metro Manila
- URL: https://www.lazada.com.ph/products/pdp-i111662523.html
- Backup (1m kit ₱83.80): https://www.lazada.com.ph/products/pdp-i4824120037.html

### UI & indicators

**16×2 LCD with I2C — ₱165 (Makerlab PH)**
- Listing: 1602 16x2 Character LCD Module HD44780 with I2C | ⭐4.9 (681) | 5.8K sold
- URL: https://www.lazada.com.ph/products/pdp-i104139284.html
- Backup (plain LCD no I2C ₱105): https://www.lazada.com.ph/products/pdp-i156791905.html

**Push Buttons 12mm ×10 — ₱79 (Makerlab PH)**
- Listing: 10pcs 12mm Round Button Tactile Switch | ⭐4.9 (92) | Makerlab store
- URL: https://www.lazada.com.ph/products/pdp-i118682689.html

**5mm LED Kit (10pc multi-color) — ₱29**
- Listing: 10Pcs 5mm Led Kit Red Green Yellow Blue White | (433) | 3.0K sold | Bulacan
- URL: https://www.lazada.com.ph/products/pdp-i3105641040.html

**Active Buzzer Module — ₱35 (Makerlab PH)**
- Listing: Active Alarm Buzzer Driver Module High Current | ⭐4.9 (78) | 537 sold
- URL: https://www.lazada.com.ph/products/pdp-i3474748260.html
- Backup (piezo 3-24V ₱55): https://www.lazada.com.ph/products/pdp-i2270182027.html

### Drivetrain & mechanicals

**Worm Gear Motor 12V — Makerlab website ₱1,249 ×3 — one per umbrella station** (primary)
- Makerlab.ph: DC Worm Gear Motor SGM-A58SW31ZYS 12V 16/80RPM (60 kg·cm class, self-locking) — confirmed NOT on their Lazada store, order from makerlab.ph.
- **Rev 4: qty 3 — put all three in one makerlab.ph order.**
- The Lazada JGY370 (~25 kg·cm, different shaft size) is NOT an acceptable substitute at any quantity.

**8mm Steel Shaft — 304 SS ground rod (₱222.40+) — qty 3, one per station**
- Primary: 304 Stainless Steel Rod 6/7/8/10mm Linear Shaft Ground Stock 300/500/1000mm — **8mm × 300mm variant** | 370 sold | (80) — https://www.lazada.com.ph/products/pdp-i5154908354.html
- Alternate (price-verified ₱222.40, 28% off, 77 sold, (19)): https://www.lazada.com.ph/products/pdp-i4473127402.html

**KP08 Pillow Block Bearings — ₱310 per 2-pc set, qty 3 sets = 6 bearings (2 per station)**
- Listing: 2 pcs Pillow Block Bearing KP08 KP000-KP003 8mm-20mm | (44) | 286 sold | Bulacan
- URL: https://www.lazada.com.ph/products/pdp-i5039609084.html
- Variant: **select KP08 (8mm bore)** — listing spans KP08-KP004.
- Single-unit backups: zinc KP08 ₱49-87, 311 sold, QC — https://www.lazada.com.ph/products/pdp-i4139708194.html

**Shaft Coupling (incl. 8×8) — ₱82.84 (FUXING)**
- Listing: 1set Rigid Shaft Coupling 4/5/6/8/10mm Motor Connector Sleeve #45 Steel | (185) | 408 sold
- URL: https://www.lazada.com.ph/products/pdp-i2734273953.html
- Set includes 8mm — clamp-style rigid sleeve. Use the 8×8 config for motor-to-shaft. **Qty 2 sets** (3× 8×8 configs needed + spare).

## ⚠️ Watch-outs (read before ordering)

1. **Relay contacts are 30VDC-rated** — never on mains AC; heater uses slow duty cycling only (2–5s period).
2. **Heater wattage:** only 70W/100W 12V PTC variants exist on Lazada — no 120W. Plan around 100W (cycle ~20% longer than the 120W math).
3. **Battery lead time:** PowMr 30Ah flagged pre-order (~60 days). Order FIRST or find local stock. 30Ah ≈ 3–4 cycles/charge with 3 motor stations.
4. **Rocker DC derating:** don't push a 16A AC-rated switch on the battery load — switch the control side instead.
5. **Motor torque:** the JGY370 Lazada listing is ~25 kg·cm — under the 60 kg·cm spec. Makerlab's SGM-A58SW31ZYS (site-only, qty 3) is the spec-correct choice.

## One-stop alternatives

Makerlab.ph website (not Lazada) also carries: DHT22 (₱200), DS18B20 (₱99), LCD 1602 (plain ₱105 / I2C versions), fuse holders, KCD11 rockers (3A — too small for main switch), SGM worm motors (order all ×3 here), couplings. If you want fewer shipments, order the Makerlab-website-only items there and the rest from their Lazada store.

**Shopee PH not checked** (login-walled for automated verification). All listings above are Lazada PH.
