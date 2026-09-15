# Wiring Reference — Arduino Mega 2560

Master connection list for every component. Pure 12V DC architecture: **all loads run from the battery bank** — no mains voltage, no inverter, no changeover switch. Pin map source: `docs/BOM.md` section 14.

## 0. Domains overview

| Domain | Source | Loads | Switched by |
|---|---|---|---|
| 12V DC | 2× LiFePO4 200Ah (parallel) → 25A main fuse | PTC heaters, BLDC fans, worm motors | Relay modules (PTC + motors), automotive relay (fan bus), ESC PWM (fans) |
| 5V DC | LM2596S buck (12V→5V) | Mega, sensors, LCD, relay coils, ESC logic | — |

## 1. Pin map — Mega 2560 side

| Mega pin | Direction | Connects to | Wire / notes |
|---|---|---|---|
| 5V | power in | LM2596S buck OUT+ (set 5.00 V) | 22 AWG — never the barrel jack |
| GND | common | Ground rail (DC side) | 22 AWG |
| D2 | in | DHT22 DATA | 22 AWG |
| D3 | in | DS18B20 yellow DATA | + 4.7 kΩ pull-up D3→5V |
| D4 | out | 2-CH relay #1 ch1 — Station 1 PTC heaters (3× 100W) | + 10 kΩ pull-up to VCC (active-LOW) |
| D5 | out | 2-CH relay #1 ch2 — Station 2 PTC heaters (3× 100W) | + 10 kΩ pull-up |
| D6 | out | 2-CH relay #2 ch1 — Station 1 motor (SGM-370) | + 10 kΩ pull-up |
| D7 | out | 2-CH relay #2 ch2 — Station 2 motor (SGM-370) | + 10 kΩ pull-up |
| D8 | out | 2-CH relay #3 ch1 — Station 3 motor (SGM-370) | + 10 kΩ pull-up |
| D9 | out | 40A automotive relay (fan power bus) — via 2N2222 NPN + 1 kΩ base resistor | Relay coil + → D9, relay coil − → GND |
| D10 | out | ESC #1 PWM signal — Station 1 BLDC fans (3× parallel) | Servo library, 50 Hz |
| D11 | out | ESC #2 PWM signal — Station 2 BLDC fans (3× parallel) | Servo library, 50 Hz |
| D12 | out | ESC #3 PWM signal — Station 3 BLDC fans (3× parallel) | Servo library, 50 Hz |
| D13 | in | Start button — arcade switch side (other side → GND) | INPUT_PULLUP; arcade LED ring: + → 5V, − → GND |
| 20/21 | I2C | LCD SDA / SCL | addr 0x27/0x3F |

## 2. 12V DC power distribution

| From | To | Wire | Protection |
|---|---|---|---|
| Battery + (parallel bank) | DC rocker switch | 12 AWG | — |
| DC rocker | **25A main fuse** → barrier block MAIN | 12 AWG | 25 A blade fuse |
| Unit A ↔ Unit B parallel links | battery-to-battery bus | 4 AWG | — |
| MAIN | Station 1 branch: **20A fuse** → relay COM→NO → PTC heaters 3×100W + motor | 14 AWG | 20 A |
| MAIN | Station 2 branch: **20A fuse** → relay COM→NO → PTC heaters 3×100W + motor | 14 AWG | 20 A |
| MAIN | Station 3 branch: **20A fuse** → relay COM→NO → PTC heaters 3×100W + motor | 14 AWG | 20 A |
| MAIN | Fan bus: **15A fuse** → automotive relay COM→NO → ESCs (9 fans) | 14 AWG | 15 A |
| MAIN | Logic: **3A fuse** → buck IN+ | 16 AWG | 3 A |
| Motor − / relay GND | Ground rail (DC) | — | single point |
| Buck OUT+ (5V) | Mega 5V, relay VCCs, sensors, LCD, ESC logic VCC | 22 AWG | set 5.00 V first |

## 3. Relay module wiring

### 3-CH relay module (D4–D8) — PTC heaters + motors

| Board pin | Goes to |
|---|---|
| VCC | 5V rail (NOT a Mega pin) |
| GND | DC ground rail |
| IN1 | Mega D4 (Station 1 PTC) |
| IN2 | Mega D5 (Station 2 PTC) |
| IN3 | Mega D6 (Station 1 motor) |
| IN4 | Mega D7 (Station 2 motor) |
| IN5 | Mega D8 (Station 3 motor) |
| COM/NO | 12V station branches |

### 40A automotive relay (D9) — BLDC fan power bus

| Terminal | Goes to |
|---|---|
| 30 (COM) | 12V main bus (after 15A fuse) |
| 87 (NO) | ESC VIN pins (9 fans in parallel) |
| 85 (coil +) | Mega D9 via 2N2222 NPN collector |
| 86 (coil −) | GND |
| 87a (NC) | unused |

The 2N2222 NPN transistor switches the relay coil: D9 HIGH → base current through 1 kΩ → collector pulls 86 LOW → relay energizes → fan bus powered. A flyback diode (1N4007) across the relay coil protects the transistor.

### ESC wiring (D10–D12) — BLDC fan control

| ESC wire | Goes to |
|---|---|
| Red (VIN) | Fan bus 12V (from automotive relay NO) |
| Black (GND) | Common ground |
| White/Orange (Signal) | Mega D10 (Station 1) / D11 (Station 2) / D12 (Station 3) |

3 BLDC fans per station are wired in parallel to their station's ESC. ESC arming sequence: write `SERVO_MIN` at boot, delay 2s, then write `FAN_OFF`.

## 4. Safety features

1. **25A main fuse** — protects the entire DC bus
2. **20A per-station fuses** — isolate heater + motor faults
3. **15A fan bus fuse** — protects BLDC fan branch
4. **PTC self-regulation** — heaters reduce current as temperature rises
5. **Thermal fuse (130°C)** on each heater cluster — permanent cutoff
6. **DS18B20 firmware cutoff** — software temperature limit
7. **No mains voltage** — entire system is SELV (Safety Extra Low Voltage)
8. **Single-point DC ground** — all returns meet at one bus bar
