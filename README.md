# Smart Umbrella Dryer

**Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control**
Capstone project (BS Computer Engineering).

Dries **3 umbrellas simultaneously** (or any 1–3 mix) using heated forced air and sensor-based (humidity + temperature) feedback control — powered entirely by a **12V LiFePO4 battery** with energy-efficient staged duty cycling.

## How it works

1. Each umbrella mounts on its **own motorized station** — a SGM-370 worm gear motor (14 kg·cm) driving through a rigid coupling into a 6mm SS shaft (supported mid-span by a UCP06 pillow block), then a 6mm flange coupling to the umbrella hub — inside the drying chamber. Stations run independently; firmware stages one station at a time to stay within the BMS current budget.
2. **9× PTC ceramic heaters (12V 100W)** provide heating (3 per station), switched by **DC-output SSRs (SSR-40DD class)** driven directly from the Mega. **9× AVC 12V 4.5A blowers** circulate warm air (40–60°C) via direct PWM from the Mega.
3. **DHT22** (humidity) + **DS18B20** (heater-zone temp) drive the cycle on the **Arduino Mega 2560** — PREHEAT gates on temperature (45°C), and DRY auto-stops early once chamber humidity bottoms out at ≤ 60% RH (the "energy efficient control" of the study).
4. When chamber humidity drops below threshold → auto-shutoff + buzzer + green LED. Condensate drains passively (sloped floor → drain tube → drip tray).

## Core components

| Subsystem | Component |
|---|---|
| Controller | Arduino Mega 2560 |
| Heat | **9× PTC ceramic heaters 12V 100W** (3 per station), **LCTC DC-DC SSR 40A switched** |
| Rotation | **3× SGM-370 worm gear motors** 12V (14 kg·cm each), LCTC DC-DC SSR 10A switched |
| Fans | **9× AVC 12V 4.5A blowers** (3 per station), PWM via Mega D10/D11/D12 |
| Sensors | DHT22 (humidity) · DS18B20 (heater-zone temp) |
| Thermal safety | PTC self-regulation · firmware 65°C cutoff · BMS |
| UI | 16×2 LCD (I2C, pins 20/21), 3 status LEDs, buzzer, illuminated arcade start button |
| Mechanical | 3× drivetrains (rigid coupling 6×8mm → 6mm SS shaft on UCP06 pillow block → PETIYOUZA 6mm flange coupling), aluminum chassis |

## Where to start (read in this order)

| Order | Doc | Why |
|---|---|---|
| 1 | [docs/BOM.md](docs/BOM.md) | What to buy — printable shopping checklist |
| 2 | [docs/HARDWARE.md](docs/HARDWARE.md) | What each part is and its ratings |
| 3 | [model/README.md](model/README.md) | What you are building — dimensioned views |
| 4 | [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | How everything wires together |
| 5 | [wiring/README.md](wiring/README.md) | Pin map and all connections |
| 6 | [docs/SETUP.md](docs/SETUP.md) | Build it — numbered steps, check after each |
| 7 | [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Load and tune the code |
| 8 | [docs/TESTING.md](docs/TESTING.md) | Prove it works, record results |
| 9 | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | When a check fails |

Reference material: `docs/SYSTEM-ARCHITECTURE.md`, `docs/FLOWCHART.md`, `docs/STACKS.md`, `docs/SOURCING-ANNEX.md`.

## Verified performance

- **Cycle:** ≈ 15–25 min (light rain) – ~45 min (fully soaked), humidity auto-stop
- **Energy:** staged operation (1 station) ≈ 39.3A draw → ~3.7 h continuous, or ≈ 9.6 quick cycles (~29 umbrellas) per charge (144 Ah usable)
- **Margins:** motor torque ≥4.6× per station · BMS 5.5× vs staged DC draw · PTC self-regulation prevents thermal runaway
- **Cost:** ≈ ₱29,000 (battery + charger included)

## Key design decisions

1. **12V DC only** — no mains wiring, no RCD, no changeover switch. Safer, simpler, cheaper.
2. **DC-output SSRs for switching** — PTC draw (25A/station) and fan bus (40.5A) exceed PCB-relay ratings; SSR-40DD driven directly from Mega pins, SSR-10A for motors.
3. **PTC self-regulating** — heaters auto-limit current as temperature rises (secondary over-temperature protection).
4. **AVC blowers with PWM** — active air circulation for faster drying; PWM speed control via Mega `analogWrite()` (no ESC needed).
5. **Staged operation** — one station at a time keeps total current well within the 200A BMS limit.
6. **SGM-370 worm gear drivetrain** — self-locking, ≥4.6× torque margin, 6 RPM gentle speed; motor → rigid coupling → pillow-block-supported shaft → flange coupling.
7. **No-fuse 12V path** — main disconnect is a 50A DC rocker switch; over-current protection = 200A BMS + firmware cutoffs.
