# Umbrella Dryer V2 — Documentation

> A 3-station automated umbrella drying system powered by **12V DC** — battery-operated, no mains voltage. Uses PTC ceramic heaters, BLDC fans with ESC control, and worm gear motors for umbrella rotation. Controlled by Arduino Mega 2560.

---

## Quick links

| Document | What it covers |
|---|---|
| [BOM.md](BOM.md) | Full bill of materials with prices, sellers, and URLs |
| [HARDWARE.md](HARDWARE.md) | Components, wiring diagrams, and mechanical assembly |
| [BLOCK-DIAGRAM.md](BLOCK-DIAGRAM.md) | Mermaid block diagrams of the system |
| [SYSTEM-ARCHITECTURE.md](SYSTEM-ARCHITECTURE.md) | Architecture overview, power tree, safety design |
| [FIRMWARE-GUIDE.md](FIRMWARE-GUIDE.md) | Complete Arduino sketch + pin map + wiring table |
| [STACKS.md](STACKS.md) | Software and hardware layer overview |
| [SETUP.md](SETUP.md) | Step-by-step setup instructions |
| [TESTING.md](TESTING.md) | Test plan (L1 smoke test → L4 stress test) |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and fixes |
| [SOURCING-ANNEX.md](SOURCING-ANNEX.md) | Where to buy everything (Lazada + makerlab.ph) |
| [references/](references/) | Original research paper and reference materials |

---

## System summary

- **Power:** 12V DC only — 2× 200Ah LiFePO4 batteries in parallel (no mains, no inverter)
- **Heating:** 9× PTC ceramic heaters (12V 100W each) — 3 per station, self-regulating
- **Fans:** 9× BLDC ducted fans (50mm, 12V, with ESC) — 3 per station, PWM-controlled
- **Motors:** 3× SGM-370 worm gear (12V 6RPM, 14 kg·cm, self-locking)
- **Control:** Arduino Mega 2560 with DHT22 + DS18B20 sensors, 16×2 LCD, relay modules, ESC PWM
- **Safety:** DS18B20 thermal cutoff + thermal fuse + PTC self-regulation + per-station fusing
- **Cost:** ≈ ₱33,300–34,500 (batteries + charger included)

---

## Build steps

1. **Order parts** — See [SOURCING-ANNEX.md](SOURCING-ANNEX.md). Order batteries first.
2. **Upload firmware** — See [FIRMWARE-GUIDE.md](FIRMWARE-GUIDE.md). Install libraries, upload sketch.
3. **Calibrate buck** — Set LM2596S to 5.0V before connecting to Mega.
4. **Build frame** — 3-station frame for inverted umbrellas.
5. **Mount motors** — SGM-370 on aluminum plates, shafts through KP08 pillow blocks.
6. **Wire power** — Battery → 25A fuse → DC distribution → per-station fuses.
7. **Wire relays** — PTC heaters and motors through relay modules; fans through automotive relay + ESC.
8. **Wire sensors** — DHT22 (humidity), DS18B20 (temperature), LCD I2C.
9. **Test** — Follow [TESTING.md](TESTING.md): L1 smoke test → L2 component → L3 integration → L4 stress.
10. **Deploy** — Place umbrellas, press button, dry.

---

## Capstone info

- **Program:** BS in Information Technology
- **Semester:** 2nd Semester, AY 2025–2026
- **Adviser:** Engr. [Adviser Name]
- **Authors:** [Author Name(s)]
- **Repository:** [Repository URL]
- **License:** MIT

---

## Key design decisions

1. **12V DC only** — eliminates mains wiring, RCD, changeover switch. Safer, simpler, cheaper.
2. **PTC self-regulating** — no SSR needed; PTC heaters auto-limit current as temperature rises.
3. **BLDC fans with ESC** — active air circulation for faster drying; PWM speed control via Arduino.
4. **Staged operation** — one station at a time keeps total current within 25A main fuse.
5. **SGM-370 worm gear** — self-locking, ≥4.6× torque margin, 6 RPM gentle speed.
