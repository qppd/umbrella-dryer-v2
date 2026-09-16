# Stack — 12V DC

> 12V DC-only umbrella dryer — no mains, no inverter, no RCD. Self-contained battery-powered system.

---

## 1. What this stack is

- An Arduino-controlled umbrella dryer with 3 stations.
- Each station has 3× PTC ceramic heaters (12V 100W) and 3× BLDC fans (50mm ducted, ESC-controlled).
- Each station has 1× SGM-370 worm gear motor for umbrella rotation.
- Everything runs on 12V DC from a 2× 200Ah LiFePO4 battery bank.
- **40A automotive relays** (NPN-driven) switch PTC heaters; **optocoupler module** switches motors; **ESC PWM** controls BLDC fans.
- Staged operation: one station at a time (firmware-enforced).

---

## 2. Hardware layers (bottom-up)

| Layer | Components |
|---|---|
| Power | 2× LiFePO4 200Ah → 50A disconnect → 50A ANL main fuse → DC distribution → per-branch fuses |
| Conversion | LM2596S buck: 12V → 5V for Mega (5V pin only) |
| Actuation | 3× PTC heater groups (40A automotive relays via 2N2222), 3× BLDC fan groups (ESC PWM + 40A auto relay bus), 3× worm motors (10A opto module) |
| Thermal protection | 130°C one-shot thermal fuse per heater (9×), PTC self-regulation, DS18B20 firmware cutoff |
| Sensing | DHT22 (humidity), DS18B20 (temperature) |
| Control | Arduino Mega 2560 |
| UI | 16×2 LCD I2C (pins 20/21), 3× LEDs (D15–D17), 1× buzzer (D18), 1× arcade button (D14) |

---

## 3. Power tree

```
Battery (12.8V 200Ah × 2 parallel)
  └─ 50A disconnect switch
      └─ 50A ANL main fuse
          ├─ 30A fuse → Station 1 PTC (3× 100W, ~25A)
          ├─ 30A fuse → Station 2 PTC (3× 100W)
          ├─ 30A fuse → Station 3 PTC (3× 100W)
          ├─ 3A fuse  → Motor Station 1 (SGM-370, ~0.8A)
          ├─ 3A fuse  → Motor Station 2 (SGM-370)
          ├─ 3A fuse  → Motor Station 3 (SGM-370)
          ├─ 30A fuse → Fan bus (9× BLDC fans, 28.8A)
          ├─ 3A fuse  → Logic (buck → Mega + sensors)
          └─ single-point GND rail (chassis bonded at one bolt)
```

---

## 4. Software layers

| Layer | Role |
|---|---|
| DHT library | Reads humidity from DHT22 |
| OneWire + DallasTemperature | Reads temperature from DS18B20 |
| Servo library | Generates 50Hz PWM for ESC signals (D10/D11/D12) |
| LiquidCrystal_I2C | Drives 16×2 LCD display (I2C on Mega pins 20/21) |
| Main sketch | State machine (IDLE → PREHEAT → DRY → COOL → DONE), staged relay control, ESC throttle, thermal safety cutoff |

---

## 5. Full-stack wiring

| Cable | From | To | AWG |
|---|---|---|---|
| Battery parallel links | battery + ↔ battery + | bank + | 4 |
| Bank → disconnect → main fuse → bus | bank + | distribution bus | 8 |
| PTC heater branch | bus → 30A fuse → 40A auto relay → thermal fuse → heater + | PTC heater | 10 |
| Motor branch | bus → 3A fuse → opto module → motor + | SGM-370 | 18 |
| Fan power | bus → 30A fuse → 40A auto relay → ESC VIN | BLDC fans | 10 (18 pigtail) |
| Fan signal | Mega D10/D11/D12 → ESC signal wire | — | 22 |
| Logic power | 12V → 3A fuse → buck → 5V → Mega 5V pin | Mega + sensors | 20 |
| Sensor data | DHT22→D2, DS18B20→D3, LCD→D20/D21 | — | 22 jumper |
| Relay signals | Mega D4–D13 → relay driver stages | — | 22 jumper |
| Button | D14 → button → GND | — | 22 jumper |
| LED/buzzer | D15–D18 → components → GND | — | 22 |

---

## 6. BOM per layer

| Layer | Price (est.) |
|---|---|
| Battery (2× 200Ah) + charger | ≈ ₱19,800 |
| PTC heaters (9×₱484) + thermal fuses (9×₱15) | ≈ ₱4,491 |
| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
| Motors + mechanical | ≈ ₱3,028 |
| Automotive relays (4) + opto module + NPN components | ≈ ₱580 |
| Control electronics (Mega, sensors, LCD, buck) | ≈ ₱1,589 |
| Disconnect switch + fuses + UI + wiring + consumables | ≈ ₱2,330 |
| **Total** | **≈ ₱36,000–37,000** |
