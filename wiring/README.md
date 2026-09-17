# Wiring Reference — Arduino Mega 2560

> Pin map for every component. Pure 12V DC architecture: **all loads run from the battery** — no mains voltage, no inverter, no changeover switch. If any other doc disagrees with this file, this file wins.

## 0. Domains overview

| Domain | Source | Loads | Switched by |
|---|---|---|---|
| 12V DC | 1× LiFePO4 200Ah | PTC heaters, BLDC fans, worm motors | 4× SSR-40DD (3 PTC + 1 fan bus, direct-drive), 4-CH opto module (motors), ESC PWM (fans) |
| 5V DC | LM2596S buck (12V→5V) | Mega, sensors, LCD, 4-CH module coils | — |

> **SSR architecture:** a station's 3 PTC heaters draw ~25A — over the 10A rating
> of PCB relay modules. Every PTC group therefore uses a **DC-output SSR-40DD** (40A).
> The 10A-rated 4-CH opto module only switches the worm motors (~0.8A). The fan bus
> (9 fans, ~28.8A) uses a 4th SSR-40DD. Each SSR requires a heatsink (≈1 W/A dissipation → ~25 W per PTC SSR).

## 1. Pin map — Mega 2560 side

| Mega pin | Direction | Connects to | Active level | Wire / notes |
|---|---|---|---|---|
| 5V | power in | LM2596S buck OUT+ (set 5.00 V) | — | 20 AWG — never the barrel jack |
| GND | common | Ground rail (DC side) | — | 20 AWG |
| D2 | in | DHT22 DATA | — | 22 AWG + 10 kΩ pull-up to 5V |
| D3 | in | DS18B20 yellow/white DATA | — | 22 AWG + 4.7 kΩ pull-up to 5V |
| **D4** | out | Station 1 PTC SSR-40DD (input +) | HIGH = ON | 22 AWG — heater group 1 (3× 100W) |
| **D5** | out | Station 1 motor relay (4-CH module IN1) | LOW = ON | 22 AWG — SGM-370 #1 |
| **D6** | out | Station 2 PTC SSR-40DD (input +) | HIGH = ON | 22 AWG — heater group 2 |
| **D7** | out | Station 2 motor relay (module IN2) | LOW = ON | 22 AWG — SGM-370 #2 |
| **D8** | out | Station 3 PTC SSR-40DD (input +) | HIGH = ON | 22 AWG — heater group 3 |
| **D9** | out | Station 3 motor relay (module IN3) | LOW = ON | 22 AWG — SGM-370 #3 |
| **D13** | out | Fan bus SSR-40DD (input +) | HIGH = ON | 22 AWG — powers all 9 ESCs |
| **D10** | out (PWM) | ESC signal — Station 1 fans (3 in parallel) | — | Servo library, 50 Hz, 1000–2000 µs |
| **D11** | out (PWM) | ESC signal — Station 2 fans | — | Servo library, 50 Hz |
| **D12** | out (PWM) | ESC signal — Station 3 fans | — | Servo library, 50 Hz |
| **D14** | in | Start button (other side → GND) | LOW = pressed | INPUT_PULLUP |
| D15 | out | Red LED (heater active) via 220 Ω | HIGH = ON | 22 AWG |
| D16 | out | Yellow LED (cycle running) via 220 Ω | HIGH = ON | 22 AWG |
| D17 | out | Green LED (done) via 220 Ω | HIGH = ON | 22 AWG |
| D18 | out | Active buzzer + (− → GND) | HIGH = ON | 22 AWG |
| **20 (SDA)** | I2C | LCD SDA | — | addr 0x27 or 0x3F |
| **21 (SCL)** | I2C | LCD SCL | — | Mega I2C is pins 20/21 — NOT A4/A5 |

> Mixed active levels are deliberate: SSRs are active-HIGH (floating pin at boot = SSR OFF).
> Opto module channels are active-LOW with onboard pull-ups (floating pin at boot = relay OFF).

## 2. 12V DC power distribution

The system uses **two heavy-duty 10-terminal 150A copper bus bars** (20 holes total) for the main high-current 12V DC power distribution (Positive and Negative/GND). The existing **15A Barrier Terminal Block** remains unchanged; do not replace or rewire it for this bus-bar change.

| From | To | Wire | Protection |
|---|---|---|---|
| Battery + | 2-pin screw terminal (battery in) | 8 AWG | — |
| Battery − | 12V Negative Ground Bus Bar (10-Terminal Copper) | 8 AWG | — |
| Screw terminal + | 12V Positive Bus Bar (10-Terminal Copper) | 8 AWG | — |
| 12V Positive Bus | Station 1 PTC branch → SSR-40DD → heaters | 10 AWG | — |
| 12V Positive Bus | Station 2 PTC branch → SSR-40DD → heaters | 10 AWG | — |
| 12V Positive Bus | Station 3 PTC branch → SSR-40DD → heaters | 10 AWG | — |
| 12V Positive Bus | Fan bus branch → SSR-40DD → ESC distribution | 10 AWG | — |
| 12V Positive Bus | Motor 1/2/3 branches → SSR-10A COM/NO → motors | 18 AWG | — |
| 12V Positive Bus | Buck IN+ (logic power) | 20 AWG | — |
| All returns | 12V Negative Ground Bus Bar (10-Terminal Copper) → bank − | — | chassis bonded at one bolt |
| Buck OUT+ (5V) | Mega 5V pin, sensors, LCD, button LED ring | 20 AWG | set 5.00 V first |

