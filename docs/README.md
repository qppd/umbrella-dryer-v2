# Umbrella Dryer V2 — Documentation

> 3-station automated umbrella drying system. 12V DC battery power, no mains. PTC heaters switched by 40A automotive relays, BLDC fans with ESC control, worm gear motors for umbrella rotation. Arduino Mega 2560 controller.

---

## Quick start

| Doc | What it covers |
|---|---|
| [BOM.md](BOM.md) | Full bill of materials with prices, sellers, and URLs |
| [HARDWARE.md](HARDWARE.md) | Components, ratings, build standards, safety |
| [BLOCK-DIAGRAM.md](BLOCK-DIAGRAM.md) | Block diagrams of the electrical system |
| [SYSTEM-ARCHITECTURE.md](SYSTEM-ARCHITECTURE.md) | Architecture overview, power tree, safety design |
| [FIRMWARE-GUIDE.md](FIRMWARE-GUIDE.md) | Arduino sketch, pin map, wiring table |
| [SETUP.md](SETUP.md) | Step-by-step setup instructions |
| [TESTING.md](TESTING.md) | Test plan (L1 smoke test → L4 stress test) |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and fixes |
| [SOURCING-ANNEX.md](SOURCING-ANNEX.md) | Where to buy everything (Lazada + makerlab.ph) |
| [../wiring/README.md](../wiring/README.md) | Pin map and all connections |
| [../model/README.md](../model/README.md) | 3D model views and dimensions |
| [references/](references/) | Original research paper and reference materials |

---

## System summary

- **Power:** 12V DC — 1× 200Ah LiFePO4 battery (no mains, no inverter)
- **Main fuse:** 50A ANL (one station at a time ≈ 36A)
- **Heating:** 9× PTC ceramic heaters 12V 100W — 3 per station, 40A automotive relay-switched
- **Fans:** 9× BLDC ducted fans 50mm 12V with ESC — 3 per station, PWM-controlled
- **Motors:** 3× SGM-370 worm gear 12V 6RPM 14 kg·cm, self-locking
- **Control:** Arduino Mega 2560, DHT22 + DS18B20, LCD 16×2 I2C (pins 20/21)
- **Thermal safety:** DS18B20 firmware cutoff 65°C + 130°C thermal fuse per heater (9×) + PTC self-regulation + BMS
- **Staged operation:** one station at a time (firmware-enforced 30s rotation)
- **Cost:** ≈ ₱27,100–28,100 (battery + charger included)

---

## Build steps

1. **Order parts** — See SOURCING-ANNEX.md. Order battery first.
2. **Upload firmware** — See FIRMWARE-GUIDE.md. Install libraries, upload sketch.
3. **Calibrate buck** — Set LM2596S to 5.0V. Connect to Mega 5V pin (not barrel jack).
4. **Build frame** — 3-station frame for inverted umbrellas (700mm pitch).
5. **Mount motors** — SGM-370 on aluminum plates, connect output shaft to umbrella hub via 6mm flange coupling.
6. **Wire power** — Battery → 50A disconnect → 50A ANL → distribution → per-branch fuses.
7. **Wire relays** — PTC heaters via 40A automotive relays + 2N2222 NPN drivers; motors via opto module; fans via 40A auto relay + ESC.
8. **Wire sensors** — DHT22 (D2), DS18B20 (D3), LCD I2C (D20/D21).
9. **Test** — Follow TESTING.md: L1 smoke test → L2 component → L3 integration → L4 stress.
10. **Deploy** — Place umbrellas, press button, dry.
