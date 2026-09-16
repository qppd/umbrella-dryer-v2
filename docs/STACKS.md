# Stack — 12V DC

> Quick-reference card for the full hardware + software stack.

---

## Hardware layers

| Layer | Components |
|---|---|
| Power | 1× LiFePO4 200Ah → 50A disconnect → 50A ANL main fuse → DC distribution → per-branch fuses |
| Conversion | LM2596S buck: 12V → 5V for Mega (5V pin only) |
| Actuation | 3× PTC heater groups (40A automotive relays via 2N2222), 3× BLDC fan groups (ESC PWM + 40A auto relay bus), 3× worm motors (10A opto module) |
| Thermal protection | 130°C one-shot thermal fuse per heater (9×), PTC self-regulation, DS18B20 firmware cutoff |
| Sensing | DHT22 (humidity), DS18B20 (temperature) |
| Control | Arduino Mega 2560 |
| UI | 16×2 LCD I2C (pins 20/21), 3× LEDs (D15–D17), buzzer (D18), arcade button (D14) |

---

## Software stack

| Library | Purpose |
|---|---|
| DHT | Humidity from DHT22 |
| OneWire + DallasTemperature | Temperature from DS18B20 |
| Servo | 50Hz PWM for ESC signals (D10/D11/D12) |
| LiquidCrystal_I2C | LCD display (Mega pins 20/21) |
| Main sketch | State machine (IDLE → PREHEAT → DRY → COOL → DONE), staged relay control, ESC throttle, thermal cutoff |

---

## BOM summary

| Layer | Price (est.) |
|---|---|
| Battery (1× 200Ah) + charger | ≈ ₱10,900 |
| PTC heaters (9×₱484) + thermal fuses (9×₱15) | ≈ ₱4,491 |
| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
| Motors + mechanical | ≈ ₱3,028 |
| Automotive relays (4) + opto module + NPN components | ≈ ₱580 |
| Control electronics (Mega, sensors, LCD, buck) | ≈ ₱1,589 |
| Disconnect switch + fuses + UI + wiring + consumables | ≈ ₱2,330 |
| **Total** | **≈ ₱27,100–28,100** |