> **Staged operation is mandatory:** one station's PTC + fans + motor ≈ 36A. Two
> stations at once ≈ 70A — exceeds the BMS 200A continuous rating and stresses the
> battery. The firmware enforces one station at a time (`docs/FIRMWARE-GUIDE.md`).
> With fuses removed, the BMS + firmware cutoff are the only over-current protections.

## 3. Station PTC branch — SSR-40DD (×3, D4/D6/D8)

Each station's 3 PTC heaters (~25A) are switched by one DC-output SSR-40DD (40A, input 3–32VDC).

| SSR terminal | Goes to |
|---|---|
| IN+ | Mega pin D4/D6/D8 |
| IN− | GND |
| COM (input side) | +12V bus |
| NO (output side) | Parallel + leads of the 3 PTC heaters |

> Pin HIGH → SSR energizes (≈10–20 mA input current). Pin floats/LOW at boot → SSR OFF.

**Heater side:** PTC − leads → ground rail. Each SSR requires a heatsink (dissipation ≈1 W/A → ~25 W per PTC SSR at 25A).

## 4. Motor branch — LCTC DC-DC SSR 10A (D5/D7/D9)

|| SSR terminal | Goes to |
||---|---|
|| IN+ | Mega pin D5/D7/D9 |
|| IN− | GND |
|| COM (input side) | +12V motor branch |
|| NO (output side) | SGM-370 motor + |

Active-HIGH: `digitalWrite(pin, HIGH)` = SSR ON. Onboard optocoupler holds SSR OFF at boot (floating pin = OFF).

## 5. Fan power bus — LCTC DC-DC SSR 40A (D13)

| SSR terminal | Goes to |
|---|---|
| IN+ | Mega pin D13 |
| IN− | GND |
| COM (input side) | +12V bus |
| NO (output side) | ESC distribution block — red (VIN) of all 9 ESCs in parallel |

D13 HIGH → all ESCs powered. D13 LOW → every fan dies instantly (emergency kill).
On the Mega, D13 also blinks the onboard LED when the fan bus is on — free indicator.

## 6. ESC + BLDC fan wiring (D10/D11/D12)

Each of the 9 BLDC fans ships with its own ESC. Per station, the 3 ESCs share one
Mega PWM pin (signal wires in parallel) and the switched 12V fan bus.

| ESC wire | Goes to |
|---|---|
| Red (VIN) | Fan bus from SSR-40DD (10 AWG bus → 18 AWG pigtails) |
| Black (GND) | Common ground rail |
| White/orange (signal) | D10 (station 1) / D11 (station 2) / D12 (station 3) — 3 leads per pin |

> **ESC arming:** on boot write `esc.writeMicroseconds(1000)` for 2 s before any
> throttle. Use the 1100–1900 µs window in operation.

## 7. Sensor wiring

| Sensor | Wire | Goes to |
|---|---|---|
| DHT22 | VCC / GND / DATA | 5V rail / ground rail / D2 + 10 kΩ pull-up to 5V |
| DS18B20 | red / black / yellow(white) | 5V rail / ground rail / D3 + 4.7 kΩ pull-up to 5V |
| LCD 16×2 I2C | VCC / GND / SDA / SCL | 5V rail / ground rail / **D20** / **D21** |

## 8. UI wiring

| Part | Goes to |
|---|---|
| Arcade button | pin 1 → D14, pin 2 → GND (INPUT_PULLUP). LED ring: + → 5V, − → GND |
| Red LED | anode → D15 via 220 Ω, cathode → GND |
| Yellow LED | anode → D16 via 220 Ω, cathode → GND |
| Green LED | anode → D17 via 220 Ω, cathode → GND |
| Active buzzer | + → D18, − → GND |

## 9. Wire gauge schedule

| Run | Gauge |
|---|---|
| Battery → screw terminal → bus | 8 AWG |
| Bus → station PTC SSR → heaters | 10 AWG |
| Bus → fan SSR → ESC distribution | 10 AWG (18 AWG ESC pigtails) |
| Bus → motor branch → module → motor | 18 AWG |
| Bus → buck IN+ | 20 AWG |
| Buck OUT → 5V rail | 20 AWG |
| All Mega signal / sensor jumpers | 22 AWG |

## 10. Safety features

1. **PTC self-regulation** — current drops as element temperature rises
2. **DS18B20 firmware cutoff** at 65 °C — cuts PTC SSRs + motor relays + fan bus
3. **Boot-safe by design** — SSRs are active-HIGH (floating pin at boot = SSR OFF), opto module
   channels have onboard pull-ups (OFF); firmware writes safe states first in `setup()`
4. **No mains voltage** — entire system is SELV
5. **Single-point DC ground** — all returns meet at one bus bar
6. **Emergency kill** — pull battery cable from 2-pin screw terminal
7. **BMS 200A** — over-current protection on battery output

> With fuses removed, the BMS and firmware cutoff are the only over-current/over-temperature
> protections. There is no hardware fuse backstop anymore.
