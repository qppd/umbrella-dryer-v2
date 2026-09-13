# Testing & Validation Plan (Rev 5)

Formal test protocol for the build — module bench tests through full-system validation against the study's claims. Bench bring-up steps live in `docs/SETUP.md` §3; this doc expands them into a pass/fail record for the capstone paper.

## 1. Test levels

| Level | Scope | When |
|---|---|---|
| **T0 — Module bench** | Each part alone (sensors, relays, motors, heater, buck) | During assembly |
| **T1 — Subsystem** | Power path, one station loop, heater loop, sensing loop | After wiring each subsystem |
| **T2 — Integration** | Full firmware + all subsystems, no umbrellas | First full power-on |
| **T3 — System validation** | Loaded cycles: 1, 2, 3 umbrellas; energy + time measurement | Acceptance |
| **T4 — Safety drills** | Fault injection: over-temp, fail-short relay, fuse isolation, sensor loss | Before any unattended use |

## 2. T0 — Module bench tests

| ID | Test | Procedure | Pass criteria |
|---|---|---|---|
| T0.1 | Buck output | Set trimmer with meter, no load then 0.5 A dummy | 5.00 V ± 0.05 V, stable |
| T0.2 | DHT22 | Read every 3 s ×10 reads | Valid numbers, ±5 %RH spread max |
| T0.3 | DS18B20 | Read at room temp; pinch between fingers → rises | Valid temp, responds in <5 s |
| T0.4 | Each relay board | Toggle input from Mega, listen + meter the contacts | Clicks; NO closes; coil drawn from 5V rail |
| T0.5 | Each motor | 12 V direct, uncoupled then coupled | 16 RPM; self-locks when de-energized; no grinding |
| T0.6 | Each SSR-40DA | 12V lamp / appliance load on output; drive input from Mega | Load switches cleanly; OFF leakage ≈ 0; no heating without heatsink check |
| T0.6b | RCD test button | Press test on the RCD outlet | Trips immediately; reset works |
| T0.7 | Heater-fan + exhaust fan (220V) | Plug into RCD outlet via rocker, 60 s on tile | Warm air + airflow; appliance thermostats in circuit; plugs accessible |
| T0.7 | LCD / LEDs / buzzer / button | Sketch I/O test | All visible/audible; button debounces |

## 3. T1 — Subsystem tests

| ID | Test | Procedure | Pass criteria |
|---|---|---|---|
| T1.1 | Power path | Battery → rocker → main fuse → branches, all loads OFF | No voltage drops >0.2 V across each fuse/switch |
| T1.2 | Station loop | Command ST1 ON via firmware; repeat ×3 | Only that motor runs; 1.2 A ±; others unaffected |
| T1.3 | Heater loop | Command SSR1 ON 60 s via firmware | Heater-fan runs; branch current 6.8 A ±10 % on the clamp meter |
| T1.4 | Duty-cycle actuator | Serial-set duty 25/50/75 % | ON-time ratio matches within ±10 % over 3 periods |
| T1.5 | Sensor loop | Serial-print H/T every 500 ms for 5 min | No NaN; values track ambient |
| T1.6 | Condensate path | Pour 200 mL on chamber floor | Fully drains to tray; no leaks at seams/grommets |
| T1.7 | Staging logic | Serial-set humidity error low then high | Stage 1 → stage 2 transition per FIRMWARE-GUIDE §3; SSR2 engages at E_BOOST |

## 4. T2 — Integration (no umbrellas)

| ID | Test | Procedure | Pass criteria |
|---|---|---|---|
| T2.1 | Boot safe-state | Flash with heater fuse OUT; power on | Serial shows heater OFF at boot; relays silent |
| T2.2 | Start cycle | Press start; watch Serial + LCD | IDLE→DRYING; stations (loaded flags) + fan + duty ON |
| T2.3 | Humidity control | Breath into chamber / add damp cloth | Duty rises with humidity; falls as it dries |
| T2.4 | Auto-stop | Let chamber dry below H_TARGET | COMPLETE after 5 min steady; buzzer + green LED; fan purge 2 min |
| T2.5 | Multi-station start | Load-flag only ST1+ST3 | Exactly those two run; ST2 stays off |

## 5. T3 — System validation (matches the paper's claims)

Measure energy at the battery with a DC watt-meter (inline on the main branch).

| ID | Condition | Metric | Claim (docs/BOM.md §9–10) | Pass |
|---|---|---|---|---|
| T3.1 | 1 umbrella, light moisture | Cycle time | ≈ 15–20 min |  |
| T3.2 | 3 umbrellas, light moisture | Cycle time | ≈ 15–25 min |  |
| T3.3 | 3 umbrellas, soaked | Cycle time | ≈ 30–45 min |  |
| T3.4 | 3-umbrella cycle | **Energy (plug-in kWh meter)** | **≈ 0.6–1.0 kWh** |  |
| T3.5 | Battery autonomy | Control + rotation runtime on one charge | ≈ 27 h (25+ cycles) |  |
| T3.6 | Mid-cycle | Chamber air temp | 40–60 °C |  |
| T3.7 | Result | Canopy condition | Dry to touch, no fabric odor/deformation |  |
| T3.8 | Steady draw | Battery current | ≤ 4.4 A (3 motors + logic) |  |
| T3.9 | Station independence | Jam one umbrella mid-cycle | Other stations + heaters continue; only that 3A fuse opens if stalled |  |

## 6. T4 — Safety drills (all must pass before unattended use)

| ID | Drill | Procedure | Pass criteria |
|---|---|---|---|
| T4.1 | Over-temp cutoff | Heat chamber; temporarily lower `T_CUT` to 45 °C | Both SSRs drop; latched until `T < T_RESET`; stations keep running |
| T4.2 | Sensor loss | Unplug DS18B20 mid-cycle (3-fail logic) | FAULT state; both SSRs OFF; red LED + buzzer |
| T4.3 | Fail-short SSR | Simulate welded SSR (jumper output) | Mains rocker kills it; 10 A branch fuse opens on sustained overload; RCD trips on any earth fault |
| T4.4 | Fuse isolation | Run 3 stations; short one motor | Only that station's 3A fuse opens; others keep running |
| T4.5 | BMS / battery | Attempt discharge below cutoff / verify charge cycle | BMS protects; charger terminates at 14.6 V profile |
| T4.6 | Water vs electronics | Sprinkle near chamber pass-throughs | No ingress at grommets; tray catches all condensate |
| T4.7 | Earth integrity | Continuity earth→box, earth→frame, earth→appliance chassis | < 1 Ω each; verified before first mains power-on |

## 7. Test record (copy per run)

| Field | Entry |
|---|---|
| Date / testers | |
| Ambient temp / RH | |
| Umbrellas (count, type, wet state) | |
| Cycle start / end time | |
| kWh-meter reading (mains) | |
| Battery Wh used | |
| Avg duty % (from Serial log) | |
| Peak current (A) | |
| Fuses blown / incidents | |
| Result vs claim (T3 row) | PASS / FAIL + numbers |

## 8. Failure handling

- Any **T4** failure = do not operate until fixed; re-run that drill.
- **T3** misses >15 % of a claim → re-check the linked subsystem (`docs/TROUBLESHOOTING.md`), recalibrate `KP_DUTY` / `H_TARGET` (`docs/FIRMWARE-GUIDE.md` §5), retest.
- Log every run — the record table becomes the paper's validation chapter evidence.
