# Stack — 12V DC

> 12V DC-only umbrella dryer — no mains, no inverter, no RCD. Self-contained battery-powered system.

---

## 1. What this stack is

- An Arduino-controlled umbrella dryer with 3 stations.
- Each station has 3× PTC ceramic heaters (12V 100W) and 3× BLDC fans (50mm ducted, ESC-controlled).
- Each station has 1× SGM-370 worm gear motor for umbrella rotation.
- Everything runs on 12V DC from a 2× 200Ah LiFePO4 battery bank.
- Relays switch PTC heaters and motors. ESCs control BLDC fans via PWM.
- Self-regulating PTC heaters + DS18B20 thermal fuse + thermal fuse = triple safety.

---

## 2. Hardware layers (bottom-up)

| Layer | Components |
|---|---|
| Power | 2× LiFePO4 200Ah → 25A main fuse → DC distribution → per-station fuses |
| Conversion | LM2596S buck: 12V → 5V for logic |
| Actuation | 3× PTC heater groups (relay-switched 12V), 3× BLDC fan groups (ESC PWM + relay bus), 3× worm motors (relay-switched 12V) |
| Sensing | DHT22 (humidity), DS18B20 (temperature) |
| Control | Arduino Mega 2560 |
| UI | 16×2 LCD I2C, 3× LEDs, 1× buzzer, 1× arcade button |

---

## 3. Power tree

```
Battery (12.8V 200Ah × 2 parallel)
  └─ 25A main fuse
      ├─ 10A fuse → PTC Station 1 (3× 100W, 25A total)
      ├─ 10A fuse → PTC Station 2 (3× 100W)
      ├─ 10A fuse → PTC Station 3 (3× 100W)
      ├─ 3A fuse  → Motor Station 1 (SGM-370)
      ├─ 3A fuse  → Motor Station 2 (SGM-370)
      ├─ 3A fuse  → Motor Station 3 (SGM-370)
      ├─ 15A fuse → Fan bus (9× BLDC fans)
      ├─ 3A fuse  → Logic (buck → Mega + sensors)
      └─ DC rocker (kill switch)
```

---

## 4. Software layers

| Layer | Role |
|---|---|
| DHT library | Reads humidity from DHT22 |
| OneWire + DallasTemperature | Reads temperature from DS18B20 |
| Servo library | Generates 50Hz PWM for ESC signals (D10/D11/D12) |
| LiquidCrystal_I2C | Drives 16×2 LCD display |
| Main sketch | State machine (IDLE → PREHEAT → DRY → COOL → DONE), relay control, ESC throttle, safety cutoff |

---

## 5. Full-stack wiring (12V DC — no mains)

| Cable | From | To | AWG |
|---|---|---|---|
| Battery positive | Battery + | 25A main fuse | 14 |
| Battery negative | Battery − | Common GND bus | 14 |
| PTC heater power | Relay COM/NO → fuse → heater | 12V bus | 16 |
| Motor power | Relay COM/NO → fuse → motor | 12V bus | 18 |
| Fan power | Auto relay → 15A fuse → ESC VCC | 12V bus | 16 |
| Fan signal | Mega D10/D11/D12 → ESC signal wire | — | 20 |
| Logic power | 12V → buck → 5V → Mega Vin | — | 20 |
| Sensor data | DHT22→D2, DS18B20→D3, LCD→A4/A5 | — | jumper |
| Control signals | Mega D4–D9 → relay inputs | — | jumper |
| Button | D13 → button → GND | — | jumper |
| LED/buzzer | D14–D17 → components → GND | — | 22 |

> No mains wiring, no N/E/Ground, no RCD, no changeover switch.

---

## 6. BOM per layer

| Layer | Price (est.) |
|---|---|
| Battery (2× 200Ah) + charger | ≈ ₱19,800 |
| PTC heaters (9×₱280) | ≈ ₱2,520 |
| BLDC fans + ESCs (9×₱470) | ≈ ₱4,230 |
| Motors + mechanical | ≈ ₱2,956 |
| Control electronics | ≈ ₱1,653 |
| UI + wiring + fuses + consumables | ≈ ₱2,500 |
| **Total** | **≈ ₱33,660** |
