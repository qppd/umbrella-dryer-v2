# Troubleshooting (Rev 4)

Symptom → cause → fix, per subsystem. Wiring map: `docs/BLOCK-DIAGRAM.md`. Control behavior: `docs/FLOWCHART.md`.

## 1. Power & logic

| Symptom | Likely cause | Fix |
|---|---|---|
| No LED anywhere, LCD blank | Battery low / rocker on control side not closed / 3A logic fuse open | Check battery ≥ 12.0V; rocker; fuse; then buck input voltage |
| Mega resets when heater relay clicks | Buck output set too low or coil share overloads it | Re-verify buck at 5.0V under load; relay coils must draw from the 5V rail, not the Mega |
| Buck output ~1.2V or erratic | Trimmer never set / bad connection | Set buck to 5.0V with a meter BEFORE the Mega is connected |
| Mega brownout on start | 12V into the barrel jack | Mega is fed from buck 5V → 5V pin only (Makerlab warning) |
| Battery BMS won't deliver | BMS tripped (short/over-discharge) → remove load, charge with LiFePO4 charger | Charger must be the 14.6V LiFePO4 model — a 13.8V lead-acid charger undercharges |

## 2. Heater

| Symptom | Likely cause | Fix |
|---|---|---|
| Heater never on, relay never clicks | Input polarity to optocoupler / wiring to wrong pin / cycle not started | Check D4 mapping per module (LOW-level trigger); confirm state on Serial |
| Relay clicks, no heat | 15A fuse open / loose COM-NO / heater lead off | Fuse, then meter across heater terminals (12V?), then heater itself |
| Heater runs but cycle crawls | 70W variant was shipped instead of 100W / chamber leaks | Verify wattage marking; seal chamber seams (silicone) |
| Over-temp FAULT frequently | `T_CUT` too close to normal / probe touching heater body / poor airflow | `T_CUT` 65 °C default; reposition probe; fan must cross all stations |
| Heater latches ON regardless of code | Relay welded (duty period too short historically) | Replace relay board; keep PERIOD_MS ≥ 2 s; rocker is the kill switch |
| PTC hot spot / smell | PTC running past spec | Power off; PTC self-regulates only within rated airflow — check the blower runs with it |

## 3. Motors / stations

| Symptom | Likely cause | Fix |
|---|---|---|
| One station dead, others fine | That station's 3A fuse (jam blow) or relay ch wiring | Check fuse; motor terminals; swap relay channels to isolate |
| Station hums/clicks but no rotation | Jam / coupling set screw loose | Clear jam (worm is stall-tolerant but the fuse may already be open); tighten 8×8 coupling screws |
| Motor reversed | Leads swapped | Swap motor+ / motor− at that branch |
| Runs hot, slow | Undervoltage (branch drop) or binding shaft | Meter at motor under load ≥ 11V; re-check pillow-block alignment |
| Station stops mid-cycle | Thermal? Fuse half-seated | Meter continuity on the 3A fuse; seat fully |
| Umbrella wobbles violently | Holder off-axis / bent shaft | Re-seat holder; shaft is ground 304 SS — replace if bent |

## 4. Sensors

| Symptom | Likely cause | Fix |
|---|---|---|
| DHT22 reads NaN / 99.9 | Bad pull / too-fast polling (needs ≥2 s interval) / wrong variant | Verify it's the module variant; 2 s+ between reads; check D2 wiring |
| DS18B20 reads −127 | No 4.7kΩ pull-up / probe damaged | Add pull-up data→5V; try the backup probe point |
| Humidity stuck high | DHT22 saturated after a wet 3-up cycle | Let it air-dry; silica gel pack in the chamber helps between cycles |
| Humidity disagrees with feel | Sensor near drain/fan stream | Mount DHT22 mid-chamber, away from direct air jets |
| LCD blank / blocks | Wrong I2C address / contrast | Scan for 0x27 vs 0x3F; adjust pot on backpack |

## 5. Control behavior

| Symptom | Likely cause | Fix |
|---|---|---|
| Relay chatter (fast ticking) | Duty period too short or KP too high | PERIOD_MS ≥ 2 s; lower KP_DUTY |
| Cycle never completes | `H_TARGET` too low for the day's ambient / DHT drift | Raise H_TARGET a few %; verify with a second hygrometer |
| Completes too early (damp umbrellas) | Threshold hit by brief humidity dip | H_STEADY_MS enforces 5 min — verify it's implemented; lower H_TARGET |
| Battery gives fewer cycles than spec'd | Heater duty stuck high (leaky chamber) / battery degraded | Log duty; check door seal; charge to full with LiFePO4 charger |

## 6. Mechanical / water

| Symptom | Likely cause | Fix |
|---|---|---|
| Water pooling, not draining | Slope < 3° or drain blocked | Re-shim floor; clear tube; mesh liner funnel check |
| Drip tray overflows mid-cycle | Tray too small / 3 golf umbrellas soaked | 500 mL tray spec; empty between cycles |
| Rust spots on chassis | Mild-steel budget plate used | Rust-proof; prefer the 6061 aluminum plate near condensate |

## 7. Escalation

1. Isolate: single-branch test (one fuse in, others out).
2. Meter before multimeter-guessing: voltage at battery → main fuse → branch fuse → load terminal.
3. Swap test: relay boards and channels are identical — swap to see if the fault follows the part.
4. Serial prints at every state transition show exactly which interlock blocked the heater.
