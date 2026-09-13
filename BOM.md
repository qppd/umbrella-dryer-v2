# BOM — Smart Umbrella Dryer (Rev 4: Three-Station Direct Drive)

**Project:** Smart Umbrella Dryer — PUP Santa Maria, BS CpE capstone
**Change from Rev 3:**
1. **3× worm gear motors (₱1,249 ea.) — one per umbrella.** Each umbrella hangs from its own driven shaft; no shared carousel, no 60 kg·cm single-motor sizing problem, no crossbar imbalance. Stations are independent: any 1–3 umbrellas can run at once.
2. **2× 2-CH relay modules** (was 1) — one channel per motor (3 used of 4).
3. **3× drivetrain sets** — 3 shafts, 6× KP08 bearings, 3× 8×8 couplings.
4. **Main fuse 20A → 25A** — 3-motor worst-case peak exceeds the old 20A headroom at battery sag.
5. **MLX90614 IR sensor removed** from the design (all revisions).
**All URLs Lazada PH. Prices verified 2026-09-12 — re-check at checkout (Lazada prices move daily).**

## 1. Controller

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | Arduino Mega 2560 R3 | ATmega2560, 54 DIO, 256KB flash | ₱1,215 (no cable) / ₱1,265 (w/ USB) | Makerlab PH, ⭐4.8 (331), 2.4K sold | https://www.lazada.com.ph/products/pdp-i5989151.html |

## 2. Switching — relay modules w/ optocoupler

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | 1-Channel 30A relay module, optocoupler isolation | 30A@30VDC — 100W PTC heater (8.3A) at 3.6× margin | ₱113 | (14), 99 sold | https://www.lazada.com.ph/products/pdp-i5037406294.html |
| 2 | 2-Channel relay module 5V, optocoupler, low-level trigger | 10A@30VDC contacts — 1 channel per worm motor (1.2A each); 4th channel = circulation fan (0.25A) | ₱89 ea | Bulacan, (330), 2.5K sold | https://www.lazada.com.ph/products/pdp-i100047444.html |

> **Rev-4 wiring notes:** relay coils run off the LM2596S 5V rail, NOT Mega pins — the Mega drives only the optocoupler LEDs (~2–5mA each). Heater relay NO contact sits in the 15A-fused heater branch; each motor relay channel sits in its own 3A-fused station branch (stations 1–3). All modules have built-in flyback diodes. **Contacts are 30VDC-rated — never use on mains AC.**

## 3. Sensors

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | DHT22 temp/humidity module | Chamber humidity — core feedback (select **"DHT22 Black"** variant) | ₱69 | FU-LABS 98%, ⭐5.0 (34), 549 sold | https://www.lazada.com.ph/products/pdp-i4888079786.html |
| 1 | DS18B20 waterproof probe 3m | Heater-zone air temp, over-temp cutoff (+4.7kΩ pull-up) | ₱105 | Circuitrocks, (24), 325 sold | https://www.lazada.com.ph/products/pdp-i111662523.html |

## 4. Heater & airflow

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | PTC air heater 12V w/ fan, **100W** | Self-regulating ceramic — Lazada's max 12V variant | ₱546.67 | PTCYIDU 99%, ⭐4.9 (39), 2.6K sold | https://www.lazada.com.ph/products/pdp-i2108420762.html |
| 1 | 120mm 12V fan | Chamber air circulation | ₱54 | Allan Head 97%, ⭐4.7 (760) | https://www.lazada.com.ph/products/pdp-i1022138302.html |

## 5. Logic power

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | LM2596S buck w/ 7-seg display | 12.8V→5V @3A; Mega via 5V pin (never the DC jack) | ₱155 | Makerlab PH, ⭐4.8 (264), 1.3K sold | https://www.lazada.com.ph/products/pdp-i127879071.html |

