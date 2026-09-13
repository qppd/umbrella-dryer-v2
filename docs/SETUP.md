# Setup & Assembly Guide (Rev 4)

From boxes of parts to a working dryer. Order matters: assemble mechanical first, wire low-current logic before power, and bring the system up stage-by-stage. Shopping list: `docs/BOM.md` Appendix A.

## 0. Prep — what you need beyond the kit

- Soldering iron + solder (relay terminals, LED/buzzer wiring)
- Phillips/screwdriver set, hex keys, crimping tool
- Multimeter (continuity + voltage — mandatory before first power-on)
- Drill + 4/6/8mm bits (aluminum plate, chamber wall pass-throughs)
- Thermal paste *(if reusing the aluminum plate as a heatsink surface for the relay board backplate)*

## 1. Mechanical assembly

1. **Mount the 3 motors** on the 6mm aluminum plate, equally spaced across the chamber top — one station position per umbrella. Shaft points down into the chamber.
2. **Fit 8×8 couplings** to each motor shaft; then the 8mm × 300mm shafts into the couplings with the shafts running through **2× KP08 pillow blocks each** (mounted at the plate edges).
3. **Attach the 3 umbrella holders** to the lower shaft ends — each holder must clear the others; umbrella canopies must not overlap when spinning (16 RPM is slow, but check tip clearance ≥ 5 cm).
4. **Chamber:** sloped floor 3–5° toward one corner → slotted drain hole → silicone drain tube → drip tray outside. Seal the floor seam with silicone sealant.
5. **Heater + fan:** mount the PTC heater low on one wall and the 120mm fan opposite (air crosses all 3 stations before returning past the heater). Verify no wire runs within 5 cm of the heater body.
6. **Spin test (dry, no power to heater):** hand-rotate each shaft — free, no wobble, no binding. Then briefly power each motor alone: smooth 16 RPM, self-locking when de-energized.

## 2. Electrical build — order: fuses → power → logic → actuators → sensors

1. **Fuse box first:** 25A main at the battery positive tap; then 15A (heater), 3A ×3 (stations), 3A (logic) branches off the barrier terminal block. All fuses OUT (removed) at this stage.
2. **Battery → rocker switch → main fuse block.** Rocker OFF. Measure: continuity across switch terminals toggles; no shorts to the aluminum chassis.
3. **Buck converter:** battery+ → buck IN+ (through its 3A fuse), battery− → IN−. Set output to **5.0V with a multimeter BEFORE connecting anything downstream** (turn the trimmer; the 7-seg display is a hint, the meter is the truth). Only then: buck OUT → 5V rail → **Mega 5V pin** (never the barrel jack).
4. **Relay boards:** mount on nylon standoffs. Coil VCC/GND from the 5V rail. Each input pin (IN1–IN4) → Mega D4–D8 per `docs/BLOCK-DIAGRAM.md`. Jumper common grounds only at the barrier block.
5. **Heater branch:** fuse 15A in, wire 16 AWG: relay COM → heater+, heater− → battery−. Blower fan wired on the heater branch (it must run whenever the heater can).
6. **Station branches:** fuse 3A in, wire 18 AWG: relay ch COM → motor+, motor− → battery−. One branch per station — label them ST1/ST2/ST3 at both ends.
7. **Circulation fan:** 4th relay channel, 18 AWG.
8. **Sensors:** DHT22 → D2 (data), DS18B20 → D3 with **4.7kΩ pull-up data-to-5V**, probe positioned in the heater air stream. LCD → SDA 20 / SCL 21. LEDs (220Ω each) D9/D10/D11 → GND. Buzzer D12. Start button D13→GND (INPUT_PULLUP, no resistor).
9. **Grounding:** every − returns to the battery − rail; the aluminum chassis bonds to battery − at one point.

## 3. First power-on — stage by stage

| Step | Action | Pass criteria |
|---|---|---|
| 1 | All fuses out except logic. Rocker ON. | Buck shows 5.0V; Mega power LED on; LCD shows sketch boot line |
| 2 | Flash firmware (`docs/FIRMWARE-GUIDE.md`), open Serial Monitor @115200 | Self-test prints: DHT22 valid, DS18B20 valid, relays in safe OFF state |
| 3 | Insert heater fuse. Serial: command heater ON for 5 s, watch | Relay clicks; meter across heater: ~12V; warm air within ~30 s; OFF returns 0V |
| 4 | Insert station fuses one at a time; command each motor | Each shaft spins 16 RPM; other stations unaffected |
| 5 | Insert nothing new; run a **no-umbrella test cycle** | Duty cycling visible on serial (heater % drops as chamber warms), auto-stop on humidity logic, buzzer + green LED |
| 6 | **Fail-safety drill:** with heater ON, lift the DS18B20 probe toward the heater outlet / or temporarily set cutoff to 45°C | Heater relay drops out on over-temp; latches until temp falls |
| 7 | Load 1 umbrella, full cycle | Complete cycle within expected time; drip tray collects condensate |
| 8 | Full 3-umbrella cycle | ≈90–95 Wh on the cycle (if metering); all stations stop; no nuisance fuse blows |

## 4. Software setup (Arduino IDE)

1. **IDE:** Arduino IDE 2.x → Boards Manager → **Arduino Mega 2560**.
2. **Libraries (Library Manager):**
   - `DHT sensor library` (Adafruit) + `Adafruit Unified Sensor`
   - `OneWire` + `DallasTemperature`
   - `LiquidCrystal I2C` (address 0x27 **or** 0x3F — scan if blank)
3. **Board settings:** Tool → Board → *Arduino Mega or Mega 2560*; Processor → *ATmega2560*; Port → the Mega's COM port.
4. Flash and watch Serial @115200. Wiring reference while you work: `docs/BLOCK-DIAGRAM.md`. Behavior reference: `docs/FLOWCHART.md`.

## 5. Pre-operation checklist

- ☐ Buck verified 5.0V **before** Mega connection
- ☐ Correct fuses in every branch (25/15/3/3/3/3)
- ☐ Rocker switches the **control side**, not full battery load
- ☐ No wire within 5 cm of heater body; heater branch fan runs with heater
- ☐ Over-temp drill passed (step 6)
- ☐ Drip tray seated; drain unobstructed
- ☐ Battery charged with the **LiFePO4 14.6V** charger only
