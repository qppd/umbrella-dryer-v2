# Stack — 12V DC

> Quick-reference card for the full hardware + software stack.

---

## Hardware layers

| Layer | Components |
|---|---|
| Power | 1× LiFePO4 200Ah → 50A disconnect → 50A ANL main fuse → DC distribution → per-branch fuses |
| Conversion | LM2596S buck: 12V → 5V for Mega (5V pin only) |
|| Actuation | 3× PTC heater groups (LCTC DC-DC SSR 40A), 3× BLDC fan groups (ESC PWM + LCTC DC-DC SSR 40A bus), 3× worm motors (LCTC DC-DC SSR 10A) |
|| Thermal protection | PTC self-regulation, DS18B20 firmware cutoff |
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
|| PTC heaters (9×₱484) + thermal fuses (9×₱15) | ≈ ₱4,491 |
|| BLDC fans + ESCs (9×₱469) | ≈ ₱4,221 |
|| Motors + mechanical | ≈ ₱3,028 |
|| LCTC DC-DC SSR 40A (4×₱344) + SSR 10A (3×₱164) + heatsinks | ≈ ₱2,068 |
|| Control electronics (Mega, sensors, LCD, buck) | ≈ ₱1,589 |
|| Battery (1× 200Ah) + charger | ≈ ₱10,900–11,600 |
|| UI (LEDs, buzzer, button) | ≈ ₱109 |
|| Wiring + consumables | ≈ ₱1,500–1,900 |
|| **Total** | **≈ ₱27,600–28,100** |
