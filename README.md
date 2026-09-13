# Smart Umbrella Dryer

**Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control**
Capstone project — Polytechnic University of the Philippines, Santa Maria, Bulacan Campus (BS Computer Engineering).

Dries **3 umbrellas simultaneously** (or any 1–3 mix) using heated forced air and sensor-based (humidity + temperature) feedback control — powered by a 12V LiFePO4 battery backup with energy-efficient duty cycling.

## How it works

1. Each umbrella mounts on its **own motorized station** — a worm gear motor (60 kg·cm) direct-driving an 8mm shaft — inside the drying chamber. Stations run independently: dry 1, 2, or 3 umbrellas per cycle.
2. **Two 1500W PTC heater-fans (220V mains)** and a **12-inch industrial exhaust fan** heat and refresh the chamber (40–60°C — safe for nylon/polyester), switched by **Fotek SSR-40DAs** and staged by the controller.
3. **DHT22** (humidity) + **DS18B20** (heater-zone temp) drive the duty-cycling controller on the **Arduino Mega 2560** — heaters run only while chamber humidity is above threshold (the "energy efficient control" of the study).
4. When chamber humidity drops below threshold → auto-shutoff + buzzer + green LED. Condensate drains passively (sloped floor → drain tube → drip tray).

## Core components (Rev 4)

| Subsystem | Component |
|---|---|
| Controller | Arduino Mega 2560 |
| Heat | **2× 1500W PTC heater-fans (220V mains)** switched by **2× Fotek SSR-40DA** (heatsinked, staged on/off) |
| Air exchange | **Omni 12-inch industrial exhaust fan (220V)** on the mains rocker |
| Rotation | **3× SGM-A58SW31ZY worm gear motors** 12V (60 kg·cm each, one per umbrella) via **2-CH relay modules w/ optocoupler** (fixed 16 RPM) |
| Power | **220V mains** for heat + fan (RCD-protected) · **LiFePO4 12.8V 30Ah** for motors + control → LM2596S buck → 5V logic |
| Sensors | DHT22 · DS18B20 waterproof |
| UI | 16×2 LCD (I2C), 3 status LEDs, buzzer, start button, 2 labeled rockers (MAINS / DC) |
| Mechanical | 3× 8mm steel shafts, 6× KP08 pillow blocks, 3× 8×8 couplings, aluminum chassis |

> Rev 5 change: heating moved to mains (2× 1500W PTC heater-fans via SSR-40DAs, 12" exhaust fan) — cycle time drops to ~15–45 min; the battery now carries motors + control only (~27 h autonomy). Rev 4: 3 independent stations replaced the single-motor carousel; relays replaced the SSR + BTS7960 (12V era). MLX90614 removed.

## Where to start (read in this order)

| Order | Doc | Why |
|---|---|---|
| 1 | [docs/BOM.md](docs/BOM.md) | What to buy — Appendix A is the printable shopping checklist |
| 2 | [docs/HARDWARE.md](docs/HARDWARE.md) | What each part is and its ratings |
| 3 | [model/README.md](model/README.md) | What you are building — 6 dimensioned views |
| 4 | [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | How everything wires together |
| 5 | [docs/SETUP.md](docs/SETUP.md) | Build it — numbered steps, check after each |
| 6 | [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Load and tune the code |
| 7 | [docs/TESTING.md](docs/TESTING.md) | Prove it works, record results |
| 8 | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | When a check fails |

Reference material (dip in as needed): `docs/SYSTEM-ARCHITECTURE.md`, `docs/FLOWCHART.md`, `docs/STACKS.md`, `docs/PROCUREMENT.md`.

## Documentation

| Doc | Contents |
|---|---|
| [docs/BOM.md](docs/BOM.md) | Rev 4 component analysis & compatibility verification, itemized Lazada BOM, printable shopping checklist (Appendix A) |
| [docs/PROCUREMENT.md](docs/PROCUREMENT.md) | Per-listing annex: seller ratings, backup listings, watch-outs |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware reference — part ratings, module spec sheets, build standards |
| [docs/STACKS.md](docs/STACKS.md) | Technology stacks — firmware/libraries, power chain, tooling |
| [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | Electrical block diagram — power domain, fuses, actuation, sensing (mermaid) |
| [docs/SYSTEM-ARCHITECTURE.md](docs/SYSTEM-ARCHITECTURE.md) | Layered architecture, power domains, cycle sequence, design principles |
| [docs/FLOWCHART.md](docs/FLOWCHART.md) | Control-loop and safety-interlock flowcharts (mermaid) |
| [docs/SETUP.md](docs/SETUP.md) | Assembly, wiring, first power-on, Arduino IDE setup |
| [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Sketch structure, state machine, duty-cycle control, tunables |
| [docs/TESTING.md](docs/TESTING.md) | Test plan T0–T4: bench → integration → validation vs study claims |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Symptom → cause → fix per subsystem |
| [model/README.md](model/README.md) | Dimensioned 3D model views (PNG): exploded, front, side, top, front-right, front-left + generator script |

## Verified performance (Rev 5 analysis)

- **Cycle:** ≈ 15–25 min (light rain) – ~45 min (fully soaked), humidity auto-stop
- **Energy:** ≈ 0.6–1.0 kWh per 3-umbrella cycle from mains (staged control, no dry heating); battery runs motors + control ≈ 27 h per charge (25+ cycles)
- **Margins:** SSR-40DA 5.9× per heater (40A vs 6.8A) · motor torque ≥20× per station · BMS 5.7× vs worst-case DC draw · RCD 30mA life protection on the mains domain

## Team

Aliyah Beatriz DR. Buenviaje · Arianne Rose A. Lapig · Roxanne R. Reyes · Hannah Althea G. Tuazon
