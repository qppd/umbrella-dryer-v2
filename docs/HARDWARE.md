# Hardware Reference (Rev 5)

Spec sheets for what was actually bought (sources & prices: `docs/BOM.md` §14). Use this during assembly and testing when you need a part's ratings, dimensions, or limits — not the store listing.

## 1. Module spec sheets

### Controller — Arduino Mega 2560 R3

| Spec | Value | Design implication |
|---|---|---|
| MCU | ATmega2560, AVR 8-bit @ 16 MHz | Bare-metal firmware, no OS (`docs/STACKS.md`) |
| Digital I/O | 54 (15 PWM) | 11 used — huge headroom |
| Flash / SRAM / EEPROM | 256 KB / 8 KB / 4 KB | Watch SRAM with many string literals (LCD menus) — use `F()` macro |
| Logic level | 5V | All inputs/outputs 5V; relay boards must be 5V-trigger type |
| Power input | **5V pin from buck only** | Never 12V on the barrel jack (Makerlab warning) |
| Serial | USB + Serial0 (pins 0/1), 115200 debug | Keep 0/1 free while debugging |

### Solid-state relays — 2× Fotek SSR-40DA (mains heat switching, Rev 5)

| Spec | Value | Note |
|---|---|---|
| Output | 24–380VAC, 40A | **DA = AC output — the correct type for the 220V heater-fans.** Never DD on these |
| Input | 3–32VDC, ~12 mA | direct Mega pin (D4/D5) + 10 kΩ pull-up to hold OFF at boot |
| Duty | 1× 1500W heater each (6.8A) | 5.9× margin |
| Dissipation | ≈ 7–10W each | **heatsink mandatory**, thermal paste, inside the grounded metal box |
| Switching | slow time-proportional 2–5s | zero-cross DA type; no fast PWM |
| Fail mode | fail-short possible | mitigated: mains rocker kill + 10A fuse + appliance thermostat + DS18B20 cutoff + RCD |

### Relay modules (optocoupler, low-level trigger) — 12V stations

| Spec | 2-CH 10A boards (×2) |
|---|---|
| Contact rating | 10A @ 30VDC |
| Duty | 3 motor stations (3.5A stall) + 1 spare channel |
| Coil | 5V, ~70 mA — from buck 5V rail, **not** Mega pins |
| Trigger | Optocoupler LED, 2–5 mA, **active-LOW** + 10 kΩ input pull-ups |
| Protection | Built-in flyback diode |
| Limits | DC only, 30VDC max contacts; slow switching only (≥2 s period) |

### Heaters + air exchange (220V mains, Rev 5)

| Spec | 2× 1500W PTC heater-fan | Omni 12" exhaust fan |
|---|---|---|
| Power | 1500W each @ 220V (6.8A) | ~1.5–2.5A @ 220V |
| Switching | SSR-40DA each (staged: base + boost) | mains rocker gang (no SSR) |
| Built-in protection | thermostat + thermal cutoff | motor thermal fuse |
| Role | 40–60C chamber heat + forced air | pulls humid air out of the chamber |
| Mounting | outside the wet zone, plugs accessible | wall/lid opening, ducted out |

### Motors — 3× SGM-A58SW31ZY worm gear (one per station)

| Spec | Value |
|---|---|
| Rated | 12 V, 16 RPM, **60 kg·cm**, 1.2 A @ rated load |
| No-load | 16 RPM, 240 mA |
| Stall | 70 kg·cm, 3.5 A |
| Shaft | 8 mm Ø × 15 mm, single shaft |
| Body | 115 × 40 × 35.7 mm, 357 g |
| Behavior | **Self-locking** (worm not back-drivable); stall-tolerant |

### Mechanical drivetrain (per station ×3)

| Part | Spec |
|---|---|
| Shaft | 304 SS, 8 mm Ø × 300 mm, ground finish |
| Bearings | 2× KP08 pillow block, 8 mm bore, ~160 kgf dynamic — mount ≤ 40 mm from each shaft end |
| Coupling | 8×8 mm rigid clamp sleeve — grub screws on motor flat + shaft, thread-check after first run |
| Umbrella holder | Fabricated, one per station; canopy tip clearance ≥ 5 cm between stations and chamber walls |

### Battery system (control + rotation only since Rev 5)

