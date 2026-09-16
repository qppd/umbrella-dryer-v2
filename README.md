# Smart Umbrella Dryer

**Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control**
Capstone project (BS Computer Engineering).

Dries **3 umbrellas simultaneously** (or any 1–3 mix) using heated forced air and sensor-based (humidity + temperature) feedback control — powered entirely by a **12V LiFePO4 battery bank** with energy-efficient staged duty cycling.

## How it works

1. Each umbrella mounts on its **own motorized station** — a SGM-370 worm gear motor (14 kg·cm) direct-driving a 6mm shaft — inside the drying chamber. Stations run independently; firmware stages one station at a time to stay within fuse budget.
2. **9× PTC ceramic heaters (12V 100W)** provide heating (3 per station), switched by **40A automotive relays** (NPN-driven from Mega). **9× BLDC ducted fans (50mm, ESC-controlled)** circulate warm air (40–60°C).
3. **DHT22** (humidity) + **DS18B20** (heater-zone temp) drive the duty-cycling controller on the **Arduino Mega 2560** — heaters run only while chamber humidity is above threshold (the "energy efficient control" of the study).
4. When chamber humidity drops below threshold → auto-shutoff + buzzer + green LED. Condensate drains passively (sloped floor → drain tube → drip tray).

## Core components

| Subsystem | Component |
|---|---|
| Controller | Arduino Mega 2560 |
| Heat | **9× PTC ceramic heaters 12V 100W** (3 per station), **40A automotive relay-switched** |
| Air circulation | **9× BLDC ducted fans 50mm 12V** (3 per station), ESC PWM-controlled |
| Rotation | **3× SGM-370 worm gear motors** 12V (14 kg·cm each), optocoupler relay-switched (6 RPM) |
| Power | **2× LiFePO4 12.8V 200Ah** in parallel → 50A disconnect → 50A ANL main fuse → per-branch fuses |
| Sensors | DHT22 (humidity) · DS18B20 (heater-zone temp) |
| Thermal safety | 130°C one-shot thermal fuse per heater (9×) · PTC self-regulation · firmware 65°C cutoff · BMS |
| UI | 16×2 LCD (I2C, pins 20/21), 3 status LEDs, buzzer, illuminated arcade start button |
| Mechanical | 3× 6mm SS shafts, 6× KP08 pillow blocks, 3× 6×8 couplings, aluminum chassis |

## Where to start (read in this order)

| Order | Doc | Why |
|---|---|---|
| 1 | [docs/BOM.md](docs/BOM.md) | What to buy — printable shopping checklist |
| 2 | [docs/HARDWARE.md](docs/HARDWARE.md) | What each part is and its ratings |
| 3 | [model/README.md](model/README.md) | What you are building — dimensioned views |
| 4 | [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | How everything wires together |
| 5 | [wiring/README.md](wiring/README.md) | **Canonical** pin map and all connections |
| 6 | [docs/SETUP.md](docs/SETUP.md) | Build it — numbered steps, check after each |
| 7 | [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Load and tune the code |
| 8 | [docs/TESTING.md](docs/TESTING.md) | Prove it works, record results |
| 9 | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | When a check fails |

Reference material: `docs/SYSTEM-ARCHITECTURE.md`, `docs/FLOWCHART.md`, `docs/STACKS.md`, `docs/SOURCING-ANNEX.md`.

## Documentation

| Doc | Contents |
|---|---|
| [docs/BOM.md](docs/BOM.md) | Itemized BOM with prices, sellers, and URLs |
| [docs/SOURCING-ANNEX.md](docs/SOURCING-ANNEX.md) | Verified store links, seller ratings, backup listings |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Hardware reference — part ratings, module spec sheets, build standards |
| [docs/STACKS.md](docs/STACKS.md) | Technology stacks — firmware/libraries, power chain, tooling |
| [docs/BLOCK-DIAGRAM.md](docs/BLOCK-DIAGRAM.md) | Electrical block diagram — power domain, fuses, actuation, sensing (mermaid) |
| [docs/SYSTEM-ARCHITECTURE.md](docs/SYSTEM-ARCHITECTURE.md) | Layered architecture, power domains, cycle sequence, design principles |
| [docs/FLOWCHART.md](docs/FLOWCHART.md) | Control-loop and safety-interlock flowcharts (mermaid) |
| [wiring/README.md](wiring/README.md) | **Canonical** pin map, all connections, wire gauge schedule |
| [docs/SETUP.md](docs/SETUP.md) | Assembly, wiring, first power-on, Arduino IDE setup |
| [docs/FIRMWARE-GUIDE.md](docs/FIRMWARE-GUIDE.md) | Complete staged sketch, state machine, wiring table, debug tips |
| [docs/TESTING.md](docs/TESTING.md) | Test plan L1–L4: smoke → component → integration → stress |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Symptom → cause → fix per subsystem |
| [model/README.md](model/README.md) | Dimensioned 3D model views (PNG): exploded, front, side, top + generator script |

## Verified performance

- **Cycle:** ≈ 15–25 min (light rain) – ~45 min (fully soaked), humidity auto-stop
- **Energy:** staged operation (1 station) ≈ 35.5A draw → ~8.1 h continuous, or ≈ 19 quick cycles (57 umbrellas) per charge on the 400Ah bank (288 Ah usable)
- **Margins:** motor torque ≥4.6× per station · BMS 5.5× vs staged DC draw · PTC self-regulation prevents thermal runaway
- **Cost:** ≈ ₱36,000–37,000 (batteries + charger included)

## Key design decisions

1. **12V DC only** — eliminates mains wiring, RCD, changeover switch. Safer, simpler, cheaper.
2. **PTC self-regulating** — no SSR needed; PTC heaters auto-limit current as temperature rises.
3. **BLDC fans with ESC** — active air circulation for faster drying; PWM speed control via Arduino.
4. **Staged operation** — one station at a time keeps total current within the 50A main fuse.
5. **SGM-370 worm gear** — self-locking, ≥4.6× torque margin, 6 RPM gentle speed.
6. **40A automotive relays for PTC** — PTC draw (25A) exceeds 10A PCB relay ratings; automotive-grade with NPN drivers.
7. **130°C thermal fuse per heater** (9×) — independent hardware cutoff, non-resettable.
