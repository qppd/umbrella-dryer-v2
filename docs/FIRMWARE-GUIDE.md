# Firmware Guide (Rev 4)

How the Mega's sketch is organized, how the energy-efficient duty cycling works, and every constant you may tune. Behavior spec: `docs/FLOWCHART.md`. Wiring: `docs/BLOCK-DIAGRAM.md`.

## 1. Pins & libraries

| Pin | Direction | Function |
|---|---|---|
| D2 | in | DHT22 data |
| D3 | in | DS18B20 data (4.7kΩ pull-up to 5V) |
| D4 | out | Heater relay (LOW-level trigger module → `digitalWrite` mapping per module) |
| D5 | out | Station 1 relay |
| D6 | out | Station 2 relay |
| D7 | out | Station 3 relay |
| D8 | out | Chamber fan relay — OPTIONAL; the PTC blower is hardwired on the heater branch and runs whenever the heater is energized. D8 adds post-cycle purge control only |
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

## 3. The energy-efficient control — time-proportional duty

Fast PWM would eat the mechanical relay contacts (§14 note 2 in `docs/BOM.md`). Instead, slow time-proportional control:

```cpp
const unsigned long PERIOD_MS = 4000;          // 4 s cycle period
unsigned long windowStart = 0;

void applyHeaterDuty(float duty /*0..100*/) {
    unsigned long onMs = (unsigned long)(PERIOD_MS * duty / 100.0);
    unsigned long t = millis() % PERIOD_MS;
    digitalWrite(HEATER_PIN, (t < onMs) ? RELAY_ON : RELAY_OFF);
}
```

- **Duty from humidity error:** `duty = constrain(kp * (H - H_TARGET), 0, 100)` — humid chamber → long ON windows; dry chamber → short ones → zero.
- **Auto-shutoff:** when `H < H_TARGET` continuously for `H_STEADY_MS` (5 min), the cycle completes (stops chasing slow sensor drift).
- Why it's efficient: energy delivered ∝ duty, and duty tracks the *actual* moisture load — a 3-umbrella wet load runs ~60% duty; one light umbrella sits near 20%.

## 4. Safety interlock logic (every 500 ms tick)

1. **Sensor validity:** 3 consecutive failed DHT22/DS18B20 reads → FAULT state (heater OFF, red LED, buzzer).
2. **Over-temp cutoff:** `T > T_CUT` → heater OFF **latched** until `T < T_RESET` (hysteresis stops chatter around the threshold). Stations + fan keep running to purge heat.
3. **Relay-vs-state audit:** heater may be ON only if (cycle active) ∧ (humidity demand) ∧ (no over-temp latch) ∧ (sensors valid). Any false → OFF. The heater-branch blower is hardwired with the heater (same 15 A fuse) — air always moves when heat is on; the D8 relay is only the optional purge channel.

## 5. Tunables

| Constant | Default | Meaning / tuning direction |
|---|---|---|
| `T_CUT` | 65 °C | Over-temp cutoff. PTC self-limits anyway; this is the software layer |
| `T_RESET` | 50 °C | Over-temp release (hysteresis) |
| `H_TARGET` | 55 %RH | Dry-chamber target; lower = drier result, longer cycle |
| `KP_DUTY` | ~6 %/RH | Duty per %RH error; too high → relay chatter, too low → sluggish |
| `PERIOD_MS` | 4000 | Relay-safe duty period (2–5 s band; do not go below ~2 s) |
| `H_STEADY_MS` | 300000 | Below-threshold duration before COMPLETE (5 min) |
| `FAN_PURGE_MS` | 120000 | Post-cycle fan purge (2 min) |

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
3. First-ever flash with relays wired: **pull the heater 15A fuse** so a logic mistake cannot run the heater (restore after the interlock drill in `docs/SETUP.md` step 6).
