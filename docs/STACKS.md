# Stack — 12V DC

> Quick-reference card for the full hardware + software stack.

---

## Hardware layers

| Layer | Components |
|---|---|
| Power | 1× LiFePO4 200Ah → 50A DC rocker switch → 2-pin screw terminal → 150A bus bars → SSR branches (no fuses) |
| Conversion | LM2596S buck: 12V → 5V for Mega (5V pin only) |
| Actuation | 3× PTC heater groups (LCTC DC-DC SSR 40A), 9× AVC blowers (direct PWM D10–D12 + SSR-40DD fan bus), 3× worm motors (LCTC DC-DC SSR 10A) |
| Thermal protection | PTC self-regulation, DS18B20 firmware cutoff |
| Sensing | DHT22 (humidity), DS18B20 (temperature) |
| Control | Arduino Mega 2560 |
| UI | 16×2 LCD I2C (pins 20/21), 3× LEDs (D15–D17), buzzer (D18), arcade button (D14) |
| Drivetrain | 3× SGM-370 → rigid coupling 6×8mm → 6mm × 300mm SS shaft on UCP06 pillow block → PETIYOUZA 6mm flange coupling → umbrella hub |

---

## Software stack

| Library | Purpose |
|---|---|
| DHT | Humidity from DHT22 |
| OneWire + DallasTemperature | Temperature from DS18B20 |
| LiquidCrystal_I2C | LCD display (Mega pins 20/21) |
| Main sketch | State machine (IDLE → PREHEAT → DRY → COOL → DONE), staged SSR control, blower PWM (`analogWrite`), thermal cutoff |

No Servo library needed — blowers take duty-cycle PWM straight from Mega pins.

---

## BOM summary

| Layer | Price (est.) |
|---|---|
| PTC heaters (9×₱484) | ≈ ₱4,356 |
| AVC blowers (9×₱330) | ≈ ₱2,970 |
| Motors + drivetrain (3× SGM-370 + couplings + shafts + pillow blocks) | ≈ ₱3,049 |
| taxnele SSR 40A (4×) + SSR 10A (3×) + heatsinks | ≈ ₱2,051 |
| Control electronics (Mega, sensors, LCD, buck) | ≈ ₱1,094 |
| Battery (1× 200Ah) + charger | ≈ ₱11,700–12,200 |
| UI (LEDs, buzzer, button) | ≈ ₱109 |
| Wiring + consumables | ≈ ₱2,500–2,900 |
| DC Rocker Switch 50A | ~₱190 |
| **Total** | **≈ ₱29,900–30,200** |
