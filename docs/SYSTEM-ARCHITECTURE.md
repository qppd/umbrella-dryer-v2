# System Architecture — 12V DC Umbrella Dryer

Pure 12V DC umbrella dryer. No mains, no inverter, no AC anywhere. Everything runs from a parallel LiFePO4 battery bank through fused DC distribution.

## 1. Layered architecture

```mermaid
flowchart TD
    subgraph L5["LAYER 5 — Human interface"]
        LCD["16x2 LCD (I2C)"]
        BTN["Start button"]
    end

    subgraph L4["LAYER 4 — Control"]
        FW["Arduino Mega 2560<br/>IDLE / DRYING / CUTOFF / COMPLETE<br/>Humidity duty-cycling + thermal interlock"]
    end

    subgraph L3["LAYER 3 — Sensing"]
        DHT["DHT22 — chamber humidity + ambient temp"]
        DS["DS18B20 — heater-zone temp (safety signal)"]
    end

    subgraph L2["LAYER 2 — Actuation"]
        subgraph RELAY["Relay module (D4-D8)"]
            PTC["PTC heater relays x3"]
            MOT["Worm motor relays x3"]
        end
        FAN_BUS["Automotive relay (D9) — fan bus enable"]
        ESC_X["ESC PWM (D10-D12) — BLDC fan speed x3"]
    end

    subgraph L1["LAYER 1 — Power"]
        BANK["2x LiFePO4 12.8V 200Ah parallel<br/>BMS 200A per pack"]
        FUSE_MAIN["25A main fuse"]
        DIST["12V DC distribution bus"]
        FUSE_ST["Per-station 25A blade fuse x3"]
        FUSE_FAN["5A fan bus fuse"]
        FUSE_LOGIC["3A logic fuse"]
        BUCK["Buck converter 12V -> 5V"]
    end

    subgraph L0["LAYER 0 — Plant (mechanical + thermal)"]
        CH["3 drying stations"]
        PTC_ALL["PTC heaters 100W x9 (3 per station)"]
        FAN_ALL["BLDC fans x3 (1 per station)"]
        MOT_ALL["SGM-370 worm motors x3 (1 per station)"]
    end

    L0 --> L3
    L3 --> L4
    L4 --> L2
    L2 --> L0
    L1 --> L2
    L1 --> L4
    L4 <--> L5
```

## 2. Power architecture

Single domain: 12V DC throughout. No AC anywhere. The 25A main fuse caps total system draw; stations are time-multiplexed so only one station runs its PTC heaters at a time.

```mermaid
flowchart LR
    BANK["LiFePO4 Bank<br/>2x 12.8V 200Ah<br/>400Ah total"]
    BMS["BMS 200A<br/>per pack"]
    FUSE_M["25A main fuse"]
    BUS["12V DC bus"]

    BANK --> BMS --> FUSE_M --> BUS

    BUS -->|"25A blade fuse"| S1["Station 1<br/>PTC + motor"]
    BUS -->|"25A blade fuse"| S2["Station 2<br/>PTC + motor"]
    BUS -->|"25A blade fuse"| S3["Station 3<br/>PTC + motor"]
    BUS -->|"5A fuse"| FANS["Fan bus<br/>auto relay + ESCs"]
    BUS -->|"3A fuse"| LOGIC["5V buck<br/>Mega + LCD + sensors"]
```

### Per-station load budget

| Component | Qty (per station) | Voltage | Each | Total (station) |
|---|---|---|---|---|
| PTC heater | 3 | 12V | 100W / 8.3A | 300W / 25A |
| BLDC fan | 1 | 12V | ~30W / 2.5A | ~30W / ~2.5A |
| SGM-370 worm motor | 1 | 12V | ~43W / 3.6A | ~43W / 3.6A |
| **Station total (peak)** | — | — | — | **~373W / ~31A** |

> **Fuse constraint:** The 25A main fuse allows one station's PTC heaters (25A) plus one fan (2.5A) plus one motor (3.6A) ≈ 31A momentarily but the firmware time-multiplexes heater activation across stations to stay within continuous rating. Motor and fan draw is always well under budget.

### System-wide power budget

| Rail | Fuse | Consumers |
|---|---|---|
| Station 1 | 25A blade | 3x PTC heaters + 1x worm motor |
| Station 2 | 25A blade | 3x PTC heaters + 1x worm motor |
| Station 3 | 25A blade | 3x PTC heaters + 1x worm motor |
| Fan bus | 5A blade | 3x BLDC fans (via automotive relay D9) |
| Logic | 3A blade | Mega + LCD + DHT22 + DS18B20 via buck to 5V |

## 3. Control — pin mapping

| Arduino Pin | Function | Actuator | Drive |
|---|---|---|---|
| D4 | Station 1 PTC heaters | 3x PTC parallel (one relay) | Active-LOW relay |
| D5 | Station 1 worm motor | SGM-370 | Active-LOW relay |
| D6 | Station 2 PTC heaters | 3x PTC parallel (one relay) | Active-LOW relay |
| D7 | Station 2 worm motor | SGM-370 | Active-LOW relay |
| D8 | Station 3 heater + motor | PTC + motor combined | Active-LOW relay |
| D9 | Fan bus enable | Automotive relay (12V switching) | Active-HIGH |
| D10 | Station 1 BLDC fan | ESC-1 | PWM 1000-2000 us |
| D11 | Station 2 BLDC fan | ESC-2 | PWM 1000-2000 us |
| D12 | Station 3 BLDC fan | ESC-3 | PWM 1000-2000 us |
| D2 (INT0) | DS18B20 bus | OneWire temp sensors | Data |
| D20 (SDA) | LCD I2C | 16x2 LCD | I2C |
| D21 (SCL) | LCD I2C | 16x2 LCD | I2C |
| A0 | DHT22 data | Humidity + temperature | Digital |
| A1 | Start button | Push-button | INPUT_PULLUP |

