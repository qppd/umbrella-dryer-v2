# Hardware Reference (Rev 4)

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

### Relay modules (optocoupler, low-level trigger)

| Spec | 1-CH 30A board | 2-CH 10A boards |
|---|---|---|
| Contact rating | 30A @ 30VDC | 10A @ 30VDC |
| Duty | Heater (8.3A) | 3 motor stations (3.5A stall) + fan (0.25A) |
| Coil | 5V, ~70 mA — from buck 5V rail, **not** Mega pins | same |
| Trigger | Optocoupler LED, 2–5 mA, **active-LOW** | same |
| Protection | Built-in flyback diode | same |
| Limits | **DC only — 30VDC max contact voltage. Mains prohibited.** | Mechanical contacts: slow switching only (≥2 s period) |

### Heater — PTC air heater 12V 100W w/ blower

| Spec | Value | Note |
|---|---|---|
| Power | 100 W @ 12 V (8.3 A) | Lazada's max 12V variant (no 120W exists) |
| Self-regulation | Ceramic PTC auto-limits at Curie point | The hardware layer of over-temp defense |
| Air temp | 40–60 °C effective in chamber | Safe for nylon/polyester canopies |
| Blower | Integrated — **must run whenever heater is on** | Wired on the heater branch, behind the same 15A fuse |
| Cold start | Inrush above rated current briefly | 30A relay contact covers it |

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

### Battery system

| Spec | PowMr 12.8V 30Ah | FOXSUR charger |
|---|---|---|
| Chemistry | LiFePO4, 384 Wh | LiFePO4 profile, **14.6 V / 6 A** |
| BMS | 30 A continuous, over-charge/discharge/short/temp | — |
| Charge rule | Never a 13.8 V lead-acid charger | Order-first item (~60-day lead time) |

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
| Wire gauge | 16 AWG main + heater · 18 AWG station branches + fan · 22 AWG logic |
| Fuse map | 25 A main · 15 A heater · 3 A ×3 stations · 3 A logic |
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
| Services | Heater 200×100 left wall, low (center 220 mm above floor, bottom 50 clear); 120 mm fan right wall, low (same height); DHT22 mid-chamber; DS18B20 probe in the heater air stream |

> The verification math (`docs/BOM.md` §9) is layout-independent: each motor sees only its own umbrella's ≤3 kg·cm, and airflow crosses all stations regardless of arrangement. If the team later prefers fully-open canopies, re-run the width check in `model/generate_models.py` before committing to a box size.

## 4. Revision history of the hardware set

| Rev | Hardware change |
|---|---|
| Rev 2 | SSR-25DD + BTS7960 + single carousel motor + (optional) MLX90614 |
| Rev 3 | Relays replace SSR + driver; MLX90614 dropped |
| **Rev 4** | **3 independent stations** (3× motors, shafts, KP08 sets); 25A main fuse; per-station 3A fuses |
