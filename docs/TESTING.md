# Testing Guide (Rev 7 — 12V DC)

> Test plan for the 12V DC umbrella dryer. No mains voltage — all tests on 12V DC battery power.

---

## 1. Test levels

| Level | What | Pass criteria |
|---|---|---|
| L1 — Smoke test | Power on with no loads | Buck outputs 5V, Mega boots, LCD shows "READY", ESCs arm |
| L2 — Component test | Each subsystem individually | Each relay clicks, each ESC spins fan, each motor rotates, sensors read values |
| L3 — Integration test | Full cycle with loads | PREHEAT → DRY → COOL → DONE completes; safety cutoff works |
| L4 — Stress test | Extended run | Battery drains correctly, no overheating, fuse ratings correct |

---

## 2. L1 — Smoke test

1. Disconnect all relay outputs (no PTC, no motors, no fans).
2. Connect battery, flip DC rocker.
3. **Check:**
   - [ ] Buck LED lights, output = 5.0V
   - [ ] Mega boots, Serial Monitor prints "Rev 7"
   - [ ] LCD shows "Umbrella Dryer / Rev 7 - 12V DC"
   - [ ] ESCs arm (fan twitch or beep)
   - [ ] LCD settles on "READY / Press to start"
4. If anything fails → check wiring, buck voltage, I2C address.

---

## 3. L2 — Component tests

### 3a. Relay test

1. Connect only relay module (no loads on COM/NO).
2. Press button → PREHEAT phase.
3. **Check:**
   - [ ] Relay 1A clicks ON (PTC group A)
   - [ ] Relay 1B clicks ON (PTC group B)
4. Wait for DRY phase:
   - [ ] Relay 2A clicks ON (motor 1)
   - [ ] Relay 2B clicks ON (motor 2)
   - [ ] Automotive relay clicks ON (motor 3)
   - [ ] Automotive relay clicks ON (fan bus)
5. COOL phase: relays click OFF.
6. If relay doesn't click → check D4–D9 wiring, relay VCC/GND.

### 3b. ESC / BLDC fan test

1. Connect one BLDC fan to ESC, ESC signal to D10, ESC VCC to 12V (bypass relay).
2. Upload sketch. On boot, ESC arms.
3. Press button → PREHEAT → fan should spin up.
4. **Check:**
   - [ ] Fan spins smoothly at full speed
   - [ ] No unusual vibration or noise
   - [ ] Fan stops when ESC write(0) in COOL/DONE
5. Repeat for D11 (station 2) and D12 (station 3).

### 3c. Motor test

1. Connect one SGM-370 motor to relay output.
2. Press button → DRY phase (motor ON).
3. **Check:**
   - [ ] Motor rotates at ~6 RPM
   - [ ] Direction: umbrella should spin (reverse any two leads if wrong)
   - [ ] Motor stops when relay OFF
   - [ ] Motor holds position when off (self-locking)

### 3d. Sensor test

1. DHT22: Serial Monitor should print humidity % and temperature °C.
2. DS18B20: Serial Monitor should print temperature.
3. **Check:**
   - [ ] DHT22 reads 30–80% humidity (realistic range)
   - [ ] DS18B20 reads 20–35°C (ambient)
   - [ ] Values update every 500ms

### 3e. Button test

1. Press button → should start cycle (IDLE → PREHEAT).
2. Press again during PREHEAT → should emergency stop (back to IDLE).
3. **Check:**
   - [ ] No false triggers from noise
   - [ ] Button responsive within 200ms

---

## 4. L3 — Integration test (full cycle)

1. Connect all loads: PTC heaters, motors, fans.
2. Place umbrellas on stations.
3. Press button → observe full cycle:

| Phase | Expected | Time |
|---|---|---|
| PREHEAT | Fans spin, PTC warm, LCD shows temp rising | Until DHT22 ≥ 45°C |
| DRY | Motor spins umbrella, fans + PTC stay on | 15 min timer |
| COOL | Motor off, PTC off, fans run for cooling | 2 min |
| DONE | Everything off, buzzer beeps 3×, LED green | Until button press |

4. **Check:**
   - [ ] Umbrella fabric dries (no wet spots after cycle)
   - [ ] No burning smell from PTC heaters
   - [ ] Temperature stays 40–60°C during DRY phase
   - [ ] Thermal cutoff does NOT trigger during normal operation
   - [ ] Buzzer beeps clearly at end

---

## 5. L4 — Stress test

1. Run 3 consecutive cycles (30 min each, 90 min total).
2. **Check:**
   - [ ] Battery voltage stays above 12.0V after 3 cycles
   - [ ] No component overheats (touch test: motor, relay, ESC, PTC mounting)
   - [ ] Fuse ratings correct (no blown fuses)
   - [ ] Buck output stable at 5.0V throughout
   - [ ] LCD remains readable (no flickering)

---

## 6. Safety test

1. **Thermal cutoff:** Hold DS18B20 probe near a heat source (hair dryer). When reading exceeds 65°C → everything should shut off immediately.
2. **Fuse test:** Intentionally overload one station (block fan airflow, let temperature rise). Verify thermal fuse blows before damage occurs.
3. **Battery BMS:** Run until battery BMS disconnects (low voltage protection). Verify system shuts down gracefully.

---

## 7. Pass/fail checklist

| Test | Pass | Fail | Notes |
|---|---|---|---|
| L1: Smoke test | | | |
| L2a: Relays | | | |
| L2b: ESC/fans | | | |
| L2c: Motors | | | |
| L2d: Sensors | | | |
| L2e: Button | | | |
| L3: Full cycle | | | |
| L4: Stress (3 cycles) | | | |
| Safety: Thermal cutoff | | | |
| Safety: Fuse | | | |
| Safety: BMS | | | |
