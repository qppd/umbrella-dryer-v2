# PROCUREMENT — Verified Component Sourcing (Lazada PH)

> **Annex to [`docs/BOM.md`](BOM.md) §14** — this file carries the per-listing detail: backup listings, seller ratings and reasoning, and watch-outs. The consolidated order cart lives in BOM.md Appendix A.

**Project:** Smart Umbrella Dryer (PUP Santa Maria, BS CpE capstone)
**Sourcing policy:** Makerlab PH first — verified trusted Lazada store (98% seller rating, 845.6K items sold, 10-Year Store, Bulacan). Items Makerlab doesn't carry → trusted third-party sellers with high rating/sold counts only.
**Prices verified:** 2026-09-12 (Lazada prices move — re-check before ordering)
**Rev 5 quantities:** 3× worm gear motors (one per umbrella station) · **2× Fotek SSR-40DA (AC output — mains heaters)** + 2× 2-CH relay modules · **2× 1500W 220V PTC heater-fans + 12" Omni exhaust fan** · mains kit (RCD, grounded box, 10A fuses, 2.0mm² wire) · 3× shafts / bearing sets / couplings · 25A DC main fuse · MLX90614 removed.

##  All components sourced

### Controller & drivers

**Arduino Mega 2560 R3 — ₱1,215 (Makerlab PH)**
- Listing: Mega 2560 R3 Board based on Arduino® | 4.8 (331) | 2.4K sold
- URL: https://www.lazada.com.ph/products/pdp-i5989151.html
- Variant: ₱1,215 = "no cable" · ₱1,265 = with USB cable

**LM2596S Buck Converter w/ 7-seg display — ₱155 (Makerlab PH)**
- Listing: DC-DC Buck Converter with 7 Segment Display LM2596S | 4.8 (264) | 1.3K sold
- URL: https://www.lazada.com.ph/products/pdp-i127879071.html
- Backup (plain, ₱49, 4.8 (494), 4.5K sold): https://www.lazada.com.ph/products/pdp-i6005010.html

### Heater & power path

**2-Channel Relay Module 5V w/ optocoupler, low-level trigger — ₱89 ea ×2 (3 motor stations)**
- Listing: 2 Channel Relay Module 5V Optocoupler Low Level Trigger | (330) | 2.5K sold | Bulacan
- URL: https://www.lazada.com.ph/products/pdp-i100047444.html
- Qty 2 → 4 channels: 3 worm-motor stations (1 ch each) + 1 spare. Coils fed from the LM2596S 5V rail; Mega drives only the optocoupler LEDs.
- Rev 5 note: the 1-CH 30A relay and the 12V PTC heater that used to sit here are **removed** — heaters moved to mains AC via 2× SSR-40DA (see the Mains AC kit section above).

### Heaters & airflow (Rev 5)

**(moved to the Mains AC kit section above — the 120mm 12V fan is no longer used; replaced by the Omni 12-inch exhaust fan)**

