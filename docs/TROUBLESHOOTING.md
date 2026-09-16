# Troubleshooting — 12V DC

> All voltages are 12V DC or 5V logic. No mains voltage in this system.

---

## 1. Power issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing turns on | Disconnect switch off / battery disconnected | Flip 50A disconnect; check battery terminals; verify 50A ANL main fuse |
| Buck LED off | Fuse blown / battery dead | Check 3A logic fuse; measure battery voltage (>12.0V) |
| Buck output ≠ 5V | Potentiometer misadjusted | Re-calibrate buck with multimeter BEFORE connecting to Mega 5V pin |
| Mega won't boot | Buck not providing 5V | Verify 5V at Mega **5V pin** (NOT barrel jack); check GND continuity |
| Battery dies fast | Too many stations running | Run staged operation (one at a time); check for shorts |

---

## 2. Sensor issues

| Symptom | Likely cause | Fix |
|---|---|---|
| DHT22 reads NaN | Wiring / library issue | Check VCC→5V, GND→GND, DATA→D2 with 10kΩ pull-up; use DHT22 **module** |
| DHT22 reads 0% or 100% | Damaged sensor or wiring | Replace DHT22; verify no solder bridges |
| DS18B20 reads −127°C | Bad connection / missing pull-up | Check white wire→D3 with 4.7kΩ pull-up; run OneWire scanner |
| DS18B20 reads 85°C only | Power issue (parasitic mode) | Connect VCC (red wire) to 5V |
| Temperature too high / low | Probe placement | Mount DS18B20 in heater air stream, not on metal surface |

---

## 3. LCD issues

| Symptom | Likely cause | Fix |
|---|---|---|
| LCD blank | Wrong I2C address | Try 0x3F instead of 0x27; use I2C scanner sketch |
| LCD shows squares | I2C not initialized | Call `lcd.init()` not `lcd.begin()`; **on Mega, I2C is pins 20/21 — NOT A4/A5** |
| LCD flickers | Loose connection | Check VCC, GND, SDA→D20, SCL→D21; reseat dupont connectors |

---

## 4. PTC relay issues (40A automotive + 2N2222)

| Symptom | Likely cause | Fix |
|---|---|---|
| PTC relay doesn't click | NPN circuit not driving coil | Check: D4/D6/D8 → 1kΩ → 2N2222 base; collector → coil 85; coil 86 → +12V; emitter → GND; 10kΩ base-to-GND pull-down present |
| Relay clicks but heaters stay off | Wrong COM/NO terminals | Verify: fused 12V → COM (30), heaters → NO (87); check 30A branch fuse |
| Relay stays ON at boot | Pull-down resistor missing | Add 10kΩ between 2N2222 base and GND; verify `allOff()` in setup |
| Load turns on/off randomly | Floating base pin | Ensure 10kΩ pull-down; enable `pinMode(OUTPUT)` + default LOW in setup |

---

## 5. Motor relay issues (opto module)

| Symptom | Likely cause | Fix |
|---|---|---|
| Motor relay doesn't click | Module not powered / wrong pin | Check: module VCC → 5V buck rail (NOT Mega pin); D5/D7/D9 → IN1/IN2/IN3; active-LOW: LOW = ON |
| Relay clicks but motor stays off | Wrong COM/NO / fuse blown | Check COM→3A-fused 12V, NO→motor +; verify 3A fuse intact |
| Motor spins wrong direction | Polarity reversed | Swap the two motor leads (DC motor direction = polarity) |
| Motor hums but doesn't spin | Coupling misaligned / shaft binding | Loosen coupling; realign; check KP08 pillow blocks |

---

## 6. Fan bus relay issues (40A automotive + NPN)

| Symptom | Likely cause | Fix |
|---|---|---|
| All 9 fans don't start | Fan bus relay not ON | Check D13 → 1kΩ → 2N2222 → coil; measure 12V at ESC VIN after D13 goes HIGH |
| Fan bus relay clicks but no power at ESCs | Wrong COM/NO | Verify: 30A-fused 12V → COM (30); ESC distribution → NO (87) |
| D13 LED (built-in Mega) doesn't blink | Firmware not driving D13 | Verify `allOff()` / `fansOn()` functions |

---

## 7. ESC / BLDC fan issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Fan doesn't spin | ESC not armed | Verify `esc.attach()` + `esc.writeMicroseconds(1000)` for 2s on boot; D13 must be HIGH during arming |
| Fan spins then stops | ESC lost signal | Ensure `esc.write()` called continuously; check D10/D11/D12 wiring |
| ESC gets hot | Drawing too much current | Verify fan current < 3.2A each; check 30A fan bus fuse |
| Fan vibrates excessively | Bent propeller / unbalanced | Check propeller; ensure duct clears blades |

---

## 8. Motor issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Motor doesn't relay not switching | Fuse blown / module unpowered | Check D5/D7/D9 wiring; verify 3A motor fuse; check module VCC→5V |
| Motor stalls under load | Insufficient torque | Verify umbrella not too heavy (<3 kg·cm); check 12V supply |
| Motor holds when off | That's correct! | SGM-370 worm gear is self-locking by design |

---

## 9. Thermal issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Thermal cutoff triggers immediately | DS18B20 reads >65°C at boot | Move probe away from direct contact with heater; mount in air stream |
| PTC heaters don't get hot | Relay not switching / wrong voltage | Verify 12V at PTC terminals; check NPN relay circuit; confirm 12V heaters (not 220V) |
| Chamber too hot (>60°C) | Multiple stations active | Ensure staged operation (firmware enforces one at a time); check `activeStation` rotation |
| Burning smell | Wiring too thin / loose | Check wire gauges (10 AWG heater branches, 8 AWG main); tighten all terminals |

---

## 10. Battery issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Battery voltage drops fast | High current draw / old battery | Run staged operation; check for shorts; verify BMS functioning |
| Battery won't charge | Wrong charger | Use 14.6V LiFePO4 charger ONLY |
| BMS disconnects | Over-discharge / over-current | Recharge; check total current draw stays within BMS limits |

---

## 11. Fuse issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Main fuse (50A ANL) blows | Total current > 50A | Multiple stations active? Verify staged operation; check for short |
| Station PTC fuse (30A) blows | Single station overcurrent | Check PTC heater count (3 max per station); verify wiring gauge |
| Fan bus fuse (30A) blows | Fan bus short / all fans jammed | Check fan wiring; verify no bare wire on bus |
| Motor fuse (3A) blows | Motor jam / stall | Remove umbrella jam; replace fuse |
| Fuse blows immediately | Dead short | Trace wiring with multimeter (continuity mode); check for bare wire touching chassis |

---

## 12. Debug mode

Add to sketch for verbose Serial output:

```cpp
// Add in loop():
Serial.print("Phase: "); Serial.print(currentPhase);
Serial.print(" | Stn: "); Serial.print(activeStation);
Serial.print(" | H: "); Serial.print(humidity);
Serial.print(" | T: "); Serial.print(temperature);
Serial.print(" | PTC1: "); Serial.print(digitalRead(PIN_RELAY_PTC_1));
Serial.print(" | PTC2: "); Serial.print(digitalRead(PIN_RELAY_PTC_2));
Serial.print(" | PTC3: "); Serial.print(digitalRead(PIN_RELAY_PTC_3));
Serial.print(" | FAN: "); Serial.println(digitalRead(PIN_RELAY_FAN_BUS));
```
