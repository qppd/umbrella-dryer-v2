# Smart Umbrella Dryer — Component & Material Validation

## Study Overview

**Title:** Smart Umbrella Dryer: Design and Development of a Multi-Umbrella Drying System with Energy Efficient Control

**Key Requirements:**
1. Dry multiple umbrellas simultaneously
2. Energy-efficient operation (backup battery support)
3. Smart/automated control via sensors
4. Safe operating temperatures for umbrella materials

---

## 1. Microcontroller — Arduino Mega 2560

| Parameter | Value |
|---|---|
| Processor | ATmega2560 |
| Digital I/O Pins | 54 (15 PWM) |
| Analog Pins | 16 |
| Flash Memory | 256 KB |
| SRAM | 8 KB |
| Clock Speed | 16 MHz |
| Operating Voltage | 5V |
| Input Voltage | 7–12V |
| I2C Support | Yes (SDA/SCL) |
| UART | 4 Hardware Serial |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **Pin Count:** The project requires connections for DHT22 (1 digital), DS18B20 (1 digital + 4.7kΩ pull-up), BTS7960 (4 PWM + 2 enable = 6 pins), LCD I2C (2 pins shared I2C), LEDs (3–4 digital), buzzer (1 digital), buttons (2 digital), water pump relay (1 digital), rocker switch (1 digital). **Total ≈ 18–22 pins** — well within Arduino Mega's 54 digital + 16 analog pins.
- **I2C Bus:** LCD I2C (typically 0x27 or 0x3F) uses I2C. MLX90614 (if used, address 0x5A) shares I2C bus with no conflict. DS18B20 uses 1-Wire (separate bus).
- **1-Wire Bus:** DS18B20 uses a dedicated 1-Wire bus (1 digital pin). Multiple DS18B20 sensors can share this bus if needed.
- **PWM Channels:** BTS7960 motor driver needs PWM for speed control. Arduino Mega has 15 PWM pins — sufficient.
- **Flash/SRAM:** 256 KB flash and 8 KB SRAM are more than enough for the sensor reading, motor control, display, and logic code.

### ⚠️ Concerns
- None significant. Arduino Mega is well-suited for this application.

---

## 2. Power Supply — ExpertPower 12.8V 35Ah LiFePO4 Battery

| Parameter | Value |
|---|---|
| Nominal Voltage | 12.8V |
| Capacity | 35Ah (448 Wh) |
| Chemistry | LiFePO4 (Lithium Iron Phosphate) |
| Weight | ~4.5 kg |
| Cycle Life | 2000–5000 cycles |
| Operating Temp | -20°C to 60°C |
| Max Continuous Discharge | ~35A (typically 1C) |
| BMS | Built-in (overcharge, over-discharge, short circuit, over-temp) |

### Power Budget Analysis

| Component | Voltage | Current Draw | Power |
|---|---|---|---|
| PTC 12V 120W Air Heater Fan | 12V | 10A | 120W |
| DC Gear Motor 12V | 12V | 0.5–2A | 6–24W |
| 120mm DC Cooling Fan 12V | 12V | 0.2–0.3A | 2.4–3.6W |
| DC Water Pump 12V | 12V | 0.3–0.5A | 3.6–6W |
| Arduino Mega 5V (via buck converter) | 5V | 0.2A | 1W |
| Sensors (DHT22 + MLX90614) | 3.3–5V | 0.003A | 0.015W |
| LCD I2C Display | 5V | 0.02A | 0.1W |
| LEDs + Buzzer | 5V | 0.05A | 0.25W |
| **Total** | — | — | **~134–155W** |

### Runtime on Battery
- **Energy Available:** 448 Wh
- **At max load (~155W):** 448 ÷ 155 ≈ **2.9 hours**
- **At typical load (~100W, heater cycling):** 448 ÷ 100 ≈ **4.5 hours**

### ✅ Compatibility Assessment — **COMPATIBLE**
- The 12.8V nominal voltage matches the 12V components (PTC heater, motor, fans, pump) directly.
- 35Ah capacity provides adequate backup for 2.9–4.5 hours of operation.
- Built-in BMS protects against overcharge/over-discharge.
- LiFePO4 chemistry is safe (no thermal runaway), suitable for an enclosed drying system.

### ⚠️ Concerns
- **Buck Converter Required:** LM2596S buck converter steps down 12V → 5V for Arduino and sensors. Must be rated ≥ 3A to handle Arduino + sensors + LCD + LEDs safely.
- **Heater Dominates Power Budget:** The 120W PTC heater accounts for ~80% of total power. If energy efficiency is critical, PWM-based duty cycling of the heater is essential (which the Arduino Mega can provide).

