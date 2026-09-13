# Smart Umbrella Dryer

**Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control**
Capstone project — Polytechnic University of the Philippines, Santa Maria, Bulacan Campus (BS Computer Engineering).

Dries **3 umbrellas simultaneously** (or any 1–3 mix) using heated forced air and sensor-based (humidity + temperature) feedback control — powered by a 12V LiFePO4 battery backup with energy-efficient duty cycling.

## How it works

1. Each umbrella mounts on its **own motorized station** — a worm gear motor (60 kg·cm) direct-driving an 8mm shaft — inside the drying chamber. Stations run independently: dry 1, 2, or 3 umbrellas per cycle.
2. A 100W PTC air heater (self-regulating ceramic, with blower) heats the chamber to 40–60°C — safe for nylon/polyester fabric.
3. **DHT22** (humidity) + **DS18B20** (heater-zone temp) drive a duty-cycling controller on the **Arduino Mega 2560** — the heater runs only while chamber humidity is above threshold (the "energy efficient control" of the study).
4. When humidity drops below threshold → auto-shutoff + buzzer + green LED. Condensate drains passively (sloped floor → drain tube → drip tray).

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

> Rev 4 change: the single-motor carousel became **3 independent motorized stations** (one motor per umbrella). Earlier: Rev 3 replaced the SSR + BTS7960 of Rev 2 with optocoupler relay modules (~₱1,900 saved). The heater and motors only need on/off control. MLX90614 IR sensor removed from the design. See `BOM.md` and `docs/PROCUREMENT.md` for verified Lazada listings.

## Documentation

| Doc | Contents |
|---|---|
| [docs/COMPONENT_VALIDATION.md](docs/COMPONENT_VALIDATION.md) | Rev 4 component compatibility analysis, 3-station capacity verification (torque/thermal/electrical), power budget, safety matrix, pin map, BOM |
| docs/PROCUREMENT.md | Verified Lazada/Store listings per component (seller, rating, price, URL) |
| references/FINALFINAL_SUD_CHAPTER-1-3.docx / .md | Capstone paper chapters 1–3 |

## Verified performance (Rev 4 analysis)

- **Cycle:** ≈ 40 min (light rain) – 2 h (fully soaked), humidity auto-stop; per-station stop when an umbrella is dry
- **Energy:** ≈ 90 Wh per 3-umbrella cycle → **3–4 cycles per battery charge**
- **Margins:** motor torque ≥20× per station (≤3 kg·cm per umbrella vs 60 kg·cm) · relay contacts 6.7× vs motor stall · BMS 2.3× vs worst-case draw

## Team

Aliyah Beatriz DR. Buenviaje · Arianne Rose A. Lapig · Roxanne R. Reyes · Hannah Althea G. Tuazon
