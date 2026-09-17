# Testing Guide — 12V DC

> Test plan for the 12V DC umbrella dryer. No mains voltage — all tests on 12V DC battery power.

---

## 1. Test levels

| Level | What | Pass criteria |
|---|---|---|
| L1 — Smoke test | Power on with no loads | Buck outputs 5V, Mega boots, LCD shows "READY", ESCs arm |
|| L2 — Component test | Each subsystem individually | Each SSR triggers, each ESC spins fan, each motor rotates, sensors read values |
|| L3 — Integration test | Full cycle with loads | PREHEAT → DRY → COOL → COMPLETE completes; safety cutoff works |
|| L4 — Stress test | Extended run | Battery drains correctly, no overheating, SSR ratings adequate |

---

## 2. L1 — Smoke test

1. Disconnect all SSR outputs (no PTC, no motors, no fans).
2. Connect battery.
3. **Check:**
   - [ ] Buck LED lights, output = 5.0V at Mega **5V pin** (NOT barrel jack)
   - [ ] Mega boots, Serial Monitor prints "Umbrella Dryer V2"
   - [ ] LCD shows "Umbrella Dryer V2 DC SYSTEM"
   - [ ] ESCs arm — D13 briefly ON (fan twitch or beep), then OFF
   - [ ] LCD settles on "SYSTEM READY / Press Button"
4. If anything fails → check wiring, buck voltage, I2C address (try 0x3F), **LCD on Mega pins 20/21**.

---

## 3. L2 — Component tests

### 3a. SSR test

1. Connect only SSR modules (no loads on COM/NO).
2. Press button → PREHEAT phase.
3. **Check:**
   - [ ] D4 goes HIGH → station 1 PTC SSR clicks ON
   - [ ] Fans spin (D13 HIGH + ESC throttle)
4. Wait for DRY phase:
   - [ ] D5 goes HIGH → station 1 motor SSR clicks ON
   - [ ] After 30s rotation: D5→OFF, D6→HIGH (station 2 PTC), D7→HIGH (station 2 motor)
5. COOL phase: all SSRs OFF, fans stay ON.
6. If PTC SSR doesn't trigger → check D4 connection to SSR IN+; IN− → GND; COM → +12V, NO → heaters.
7. If motor SSR doesn't trigger → check D5 → SSR IN+; SSR IN− → GND; COM → +12V.

### 3b. ESC / BLDC fan test

1. Connect one BLDC fan to ESC, ESC signal to D10, ESC VCC to 12V (bypass relay).
2. Upload sketch. On boot, D13 goes HIGH briefly for ESC arming.
3. Press button → PREHEAT → fan should spin up.
4. **Check:**
   - [ ] Fan spins smoothly at full speed
   - [ ] No unusual vibration or noise
   - [ ] Fan stops when ESC write(0) in COOL/DONE
5. Repeat for D11 (station 2) and D12 (station 3).

### 3c. Motor test

1. Connect one SGM-370 motor to LCTC DC-DC SSR 10A output.
2. Press button → DRY phase → staged rotation → D5 goes HIGH for station 1.
3. **Check:**
   - [ ] Motor rotates at ~6 RPM
   - [ ] Direction: umbrella should spin (reverse any two leads if wrong)
   - [ ] Motor stops when SSR OFF (D5 goes LOW)
   - [ ] Motor holds position when off (self-locking)

### 3d. Sensor test

1. DHT22: Serial Monitor should print humidity % and temperature °C.
2. DS18B20: Serial Monitor should print temperature.
3. **Check:**
   - [ ] DHT22 reads 30–80% humidity
   - [ ] DS18B20 reads 20–35°C (ambient)
   - [ ] Values update every 500ms

### 3e. Button test

1. Press button → should start cycle (IDLE → PREHEAT).
2. Press again during PREHEAT → should emergency stop (back to IDLE).
3. **Check:**
   - [ ] No false triggers from noise
   - [ ] Button responsive within 300ms

---

## 4. L3 — Integration test (full cycle)

1. Connect all loads: PTC heaters, motors, fans.
2. Place umbrellas on stations.
3. Press button → observe full cycle:

| Phase | Expected | Time |
|---|---|---|
| PREHEAT | Fans spin, PTC warm, staged station rotation every 30s | Until DHT22 ≥ 45°C |
| DRY | Motor spins umbrella (staged), fans + PTC stay on | 15 min timer |
| COOL | Motor off, PTC off, fans run for cooling | 2 min |
| COMPLETE | Everything off, buzzer beeps 3×, LED green | Until button press |

4. **Check:**
   - [ ] Umbrella fabric dries (no wet spots after cycle)
   - [ ] No burning smell from PTC heaters
   - [ ] Temperature stays 40–60°C during DRY phase
   - [ ] Thermal cutoff does NOT trigger during normal operation
   - [ ] Staged rotation verified: only one station's PTC + motor ON at a time

---

## 5. L4 — Stress test

1. Run 3 consecutive cycles (30 min each, 90 min total).
2. **Check:**
   - [ ] Battery voltage stays above 12.0V after 3 cycles
   - [ ] No component overheats (touch test: motor, relay, ESC, PTC mounting)
   - [ ] Fuse ratings correct (no blown fuses)
   - [ ] Buck output stable at 5.0V throughout
   - [ ] LCD remains readable

---

## 6. Safety test

1. **Thermal cutoff:** Hold DS18B20 probe near a heat source (hair dryer). When reading exceeds 65°C → everything should shut off immediately. LCD shows "CRITICAL ERROR! OVERHEAT: XXC". Pressing button should only reset if T < 50°C.
2. **Thermal fuse test:** Monitor PTC heater temperature with DS18B20. If PTC self-regulation fails, 130°C thermal fuse should blow before plastic housing damage.
3. **Battery BMS:** Run until BMS disconnects (low voltage protection). Verify system shuts down gracefully.

---

## 7. Pass/fail checklist

| Test | Pass | Fail | Notes |
|---|---|---|---|
| L1: Smoke test | | | |
| L2a: Relays (PTC + motor) | | | |
| L2b: ESC/fans | | | |
| L2c: Motors | | | |
| L2d: Sensors | | | |
| L2e: Button | | | |
| L3: Full cycle (staged) | | | |
| L4: Stress (3 cycles) | | | |
| Safety: Thermal cutoff | | | |
| Safety: Thermal fuse | | | |
| Safety: BMS | | | |
