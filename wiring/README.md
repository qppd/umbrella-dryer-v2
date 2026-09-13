# Wiring Reference — Arduino Mega 2560 (Rev 5: mains heat + 12V stations)

Master connection list for every component. Rev 5 architecture: **heat is 220V AC** (2x 1500W PTC heater-fans via SSR-40DA), **rotation + control stay 12V DC** (battery-backed). The Mega never touches mains — SSRs and DC relays keep the domains separate. Pin map source: `docs/BOM.md` section 15.

## 0. Domains overview

| Domain | Source | Loads | Switched by | Mega sees it? |
|---|---|---|---|---|
| 220V AC | Wall outlet | 2x 1500W PTC heater-fans, 12" Omni exhaust fan | 2x Fotek SSR-40DA | NO — SSR input side only |
| 12V DC | LiFePO4 battery | 3 worm motors | 3x relay channels | NO — optocoupler input only |
| 5V DC | LM2596S buck | Mega, sensors, LCD, relay coils | — | yes (this is the Mega's home) |

## 1. Pin map — Mega 2560 side

| Mega pin | Direction | Connects to | Wire / notes |
|---|---|---|---|
| 5V | power in | LM2596S buck OUT+ (set 5.00 V) | 22 AWG — never the barrel jack |
| GND | common | Ground rail (DC side only) | 22 AWG |
| D2 | in | DHT22 DATA | 22 AWG |
| D3 | in | DS18B20 yellow DATA | + 4.7 kΩ pull-up D3→5V |
| D4 | out | SSR-40DA #1 input (3–32VDC) — heater-fan 1 | + 10 kΩ pull-up to SSR input− (off at boot) |
| D5 | out | SSR-40DA #2 input — heater-fan 2 | + 10 kΩ pull-up |
| D6 | out | 2-CH relay #1 ch1 — Station 1 motor | + 10 kΩ pull-up to relay VCC |
| D7 | out | 2-CH relay #1 ch2 — Station 2 motor | + 10 kΩ pull-up |
| D8 | out | 2-CH relay #2 ch1 — Station 3 motor | + 10 kΩ pull-up |
| D9 | out | Green LED (220 Ω) | cathode→GND |
| D10 | out | Yellow LED (220 Ω) | cathode→GND |
| D11 | out | Red LED (220 Ω) | cathode→GND |
| D12 | out | Buzzer + | − → GND |
| D13 | in | Start button (other leg → GND) | INPUT_PULLUP |
| 20/21 | I2C | LCD SDA / SCL | addr 0x27/0x3F |

Note: the 12" exhaust fan has **no Mega control channel** — it switches with the mains rocker (see section 2). Fan stage control = stage 1 only.

## 2. 220V AC domain (mains — hazardous)

| From | To | Wire | Protection |
|---|---|---|---|
| Wall outlet | **GFCI/RCD outlet** | — | 30 mA life protection — mandatory |
| RCD outlet | Mains rocker + 10 A** mains fuses (2 lines) | 3-core 2.0 mm² (14 AWG eq.) | Line + neutral fused |
| Fused line 1 | SSR-40DA #1 OUT → heater-fan 1 plug/socket | 2.0 mm² | 10 A |
| Fused line 2 | SSR-40DA #2 OUT → heater-fan 2 plug/socket | 2.0 mm² | 10 A |
| Mains rocker (second gang) | 12" Omni exhaust fan plug | 2.0 mm² | 10 A |
| SSR input + (per SSR) | Mega D4 / D5 through the 10 kΩ pull-up | 22 AWG | — |
| SSR input − | SSR common to Mega GND (DC domain) | 22 AWG | — |

**1500 W = 6.8 A at 220V.** SSR-40DA (40 A) per heater = 5.9x margin; the 10 A branch fuses protect wiring. SSRs mount on a **heatsink** (7–10 W each dissipated at 6.8 A) inside the electrical box, away from the chamber heat.

### Mains safety rules (non-negotiable)
1. **GFCI/RCD-protected outlet only.**
2. Every mains terminal inside a **closed grounded metal electrical box**; earth the box, the chamber frame, and both appliance chassis.
3. SSR fail-short now means an **AC heater stuck ON**: mitigated by RCD + branch fuses + PTC self-regulation + the **mains rocker as the manual kill** (not the battery rocker).
4. The appliance plugs stay accessible — unplug before any chamber service.
5. Thermal cutoffs in each heater-fan appliance stay in circuit (they are built in).

## 3. 12V DC domain (battery)

| From | To | Wire | Protection |
|---|---|---|---|
| Battery + | DC rocker → 25 A main fuse → barrier MAIN | 16 AWG | 25 A |
| MAIN | Station branches x3: 3 A fuse → relay COM→NO → motor + | 18 AWG | 3 A each |
| MAIN | Logic: 3 A fuse → buck IN+ | 16 AWG | 3 A |
| Motor − / relay GND | Ground rail (DC) | — | single point |
| Buck OUT+ (5 V) | Mega 5V, relay VCCs, sensors, LCD | 22 AWG | set 5.00 V first |

Load check: 3 motors 3.6 A + logic ~0.8 A ≈ **4.4 A steady** — BMS 30 A now has a huge margin; runtime is battery-limited only (384 Wh ÷ ~14 W ≈ days; realistic limit = mains availability).

## 4. Component terminal tables

### Fotek SSR-40DA (x2) — AC output
| SSR terminal | Goes to |
|---|---|
| Input + | Mega D4 (SSR1) / D5 (SSR2) |
| Input − | Mega GND (DC common) |
| Output 1 (line) | Fused mains line (10 A) |
| Output 2 (load) | Heater-fan plug line |

Active-LOW behavior at boot: 10 kΩ pull-ups hold SSR inputs OFF until firmware drives them.

### 2x 2-CH relay boards (12V motor switching)
| Board pin | Goes to |
|---|---|
| VCC | 5 V rail (NOT a Mega pin) |
| GND | DC ground rail |
| IN1–IN4 | Mega D6–D8 (3 used) + spare |
| COM/NO | 12 V station branches |

### Appliances
- **2x 1500W PTC heater-fans (220V):** plug/socket on each SSR output; built-in thermostat + thermal cutoff stay in circuit.
- **Omni 12" exhaust fan (220V):** its own fused mains gang on the mains rocker, NOT SSR-controlled.
- **3x worm motors (12V):** relay NO → motor +; motor − → ground rail.
- **DHT22 / DS18B20 / LCD / LEDs / buzzer / button:** unchanged from Rev 4 — see `docs/FIRMWARE-GUIDE.md` pin table and section 1 above.

## 5. Rules that keep this wiring safe

1. **Two separate kill switches:** mains rocker (AC domain) and DC rocker (battery) — label both.
2. Mega never sees mains or 12V — only buck 5 V and sensor-level signals.
3. SSR heatsinks sized for 7–10 W each; thermal paste; vertical fins; inside the closed box.
4. Slow duty cycling on the SSRs too (zero-cross DA type tolerates kHz poorly at load; keep 2–5 s period).
5. Single-point DC ground; mains earth separate and complete (box, frame, chassis).
6. Every chamber wall pass-through gets a grommet; keep appliance cords off the hot floor side.
