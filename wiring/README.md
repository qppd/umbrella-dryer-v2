# Wiring Reference — Arduino Mega 2560

> Pin map for every component. Pure 12V DC architecture: **all loads run from the battery** — no mains voltage, no inverter, no changeover switch. If any other doc disagrees with this file, this file wins.

## 0. Domains overview

| Domain | Source | Loads | Switched by |
|---|---|---|---|
| 12V DC | 1× LiFePO4 200Ah → 50A main fuse | PTC heaters, BLDC fans, worm motors | 4× automotive 40A relays (3 PTC + 1 fan bus, NPN-driven), 4-CH opto module (motors), ESC PWM (fans) |
| 5V DC | LM2596S buck (12V→5V) | Mega, sensors, LCD, 4-CH module coils | — |

> **Relay architecture:** a station's 3 PTC heaters draw ~25A — over the 10A rating
> of PCB relay modules. Every PTC group therefore uses a **40A automotive relay**. The
> 10A-rated 4-CH opto module only switches the worm motors (~0.8A). The fan bus
> (9 fans, ~28.8A) uses a 4th automotive relay.

## 1. Pin map — Mega 2560 side

| Mega pin | Direction | Connects to | Active level | Wire / notes |
|---|---|---|---|---|
| 5V | power in | LM2596S buck OUT+ (set 5.00 V) | — | 20 AWG — never the barrel jack |
| GND | common | Ground rail (DC side) | — | 20 AWG |
| D2 | in | DHT22 DATA | — | 22 AWG + 10 kΩ pull-up to 5V |
| D3 | in | DS18B20 yellow/white DATA | — | 22 AWG + 4.7 kΩ pull-up to 5V |
| **D4** | out | Station 1 PTC relay (auto 40A, via 2N2222) | HIGH = ON | 22 AWG — heater group 1 (3× 100W) |
| **D5** | out | Station 1 motor relay (4-CH module IN1) | LOW = ON | 22 AWG — SGM-370 #1 |
| **D6** | out | Station 2 PTC relay (auto 40A, via 2N2222) | HIGH = ON | 22 AWG — heater group 2 |
| **D7** | out | Station 2 motor relay (module IN2) | LOW = ON | 22 AWG — SGM-370 #2 |
| **D8** | out | Station 3 PTC relay (auto 40A, via 2N2222) | HIGH = ON | 22 AWG — heater group 3 |
| **D9** | out | Station 3 motor relay (module IN3) | LOW = ON | 22 AWG — SGM-370 #3 |
| **D13** | out | Fan bus relay (auto 40A, via 2N2222) | HIGH = ON | 22 AWG — powers all 9 ESCs |
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

> Mixed active levels are deliberate: NPN-driven automotive relays are active-HIGH
> (floating pin at boot = relay OFF, extra 10 kΩ base pull-down). Opto module channels
> are active-LOW with onboard pull-ups (floating pin at boot = relay OFF).

## 2. 12V DC power distribution

| From | To | Wire | Protection |
|---|---|---|---|
| Battery A + ↔ Battery B + (main link) | bank + | 4 AWG | — |
| Battery A − ↔ Battery B − (main link) | bank − | 4 AWG | — |
| Bank + | 50A battery disconnect switch | 8 AWG | — |
| Disconnect | **50A ANL main fuse** → distribution bus | 8 AWG | 50 A ANL |
| Bus | Station 1 PTC branch: **30A fuse** → auto relay 30 → 87 → heaters | 10 AWG | 30 A blade |
| Bus | Station 2 PTC branch: **30A fuse** → auto relay → heaters | 10 AWG | 30 A blade |
| Bus | Station 3 PTC branch: **30A fuse** → auto relay → heaters | 10 AWG | 30 A blade |
| Bus | Fan bus: **30A fuse** → auto relay 30 → 87 → ESC distribution | 10 AWG | 30 A blade |
| Bus | Motor 1/2/3 branches: **3A fuse ×3** → 4-CH module COM/NO → motors | 18 AWG | 3 A blade ×3 |
| Bus | Logic: **3A fuse** → buck IN+ | 20 AWG | 3 A blade |
| All returns | Single-point ground bus bar → bank − | — | chassis bonded at one bolt |
| Buck OUT+ (5V) | Mega 5V pin, 4-CH module VCC, sensors, LCD, button LED ring | 20 AWG | set 5.00 V first |

> **Staged operation is mandatory:** one station's PTC + fans + motor ≈ 36A. Two
> stations at once ≈ 70A — the 50A main fuse blows. The firmware enforces one station
> at a time (`docs/FIRMWARE-GUIDE.md`); the fuse is the hardware backstop.

## 3. Station PTC branch — automotive relay via 2N2222 (×3, D4/D6/D8)