**LiFePO4 Battery 12.8V 30Ah w/ BMS (PowMr)**  pre-order flag
- Listing: PowMr 12.8V 30AH LiFePO4 Battery Built-in BMS | 152.9K store sold
- URL: https://www.lazada.com.ph/products/pdp-i4660631878.html
- PDP-verified: **LiFePO4 chemistry, 12.8V, 30Ah, BMS** . ExpertPower 35Ah (paper's choice) is NOT on Lazada PH — this PowMr 30Ah is the best local equivalent (spec re-check: 30Ah = ~4 cycles/charge instead of 5).
-  Price varies by promo — check PDP. Scout noted a **pre-order / ship-in-60-days flag** — confirm stock before committing, or order early.

**Blade fuses + holder — ₱122.53 + ₱25**
- Fuses: 100pcs Car Blade Fuse Assortment 2-35A w/ box | 4.9 (5022) | 14.3K sold — needs **25A DC main, 3A ×3 motor stations, 3A logic** (mains 10A fuses come from the AC box kit) — https://www.lazada.com.ph/products/pdp-i4214903852.html
- Holder: 1× Panel-Mount Fuse Holder | ₱25 · 131 sold · (13) · Bulacan (Makerlab listing) — https://www.lazada.com.ph/products/pdp-i2502994973.html — for the 25A DC main; motor-branch 3A fuses use inline holders from the assortment.

**Rocker Switch 16A — ₱72 (Unnicoco, 97%)**  DC derating
- Listing: Unnicoco 16A 250VAC / 20A 125VAC Rocker Switch 4 Pins | 111.4K store sold
- URL: https://www.lazada.com.ph/products/pdp-i2272943066.html
-  Rating is AC. At 12V DC, arcing is worse — derate ~50%. **Recommended wiring: rocker switches the control side (buck input + relay coils), NOT the full battery load.** The AC mains rocker is a separate 2-gang part from the hardware kit.

### Mains AC kit (Rev 5)

**2× 1500W PTC industrial heater-fan, 220V — ₱1,395.35 ea**
- Listing: Portable Industrial Electric Heater Fan Commercial Thermostat Air Warm Heater Blower
- URL: https://www.lazada.com.ph/products/portable-industrial-electric-heater-fan-commercial-thermostat-air-warm-heater-blower-radiator-office-garage-air-fan-i4902069326-s28572024789.html
- Switched by SSR-40DA each; keep built-in thermostat + thermal cutoff in circuit; plug accessible.

**Omni industrial exhaust fan w/ grill, wall-mount — ~₱1,000–1,500 (verify variant)**
- Listing: Omni Industrial Exhaust Fan W/ Grill Wall Mounted | spans 12/14/16-inch
- URL: https://www.lazada.com.ph/products/omni-industrial-exhaust-fan-w-grill-wall-mounted-12-inch-14-inch-16-inch-i4020672066-s21738898500.html
- ⚠️ **Select the 12-inch variant.** Runs on its own mains rocker gang — no SSR.

**Fotek SSR-40DA ×2 — ₱850 ea (makerlab.ph)**
- 3–32VDC input, 24–380VAC output, 40A. ⚠️ MUST be **DA** (AC output) for these 220V heaters — the DD type cannot switch AC loads. Heatsink mandatory (7–10W each).
- URL: https://makerlab.ph/products/original-solid-state-relay-ssr-40da-ssr-75da-ssr-25dd-4-32v-dc-input

**Hardware-store additions (EST, add at checkout):** RCD/GFCI 30mA outlet or breaker · grounded metal electrical box · 2-gang mains rocker + plate · 2.0mm² 3-core wire + plug/socket set · 2× SSR heatsink profiles.

### Sensors

**DHT22 Temp/Humidity Sensor — ₱69 (FU-LABS, 98%)**
- Listing: DHT11/DHT22 Digital Temperature and Humidity Sensor | 5.0 (34) | 549 sold
- URL: https://www.lazada.com.ph/products/pdp-i4888079786.html
- Variant: **"DHT22 Black" module = ₱69** (default PDP shows ₱239 bare-probe variant). Makerlab website also sells DHT22 (₱200) — FU-LABS module is cheaper.

**DS18B20 Waterproof Sensor — ₱105 (Circuitrocks)**
- Listing: Waterproof One Wire Sensor DS18B20 3 Meters | (24) | 325 sold | Metro Manila
- URL: https://www.lazada.com.ph/products/pdp-i111662523.html
- Backup (1m kit ₱83.80): https://www.lazada.com.ph/products/pdp-i4824120037.html

### UI & indicators

**16×2 LCD with I2C — ₱165 (Makerlab PH)**
- Listing: 1602 16x2 Character LCD Module HD44780 with I2C | 4.9 (681) | 5.8K sold
- URL: https://www.lazada.com.ph/products/pdp-i104139284.html
- Backup (plain LCD no I2C ₱105): https://www.lazada.com.ph/products/pdp-i156791905.html

**Push Buttons 12mm ×10 — ₱79 (Makerlab PH)**
- Listing: 10pcs 12mm Round Button Tactile Switch | 4.9 (92) | Makerlab store
- URL: https://www.lazada.com.ph/products/pdp-i118682689.html

**5mm LED Kit (10pc multi-color) — ₱29**
- Listing: 10Pcs 5mm Led Kit Red Green Yellow Blue White | (433) | 3.0K sold | Bulacan
- URL: https://www.lazada.com.ph/products/pdp-i3105641040.html

**Active Buzzer Module — ₱35 (Makerlab PH)**
- Listing: Active Alarm Buzzer Driver Module High Current | 4.9 (78) | 537 sold
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

##  Watch-outs (read before ordering)

1. **Relay contacts are 30VDC-rated** — never on mains AC; heater uses slow duty cycling only (2–5s period).
2. **Heater wattage:** only 70W/100W 12V PTC variants exist on Lazada — no 120W. Plan around 100W (cycle ~20% longer than the 120W math).
3. **Battery lead time:** PowMr 30Ah flagged pre-order (~60 days). Order FIRST or find local stock. 30Ah ≈ 3–4 cycles/charge with 3 motor stations.
4. **Rocker DC derating:** don't push a 16A AC-rated switch on the battery load — switch the control side instead.
5. **Motor torque:** the JGY370 Lazada listing is ~25 kg·cm — under the 60 kg·cm spec. Makerlab's SGM-A58SW31ZYS (site-only, qty 3) is the spec-correct choice.

## One-stop alternatives

Makerlab.ph website (not Lazada) also carries: DHT22 (₱200), DS18B20 (₱99), LCD 1602 (plain ₱105 / I2C versions), fuse holders, KCD11 rockers (3A — too small for main switch), SGM worm motors (order all ×3 here), couplings. If you want fewer shipments, order the Makerlab-website-only items there and the rest from their Lazada store.

**Shopee PH not checked** (login-walled for automated verification). All listings above are Lazada PH.
