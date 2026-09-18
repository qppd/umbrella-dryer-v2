# Umbrella Dryer V2 — Documentation

> 3-station automated umbrella drying system. 12V DC battery power, no mains. PTC heaters + fan bus switched by DC-output SSRs, AVC blowers PWM-controlled directly from the Mega, worm gear motors for umbrella rotation. Arduino Mega 2560 controller.

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
- **Main disconnect:** 50A DC rocker switch (no fuses — 200A BMS + firmware cutoff; one station at a time ≈ 39A)
- **Heating:** 9× PTC ceramic heaters 12V 100W — 3 per station, SSR-40DD-switched
- **Fans:** 9× AVC 12V 4.5A blowers — 3 per station, direct PWM from Mega D10/D11/D12
- **Motors:** 3× SGM-370 worm gear 12V 6RPM 14 kg·cm, self-locking — rigid coupling → SS shaft on UCP06 pillow block → flange coupling to hub
- **Control:** Arduino Mega 2560, DHT22 + DS18B20, LCD 16×2 I2C (pins 20/21)
- **Thermal safety:** DS18B20 firmware cutoff 65°C + PTC self-regulation + BMS 200A (no thermal fuses)
- **Staged operation:** one station at a time (firmware-enforced 30s rotation)
- **Cost:** ≈ ₱29,900–30,200 (battery + charger included)

---

## Build steps

1. **Order parts** — See SOURCING-ANNEX.md. Order battery first.
2. **Upload firmware** — See FIRMWARE-GUIDE.md. Install libraries, upload sketch.
3. **Calibrate buck** — Set LM2596S to 5.0V. Connect to Mega 5V pin (not barrel jack).
4. **Build frame** — 3-station frame for inverted umbrellas (700mm pitch).
5. **Mount drivetrain** — SGM-370 on aluminum plates; per station: rigid coupling 6×8mm → 6mm SS shaft through a UCP06 pillow block → 6mm flange coupling to umbrella hub.
6. **Wire power** — Battery → 50A DC rocker switch → 2-pin terminal → 150A bus bars → SSR branches (no fuses).
7. **Wire SSRs** — PTC + fan bus via SSR-40DD, motors via SSR-10A, all driven directly from Mega pins; blower PWM on D10/D11/D12.
8. **Wire sensors** — DHT22 (D2), DS18B20 (D3), LCD I2C (D20/D21).
9. **Test** — Follow TESTING.md: L1 smoke test → L2 component → L3 integration → L4 stress.
10. **Deploy** — Place umbrellas, press button, dry.
