# Troubleshooting (Rev 7 — 12V DC)

> All voltages are 12V DC or 5V logic. No mains voltage in this system.

---

## 1. Power issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing turns on | DC rocker off / battery disconnected | Flip DC rocker; check battery terminals; verify 25A main fuse |
| Buck LED off | Fuse blown / battery dead | Check 3A logic fuse; measure battery voltage (should be >12.0V) |
| Buck output ≠ 5V | Potentiometer misadjusted | Re-calibrate buck with multimeter BEFORE connecting to Mega |
| Mega won't boot | Buck not providing 5V / wrong Vin | Verify 5V at Mega Vin pin; check GND continuity |
| Battery dies fast | Too many stations running simultaneously | Run one station at a time (staged operation); check for shorts |

---

## 2. Sensor issues

| Symptom | Likely cause | Fix |
|---|---|---|
| DHT22 reads NaN | Wiring / library issue | Check VCC→5V, GND→GND, DATA→D2 with 10kΩ pull-up; try `DHT22 Black` module |
| DHT22 reads 0% or 100% | Damaged sensor or wiring fault | Replace DHT22; verify no solder bridges |
| DS18B20 reads −127°C | Bad connection / missing pull-up | Check white wire→D3 with 4.7kΩ pull-up; run OneWire scanner |
| DS18B20 reads 85°C only | Power issue (parasitic mode) | Connect VCC (red wire) to 5V; don't rely on parasitic power |
| Temperature too high / low | Probe placement | Mount DS18B20 near PTC heaters in airflow path, not on metal surface |

---

## 3. LCD issues

| Symptom | Likely cause | Fix |
|---|---|---|
| LCD blank | Wrong I2C address | Try 0x3F instead of 0x27; use I2C scanner sketch |
| LCD shows squares | Contrast / I2C not initialized | Call `lcd.init()` not `lcd.begin()`; check SDA→A4, SCL→A5 |
| LCD flickers | Loose connection | Check all 4 wires (VCC, GND, SDA, SCL); reseat dupont connectors |

---

## 4. Relay issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Relay doesn't click | No signal / no power | Check D4–D9 wiring; verify relay VCC→5V, GND→GND |
| Relay clicks but load off | Wrong terminals | Check COM and NO wiring; 12V bus → COM, load → NO |
| Relay stays ON at boot | Pin not defaulting HIGH | Verify `digitalWrite(pin, HIGH)` in setup; add 10kΩ pull-up to 5V |
| Load turns on/off by itself | Floating pin | Enable `pinMode(OUTPUT)` + default HIGH in `setup()` |

---

## 5. ESC / BLDC fan issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Fan doesn't spin | ESC not armed | Verify `esc.attach(pin)` + `esc.write(0)` for 2s on boot |
| Fan spins then stops | ESC lost signal | Ensure `esc.write()` called continuously; check D10/D11/D12 wiring |
| Fan vibrates excessively | Bent propeller / unbalanced | Check propeller; replace if damaged; ensure duct clears spinning blades |
| Fan runs at wrong speed | PWM range mismatch | Calibrate ESC (see FIRMWARE-GUIDE.md §9); try write range 0–180 |
| ESC gets hot | Drawing too much current | Verify fan current < 3.2A each; check 15A fan bus fuse not overloaded |
| All 9 fans don't start | Fan bus relay not ON | Check D9 → automotive relay coil; measure 12V at ESC VCC after relay ON |

---

## 6. Motor issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Motor doesn't spin | Relay not switching / fuse blown | Check D6–D8 wiring; verify 3A motor fuse; check COM/NO on relay |
| Motor spins wrong direction | Polarity reversed | Swap any two motor leads (DC motor direction = polarity) |
| Motor hums but doesn't spin | Coupling misaligned / shaft binding | Loosen coupling; realign motor and shaft; check KP08 pillow blocks |
| Motor stalls under load | Insufficient torque | Verify umbrella not too heavy (>3 kg·cm load); check 12V supply voltage |

---

## 7. Thermal issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Thermal cutoff triggers immediately | DS18B20 reads >65°C at boot | Move probe away from heat source; check probe is in airflow, not on heater |
| PTC heaters don't get hot | Relay not switching / wrong voltage | Verify 12V at PTC terminals; check relay wiring; confirm 12V heaters (not 220V) |
| Chamber too hot (>60°C) | Too many PTC groups on simultaneously | Run staged operation; reduce PTC groups active at once |
| Burning smell | Wiring too thin / loose connection | Check wire gauges (14 AWG main, 16 AWG station); tighten all terminals |

---

## 8. Battery issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Battery voltage drops fast | High current draw / old battery | Run one station at a time; check for shorts; verify BMS is functioning |
| Battery won't charge | Wrong charger | Use 14.6V LiFePO4 charger ONLY; never use lead-acid charger |
| BMS disconnects | Over-discharge / over-current | Recharge battery; check total current draw stays within BMS limits |

---

## 9. Fuse issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Main fuse blows | Total current > 25A | Run fewer stations simultaneously; check for short circuits |
| Station fuse blows | Single station overcurrent | Check PTC heater count per group (max 3); verify wire gauges |
| Fuse blows immediately | Dead short | Trace wiring with multimeter (continuity mode); check for bare wire touching chassis |

---

## 10. Debug mode

Add to sketch for verbose Serial output:

```cpp
// Add in loop():
Serial.print("Phase: "); Serial.print(currentPhase);
Serial.print(" | H: "); Serial.print(humidity);
Serial.print(" | T: "); Serial.print(temperature);
Serial.print(" | PTC_A: "); Serial digitalRead(PIN_RELAY_PTC_A);
Serial.print(" | PTC_B: "); Serial digitalRead(PIN_RELAY_PTC_B);
Serial.print(" | MOTOR: "); Serial.print(digitalRead(PIN_RELAY_MOTOR_1));
Serial.print(" | FAN: "); Serial.println(digitalRead(PIN_RELAY_FAN_BUS));
```
