# Setup and Build Guide (Rev 6)

A complete, in-order build of the Smart Umbrella Dryer. Every step says what to do, what you need, and how to know it worked. If a check fails, stop and fix it before moving on — the next step assumes the last one passed.

**Where to look while building:**
- What each part does and its ratings: `HARDWARE.md`
- How everything connects: `BLOCK-DIAGRAM.md` and `BOM.md` section 15 (pin map)
- Shopping list: `BOM.md` Appendix A

**Golden rules (read once, follow always):**
1. Work with the battery DISCONNECTED unless a step says otherwise.
2. The Mega gets 5 V from the buck converter ONLY — never 12 V on its barrel jack.
3. Relay coils get power from the buck's 5 V rail, never from Mega pins.
4. Relay contacts are DC-only (30 VDC max). The 220V mains side (changeover, inverter output, SSRs, heaters, exhaust fan) is wired ONLY inside the grounded metal box per `wiring/README.md` — have a licensed electrician if unsure.
5. Set the buck to 5.0 V with a multimeter BEFORE connecting anything to its output.
6. The changeover switch is the only point where wall power and the inverter meet — and they must never meet electrically. Verify the inverter remote interlock before the first heated cycle.

---

## Part 1 — Prepare (no assembly yet)

### Step 1.1 — Unbox and check the parts
1. Lay out everything from `BOM.md` Appendix A on a table.
2. Tick each item against the checklist.
3. Check for damage: cracked LCD, dented motor body, bent shafts.

**Check:** all items present, nothing visibly damaged.

### Step 1.2 — Confirm the 5 tricky variants
The store pages sell look-alike versions. Verify each:
| Part | Correct variant | How to confirm |
|---|---|---|
| DHT22 | "DHT22 Black" module (not bare probe) | Small blue/white PCB with holes, 3–4 pins |
| Heater-fans | 1500 W, 220 V, plug-in type | Label on the housing |
| Pillow blocks | KP08 (8 mm bore) | The shaft fits snugly through the inner ring |
| Steel shaft | 8 mm diameter, 300 mm long | Caliper or ruler check |
| Couplings | 8 mm x 8 mm from the set | Both ends grip the 8 mm shaft |
| Inverter | pure sine, 3000 W **continuous**, 12 V, 60 Hz | Label + manual; modified sine or surge-only = return |
| Charger | 14.6 V output, LiFePO4 mode | Label on the charger |

**Check:** all seven correct. Wrong variant = return now, not after assembly.

### Step 1.3 — Charge the battery bank
1. Charge BOTH PowMr 12.8 V 200Ah batteries with the 14.6 V LiFePO4 charger (20 A). Charge them separately if the charger is single-output; parallel charging is fine once both are confirmed healthy.
2. First charge may take hours (the 20 A charger refills ~160 Ah from 80% depth in ~10 h); the charger stops when full.

**Check:** both chargers finish or each battery reads about 13.2–14.4 V on a multimeter.
**Never use a lead-acid 13.8 V charger — it undercharges and confuses the BMS.**

### Step 1.4 — Install the Arduino IDE and libraries
1. Download Arduino IDE 2.x from arduino.cc and install.
2. In IDE: Tools > Board > Arduino Mega or Mega 2560.
3. Library Manager (Ctrl+Shift+I), install:
   - DHT sensor library (Adafruit) — accept "install all" for its dependency
   - OneWire (Paul Stoffregen)
   - DallasTemperature (Miles Burton)
   - LiquidCrystal I2C
4. Plug in the Mega by USB. Tools > Port should show a new COM port.

**Check:** File > Examples > 01.Basics > Blink uploads to the Mega and the onboard LED blinks.

---

## Part 2 — Build the mechanical frame (still no wiring)

### Step 2.1 — Cut and drill the aluminum plate
1. Mark the 3 motor positions on the 6 mm plate, equally spaced across the top of the chamber (your chosen layout — see `HARDWARE.md` section 3 for the two layout options).
2. Drill motor-mount holes per the motor's 115 x 40 mm footprint, plus a center hole for each shaft (about 10 mm).
3. Deburr edges with a file.

**Check:** each motor sits flat on its holes; shaft hole aligns with the motor shaft.

### Step 2.2 — Mount the 3 motors
1. Bolt each motor shaft-down onto the plate with M4 screws.
2. Do not overtighten — the gearbox housing can crack.

**Check:** shafts point down, each turns freely by hand.

### Step 2.3 — Fit couplings and shafts
1. Slide one 8x8 coupling onto each motor shaft; snug one grub screw onto the motor shaft flat.
2. Insert an 8 mm x 300 mm shaft into the other end; tighten the second grub screw.

**Check:** pull-test the shaft — no slip, no wobble.

### Step 2.4 — Add the pillow blocks
1. Under the plate, mount 2 KP08 blocks per shaft, one near each end.
2. Bearings must carry the shaft straight; alignment matters more than force.

