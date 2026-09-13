# System Architecture (Rev 6)

Big-picture view: layers, power domains, timing of one drying cycle, and the principles that shaped the design.

## 1. Layered architecture

```mermaid
flowchart TD
    subgraph L5["LAYER 5 — Human interface"]
        LCD["LCD 16x2 I2C"]
        LED["Status LEDs x3"]
        BUZ["Buzzer"]
        BTN["Start button"]
    end
    subgraph L4["LAYER 4 — Control"]
        FW["Firmware state machine<br/>IDLE / DRYING / CUTOFF / COMPLETE / FAULT<br/>humidity duty-cycling + over-temp interlock"]
    end
    subgraph L3["LAYER 3 — Sensing"]
        DHT22b["DHT22 — chamber humidity (feedback signal)"]
        DS18b["DS18B20 — heater-zone temp (safety signal)"]
    end
    subgraph L2["LAYER 2 — Actuation (optocoupler isolated)"]
        RH["2x SSR-40DA — mains heaters (D4/D5)"]
        RM["2x 2-CH relays — 3 stations"]
    end
    subgraph L1["LAYER 1 — Power"]
        BAT["2x LiFePO4 12.8V 200Ah parallel<br/>BMS 200A each"]
        BUCK["LM2596S buck -> 5V"]
        INV["3000W pure sine inverter<br/>+ changeover: wall OR inverter -> RCD"]
        FUSES["AC: RCD + 10A x2 heater lines | DC: 25A main / 3A x3 stations / 3A logic / 250A ANL inverter feed"]
    end
    subgraph L0["LAYER 0 — Plant (mechanical + thermal)"]
        CH["Drying chamber (sloped floor, drain, drip tray)"]
        ST["3x motor stations: worm motor -> 8x8 coupling -> 8mm shaft -> umbrella holder"]
        HEAT["2x 1500W PTC heater-fans + 12in exhaust fan -> forced convection 40-60 C"]
    end

    L0 --> L3
    L3 --> L4
    L4 --> L2
    L2 --> L0
    L1 --> L2
    L1 --> L4
    L4 <--> L5
```

## 2. Power domains (Rev 6: dual source, three power domains)

| Domain | Source | Consumers | Protection |
|---|---|---|---|
| **220V AC heat** | Wall outlet OR 3000W pure sine inverter — selected by the changeover, never both | 2× 1500W heater-fans (6.8A each) + 12" exhaust fan (~2A) | RCD 30mA + 10A branch fuses + grounded box + earthing |
| 12V DC stations | 2× LiFePO4 200Ah parallel (BMS 200A each) | 3 motors 3.6A rated + inverter DC feed (188A steady at the stage-1 cap) | 250A ANL (inverter feed) + 25A main + 3A per station |
| 5V logic | LM2596S buck | Mega · sensors · LCD · relay coils (~0.7A) | 3A branch |
| Signal | Mega pins | SSR DC inputs (~12 mA) + D14 mode sense + optocoupler LEDs (2–5 mA) | Isolation barrier to both power domains |

**Isolation philosophy:** the Mega touches no power domain — it only drives SSR inputs, reads D14, and drives optocoupler LEDs. Mains lives in a closed earthed box; the changeover is the single point where the two AC sources meet, and they never meet electrically (the inverter remote pin is grounded in wall mode).

## 3. One cycle — sequence

```mermaid
sequenceDiagram
    participant U as User
    participant FW as Firmware (Mega)
    participant S as DHT22 + DS18B20
    participant A as Relays (heater/stations/fan)

    U->>FW: Press start (umbrellas loaded)
    FW->>S: Self-test read
    FW->>A: Stations ON, fan ON (heater OFF)
    loop every 500 ms
        FW->>S: Read humidity H, temp T
        alt T > 65 C
            FW->>A: Both SSRs OFF (latched until T < 50 C)
        else H above threshold
            FW->>A: Stage heaters: SSR1 duty, SSR2 boost, 4 s period
            Note over FW,A: battery mode (D14): stage 1 only — SSR2 forced OFF
        else H below threshold for 5 min
            FW->>A: All OFF (exhaust fan via rocker purges)
        end
    end
    FW-->>U: COMPLETE — buzzer + green LED
    U->>U: Empty drip tray, unload umbrellas
```

## 4. Design principles (why it is built this way)

| Principle | Realization |
|---|---|
| **Energy efficiency is the thesis** | Staged heaters run only on humidity demand and never idle-heating: auto-shutoff + staging (wall mode ≈0.6–1.0 kWh/cycle; battery mode stage-1 ≈0.4–0.6 kWh, 6–8 cycles/charge) |
| **Defense in depth on heat** | appliance thermostat → DS18B20 software cutoff → PTC self-regulation → 10A branch fuses → mains rocker kill → RCD |
| **Fault isolation** | Per-station 3A fuses + one motor per umbrella: a jam stops one station, not the machine |
| **Simplicity over parts** | On/off relays replace SSR + motor driver (no speed control needed at 16 RPM); pump removed for gravity drain |
| **Domain separation** | No mains inside the chamber; SSRs in a closed earthed RCD-protected box; two labeled kill switches |
| **Self-locking mechanics** | Worm drives hold position when off; no freewheel, no brake needed |

## 5. Deliberate non-features

- **No per-station humidity sensor** — chamber air humidity is the shared control variable (per-station sensors would triple sensor cost for marginal gain; unload-dry umbrellas early by observation).
- **No motor speed control** — 16 RPM fixed is the design speed; PWM would add a driver stage for no drying benefit.
- **No SSR control of the exhaust fan** — it is an appliance on the mains rocker; staging heaters is what saves energy.
- **No current sensing** — jam detection is fuse + observation, per `docs/TROUBLESHOOTING.md`.
