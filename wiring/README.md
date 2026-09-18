# Wiring Reference — Arduino Mega 2560

> Pin map for every component. Pure 12V DC architecture: **all loads run from the battery** — no mains voltage, no inverter, no changeover switch. If any other doc disagrees with this file, this file wins.

## 0. Domains overview

| Domain | Source | Loads | Switched by |
|---|---|---|---|
| 12V DC | 1× LiFePO4 200Ah | PTC heaters, AVC blowers, worm motors | 4× SSR-40DD (3 PTC + 1 fan bus, direct-drive), 3× SSR-10A (motors), PWM (D10/D11/D12) |
| 5V DC | LM2596S buck (12V→5V) | Mega, sensors, LCD | — |

> **SSR architecture:** a station's 3 PTC heaters draw ~25A — over the 10A rating
> of PCB relay modules. Every PTC group therefore uses a **DC-output SSR-40DD** (40A).
> The motor SSRs are LCTC DC-DC SSR-10A (active-HIGH). No optocoupler module needed. Each motor draws only ~0.8A.
> The fan bus (9 blowers, ~40.5A) uses SSR-40DD.

## 1. Pin map — Mega 2560 side

| Mega pin | Direction | Connects to | Active level | Wire / notes |
|---|---|---|---|---|
| 5V | power in | LM2596S buck OUT+ (set 5.00 V) | — | 20 AWG — never the barrel jack |
| GND | common | Ground rail (DC side) | — | 20 AWG |
| D2 | in | DHT22 DATA | — | 22 AWG + 10 kΩ pull-up to 5V |
| D3 | in | DS18B20 yellow/white DATA | — | 22 AWG + 4.7 kΩ pull-up to 5V |
| **D4** | out | Station 1 PTC SSR-40DD (input +) | HIGH = ON | 22 AWG — heater group 1 (3× 100W) |
| **D5** | out | Station 1 motor SSR-10A (input +) | HIGH = ON | 22 AWG — SGM-370 #1 |
| **D6** | out | Station 2 PTC SSR-40DD (input +) | HIGH = ON | 22 AWG — heater group 2 |
| **D7** | out | Station 2 motor SSR-10A (input +) | HIGH = ON | 22 AWG — SGM-370 #2 |
| **D8** | out | Station 3 PTC SSR-40DD (input +) | HIGH = ON | 22 AWG — heater group 3 |
| **D9** | out | Station 3 motor SSR-10A (input +) | HIGH = ON | 22 AWG — SGM-370 #3 |
| **D13** | out | Fan bus SSR-40DD (input +) | HIGH = ON | 22 AWG — powers all 9 blowes |
| **D10** | out (PWM) | Blower PWM — Station 1 | — | `analogWrite(D10, val)` 0–255 |
| **D11** | out (PWM) | Blower PWM — Station 2 | — | `analogWrite(D11, val)` 0–255 |
| **D12** | out (PWM) | Blower PWM — Station 3 | — | `analogWrite(D12, val)` 0–255 |
| **D14** | in | Start button (other side → GND) | LOW = pressed | INPUT_PULLUP |
| D15 | out | Red LED (heater active) via 220 Ω | HIGH = ON | 22 AWG |
| D16 | out | Yellow LED (cycle running) via 220 Ω | HIGH = ON | 22 AWG |
| D17 | out | Green LED (done) via 220 Ω | HIGH = ON | 22 AWG |
| D18 | out | Active buzzer + (− → GND) | HIGH = ON | 22 AWG |
| **20 (SDA)** | I2C | LCD SDA | — | addr 0x27 or 0x3F |
| **21 (SCL)** | I2C | LCD SCL | — | Mega I2C is pins 20/21 — NOT A4/A5 |

> Mixed active levels are deliberate: SSRs are active-HIGH by design — a floating pin at boot = SSR OFF (boot-safe).

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
| 12V Positive Bus | Fan bus branch → SSR-40DD → blower distribution | 10 AWG | — |
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

Active-HIGH: `digitalWrite(pin, HIGH)` = SSR ON. Floating pin at boot = SSR OFF (no input current).

## 5. Fan power bus — LCTC DC-DC SSR 40A (D13)

| SSR terminal | Goes to |
|---|---|
| IN+ | Mega pin D13 |
| IN− | GND |
| COM (input side) | +12V bus |
| NO (output side) | Blower distribution block — VIN of all 9 blowers in parallel |

D13 HIGH → all blowers powered. D13 LOW → every blower dies instantly (emergency kill).
On the Mega, D13 also blinks the onboard LED when the fan bus is on — free indicator.

## 6. Blower PWM wiring (D10/D11/D12)

Each of the 9 AVC blowers accepts PWM duty cycle directly from Mega pins via `analogWrite()`. Per station, the 3 blowers share one Mega PWM pin.

| Blower wire | Goes to |
|---|---|
| VIN (red) | Fan bus from SSR-40DD (10 AWG bus → 18 AWG pigtails) |
| GND (black) | Common ground rail |
| PWM signal | D10 (station 1) / D11 (station 2) / D12 (station 3) — 3 leads per pin |

> **No ESC needed.** `analogWrite(D, 255)` = full speed. `analogWrite(D, 0)` = off.

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
|| Bus → fan SSR → blower distribution | 10 AWG (18 AWG signal pigtails) |
| Bus → motor branch → module → motor | 18 AWG |
| Bus → buck IN+ | 20 AWG |
| Buck OUT → 5V rail | 20 AWG |
| All Mega signal / sensor jumpers | 22 AWG |

## 10. Safety features

1. **PTC self-regulation** — current drops as element temperature rises
2. **DS18B20 firmware cutoff** at 65 °C — cuts PTC SSRs + motor relays + fan bus
3. **Boot-safe by design** — All SSRs are active-HIGH (floating pin at boot = SSR OFF). PWM pins default LOW = blowers off. `allOff()` called first in `setup()`.
   channels have onboard pull-ups (OFF); firmware writes safe states first in `setup()`
4. **No mains voltage** — entire system is SELV
5. **Single-point DC ground** — all returns meet at one bus bar
| Emergency kill | pull battery cable from 2-pin screw terminal OR flip 50A rocker switch OFF |
7. **BMS 200A** — over-current protection on battery output

> With fuses removed, the BMS and firmware cutoff are the only over-current/over-temperature
> protections. There is no hardware fuse backstop anymore.