**Check:** spin each shaft by hand — smooth, one full turn, no rubbing.

### Step 2.5 — Attach umbrella holders
1. Fabricate or fix a holder to each shaft's lower end (fabrication is team-made; any rigid hanger works).
2. With all 3 open umbrellas, canopies must not touch each other or the walls (keep 5 cm+ clearance).

**Check:** dry-fit an umbrella on each station; rotate by hand; nothing collides.

### Step 2.6 — Build the chamber floor and drain
1. Make the floor slope 3–5 degrees toward one corner.
2. Drill a drain hole there, fit a rubber grommet, push in the silicone drain tube, seal with silicone sealant.
3. Place the drip tray under the tube outside the chamber.

**Check:** pour a cup of water on the floor high side — it all reaches the tray, no leaks.

---

## Part 3 — Install the electrical box (power OFF, fuses OUT)

### Step 3.1 — Mount the electrical parts
1. On a side panel or base plate: Mega (nylon standoffs), buck converter, 2 relay boards (standoffs), barrier terminal block.
2. Label each relay board: ST1+ST2 / ST3 (spare channel unused).
3. Mount the inverter on its own bracket, away from the chamber heat, with airflow around its fan; mount the changeover switch and 250 A ANL fuse holder near the battery access panel.

**Check:** nothing loose; relay boards are not touching the aluminum directly (standoffs isolate them); inverter has clearance for ventilation.

### Step 3.2 — Wire the battery bank and main line
1. Parallel the two batteries: + to + and − to − with the 4 AWG links (same length each).
2. From the battery + bus: TWO feeds — (a) the 250 A ANL fuse → inverter DC+ on 1/0 AWG, ≤ 1 m, and (b) the DC rocker → 25 A fuse → barrier block "MAIN" on 16 AWG (motors + logic only).
3. Battery minus and inverter DC− to the single-point GND block.
4. Leave all branch fuses OUT. Rocker OFF. Inverter off via its remote pin (changeover in wall position).

**Check with meter:** continuity through the rocker toggles ON/OFF; no continuity between MAIN and GND.

### Step 3.3 — Wire and preset the buck converter
1. Buck IN+ from the MAIN block (after the 3 A logic fuse position), IN- to GND.
2. Power the buck ALONE (battery ON briefly): turn its trimmer until a multimeter on OUT reads 5.00 V.
3. Battery OFF again.

**Check:** 5.00 V +-0.05 V measured at OUT+. Do this before the Mega exists in the circuit.

### Step 3.4 — Wire the 5 V logic rail
1. Buck OUT+ to the barrier block "5V" position; OUT- to GND.
2. From 5V: wires to Mega 5V pin, and to VCC on each relay board.
3. From GND: wires to Mega GND, and GND on each relay board.

**Check:** with the battery ON, the Mega power LED lights. Battery OFF.

### Step 3.5 — Wire the SSR and relay inputs to the Mega
| Input | Mega pin |
|---|---|
| SSR-40DA #1 (heater 1) | D4 |
| SSR-40DA #2 (heater 2) | D5 |
| Station 1 IN | D6 |
| Station 2 IN | D7 |
| Station 3 IN | D8 |
| Changeover aux (mode sense) | D14 |

1. Dupont jumper from each Mega pin to that relay board's IN pin.
2. Fit 10k pull-up resistors from each IN pin to the relay board's VCC (this is the low-trigger module's OFF level) so boards stay OFF while the Mega boots.

**Check:** all 5 wires follow the table (D4–D8); bias resistors fitted — 10 kΩ pull-downs on the SSR inputs (D4/D5), 10 kΩ pull-ups on the relay inputs (D6–D8).

