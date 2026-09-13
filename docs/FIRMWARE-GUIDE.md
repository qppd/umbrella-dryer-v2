# Firmware Guide (Rev 5)

How the Mega's sketch is organized, how the energy-efficient duty cycling works, and every constant you may tune. Behavior spec: `docs/FLOWCHART.md`. Wiring: `docs/BLOCK-DIAGRAM.md`.

## 1. Pins & libraries

| Pin | Direction | Function |
|---|---|---|
| D2 | in | DHT22 data |
| D3 | in | DS18B20 data (4.7kΩ pull-up to 5V) |
| D4 | out | SSR-40DA #1 input — heater-fan 1 (staged base) |
| D5 | out | SSR-40DA #2 input — heater-fan 2 (boost stage) |
| D6 | out | Station 1 relay |
| D7 | out | Station 2 relay |
| D8 | out | Station 3 relay |
| D9/D10/D11 | out | Green / Yellow / Red LED (220Ω) |
| D12 | out | Buzzer |
| D13 | in | Start button, INPUT_PULLUP |
| 20/21 | I2C | LCD 16×2 (scan 0x27 / 0x3F) |

Libraries: `DHT sensor library`, `OneWire`, `DallasTemperature`, `LiquidCrystal I2C`.

## 2. Program layout

```cpp
// --- tunables (§5) ---
// --- pin map ---
// --- state machine: IDLE, DRYING, CUTOFF, COMPLETE, FAULT ---
// setup():  safe relay states FIRST (heater OFF), init sensors, LCD, self-test
// loop():   500 ms tick -> read sensors -> safety gate -> duty-cycle heater -> update UI
// helper:   heaterDuty(float H) -> duty% from humidity error
// helper:   applyTimeProportional(duty%) -> ON window inside 4 s period
```

**Rule #1: in `setup()`, drive all relay pins to the OFF level before anything else** — the ~100 ms before your first statement runs must not energize the heater. Low-level-trigger relay boards energize with a LOW pin, so write their ON-idle level immediately (and pick pin ordering with that in mind).

## 3. The energy-efficient control — staged heaters + time-proportional duty

Rev 5 heat is two mains heater-fans (each with its own blower) switched by SSR-40DAs. Each SSR gets slow time-proportional duty; the second heater is a boost stage:

```cpp
const unsigned long PERIOD_MS = 4000;   // 4 s period — SSR-safe

void applyHeaterDuty(int ssrPin, float duty /*0..100*/) {
    unsigned long onMs = (unsigned long)(PERIOD_MS * duty / 100.0);
    unsigned long t = millis() % PERIOD_MS;
    digitalWrite(ssrPin, (t < onMs) ? SSR_ON : SSR_OFF);
}

// staging from humidity error e = H - H_TARGET:
//   e <= 0          -> both SSRs OFF
//   e <  E_BOOST    -> SSR1 duty = kp*e,  SSR2 OFF        (stage 1)
//   e >= E_BOOST    -> SSR1 ON, SSR2 duty = kp*(e-E_BOOST) (stage 2)
```

- **Stage 1** (light load / holding 40–60C): heater 1 duty-cycles from the humidity error; heater 2 stays off — this is where the energy is saved.
- **Stage 2** (wet 3-umbrella load or pull-down): heater 1 runs steady, heater 2 duty-cycles.
- **Auto-shutoff:** humidity at/below target for `H_STEADY_MS` (5 min) → COMPLETE; DS18B20 > 65C latches both SSRs OFF until < 50C.
- Each appliance's own thermostat + thermal cutoff remain in circuit as the independent hardware layer.

The 12" exhaust fan has no controller channel — it runs on the mains rocker while drying (stage 1 airflow).

## 4. Safety interlock logic (every 500 ms tick)

1. **Sensor validity:** 3 consecutive failed DHT22/DS18B20 reads → FAULT state (heater OFF, red LED, buzzer).
2. **Over-temp cutoff:** `T > T_CUT` → heater OFF **latched** until `T < T_RESET` (hysteresis stops chatter around the threshold). Stations + fan keep running to purge heat.
3. **SSR-vs-state audit:** either heater may be ON only if (cycle active) ∧ (humidity demand) ∧ (no over-temp latch) ∧ (sensors valid). Any false → both SSRs follow the staging table down to OFF. The heater-fans' built-in blowers run with their heaters; the exhaust fan is on the mains rocker.

## 5. Tunables

| Constant | Default | Meaning / tuning direction |
|---|---|---|
| `T_CUT` | 65 °C | Over-temp cutoff (latches both SSRs OFF) |
| `T_RESET` | 50 °C | Over-temp release (hysteresis) |
| `H_TARGET` | 55 %RH | Dry-chamber target; lower = drier result |
| `E_BOOST` | ~15 %RH | Humidity error that engages heater 2 (stage 2) |
| `KP_DUTY` | ~6 %/RH | Duty per %RH error per SSR; too high → chatter |
| `PERIOD_MS` | 4000 | SSR-safe duty period (2–5 s band) |
| `H_STEADY_MS` | 300000 | Below-threshold duration before COMPLETE (5 min) |

## 6. Station logic

- Start button → stations marked **loaded** run; unmarked stay off (dry 1–3 umbrellas freely).
- All loaded stations share the single chamber humidity signal.
- UI shows which stations are running; a station that "runs" but shows no rotation per `docs/TROUBLESHOOTING.md` §Motors = blown 3A fuse (jam) — replace, then re-run.
- Self-locking worm drives hold position when a station drops off mid-cycle.

## 7. LCD screens (16×2, I2C 0x27/0x3F)

| State | Line 1 | Line 2 |
|---|---|---|
| IDLE | `UMBRELLA DRYER` | `READY - PRESS START` |
| DRYING | `DRYING H=78%` | `DUTY 62% ST:1,2,3` |
| CUTOFF | `OVERTEMP CUT!` | `T=68C COOLING` |
| COMPLETE | `CYCLE DONE` | `~xx Wh  UNLOAD` |
| FAULT | `FAULT: DHT22` | `CHECK SENSOR` |

## 8. Flashing & debugging

1. Board: *Arduino Mega or Mega 2560 (ATmega2560)*, correct COM port, Serial @115200.
2. Debug through Serial prints at each state transition + a 1 Hz sensor line — cheaper than an oscilloscope for this control loop.
3. First-ever flash with the mains side wired: keep the **mains rocker OFF** so a logic mistake cannot run the heaters (energize only after the interlock drill in `docs/SETUP.md` step 4.6).