| Spec | PowMr 12.8V 30Ah | FOXSUR charger |
|---|---|---|
| Chemistry | LiFePO4, 384 Wh | LiFePO4 profile, **14.6 V / 6 A** |
| BMS | 30 A continuous | — |
| Role | 3 motors + logic ≈ 14 W → ~27 h autonomy | never a 13.8 V lead-acid charger |

### Mains AC domain (Rev 5)

| Element | Spec |
|---|---|
| RCD/GFCI | 30 mA class — mandatory on the outlet feeding the system |
| Branch fuses | 10 A per heater line; fan shares the rocker gang |
| Enclosure | grounded metal box for SSRs, fuses, terminals; box + chamber frame + appliance chassis all earthed |
| Wire | 2.0 mm² (14 AWG eq.) 3-core mains branches |
| Kills | mains rocker (2-gang) + DC rocker — both labeled |

### Sensing & UI

| Part | Key specs |
|---|---|
| DHT22 | ±0.5 °C, ±2–5 %RH; **≥2 s between reads**; mount mid-chamber, away from air jets and drain |
| DS18B20 waterproof | ±0.5 °C, 1-Wire, 4.7 kΩ pull-up; probe in the heater air stream |
| LCD 16×2 I2C | 0x27 or 0x3F (scan), 5V |
| LEDs / buzzer / button | 220 Ω series on LEDs; active buzzer D12; button D13 INPUT_PULLUP |
| Rocker switch | 16 A **AC-rated** → derate ~50 % on DC; switches the **control side** only |

## 2. Electrical build standards

| Item | Standard |
|---|---|
| Wire gauge | 2.0 mm² mains · 16 AWG battery main + logic feed · 18 AWG station branches · 22 AWG logic |
| Fuse map | AC: 10 A ×2 heater branches (RCD upstream) · DC: 25 A main · 3 A ×3 stations · 3 A logic |
| Earthing | electrical box, chamber frame, appliance chassis — bonded to earth; RCD is the life-safety layer |
| Grounding | Single-point: all returns → battery − rail; chassis bonded to − at one bolt |
| Pass-throughs | Rubber grommets at every chamber wall penetration |
| Condensate zone | No bare copper below 5 cm above the floor; silicone-sealed seams; drain tube 6–8 mm ID |
| Environment | All-12V extra-low voltage; keep every connector ≥ 5 cm from the heater body |

## 3. Station layout — decided (Rev 4)

| Parameter | Decision |
|---|---|
| Canopy state when drying | **Half-open** — projected Ø ≈ 650 mm. A fully-open commuter canopy spans 950–1000 mm, and three in a row would need a ~3.2 m chamber; half-open exposes the full wet surface with airflow across it and keeps the box realistic |
| Chamber internal W × D × H | **2200 × 800 × 1300 mm** (walls +20 mm → cut panels 2240 × 840 × 1340) |
| Station layout | Single row of 3 stations on the long axis, pitch **700 mm** |
| Clearance check | Canopy edge at 700 + 325 = 1025 mm from center vs wall at 1100 mm → 75 mm each side; between adjacent canopies 700 − 650 = 50 mm — both pass the ≥50 mm rule |
| Hanging length | Umbrella hangs from the holder; heater blows across the canopy underside |
| Services | **2× 1500W heater-fans: freestanding appliances on the chamber floor, designated zone away from the drain/drip path, factory cords out through grommets to plugs outside** · **12" Omni exhaust fan on the rear-wall opening, ducted out** · DHT22 mid-chamber · DS18B20 probe in heater 1's airstream |

> The verification math (`docs/BOM.md` §9) is layout-independent: each motor sees only its own umbrella's ≤3 kg·cm, and airflow crosses all stations regardless of arrangement. If the team later prefers fully-open canopies, re-run the width check in `model/generate_models.py` before committing to a box size.

## 4. Revision history of the hardware set

| Rev | Hardware change |
|---|---|
| Rev 2 | SSR-25DD + BTS7960 + single carousel motor + (optional) MLX90614 |
| Rev 3 | Relays replace SSR + driver; MLX90614 dropped |
| **Rev 4** | **3 independent stations** (3× motors, shafts, KP08 sets); 25A main fuse; per-station 3A fuses |
| **Rev 5** | **Mains heat: 2× 1500W PTC heater-fans via 2× SSR-40DA; 12" Omni exhaust fan; battery = motors + control only; RCD + earthing added** |
