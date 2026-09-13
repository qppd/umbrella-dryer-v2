# Smart Umbrella Dryer

**Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control**
Capstone project — Polytechnic University of the Philippines, Santa Maria, Bulacan Campus (BS Computer Engineering).

Dries **3 umbrellas simultaneously** (or any 1–3 mix) using heated forced air and sensor-based (humidity + temperature) feedback control — powered by a 12V LiFePO4 battery backup with energy-efficient duty cycling.

## How it works

1. Each umbrella mounts on its **own motorized station** — a worm gear motor (60 kg·cm) direct-driving an 8mm shaft — inside the drying chamber. Stations run independently: dry 1, 2, or 3 umbrellas per cycle.
2. A 100W PTC air heater (self-regulating ceramic, with blower) heats the chamber to 40–60°C — safe for nylon/polyester fabric.
3. **DHT22** (humidity) + **DS18B20** (heater-zone temp) drive a duty-cycling controller on the **Arduino Mega 2560** — the heater runs only while chamber humidity is above threshold (the "energy efficient control" of the study).
4. When chamber humidity drops below threshold → auto-shutoff + buzzer + green LED. Condensate drains passively (sloped floor → drain tube → drip tray).

## Core components (Rev 4)

| Subsystem | Component |
|---|---|
| Controller | Arduino Mega 2560 |
| Heater | PTC 12V **100W** air heater w/ fan — switched by **30A relay module w/ optocoupler** (DC-rated contacts) |
| Rotation | **3× SGM-A58SW31ZY worm gear motors** 12V (60 kg·cm each, one per umbrella) via **2-CH relay modules w/ optocoupler** (fixed 16 RPM — no speed control needed) |
| Power | LiFePO4 12.8V 30Ah (BMS) → LM2596S buck → 5V logic |
| Sensors | DHT22 · DS18B20 waterproof |
| UI | 16×2 LCD (I2C), 3 status LEDs, buzzer, start button, main rocker switch |
| Mechanical | 3× 8mm steel shafts, 6× KP08 pillow blocks, 3× 8×8 couplings, aluminum chassis |

> Rev 4 change: the single-motor carousel became **3 independent motorized stations** (one motor per umbrella). Earlier: Rev 3 replaced the SSR + BTS7960 of Rev 2 with optocoupler relay modules (~₱1,900 saved) — the heater and motors only need on/off control. MLX90614 IR sensor removed from the design.

## Documentation

| Doc | Contents |
|---|---|
| [docs/BOM.md](docs/BOM.md) | **Start here** — Rev 4 component analysis & compatibility verification, itemized Lazada BOM, printable shopping checklist (Appendix A) |
| [docs/PROCUREMENT.md](docs/PROCUREMENT.md) | Per-listing annex: seller ratings, backup listings, watch-outs |
| [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | Electrical block diagram — power domain, fuses, actuation, sensing (mermaid) |
| [docs/SYSTEM-ARCHITECTURE.md](docs/SYSTEM-ARCHITECTURE.md) | Layered architecture, power domains, cycle sequence, design principles |
| [docs/FLOWCHART.md](docs/FLOWCHART.md) | Control-loop and safety-interlock flowcharts (mermaid) |
| [docs/SETUP.md](docs/SETUP.md) | Assembly, wiring, first power-on, Arduino IDE setup |
| [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Sketch structure, state machine, duty-cycle control, tunables |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Symptom → cause → fix per subsystem |

## Verified performance (Rev 4 analysis)

- **Cycle:** ≈ 50 min (light rain) – 2.5 h (fully soaked), humidity auto-stop
- **Energy:** ≈ 90–95 Wh per 3-umbrella cycle → **3–4 cycles per battery charge**
- **Margins:** motor torque ≥20× per station (≤3 kg·cm per umbrella vs 60 kg·cm) · relay contacts 2.9–3.6× · BMS 2.3× vs worst-case draw

## Team

Aliyah Beatriz DR. Buenviaje · Arianne Rose A. Lapig · Roxanne R. Reyes · Hannah Althea G. Tuazon