> **D9 fan bus logic:** The automotive relay on D9 switches the 12V rail to all three ESCs. Killing D9 shuts down every fan instantly (emergency/complete). During normal operation D9 stays HIGH and individual fan speed is controlled via ESC PWM on D10-D12.

## 4. Safety layers

```mermaid
flowchart TD
    A["DS18B20 reads heater-zone temp"] --> B{"Temp > 65 C ?"}
    B -- Yes --> C["Firmware cuts all PTC relays<br/>Latched until T < 50 C"]
    B -- No --> D["Normal operation"]

    C --> E{"Temp still rising ?"}
    E -- Yes --> F["130 C thermal fuse blows<br/>Physical, non-resettable"]
    E -- No --> G["PTC self-regulation<br/>Resistance rises with temp"]

    F --> H["Heater zone offline"]

    I["Per-station 25A blade fuse"] --> J{"Overcurrent ?"}
    J -- Yes --> K["Fuse blows<br/>Station isolated"]
    J -- No --> D

    L["BMS cell protection"] --> M{"Low V / over-current / over-temp ?"}
    M -- Yes --> N["Battery bank protected<br/>BMS disconnects"]
    M -- No --> O["Banks supply bus"]
```

### Defense-in-depth thermal protection

| Layer | Mechanism | Trip point | Response time | Resettable? |
|---|---|---|---|---|
| **Firmware interlock** | DS18B20 + software cutoff | > 65 C | < 1 s | Yes (auto when T < 50 C) |
| **PTC self-regulation** | Resistance rises with temperature | ~120 C (material limit) | Passive / instant | Yes |
| **Thermal fuse** | One-shot bimetal device | 130 C | Physical melt | No |
| **Per-station blade fuse** | Overcurrent protection | 25 A | Current-dependent | Replace fuse |
| **BMS protection** | Cell-level hardware cutoff | Per-pack thresholds | Hardware | Auto (some conditions) |

> **Four independent thermal layers** protect against heater runaway. Even if the firmware freezes, the PTC self-limits; if the PTC fails, the thermal fuse blows; if both fail, the blade fuse opens from overcurrent draw.

## 5. One drying cycle — sequence

```mermaid
sequenceDiagram
    participant U as User
    participant FW as Mega 2560
    participant S as Sensors (DHT22 + DS18B20)
    participant R as Relays (D4-D9)
    participant E as ESCs (D10-D12)

    U->>FW: Press start (umbrellas loaded)
    FW->>S: Self-test read (humidity, temp)
    FW->>E: Arm ESCs (min pulse on D10-D12)
    FW->>R: Fan bus ON (D9), Station motors ON (D5,D7,D8)

    Note over FW,R: PTC heaters remain OFF until first humidity reading

    loop Every 500 ms
        FW->>S: Read humidity H, zone temp T
        alt T > 65 C (thermal alarm)
            FW->>R: All PTC relays OFF (latched)
            Note over FW: CUTOFF state — retry in 10 s
        else H above threshold (wet)
            FW->>R: Stage PTC heaters duty-cycle
            FW->>E: Scale fan PWM with heater duty
            Note over FW: Time-multiplex: one station PTCs at a time
        else H below threshold for 5 min
            FW->>R: All relays OFF
            FW->>R: Fan bus OFF (D9)
            Note over FW: COMPLETE state
        end
    end

    FW-->>U: Display COMPLETE on LCD
    U->>U: Unload umbrellas, empty drip tray
```

## 6. Design principles

| Principle | Realization |
|---|---|
| **No mains anywhere** | Entire system is 12V DC. Eliminates shock hazard, RCD, changeover switch, and AC wiring complexity. |
| **Defense in depth on heat** | DS18B20 firmware cutoff, PTC self-regulation, 130C thermal fuse, 25A blade fuse — four independent layers. |
| **Battery-first energy model** | PTC duty-cycling and ESC speed scaling keep draw within the 25A fuse. 400Ah bank yields 8-12 cycles per charge at 30-40 min each. |
| **Fault isolation** | Per-station 25A fuses: a heater short or motor jam kills one station, not the machine. |
| **ESC for fan speed** | BLDC fans with ESC PWM give variable speed for noise and power optimization. Automotive relay on D9 gives instant all-fan kill. |
| **Worm drive self-locking** | SGM-370 worm motors hold umbrella position when de-energized. No brake, no freewheel, no holding current. |
| **Simplicity over parts** | Relay-switched PTC heaters (no PID, no SSR). ESC only on fans (not motors). Gravity drain (no pump). |

## 7. Deliberate non-features

- **No mains connection** — Deliberate. Removes RCD, changeover switch, and AC wiring entirely.
- **No per-station humidity sensor** — Chamber humidity (single DHT22) is the shared control variable. Per-station sensors triple cost for marginal gain.
- **No motor speed control** — 6 RPM fixed via worm gear. ESC is only for BLDC fan speed.
- **No current sensing** — Jam detection is fuse + observation per `docs/TROUBLESHOOTING.md`.
- **No PID temperature control** — PTC self-regulation plus firmware on/off hysteresis is sufficient for 40-60C target.
- **No solar charging (yet)** — Documented as a future expansion path, not in V2 scope.