Each station's 3 PTC heaters (~25A) are switched by one 40A automotive relay (5-pin SPDT).

| Relay terminal | Goes to |
|---|---|
| 30 (COM) | 30A-fused 12V station branch |
| 87 (NO) | Thermal fuse 130 °C → parallel + leads of the 3 PTC heaters |
| 87a (NC) | unused |
| 85 (coil −) | 2N2222 collector |
| 86 (coil +) | 12V bus (after main disconnect, before station fuse) |

NPN driver stage (one per automotive relay — 4 total, incl. fan bus):

```
Mega pin (D4/D6/D8/D13) ──1 kΩ── 2N2222 base
2N2222 base ──10 kΩ── GND          (boot pull-down)
2N2222 emitter ── GND
2N2222 collector ── relay coil − (85)
Relay coil + (86) ── +12V
1N4007 across coil: cathode (band) to +12V, anode to collector
```

> Pin HIGH → base current → collector pulls 85 LOW → relay energizes.
> Pin floats/LOW at boot → relay OFF. 10 kΩ pull-down guarantees it.

**Heater side:** one 130 °C / 10A thermal fuse **per heater** in its + lead (9 total —
a group-shared 25A feed would exceed a thermal fuse's 10A rating). Mount each thermal
fuse against its heater housing. PTC − leads → ground rail.

## 4. Motor branch — 4-CH opto relay module (D5/D7/D9)

| Board pin | Goes to |
|---|---|
| VCC | 5V rail from buck (NOT a Mega pin) |
| GND | Ground rail |
| IN1 | Mega D5 (motor station 1) |
| IN2 | Mega D7 (motor station 2) |
| IN3 | Mega D9 (motor station 3) |
| IN4 | unused (spare) |
| CH1 COM | 3A-fused 12V motor branch 1 · CH1 NO → SGM-370 #1 + |
| CH2 COM | 3A-fused 12V motor branch 2 · CH2 NO → SGM-370 #2 + |
| CH3 COM | 3A-fused 12V motor branch 3 · CH3 NO → SGM-370 #3 + |
| Motor − leads | Ground rail |

Active-LOW: `digitalWrite(pin, LOW)` = relay ON. Onboard input pull-ups hold all
channels OFF while the Mega boots. Keep JD-VCC jumper ON (coils from buck 5V rail).

## 5. Fan power bus — automotive relay via 2N2222 (D13)

| Terminal | Goes to |
|---|---|
| 30 (COM) | 30A-fused 12V fan bus branch |
| 87 (NO) | ESC distribution block — red (VIN) of all 9 ESCs in parallel |
| 87a (NC) | unused |
| 85 (coil −) | 2N2222 collector (same driver stage as §3) |
| 86 (coil +) | +12V bus |
| 1N4007 | across coil, cathode to +12V |

D13 HIGH → all ESCs powered. D13 LOW → every fan dies instantly (emergency kill).
On the Mega, D13 also blinks the onboard LED when the fan bus is on — free indicator.

## 6. ESC + BLDC fan wiring (D10/D11/D12)

Each of the 9 BLDC fans ships with its own ESC. Per station, the 3 ESCs share one
Mega PWM pin (signal wires in parallel) and the switched 12V fan bus.

| ESC wire | Goes to |
|---|---|
| Red (VIN) | Fan bus from automotive relay 87 (10 AWG bus → 18 AWG pigtails) |
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
| battery main links | 4 AWG |
| Bank → disconnect → ANL fuse → bus | 8 AWG |
| Bus → station PTC fuse → relay → heaters | 10 AWG |
| Bus → fan fuse → relay → ESC distribution | 10 AWG (18 AWG ESC pigtails) |
| Bus → 3A motor fuse → module → motor | 18 AWG |
| Bus → 3A logic fuse → buck IN+ | 20 AWG |
| Buck OUT → 5V rail | 20 AWG |
| All Mega signal / sensor jumpers | 22 AWG |

## 10. Safety features

1. **50A ANL main fuse** — protects the battery feed
2. **30A per-station PTC fuse** + **30A fan bus fuse** + **3A ×3 motor fuses** + **3A logic fuse**
3. **PTC self-regulation** — current drops as element temperature rises
4. **130 °C one-shot thermal fuse per heater** (9×) — hardware cutoff, non-resettable
5. **DS18B20 firmware cutoff** at 65 °C — cuts PTC relays + motor relays + fan bus
6. **Boot-safe by design** — NPN stages have 10 kΩ base pull-downs (OFF), opto module
   channels have onboard pull-ups (OFF); firmware writes safe states first in `setup()`
7. **No mains voltage** — entire system is SELV
8. **Single-point DC ground** — all returns meet at one bus bar
9. **50A battery disconnect** — manual kill for everything
