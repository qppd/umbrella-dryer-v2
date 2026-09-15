# Smart Umbrella Dryer

**Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control**
Capstone project (BS Computer Engineering).

Dries **3 umbrellas simultaneously** (or any 1–3 mix) using heated forced air and sensor-based (humidity + temperature) feedback control — powered entirely by a **12V LiFePO4 battery bank** with energy-efficient duty cycling.

## How it works

1. Each umbrella mounts on its **own motorized station** — a worm gear motor (14 kg·cm) direct-driving a 6mm shaft — inside the drying chamber. Stations run independently: dry 1, 2, or 3 umbrellas per cycle.
2. **9× PTC ceramic heaters (12V 100W)** provide heating (3 per station), and **9× BLDC ducted fans (50mm, ESC-controlled)** circulate warm air through the chamber (40–60°C — safe for nylon/polyester).
3. **DHT22** (humidity) + **DS18B20** (heater-zone temp) drive the duty-cycling controller on the **Arduino Mega 2560** — heaters run only while chamber humidity is above threshold (the "energy efficient control" of the study).
4. When chamber humidity drops below threshold → auto-shutoff + buzzer + green LED. Condensate drains passively (sloped floor → drain tube → drip tray).

## Core components

| Subsystem | Component |
|---|---|
| Controller | Arduino Mega 2560 |
| Heat | **9× PTC ceramic heaters 12V 100W** (3 per station), relay-switched |
| Air circulation | **9× BLDC ducted fans 50mm 12V** (3 per station), ESC PWM-controlled |
| Rotation | **3× SGM-370 worm gear motors** 12V (14 kg·cm each), relay-switched (6 RPM) |
| Power | **2× LiFePO4 12.8V 200Ah** in parallel → 25A main fuse → DC bus → per-station fuses |
| Sensors | DHT22 (humidity) · DS18B20 (heater-zone temp) |
| UI | 16×2 LCD (I2C), 3 status LEDs, buzzer, illuminated arcade start button |
| Mechanical | 3× 6mm SS shafts, 6× KP08 pillow blocks, 3× 6×8 couplings, aluminum chassis |

## Where to start (read in this order)

| Order | Doc | Why |
|---|---|---|
| 1 | [docs/BOM.md](docs/BOM.md) | What to buy — printable shopping checklist |
| 2 | [docs/HARDWARE.md](docs/HARDWARE.md) | What each part is and its ratings |
| 3 | [model/README.md](model/README.md) | What you are building — 6 dimensioned views |
| 4 | [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | How everything wires together |
| 5 | [docs/SETUP.md](docs/SETUP.md) | Build it — numbered steps, check after each |
| 6 | [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Load and tune the code |
| 7 | [docs/TESTING.md](docs/TESTING.md) | Prove it works, record results |
| 8 | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | When a check fails |

Reference material (dip in as needed): `docs/SYSTEM-ARCHITECTURE.md`, `docs/FLOWCHART.md`, `docs/STACKS.md`, `docs/SOURCING-ANNEX.md`.

## Documentation

| Doc | Contents |
|---|---|
| [docs/BOM.md](docs/BOM.md) | Itemized Lazada BOM, printable shopping checklist, cost summary |
| [docs/SOURCING-ANNEX.md](docs/SOURCING-ANNEX.md) | Verified store links, seller ratings, backup listings |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware reference — part ratings, module spec sheets, build standards |
| [docs/STACKS.md](docs/STACKS.md) | Technology stacks — firmware/libraries, power chain, tooling |
| [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | Electrical block diagram — power domain, fuses, actuation, sensing (mermaid) |
| [docs/SYSTEM-ARCHITECTURE.md](docs/SYSTEM-ARCHITECTURE.md) | Layered architecture, power domains, cycle sequence, design principles |
| [docs/FLOWCHART.md](docs/FLOWCHART.md) | Control-loop and safety-interlock flowcharts (mermaid) |
| [docs/SETUP.md](docs/SETUP.md) | Assembly, wiring, first power-on, Arduino IDE setup |
| [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Sketch structure, state machine, duty-cycle control, tunables |
| [docs/TESTING.md](docs/TESTING.md) | Test plan T0–T4: bench → integration → validation |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Symptom → cause → fix per subsystem |
| [model/README.md](model/README.md) | Dimensioned 3D model views (PNG): exploded, front, side, top + generator script |

## Verified performance

- **Cycle:** ≈ 15–25 min (light rain) – ~45 min (fully soaked), humidity auto-stop
- **Energy:** ≈ 1,260W total draw → ~3.5 hours runtime on 400Ah bank; staged operation (1 station) = ~45A, ~4.4 hours
- **Margins:** motor torque ≥4.6× per station · BMS 8.9× vs worst-case DC draw · PTC self-regulation prevents thermal runaway