## 6. UI & indicators

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | LCD 16×2 w/ I2C backpack | HD44780, addr 0x27/0x3F | ₱165 | Makerlab PH, ⭐4.9 (681), 5.8K sold | https://www.lazada.com.ph/products/pdp-i104139284.html |
| 1 | 5mm LED kit 10pc multi-color | Green/yellow/red status ×3 stations | ₱29 | (433), 3.0K sold, Bulacan | https://www.lazada.com.ph/products/pdp-i3105641040.html |
| 1 | Active buzzer module | Cycle-complete alert | ₱35 | Makerlab PH, ⭐4.9 (78), 537 sold | https://www.lazada.com.ph/products/pdp-i3474748260.html |
| 1 | Tactile push buttons 12mm ×10 | Start/reset (D13 INPUT_PULLUP) | ₱79 | Makerlab PH, ⭐4.9 (92) | https://www.lazada.com.ph/products/pdp-i118682689.html |
| 1 | Rocker switch 16A 4-pin | Main power — **control-side switching only** (AC-rated part derated on DC; don't push full battery load through it) | ₱72 | Unnicoco 97%, 111.4K store sold | https://www.lazada.com.ph/products/pdp-i2272943066.html |

## 7. Drivetrain — 3 independent stations (Rev 4 core change)

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 3 | Worm gear motor SGM-A58SW31ZY 12V 16RPM | 60 kg·cm, self-locking, stall-tolerant — **1 per umbrella station** (Makerlab **website**, not Lazada store) | ₱1,249 ea = ₱3,747 | makerlab.ph | https://makerlab.ph/products/dc-worm-gear-motor-sgm-a58sw31zys-12v-16rpm-80rpm-sgm-370-12v-40rpm-160rpm-dc-motor |
| 3 | 304 SS shaft 8mm × 300mm, ground finish | One main shaft per station | ₱222.40 ea = ₱667.20 | (19), 77 sold | https://www.lazada.com.ph/products/pdp-i4473127402.html |
| 3 | KP08 pillow block bearings (2-pc set) | 8mm bore — **6 bearings total, 2 per station**; select **KP08** variant | ₱310/set = ₱930 | (44), 286 sold, Bulacan | https://www.lazada.com.ph/products/pdp-i5039609084.html |
| 2 | Shaft coupling set 4/5/6/8/10mm rigid | 3× 8×8 configs needed (motor × station shaft); 2 sets cover it with a spare | ₱82.84 ea = ₱165.68 | (185), 408 sold | https://www.lazada.com.ph/products/pdp-i2734273953.html |

> **Per-station recipe:** 1 motor (direct drive, no belt/chain) + 1 shaft + 2 KP08 + 1 8×8 coupling. Torque per station: 1 umbrella needs ≤3 kg·cm → 60 kg·cm = ≥20× margin; a jammed umbrella stalls one motor only — the other two stations keep running. Do NOT substitute the Lazada JGY370 (~25 kg·cm) — under spec and different shaft size; order all 3 SGM motors from makerlab.ph in one order.

## 8. Wiring & interconnect

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | Silicone wire, single-core, 6–18AWG | 16AWG main/heater, 18AWG motor ×3, 22AWG logic — pick sizes on PDP | ₱218 | 6.2K sold, (55) | https://www.lazada.com.ph/products/pdp-i4880482146.html |
| 1 | Dupont jumper kit 40-pin (M-M/M-F/F-F) | Logic hookups | ₱45 | Circuitrocks, 13.7K sold, (1907) | https://www.lazada.com.ph/products/pdp-i245055558.html |
| 1 | Terminal block 15A barrier (3–12 poles) | Distribution + fused-branch junctions | ₱106 | Laguna, 296 sold, (36) | https://www.lazada.com.ph/products/pdp-i2818578034.html |
| 1 | Heat-shrink kit 3/4/5/6mm × 1m | Splice insulation | ₱111 | Toolstar, 606 sold, (133) | https://www.lazada.com.ph/products/pdp-i1085866956.html |
| 1 | Resistor kit 300pcs / 30 values 1/4W 1% | 220Ω LED, 4.7kΩ DS18B20 pull-up, 10kΩ | ₱69 | 215 sold, (73) | https://www.lazada.com.ph/products/pdp-i4888115298.html |
| 1 | Nylon standoff/spacer kit M2–M4 | Board mounting | ₱97 | 1.2K sold, (252) | https://www.lazada.com.ph/products/pdp-i2946710217.html |

## 9. Battery system

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | LiFePO4 12.8V 30Ah w/ BMS (PowMr) | 384Wh — ~3–4 cycles/charge with 3 motors. BMS 30A continuous ≥ 13.1A worst case (2.3×). ⚠ **pre-order flag (~60 days) — order FIRST** | ~₱3,500–4,500 (promo varies) | PowMr store, 152.9K sold | https://www.lazada.com.ph/products/pdp-i4660631878.html |
| 1 | Smart charger 14.6V/6A, LiFePO4 mode (FOXSUR) | NOT a lead-acid 13.8V charger | ₱945 | ⭐(615), 1.6K sold | https://www.lazada.com.ph/products/pdp-i2019767534.html |

## 10. Fuses

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | Blade fuse assortment 100pcs (2–35A) + box | **25A main**, 15A heater, 3A ×3 motor branches, 3A logic | ₱122.53 | QC, ⭐4.9 (5022), 14.3K sold | https://www.lazada.com.ph/products/pdp-i4214903852.html |
| 2 | Panel-mount fuse holder 15A | Heater branch + main (motor-branch 3A fuses use inline holders from the assortment) | ₱25 ea | Makerlab listing | https://www.lazada.com.ph/products/pdp-i2502994973.html |

## 11. Chassis & structure

| Qty | Item | Spec | Price | Seller / Trust | URL |
|---|---|---|---|---|---|
| 1 | Aluminum plate 6061, 6mm | 3× motor mounts, relay plate, 3× station bearing plates | ₱760 | 218 sold, (52) | https://www.lazada.com.ph/products/pdp-i4449859085.html |
| — | *Budget alt:* MS base plate 3mm 12"×12" (mild steel) | Rust-proof near condensate if used | ₱240 | (6), 12 sold | https://www.lazada.com.ph/products/pdp-i5180285577.html |
| 1 | Zip ties 4" (~100pcs) | Wire lacing ×3 stations | ~₱50 | generic hardware | (add to any Lazada order) |

## 12. Assembly & consumables

| Item | Use | Est. price | Where |
|---|---|---|---|
| M3/M4 screw assortment | Chassis + 3-motor mount assembly | ~₱100 | Lazada hardware |
| Pure silicone sealant 280ml | Chamber sealing, drain grommet | ~₱150 | Lazada hardware / SM |
| Shallow plastic tray or 1L container | Drip tray (100–300mL/cycle) | ~₱100 | kitchen section |
| Velcro / double-sided tape | Mega + relay module mounting | ~₱60 | stationery |
| Rubber grommet assortment *(optional)* | Drain tube + wire pass-throughs | ~₱80 | hardware |

## ✅ Cart totals

| Category | Subtotal |
|---|---|
| Electronics (controller, 3 relay modules, sensors, UI, buck, heater, fan — MLX90614 removed) | ≈ ₱2,816 |
| Wiring & interconnect | ≈ ₱646 |
| Fuses + holders | ≈ ₱173 |
| Drivetrain — 3 stations (3× motor ₱3,747 + 3× shaft ₱667 + 6× KP08 ₱930 + 2× coupling set ₱166) | ≈ ₱5,510 |
| Battery + charger | ≈ ₱4,445–5,445 |
| Chassis (aluminum plate + zip ties) | ≈ ₱810 |
| Consumables (screws, sealant, tray, tape, grommets) | ≈ ₱490 |
| **TOTAL (core)** | **≈ ₱14,890–15,890** |

*(≈ +₱3,740 vs Rev 3's single-motor carousel: +2 motors ₱2,498, +2 shafts ₱445, +4 bearings ₱620, +1 motor relay & 2nd coupling set ≈ ₱172, − carousel crossbar fabrication. Switching still saves ≈ ₱1,850 vs Rev 2's SSR + BTS7960.)*

## ⚠️ Rev-4 order notes

1. **Relay contacts are 30VDC-rated** — never use these boards on mains AC.
2. **Heater duty cycle:** keep the slow time-proportional control (2–5s period). Mechanical relays tolerate slow cycling; do NOT use fast PWM.
3. **Motors:** order all 3 SGM-A58SW31ZY 16RPM units from makerlab.ph in one order — the JGY370 Lazada backup (~25 kg·cm, different shaft) is NOT an acceptable substitute.
4. **30Ah battery:** ~3–4 cycles/charge with all 3 motors running (heater still dominates). Runtime math in `docs/COMPONENT_VALIDATION.md` §10.
5. **Battery + charger have the longest lead time** (pre-order ~60 days) — order those first.
6. **DHT22:** select the ₱69 "DHT22 Black" variant — the ₱239 default on the PDP is the bare-probe version.
7. **Rocker switch:** rated 16A AC — on 12V DC it derates ~50%. Switch the control side (buck input / relay enable), not the full battery load.
8. **Fuse sizing:** main is now 25A (3-motor stall worst case ~11.1A + heater 8.3A + margin); each motor branch gets its own 3A fuse so one jammed station can't take down the others.
9. Prices drift daily with Lazada vouchers — re-verify each PDP at checkout. Full per-listing procurement details: `docs/PROCUREMENT.md`.
