# Wiring Reference — Arduino Mega 2560 (Rev 4)

Master connection list for every component. Pin map source of truth: `docs/BOM.md` section 15; visual map: `docs/BLOCK-DIAGRAM.md`. Cross-checked against the Rev 4 wiring audit.

## 1. Pin map — Mega 2560 side

| Mega pin | Direction | Connects to | Wire / notes |
|---|---|---|---|
| 5V | power in | LM2596S buck OUT+ (set 5.00 V) | 22 AWG — NEVER the barrel jack, never 12 V |
| GND | common | Ground rail at barrier block | 22 AWG — single-point ground |
| D2 | digital in | DHT22 DATA | 22 AWG |
| D3 | digital in | DS18B20 yellow DATA | 22 AWG + 4.7 kΩ pull-up from D3 to 5V |
| D4 | digital out | Heater relay board IN (30 A 1-ch, active-LOW) | 22 AWG + 10 kΩ pull-up to relay VCC |
| D5 | digital out | 2-CH relay #1, ch1 IN — Station 1 motor | 22 AWG + 10 kΩ pull-up to relay VCC |
| D6 | digital out | 2-CH relay #1, ch2 IN — Station 2 motor | 22 AWG + 10 kΩ pull-up to relay VCC |
| D7 | digital out | 2-CH relay #2, ch1 IN — Station 3 motor | 22 AWG + 10 kΩ pull-up to relay VCC |
| D8 | digital out | 2-CH relay #2, ch2 IN — chamber fan purge (optional) | 22 AWG + 10 kΩ pull-up to relay VCC |
| D9 | digital out | Green LED anode (through 220 Ω) | LED cathode to GND |
| D10 | digital out | Yellow LED anode (through 220 Ω) | LED cathode to GND |
| D11 | digital out | Red LED anode (through 220 Ω) | LED cathode to GND |
| D12 | digital out | Active buzzer + | Buzzer − to GND |
| D13 | digital in | Start button (other leg to GND) | INPUT_PULLUP in firmware — no resistor |
| 20 (SDA) | I2C data | LCD 16×2 I2C SDA | 22 AWG |
| 21 (SCL) | I2C clock | LCD 16×2 I2C SCL | 22 AWG |

Unused but reserved: Serial0 (pins 0/1) stays free for USB debugging.

## 2. Power distribution (12 V side — none of this touches the Mega)

| From | To | Wire | Protection |
|---|---|---|---|
| Battery + (12.8 V) | Rocker switch in | 16 AWG | — |
| Rocker out | 25 A main fuse → barrier MAIN | 16 AWG | 25 A blade |
| MAIN | Heater branch: 15 A fuse → heater relay COM | 16 AWG | 15 A blade |
| Heater relay NO | PTC heater + , PTC blower + , chamber fan + (parallel) | 16 AWG | — |
| Heater − / blower − / fan − | Ground rail | 16 AWG | — |
| MAIN | Station 1: 3 A fuse → relay #1 ch1 COM | 18 AWG | 3 A blade |
| MAIN | Station 2: 3 A fuse → relay #1 ch2 COM | 18 AWG | 3 A blade |
| MAIN | Station 3: 3 A fuse → relay #2 ch1 COM | 18 AWG | 3 A blade |
| Relay NO (each) | Motor + (that station) | 18 AWG | — |
| Motor − (each) | Ground rail | 18 AWG | — |
| MAIN | Logic: 3 A fuse → buck IN+ | 16 AWG | 3 A blade |
| Buck OUT+ / OUT− | 5 V rail: Mega 5V, relay VCCs, sensors, LCD | 22 AWG | buck set 5.00 V |
| Battery − | Ground rail (single point) | 16 AWG | — |

## 3. Component-by-component

### DHT22 (humidity — core feedback)
| DHT22 pin | Goes to |
|---|---|
| VCC (+) | 5 V rail |
| DATA | Mega D2 |
| GND (−) | Ground rail |
Mount mid-chamber, away from air jets. Read interval ≥ 2 s.

### DS18B20 waterproof (heater-zone temp)
| DS18B20 wire | Goes to |
|---|---|
| Red | 5 V rail |
| Yellow | Mega D3 + 4.7 kΩ to 5 V |
| Black | Ground rail |
Probe in the heater air stream.

### LCD 16×2 with I2C backpack
| LCD pin | Goes to |
|---|---|
| VCC | 5 V rail |
| GND | Ground rail |
| SDA | Mega 20 (SDA) |
| SCL | Mega 21 (SCL) |
Address 0x27 or 0x3F (scan if blank).

### Relay boards (all three)
| Board pin | Goes to |
|---|---|
| VCC | 5 V rail (NOT a Mega pin) |
| GND | Ground rail |
| IN1–IN4 | Mega D4–D8 per table above |
| COM / NO | 12 V load branch per section 2 |
Keep the JD-VCC jumper in place (coils fed from the 5 V rail). Active-LOW boards: pin LOW = relay ON.

### Motors ×3 (via relay contacts)
Motor + → that station's relay NO; motor − → ground rail. One 3 A fuse per station branch. Polarity sets direction — swap if a station spins the wrong way.

### PTC heater 100 W + blower + chamber fan
All three in parallel on the heater branch behind the 15 A fuse, switched by the 30 A relay. Air always moves when heat is on.

### LEDs / buzzer / button
Per pin map above. 220 Ω in series with each LED is mandatory.

## 4. Rules that keep this wiring safe

1. Mega never sees 12 V — buck 5 V to the 5V pin only.
2. Relay coils and board VCC from the buck rail; Mega pins drive only optocoupler LEDs (2–5 mA).
3. 10 kΩ pull-ups on every relay IN to its board VCC — boards stay OFF while the Mega boots (floating inputs otherwise).
4. Relay contacts are 30 VDC-rated — mains AC prohibited.
5. Single-point ground: every − returns to one ground rail; chassis bonds to − at one bolt.
6. Heater duty cycling is slow (2–5 s period) — fast PWM destroys the contacts.
7. Every wall pass-through gets a rubber grommet; nothing within 50 mm of the heater body.
