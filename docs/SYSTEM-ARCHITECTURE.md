# System Architecture (Rev 4)

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
        RH["30A relay — heater"]
        RM["2x 2-CH relays — 3 stations + fan"]
    end
    subgraph L1["LAYER 1 — Power"]
        BAT["LiFePO4 12.8V 30Ah BMS"]
        BUCK["LM2596S buck -> 5V"]
        FUSES["25A main / 15A heater / 3A x3 stations / 3A logic"]
    end
    subgraph L0["LAYER 0 — Plant (mechanical + thermal)"]
        CH["Drying chamber (sloped floor, drain, drip tray)"]
        ST["3x motor stations: worm motor -> 8x8 coupling -> 8mm shaft -> umbrella holder"]
        HEAT["PTC 100W heater + 120mm fan -> forced convection 40-60 C"]
    end

    L0 --> L3
    L3 --> L4
    L4 --> L2
    L2 --> L0
    L1 --> L2
    L1 --> L4
    L4 <--> L5
```

## 2. Power domains

| Domain | Source | Consumers | Protection |
|---|---|---|---|
| 12V power | Battery (BMS 30A) | Heater 8.3A · 3 motors 3.6A · fan 0.25A | 25A main + 15A heater + 3A per station |
| 5V logic | LM2596S from 12V | Mega · sensors · LCD · relay coils (~0.8A) | 3A branch |
| Signal | Mega pins | Optocoupler LEDs only (2–5 mA each) | Isolation barrier to 12V side |

**Isolation philosophy:** the Mega never touches 12V. Relays' optocouplers + flyback diodes keep inductive/heater transients off the logic rail; the buck keeps the Mega off the battery directly (Makerlab warning: no 12V on the DC jack).

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
            FW->>A: Heater OFF (latched until T < 50 C)
        else H above threshold
            FW->>A: Heater duty = k(H - H_target), 4 s period
        else H below threshold for 5 min
            FW->>A: All OFF -> fan purge 2 min
        end
    end
    FW-->>U: COMPLETE — buzzer + green LED
    U->>U: Empty drip tray, unload umbrellas
```

## 4. Design principles (why it is built this way)

| Principle | Realization |
|---|---|
| **Energy efficiency is the thesis** | Heater runs only on humidity demand (≈90–95 Wh/cycle → 3–4 cycles/charge) |
| **Defense in depth on heat** | PTC self-regulation → DS18B20 software cutoff → 15A fuse → rocker kill |
| **Fault isolation** | Per-station 3A fuses + one motor per umbrella: a jam stops one station, not the machine |
| **Simplicity over parts** | On/off relays replace SSR + motor driver (no speed control needed at 16 RPM); pump removed for gravity drain |
| **Extra-low voltage safety** | All-12V; 30VDC-rated contacts; mains prohibited by design |
| **Self-locking mechanics** | Worm drives hold position when off; no freewheel, no brake needed |

## 5. Deliberate non-features

- **No per-station humidity sensor** — chamber air humidity is the shared control variable (per-station sensors would triple sensor cost for marginal gain; unload-dry umbrellas early by observation).
- **No motor speed control** — 16 RPM fixed is the design speed; PWM would add a driver stage for no drying benefit.
- **No current sensing** — jam detection is fuse + observation, per `docs/TROUBLESHOOTING.md`.
