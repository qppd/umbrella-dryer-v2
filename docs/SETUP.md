# Setup Guide — 12V DC

> Complete setup instructions for the 12V DC umbrella dryer. No mains wiring required.

---

## 1. Unbox and verify

- [ ] Battery bank: 1× LiFePO4 12.8V 200Ah with BMS
- [ ] Charger: 14.6V 20A LiFePO4 charger
- [ ] Mega 2560 clone + USB cable
- [ ] 4× LCTC DC-DC SSR 40A (for PTC heaters + fan bus) + 3× LCTC DC-DC SSR 10A (for motors)
- [ ] 7× SSR heatsinks (~₱50 each)
- [ ] 9× PTC ceramic heaters (12V 100W) — verify 12V, not 220V!
- [ ] 9× BLDC fan modules (50mm, with ESC) — verify ESC included
- [ ] 3× SGM-370 worm gear motors
- [ ] 3× PETIYOUZA rigid flange coupling (6mm bore)
- [ ] DHT22 module, DS18B20 waterproof, LCD 16×2 I2C
- [ ] LM2596S buck module
- [ ] LEDs (R/Y/G), buzzer, arcade button
- [ ] Wire kit (6–18 AWG silicone), connectors, heat-shrink
- [ ] Zip ties, M3/M4 screws, sealant, drip tray, velcro, grommets

---

## 2. Firmware upload

1. Install Arduino IDE.
2. Install libraries: DHT sensor library, OneWire, DallasTemperature, LiquidCrystal_I2C (Adafruit Unified Sensor is a dependency).
3. Open the sketch from `FIRMWARE-GUIDE.md` (copy the complete sketch into a new `.ino` file).
4. Select board: **Arduino Mega 2560**. Select correct COM port.
5. Upload. Open Serial Monitor at 115200 baud — should print "Umbrella Dryer V2 — 12V DC System Boot Initializing".

---

## 3. Buck module calibration (BEFORE connecting to Mega)

1. Disconnect buck output from Mega.
2. Connect buck input to 12V battery (or any 12V source).
3. Measure buck output with multimeter.
4. Turn potentiometer until output reads **5.0V ± 0.1V**.
5. **IMPORTANT:** On the Mega, connect buck OUT+ to the **5V pin** — NOT the barrel jack.
6. Disconnect 12V input. Now safe to wire to Mega.

---

## 4. Mechanical assembly

1. **Frame:** Build 3-station frame. Each station holds 1 umbrella inverted.
2. **Motor mounts:** Attach SGM-370 motors to aluminum plates. Align motor output shaft center with umbrella hub center.
3. **Couplings:** Connect each SGM-370 output shaft directly to the umbrella hub with a 6mm-bore PETIYOUZA rigid flange coupling (no separate shaft, no pillow blocks).
4. **Verify:** Spin by hand. Should rotate freely with no binding. Motor is self-locking.

---

## 5. Wiring

### 5a. Power distribution

1. Connect battery positives (main link) and negatives (main link) — use 8 AWG.
2. Battery + → 2-pin screw terminal → **positive 150A bus bar** — 8 AWG.
3. From the **positive bus bar**, run branches:
   - Station 1 PTC: 10 AWG → LCTC DC-DC SSR 40A (D4) → 3 PTC heaters
   - Station 2 PTC: 10 AWG → LCTC DC-DC SSR 40A (D6) → 3 PTC heaters
   - Station 3 PTC: 10 AWG → LCTC DC-DC SSR 40A (D8) → 3 PTC heaters
   - Fan bus: 10 AWG → LCTC DC-DC SSR 40A (D13) → ESC distribution
   - Motor 1/2/3: 18 AWG → LCTC DC-DC SSR 10A (D5/D7/D9) → SGM-370 motor
   - Logic: 20 AWG → buck module → 5V to Mega

### 5b. SSR wiring (for each LCTC DC-DC SSR — 7 total)

| SSR terminal | Goes to |
|---|---|
| IN+ | Mega pin (D4/D6/D8 for PTC, D13 for fan, D5/D7/D9 for motor) |
| IN− | GND |
| COM (input side) | +12V bus |
| NO (output side) | Load (heaters/fans/motors) |

Active-HIGH: `digitalWrite(pin, HIGH)` = SSR ON. Onboard optocoupler holds SSR OFF at boot.

### 5c. ESC wiring

1. Each ESC has 3 wires: black (GND), red (VCC 12V), white/orange (signal).
2. Connect ESC GND → common GND bus.
3. Connect ESC VCC → fan bus relay output (switched 12V from 40A auto relay).
4. Connect ESC signal → Mega D10 (station 1), D11 (station 2), D12 (station 3).

### 5e. Sensor wiring

1. DHT22: VCC→5V, GND→GND, DATA→D2 with 10kΩ pull-up to 5V.
2. DS18B20: Red→5V, Black→GND, White/Yellow→D3 with 4.7kΩ pull-up to 5V.
3. LCD I2C: VCC→5V, GND→GND, SDA→**D20**, SCL→**D21** (Mega I2C pins, NOT A4/A5).

### 5f. UI wiring

1. Arcade button: pin 1→D14, pin 2→GND (internal pull-up). LED ring: +→5V, −→GND.
2. LEDs: anode→D15(red)/D16(yellow)/D17(green) via 220Ω, cathode→GND.
3. Buzzer: +→D18, −→GND.

---

## 6. Power-on test (no load)

1. **Disconnect all SSR outputs** (no PTC heaters, no motors, no fans yet).
2. Connect battery.
3. Buck LED should light. Measure 5V at Mega 5V pin.
4. Mega should boot. LCD shows "Umbrella Dryer V2 DC SYSTEM".
5. ESCs should arm (fan twitch or beep) — D13 briefly turns on during arming.
6. After 2s, LCD settles on "SYSTEM READY / Press Button".
7. Press button → should enter PREHEAT phase on LCD.
8. Press again → should emergency stop back to IDLE.

---

## 7. Functional test (with loads)

1. Reconnect SSR outputs to PTC heaters, motors, and fans.
2. Press button → fans spin up, PTC heaters warm (feel heat after 30s).
3. Wait for DHT22 to read ≥45°C → motor starts spinning (staged — one at a time).
4. Timer counts down 15 min → enters COOL phase for 2 min.
5. Buzzer beeps 3× → COMPLETE. Press button to reset to IDLE.

---

## 8. Thermal test

1. Run cycle. Monitor DS18B20 temperature on LCD.
2. Temperature should rise during PREHEAT/DRY (40–60°C expected).
3. Verify: if DS18B20 reads >65°C, everything should shut off (thermal cutoff).
4. Let system cool. Verify fans run during COOL phase.