### Step 3.6 — Wire the source selection and mains AC box (adult supervision / electrician recommended)
1. **Changeover switch first:** wall outlet → position A; inverter AC output → position B; changeover common → RCD/GFCI. Break-before-make — the two sources must never share a node.
2. **Inverter remote interlock:** changeover second pole grounds the inverter remote pin in position A (wall). Wire the aux contact to Mega D14 (other leg to GND; LOW = wall mode).
3. RCD output feeds the 2-gang mains rocker.
4. Each heater line: rocker gang → 10 A fuse → SSR-40DA output terminals → plug/socket for that heater-fan.
5. Third gang or direct rocker line → 12" Omni exhaust fan plug.
6. SSR input terminals to the Mega side: input + from D4/D5 (each with a 10 kΩ pull-down to that SSR's input−), input − to Mega GND.
7. SSRs on heatsinks with thermal paste, inside the grounded metal box. Earth the box, the chamber frame, both appliance chassis, and the inverter chassis.

**Check:** continuity earth→box, earth→frame, earth→chassis, earth→inverter chassis each < 1 Ω; RCD test button trips; with the mains rocker OFF, no voltage at any SSR output; with the changeover in A, the inverter is OFF (its display dark) and D14 reads LOW.

### Step 3.7 — Wire the 3 station branches
Per station (1, 2, 3), repeat:
1. MAIN block to that station's 3 A fuse.
2. Fuse output to that station's relay COM.
3. Relay NO to motor + (18 AWG).
4. Motor minus to GND block.

**Check:** three separate branches, each with its own 3 A fuse. Labeled at both ends.

### Step 3.8 — Wire the sensors
1. DHT22: + to 5V, - to GND, data to D2.
2. DS18B20: red to 5V, black to GND, yellow to D3, plus a 4.7k resistor from D3 to 5V (the pull-up).
3. Mount the DS18B20 probe in the heater's air stream; mount DHT22 mid-chamber, away from direct air jets and above the drain.

**Check:** resistor reads 4.7k with a meter; probe positions match `HARDWARE.md`.

### Step 3.9 — Wire the user interface
1. LCD: VCC 5V, GND, SDA to pin 20, SCL to pin 21.
2. LEDs: each LED anode > 220 ohm resistor > its pin (green D9, yellow D10, red D11), cathode to GND.
3. Buzzer: + to D12, - to GND.
4. Start button: one leg to D13, other leg to GND (no resistor needed).

**Check:** the button legs are not shorted to each other's neighbors; LED resistors are all in place.

### Step 3.10 — Final wiring inspection
1. Compare every wire against `BLOCK-DIAGRAM.md`.
2. Tug every terminal gently — nothing loose.
3. Confirm: no wire near the heater body within 5 cm; grommets in every wall hole; one ground point per return path.

**Check:** a second team member traces the diagram independently and agrees.

---

## Part 4 — First power-on (stage by stage)

### Step 4.1 — Logic only
1. All branch fuses OUT except the 3 A logic fuse. Rocker ON.
2. Meter: buck output still 5.0 V; Mega LED on.

**Check:** buck steady, Mega boots.

### Step 4.2 — Flash the firmware
1. Open the project sketch, upload to the Mega.
2. Open Serial Monitor at 115200.

**Check:** self-test prints both sensors valid; no relay clicks during boot.

### Step 4.3 — Heater branch test (wall mode first)
1. Changeover in position A (wall). Mains rocker OFF; plug both heater-fans into their SSR-fed sockets; RCD already verified.
2. Mains rocker ON; from the serial console command SSR1 ON for about 30 seconds.

**Check:** warm air within half a minute; branch current ≈ 6.8 A on the clamp meter; exhaust fan (rocker) pulls air through the chamber. SSR1 OFF stops it; verify no SSR heating beyond warm on the heatsink.
3. **Then the battery-mode drill:** changeover to B. Confirm the inverter starts (display on, remote released, D14 HIGH). Command SSR1 ON 30 s: heater 1 + fan draw ≈ 9.3 A AC ≈ 188 A DC on the inverter feed. Confirm SSR2 never engages in this mode (stage-2 cap). Return to A and confirm the inverter shut down (remote grounded).

**Check:** both source modes heat; the interlock never allows both sources; D14 tracks the switch position on Serial.

### Step 4.4 — Station tests
Insert one station's 3 A fuse at a time; command that station only.

**Check:** that shaft spins at 16 RPM; the other shafts stay still. Repeat for all three.

### Step 4.5 — Full dry cycle (no umbrellas)
Press start.

**Check:** stations and staged heater duty run; duty percentage changes on the LCD/serial as the chamber warms; stage 2 engages when the humidity error is large; cycle completes by itself; buzzer + green LED.

### Step 4.6 — Over-temp drill (safety check)
1. Temporarily set the firmware cutoff T_CUT to 45 C.
2. Run the heater until cutoff triggers.

**Check:** both SSRs drop, yellow LED blinks, stations keep running; heaters stay OFF until temperature falls, then the cycle may resume. Set T_CUT back to 65 C after.

### Step 4.7 — Wet test, then acceptance
1. One damp umbrella: full cycle. Record time and energy per `TESTING.md` T3.
2. Then three umbrellas: the acceptance run.

**Check:** results logged in `TESTING.md` section 7; drip tray emptied after each cycle.

---

## Part 5 — Everyday use

1. Pick the source with the changeover: A (wall — full speed, stage 2 available) or B (battery — stage 1 only, ~6–8 cycles per charge).
2. Batteries charged (14.6 V LiFePO4 charger only); umbrellas shaken out, hung on stations, drip tray seated.
3. Press start. The system stops on its own when the chamber dries.
4. After the buzzer: unload, empty the drip tray, power off at the rockers.
5. Keep the charger away from the chamber; wipe the floor slope weekly.

---

## Troubleshooting during the build

If any check fails: find the symptom in `TROUBLESHOOTING.md` and fix it there before continuing. Do not skip a failed check — later steps assume earlier ones passed.