---

## 3. Heating Element — PTC 12V 120W Air Heater Fan

| Parameter | Value |
|---|---|
| Voltage | 12V DC |
| Power | 120W |
| Current | 10A |
| Type | PTC (Positive Temperature Coefficient) ceramic |
| Self-Regulating | Yes — auto-limits temperature |
| Typical Surface Temp | 150–250°C (self-limiting) |
| Airflow | Integrated fan blower |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **Self-Regulating Safety:** PTC heaters are inherently safe — they auto-limit temperature when resistance increases at the Curie point. No external thermostat required for the heater itself.
- **12V Direct Drive:** Can be powered directly from the LiFePO4 battery (12.8V nominal is within PTC 12V tolerance).
- **120W Output:** Sufficient heat for drying umbrellas in an enclosed chamber. Umbrella fabric (nylon/polyester) dries effectively at 40–60°C air temperature.
- **Integrated Fan:** Provides forced-air convection, improving drying speed.

### ⚠️ Concerns
- **10A Current Draw:** Requires thick wiring (at least 16 AWG) from battery to heater. A MOSFET or relay rated ≥ 15A should switch the heater, controlled by the Arduino.
- **Over-Temperature Protection:** Although PTC is self-regulating, an additional software safety cutoff via DS18B20 sensor (mounted near heater) is recommended as a redundant safeguard.
- **Voltage Drop:** At 10A through thin wires, voltage drop could be significant. Keep wire runs short.

---

## 4. Humidity Sensor — DHT22 (AM2302)

| Parameter | Value |
|---|---|
| Humidity Range | 0–100% RH |
| Humidity Accuracy | ±2% RH |
| Humidity Resolution | 0.1% RH |
| Temperature Range | -40°C to 80°C |
| Temperature Accuracy | ±0.5°C |
| Operating Voltage | 3.3–5.5V |
| Current | 1–1.5 mA (measuring), 40–50 µA (standby) |
| Interface | Single-wire digital |
| Sampling Rate | 1 reading every 2 seconds |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **Dual Function:** Measures both humidity and temperature — ideal for monitoring drying progress.
- **Humidity Feedback Loop:** Core sensor for the energy-efficient control system. When humidity drops below a threshold (e.g., < 40% RH), the system can turn off the heater.
- **5V Compatible:** Directly interfaces with Arduino Mega without level shifting.
- **Low Power:** Negligible power consumption (~1.5 mA).

### ⚠️ Concerns
- **Response Time:** DHT22 has a 2-second sampling interval — adequate for slow-changing humidity, but not for real-time rapid feedback.
- **Placement:** Must be placed inside the drying chamber but away from direct heat/steam from the PTC heater to avoid false readings. A radiation shield or distant mounting is recommended.
- **Condensation Risk:** In a high-humidity drying environment, condensation on the sensor can cause errors. A breather hole or waterproof housing is advised.

---

## 5a. Temperature Sensor (Heater Zone) — DS18B20 Waterproof Probe

| Parameter | Value |
|---|---|
| Temperature Range | -55°C to +125°C |
| Accuracy | ±0.5°C (from -10°C to +85°C) |
| Resolution | Configurable 9–12 bits (0.0625°C at 12-bit) |
| Interface | 1-Wire Digital (single data pin) |
| Supply Voltage | 3.0–5.5V |
| Current | 1–1.5 mA (active), 1 µA (standby) |
| Probe Type | Waterproof stainless steel |
| Response Time | ~750ms (12-bit) |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **Waterproof Probe:** Stainless steel probe can be mounted directly near the PTC heater or inside the drying chamber without risk of moisture damage.
- **Wide Range:** -55°C to +125°C covers the full operating range of the drying chamber (40–80°C) and heater zone (up to 120°C near PTC).
- **High Precision:** ±0.5°C accuracy is sufficient for temperature monitoring and safety cutoff.
- **1-Wire Interface:** Only requires 1 digital pin on Arduino Mega + 4.7kΩ pull-up resistor — minimal wiring.
- **Low Cost:** ~₱50–80 per unit — very budget-friendly.
- **Multi-Sensor Bus:** Multiple DS18B20 sensors can share the same 1-Wire bus (each has a unique 64-bit address) — ideal for monitoring multiple zones.

