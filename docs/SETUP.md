# Setup Guide (Rev 7 — 12V DC)

> Complete setup instructions for the 12V DC umbrella dryer. No mains wiring required.

---

## 1. Unbox and verify

- [ ] Battery bank: 2× LiFePO4 12.8V 200Ah with BMS
- [ ] Charger: 14.6V 20A LiFePO4 charger
- [ ] Mega 2560 clone + USB cable
- [ ] 2× 2-CH relay modules + 1× automotive 40A relay
- [ ] 9× PTC ceramic heaters (12V 100W) — verify 12V, not 220V!
- [ ] 9× BLDC fan modules (50mm, with ESC) — verify ESC included
- [ ] 3× SGM-370 worm gear motors
- [ ] 3× KP08 pillow block bearing (6mm bore)
- [ ] 3× 6mm × 300mm shafts
- [ ] 2× rigid coupling sets (use 6×8 bore)
- [ ] DHT22 module (Black), DS18B20 waterproof, LCD 16×2 I2C
- [ ] LM2596S buck module
- [ ] LEDs (R/Y/G), buzzer, arcade button, DC rockers
- [ ] Wire kit (6–18 AWG silicone), fuses, connectors, heat-shrink
- [ ] Zip ties, M3/M4 screws, sealant, drip tray, velcro, grommets

---

## 2. Firmware upload

1. Install Arduino IDE.
2. Install libraries: DHT sensor library, OneWire, DallasTemperature, LiquidCrystal_I2C (Adafruit Unified Sensor is a dependency).
3. Open the sketch from `FIRMWARE-GUIDE.md` (copy the complete sketch into a new `.ino` file).
4. Select board: **Arduino Mega 2560**. Select correct COM port.
5. Upload. Open Serial Monitor at 115200 baud — should print "Umbrella Dryer V2 — Rev 7 (12V DC + BLDC)".

---

## 3. Buck module calibration (BEFORE connecting to Mega)

1. Disconnect buck output from Mega.
2. Connect buck input to 12V battery (or any 12V source).
3. Measure buck output with multimeter.
4. Turn potentiometer until output reads **5.0V ± 0.1V**.
5. Disconnect 12V input. Now safe to wire to Mega.

---

## 4. Mechanical assembly

1. **Frame:** Build 3-station frame. Each station holds 1 umbrella inverted.
2. **Motor mounts:** Attach SGM-370 motors to aluminum plates. Align shaft center with umbrella hub center.
3. **Shafts:** Insert 6mm × 300mm shafts through KP08 pillow blocks. Connect motor shaft to umbrella shaft via 6×8 rigid coupling.
4. **Verify:** Spin by hand. Should rotate freely with no binding. Motor is self-locking (holds umbrella in place when off).

---

## 5. Wiring

### 5a. Power distribution

1. Connect battery positive → 25A main fuse → DC rocker switch.
2. From fused side, run 14 AWG to terminal block (DC distribution bus).
3. From distribution bus, run fused branches:
   - 3× 10A fuses → PTC heater groups (3 heaters in parallel per station)
   - 3× 3A fuses → worm motors (one per station)
   - 1× 15A fuse → BLDC fan power bus
   - 1× 3A fuse → buck module → 5V logic

### 5b. Relay wiring

1. Connect relay module VCC → 5V, GND → GND.
2. Connect Mega D4 → relay 1A IN, D5 → relay 1B IN (PTC groups).
3. Connect Mega D6 → relay 2A IN, D7 → relay 2B IN (motors station 1 & 2).
4. Automotive relay: connect coil− → GND, coil+ → D9 via NPN transistor (2N2222) with 1kΩ base resistor. NO contacts switch 12V to fan bus.

### 5c. ESC wiring

1. Each ESC has 3 wires: black (GND), red (VCC 12V), white/orange (signal).
2. Connect ESC GND → common GND bus.
3. Connect ESC VCC → fan bus relay output (switched 12V).
4. Connect ESC signal → Mega D10 (station 1), D11 (station 2), D12 (station 3).

### 5d. Sensor wiring

1. DHT22: VCC→5V, GND→GND, DATA→D2 with 10kΩ pull-up to 5V.
2. DS18B20: Red→5V, Black→GND, White→D3 with 4.7kΩ pull-up to 5V.
3. LCD I2C: VCC→5V, GND→GND, SDA→A4, SCL→A5.

### 5e. UI wiring

1. Arcade button: pin 1→D13, pin 2→GND (internal pull-up).
2. LEDs: anode→D14/D15/D16 via 220Ω, cathode→GND.
3. Buzzer: +→D17, −→GND.

---

## 6. Power-on test (no load)

1. **Disconnect all relay outputs** (no PTC heaters, no motors, no fans yet).
2. Connect battery. Flip DC rocker.
3. Buck LED should light. Measure 5V at Mega Vin.
4. Mega should boot. LCD shows "Umbrella Dryer / Rev 7 - 12V DC".
5. ESCs should arm (brief beep or twitch from fans).
6. After 2s, LCD shows "READY / Press to start".
7. Press button → should enter PREHEAT phase on LCD.
8. Press again → should emergency stop back to IDLE.

---

## 7. Functional test (with loads)

1. Reconnect relay outputs to PTC heaters, motors, and fans.
2. Press button → fans spin up, PTC heaters warm (feel heat after 30s).
3. Wait for DHT22 to read ≥45°C → motor starts spinning.
4. Timer counts down 15 min → motor stops, PTC off, fans cool for 2 min.
5. Buzzer beeps 3× → DONE. Press button to reset to IDLE.

---

## 8. Thermal test

1. Run cycle. Monitor DS18B20 temperature on LCD.
2. Temperature should rise during PREHEAT/DRY (40–60°C expected).
3. Verify: if DS18B20 reads >65°C, everything should shut off (thermal cutoff).
4. Let system cool. Verify fans run during COOL phase.
