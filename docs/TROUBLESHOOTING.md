# Troubleshooting — 12V DC

> All voltages are 12V DC or 5V logic. No mains voltage in this system.

---

## 1. Power issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing turns on | Rocker switch off / battery cable loose | Flip the 50A rocker ON; check battery terminals and the 2-pin screw terminal |
| Buck LED off | Battery dead / input wiring loose | Measure battery voltage (>12.0V); check the buck input taps on the positive bus |
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
| LCD flickers | Loose connection | Check VCC, GND, SDA→D20, SCL→D21; reseat wire connections |

---

## 4. PTC SSR issues (SSR-40DD, D4/D6/D8)

| Symptom | Likely cause | Fix |
|---|---|---|
| PTC heaters stay cold | SSR input not driven | Check: D4/D6/D8 → SSR IN+, SSR IN− → GND; measure ~5V at IN+ when the pin is HIGH |
| SSR input powered, heaters still off | Output side miswired | Verify +12V bus → SSR output COM, heaters → output NO; reseat the 10 AWG heater leads |
| Heaters flicker on/off | Loose input jumper | Reseat IN+/IN− wires; check the Mega pin header |
| SSR overheats / shuts down | Heatsink missing or dry | Mount the SSR Heatsink BLACK with thermal paste; keep ≤25A per 40A SSR |
| SSR stays ON at boot | Firmware not writing safe states | Verify `allOff()` runs first in `setup()` |

---

## 5. Motor SSR issues (SSR-10A, D5/D7/D9)

| Symptom | Likely cause | Fix |
|---|---|---|
| Motor stays off | SSR input not driven | Check D5/D7/D9 → SSR IN+, IN− → GND; ~5V at IN+ when commanded |
| Motor stays off (input OK) | Output side miswired | Verify 18 AWG motor branch → SSR output side; motor + → the other output terminal |
| Motor spins wrong direction | Polarity reversed | Swap the two motor leads (DC motor direction = polarity) |
| Motor hums but doesn't spin | Coupling misaligned / shaft binding | Loosen rigid + flange couplings; realign motor → shaft → hub; check the shaft spins freely in the UCP06 pillow block |

---

## 6. Fan bus issues (SSR-40DD, D13)

| Symptom | Likely cause | Fix |
|---|---|---|
| All 9 blowers dead | Fan bus SSR off / miswired | Measure 12V at the blower distribution block after D13 goes HIGH; check SSR output side |
| Bus powered, one blower dead | That blower's wiring | Check its VIN/GND pigtails and PWM lead |
| D13 LED (built-in Mega) doesn't blink | Firmware not driving D13 | Verify `allOff()` / `fansOn()` functions |

---

## 7. Blower PWM issues (D10/D11/D12)

| Symptom | Likely cause | Fix |
|---|---|---|
| Blower doesn't spin | PWM duty 0 or fan bus off | Raise `analogWrite(D10–D12, …)`; confirm D13 HIGH |
| Blower spins then stops | Loose PWM lead | Reseat the signal wire — 3 leads share one pin, find the loose one |
| Blower always full speed | PWM lead on 5V by mistake | Signal must go to D10/D11/D12 only |
| Blower weak | Low duty cycle / low bus voltage | Increase duty; verify 12V at the fan bus |
| Blower vibrates excessively | Mount loose / unbalanced | Tighten mount; check impeller clearance |

---

## 8. Motor issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Motor doesn't run | SSR not switching | Check D5/D7/D9 wiring and the SSR output side (see §5) |
| Motor stalls under load | Insufficient torque | Verify umbrella load (<3 kg·cm); check 12V supply |
| Motor holds when off | That's correct! | SGM-370 worm gear is self-locking by design |

---

## 9. Thermal issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Thermal cutoff triggers immediately | DS18B20 reads >65°C at boot | Move probe away from direct contact with heater; mount in air stream |
| PTC heaters don't get hot | SSR not switching / wrong voltage | Verify 12V at PTC terminals; check SSR wiring (§4); confirm 12V heaters (not 220V) |
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

## 11. Over-current protection (no-fuse design)

There are no fuses in this build — the 200A BMS is the backstop.

| Symptom | Likely cause | Fix |
|---|---|---|
| Station commanded ON but nothing runs | BMS tripped or branch open | Measure 12V at the positive bus bar; if 0V, power-cycle the battery to reset the BMS; check for shorts |
| BMS disconnects under load | Draw exceeds BMS limit | Verify staged operation (one station at a time ≈ 39A); check for shorts |
| Branch dead but bus bar live | Branch wiring open | Trace the 10/18 AWG branch and its SSR output side with a multimeter |
| Burning smell / hot wire | Overload or loose terminal | Stop: flip the 50A rocker OFF; check gauges and tighten terminals |

---

## 12. Debug mode

Add to sketch for verbose Serial output:

```cpp
// Add in loop():
Serial.print("Phase: "); Serial.print(currentPhase);
Serial.print(" | Stn: "); Serial.print(activeStation);
Serial.print(" | H: "); Serial.print(humidity);
Serial.print(" | T: "); Serial.print(temperature);
Serial.print(" | PTC1: "); Serial.print(digitalRead(PIN_SSR_PTC_1));
Serial.print(" | PTC2: "); Serial.print(digitalRead(PIN_SSR_PTC_2));
Serial.print(" | PTC3: "); Serial.print(digitalRead(PIN_SSR_PTC_3));
Serial.print(" | FAN: "); Serial.println(digitalRead(PIN_SSR_FAN_BUS));
```