### ⚠️ Concerns
- **750ms Response Time:** At 12-bit resolution, each reading takes ~750ms. This is fast enough for temperature monitoring (temperatures don't change rapidly) but not for real-time control loops.
- **Probe Placement:** Mount the stainless steel probe near the PTC heater outlet to monitor heated air temperature, not directly on the PTC surface (which can exceed 150°C).

---

## 5b. Umbrella Surface Temperature Sensor — MLX90614 (Optional)

| Parameter | Value |
|---|---|
| Object Temp Range | -70°C to 382.2°C |
| Ambient Temp Range | -40°C to 85°C |
| Accuracy | ±0.5°C (room temp) |
| Resolution | 0.02°C |
| Field of View | 90° |
| Interface | I2C (SMBus), default address 0x5A |
| Supply Voltage | 3.3–5.5V |
| Current | < 2 mA |

### ✅ Compatibility Assessment — **COMPATIBLE (Optional)**
- **Non-Contact Sensing:** Measures umbrella surface temperature without physical contact — ideal for a rotating mechanism.
- **High Precision:** 0.02°C resolution for accurate surface temperature monitoring.
- **I2C Interface:** Shares the I2C bus with LCD display (different addresses — no conflict).
- **Note:** This is an **optional** sensor. The DS18B20 + DHT22 combination already provides sufficient temperature/humidity monitoring. The MLX90614 adds value only if umbrella surface temperature monitoring is critical for the study.

### Recommended Sensor Configuration

| Sensor | Purpose | Location | Priority |
|---|---|---|---|
| **DS18B20** | Air temperature near heater | Inside chamber, near PTC heater outlet | **Required** |
| **DHT22** | Humidity + ambient temperature | Inside chamber, away from direct heat | **Required** |
| **MLX90614** | Umbrella surface temperature (non-contact) | Pointed at umbrella from chamber wall | **Optional** |

---

## 6. Motor & Drive System

### 6a. DC Gear Motor (12V)

| Parameter | Estimated Value |
|---|---|
| Voltage | 12V DC |
| Type | Geared DC motor |
| Speed | Low RPM (geared down for torque) |
| Torque | High (suitable for rotating umbrella mechanism) |

### 6b. BTS7960 Motor Driver

| Parameter | Value |
|---|---|
| Operating Voltage | 5–27V |
| Max Current | 43A (peak), 25A (continuous) |
| Logic Voltage | 5V |
| Control | 2 PWM inputs (speed) + 2 direction inputs |
| Features | Over-temperature shutdown, under-voltage lockout |

### 6c. Mechanical Transmission

| Component | Specification |
|---|---|
| Steel Shaft | 8mm–12mm |
| Pillow Block Bearing | KP08 (8mm bore) |
| Shaft Coupling | 8mm × 10mm |
| Aluminum Plate | Structural chassis |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **BTS7960 is Over-Spec'd (in a good way):** At 43A peak capacity, it can easily handle the small DC gear motor's current (likely 0.5–2A). This provides a huge safety margin and reliable operation.
- **PWM Speed Control:** Arduino Mega's PWM signals control motor speed smoothly via BTS7960 RPWM/LPWM pins.
- **Direction Control:** RPWM/LPWM pins allow bidirectional motor control — useful for rotating the umbrella mechanism in both directions.
- **Mechanical Components:** KP08 pillow block bearing with 8mm bore matches the steel shaft. Shaft coupling connects motor to mechanism. Aluminum plate provides rigid chassis.

### ⚠️ Concerns
- **Motor Current vs. BTS7960 Sense Pins:** The BTS7960 has current sense outputs (RIS/LIS) proportional to motor current. These could be connected to Arduino analog pins for motor load monitoring — a useful but optional feature.
- **Mechanical Alignment:** Ensure shaft coupling properly aligns motor output shaft to the umbrella rotation mechanism. Misalignment causes vibration and premature bearing wear.

---

## 7. Voltage Regulation — LM2596S Buck Converter

| Parameter | Value |
|---|---|
| Input Voltage | 4.5–40V |
| Output Voltage | Adjustable (typically set to 5V) |
| Max Output Current | 3A |
| Efficiency | ~80–92% |
| Switching Frequency | 150 kHz |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **Input:** Accepts 12.8V from LiFePO4 battery — within the 4.5–40V range.
- **Output:** Adjustable to 5V for Arduino Mega and sensors.
- **Current:** 3A output is sufficient for Arduino Mega (~0.5A max) + sensors + LCD + LEDs + buzzer (~0.3A total) = ~0.8A. Well within 3A rating.
- **Efficiency:** 80–92% efficiency minimizes power loss — aligns with the energy-efficient design goal.

### ⚠️ Concerns
- **Heat Dissipation:** At full 3A load, the LM2596S may get warm. At the expected ~0.8A load, heat is minimal.
- **Output Capacitor:** Ensure proper output capacitors are in place for stable 5V output — noise on the 5V rail can cause Arduino resets or sensor reading errors.

---

## 8. Water Management — DC Water Pump

| Parameter | Estimated Value |
|---|---|
| Voltage | 12V DC |
| Current | 0.3–0.5A |
| Type | Small submersible or centrifugal pump |
| Purpose | Remove condensate/drainage water |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **12V Direct Drive:** Powered directly from the battery through a relay/MOSFET controlled by Arduino.
- **Low Power:** 3.6–6W is minimal in the overall power budget.
- **Function:** Essential for removing water that condenses or drips from drying umbrellas, preventing water accumulation inside the chamber.

### ⚠️ Concerns
- **Pump Protection:** Should include a check valve or anti-siphon mechanism to prevent backflow.
- **Auto-Activation:** The pump should be triggered by a water level sensor or timed intervals — relying solely on Arduino timing is acceptable but a float switch would be more robust.

---

## 9. User Interface Components

### 9a. LCD I2C Display

| Parameter | Value |
|---|---|
| Type | 16×2 or 20×4 character LCD |
| Interface | I2C (SDA/SCL) |
| Address | Typically 0x27 or 0x3F |
| Backlight | LED |

### 9b. LEDs (Status Indicators)

| LED | Purpose |
|---|---|
| Green | Drying complete / System ready |
| Yellow | Drying in progress |
| Red | Error / Over-temperature |

### 9c. Piezoelectric Buzzer

| Parameter | Value |
|---|---|
| Voltage | 3.3–5V |
| Current | ~30 mA |
| Purpose | Audio alert when drying is complete |

### 9d. User Input

| Component | Purpose |
|---|---|
| Rocker Switch | Main power ON/OFF |
| Momentary Push Button | Start drying cycle / Reset |

### 9e. Rotary Latch

| Purpose |
|---|
| Secure the drying chamber door |

### ✅ Compatibility Assessment — **COMPATIBLE**
- **LCD I2C:** Shares I2C bus with MLX90614 (different addresses). Only 2 wires needed — clean wiring.
- **LEDs:** Simple digital outputs from Arduino — no issues.
- **Buzzer:** Low current draw, can be driven directly from an Arduino digital pin (with a transistor for louder output if needed).
- **Rocker Switch:** Hardware power switch — essential for safety and power conservation.
- **Push Button:** Simple input with internal pull-up resistor — no external resistor needed.
- **Rotary Latch:** Mechanical component — ensures chamber door stays closed during operation.

---

## 10. Structural & Mechanical Components

| Component | Purpose | Compatibility |
|---|---|---|
| 8mm–12mm Steel Shaft | Rotation axis for umbrella mechanism | ✅ Rigid, durable |
| Pillow Block Bearing KP08 | Supports shaft rotation, reduces friction | ✅ 8mm bore matches shaft |
| 8mm × 10mm Shaft Coupling | Connects motor shaft to mechanism shaft | ✅ Matches motor/mechanism |
| Aluminum Plate | Chassis / structural frame | ✅ Lightweight, corrosion-resistant |

### ✅ Compatibility Assessment — **COMPATIBLE**
- All mechanical components are dimensionally compatible (8mm shaft system).
- Aluminum is ideal for the chassis — lightweight, easy to machine, and corrosion-resistant (important in a humid environment).
- Pillow block bearings are designed for radial loads — suitable for supporting the rotating umbrella mechanism.

### ⚠️ Concerns
- **Corrosion:** In a humid drying environment, steel shaft and bearings should be stainless steel or coated to prevent rust. If plain steel is used, apply anti-corrosion treatment.
- **Vibration:** Ensure proper alignment to minimize vibration during rotation.

---

## Overall Compatibility Matrix

| Component | Voltage Match | Current Sufficient | Interface Compatible | Physical Fit | Safety | Verdict |
|---|---|---|---|---|---|---|
| Arduino Mega | ✅ (via 5V buck) | ✅ | ✅ (I2C, PWM, Digital) | ✅ | ✅ | ✅ PASS |
| ExpertPower Battery | ✅ (12.8V) | ✅ (35Ah) | N/A | ✅ | ✅ (BMS) | ✅ PASS |
| PTC 120W Heater | ✅ (12V) | ✅ (10A) | Needs relay/MOSFET | ✅ | ✅ (self-reg) | ✅ PASS |
| DHT22 Sensor | ✅ (5V) | ✅ (1.5mA) | ✅ (1-wire) | ✅ | ✅ | ✅ PASS |
| MLX90614 Sensor | ✅ (3.3–5V) | ✅ (2mA) | ✅ (I2C 0x5A) | ✅ | ✅ | ✅ PASS |
| DC Gear Motor | ✅ (12V) | ✅ | Via BTS7960 | ✅ | ✅ | ✅ PASS |
| BTS7960 Driver | ✅ (5–27V) | ✅ (43A peak) | ✅ (PWM) | ✅ | ✅ | ✅ PASS |
| LM2596S Buck | ✅ (in: 12.8V, out: 5V) | ✅ (3A) | N/A | ✅ | ✅ | ✅ PASS |
| DC Water Pump | ✅ (12V) | ✅ (0.5A) | Via relay | ✅ | ✅ | ✅ PASS |
| LCD I2C | ✅ (5V) | ✅ (40mA) | ✅ (I2C) | ✅ | ✅ | ✅ PASS |
| LEDs + Buzzer | ✅ (5V) | ✅ (<100mA) | ✅ (Digital) | ✅ | ✅ | ✅ PASS |
| Mechanical Parts | N/A | N/A | N/A | ✅ (8mm system) | ✅ | ✅ PASS |

---

## Energy Efficiency Validation

The study claims **energy efficient control**. Here's the analysis:

### Control Strategy
1. **Sensor-Based Heating:** DHT22 monitors humidity → Heater cycles ON only when humidity > threshold → Reduces duty cycle.
2. **Temperature Monitoring:** MLX90614 monitors surface temp → Prevents overheating → Safety + efficiency.
3. **Auto-Shutoff:** When humidity drops below threshold (umbrella is dry), system turns off heater and motor → No wasted energy.
4. **PTC Self-Regulation:** The PTC heater inherently reduces power as it reaches operating temperature → Built-in efficiency.

### Estimated Duty Cycle
- **Continuous Heating:** 120W × 1 hour = 120 Wh
- **With 50% Duty Cycling:** 60W average → 448 Wh ÷ 60W ≈ **7.5 hours** runtime on battery
- **With 30% Duty Cycling:** 36W average → 448 Wh ÷ 36W ≈ **12.4 hours** runtime on battery

### Verdict: ✅ Energy Efficient Design Confirmed
The combination of PTC self-regulation + sensor-based duty cycling + auto-shutoff provides genuine energy savings compared to always-on heaters.

---

## Safety Validation

| Hazard | Mitigation | Status |
|---|---|---|
| Overheating | PTC self-regulation + DS18B20 software cutoff | ✅ Dual protection |
| Overcurrent | BTS7960 built-in overcurrent protection | ✅ Protected |
| Battery Overdischarge | ExpertPower BMS built-in | ✅ Protected |
| Short Circuit | ExpertPower BMS + fuse recommended | ✅ Protected |
| Water Damage | DC pump removes condensate | ✅ Managed |
| Fire Risk | PTC is self-limiting (no open-element risk) | ✅ Low risk |
| Electrical Shock | 12V DC system (extra-low voltage) | ✅ Safe |

---

## Potential Improvements / Recommendations

1. **Add a fuse** (15A) on the main battery line for overcurrent protection.
2. **Use stainless steel shaft/bearings** to prevent corrosion in the humid environment.
3. **Add a water level float switch** as a backup to timed pump activation.
4. **Consider a DHT22 radiation shield** to prevent condensation on the sensor.
5. **Add a rotary encoder or limit switch** on the motor shaft to detect jam/overload.
6. **Wire gauge:** Use at least 16 AWG for the PTC heater circuit (10A) and 18 AWG for motor circuit.

---

## Final Verdict

### ✅ ALL COMPONENTS ARE COMPATIBLE AND CAPABLE OF DRYING UMBRELLAS

The selected components form a well-integrated system:
- **Power:** LiFePO4 battery (12.8V/35Ah) provides adequate energy for 3–12 hours of operation depending on duty cycle.
- **Heating:** PTC 120W heater with integrated fan provides sufficient, self-regulating heat for umbrella drying.
- **Control:** Arduino Mega with DHT22 + MLX90614 sensors enables smart, energy-efficient feedback control.
- **Mechanics:** DC motor + BTS7960 driver + shaft/bearing system enables reliable umbrella rotation.
- **Safety:** Multi-layered protection (PTC self-regulation, sensor monitoring, BMS, motor driver protection).
- **Energy Efficiency:** Sensor-based duty cycling reduces average power consumption significantly.

The system is viable for drying multiple umbrellas in a compact, safe, and energy-efficient manner.
