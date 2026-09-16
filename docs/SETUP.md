# Setup Guide — 12V DC

> Complete setup instructions for the 12V DC umbrella dryer. No mains wiring required.

---

## 1. Unbox and verify

- [ ] Battery bank: 2× LiFePO4 12.8V 200Ah with BMS
- [ ] Charger: 14.6V 20A LiFePO4 charger
- [ ] Mega 2560 clone + USB cable
- [ ] 4× 40A automotive relay (5-pin SPDT) + 1× 4-CH opto module
- [ ] 4× 2N2222 + 4× 1kΩ + 4× 10kΩ + 4× 1N4007 (NPN driver components)
- [ ] 9× PTC ceramic heaters (12V 100W) — verify 12V, not 220V!
- [ ] 9× thermal fuse 130°C / 10A
- [ ] 9× BLDC fan modules (50mm, with ESC) — verify ESC included
- [ ] 3× SGM-370 worm gear motors
- [ ] 6× KP08 pillow block bearing (6mm bore)
- [ ] 3× 6mm × 300mm shafts
- [ ] 2× rigid coupling sets (use 6×8 bore)
- [ ] DHT22 module, DS18B20 waterproof, LCD 16×2 I2C
- [ ] LM2596S buck module
- [ ] LEDs (R/Y/G), buzzer, arcade button, 50A disconnect switch
- [ ] Wire kit (6–18 AWG silicone), fuses, connectors, heat-shrink
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
2. **Motor mounts:** Attach SGM-370 motors to aluminum plates. Align shaft center with umbrella hub center.
3. **Shafts:** Insert 6mm × 300mm shafts through KP08 pillow blocks. Connect motor shaft to umbrella shaft via 6×8 rigid coupling.
4. **Verify:** Spin by hand. Should rotate freely with no binding. Motor is self-locking.

---

## 5. Wiring

### 5a. Power distribution

1. Connect battery positives (parallel link) and negatives (parallel link) — use 4 AWG.
2. Battery + → 50A disconnect switch → 50A ANL main fuse → terminal block (DC distribution bus) — 8 AWG.
3. From distribution bus, run fused branches:
   - Station 1: 30A fuse → 40A auto relay (D4 via NPN) → thermal fuses → 3 PTC heaters
   - Station 2: 30A fuse → 40A auto relay (D6 via NPN) → thermal fuses → 3 PTC heaters
   - Station 3: 30A fuse → 40A auto relay (D8 via NPN) → thermal fuses → 3 PTC heaters
   - Fan bus: 30A fuse → 40A auto relay (D13 via NPN) → ESC distribution
   - Motor 1/2/3: 3A fuse each → opto module → SGM-370 motor
   - Logic: 3A fuse → buck module → 5V to Mega

### 5b. NPN driver stage (for each 40A automotive relay — 4 total)

```
Mega pin (D4/D6/D8/D13) ── 1kΩ ── 2N2222 base
2N2222 base ── 10kΩ ── GND                    (boot pull-down)
2N2222 emitter ── GND
2N2222 collector ── relay coil − (pin 85)
Relay coil + (pin 86) ── +12V bus (after main fuse)
1N4007 across coil: cathode (band) → +12V, anode → collector
```

### 5c. Opto module wiring (for worm motors)

1. Module VCC → 5V buck rail (NOT Mega pin). Module GND → GND rail.
2. Mega D5 → module IN1, D7 → IN2, D9 → IN3 (active-LOW: LOW = ON).
3. Module COM/NO → 3A-fused 12V → motor + / motor − → GND.
4. Keep JD-VCC jumper ON.

### 5d. ESC wiring

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

1. **Disconnect all relay outputs** (no PTC heaters, no motors, no fans yet).
2. Connect battery. Flip 50A disconnect switch.
3. Buck LED should light. Measure 5V at Mega 5V pin.
4. Mega should boot. LCD shows "Umbrella Dryer V2 DC SYSTEM".
5. ESCs should arm (fan twitch or beep) — D13 briefly turns on during arming.
6. After 2s, LCD settles on "SYSTEM READY / Press Button".
7. Press button → should enter PREHEAT phase on LCD.
8. Press again → should emergency stop back to IDLE.

---

## 7. Functional test (with loads)

1. Reconnect relay outputs to PTC heaters, motors, and fans.
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
