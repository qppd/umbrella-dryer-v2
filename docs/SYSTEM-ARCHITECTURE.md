# System Architecture — 12V DC Umbrella Dryer

Pure 12V DC umbrella dryer. No mains, no inverter, no AC anywhere. Everything runs from a parallel LiFePO4 battery bank through fused DC distribution.

## 1. Layered architecture

```mermaid
flowchart TD
    subgraph L5["LAYER 5 — Human interface"]
        LCD["16x2 LCD (I2C, pins 20/21)"]
        BTN["Start button (D14)"]
        LED["3× status LEDs (D15–D17)"]
        BUZ["Buzzer (D18)"]
    end

    subgraph L4["LAYER 4 — Control"]
        FW["Arduino Mega 2560<br/>IDLE / PREHEAT / DRY / COOL / DONE / CUTOFF<br/>Staged operation: 1 station at a time"]
    end

    subgraph L3["LAYER 3 — Sensing"]
        DHT["DHT22 — chamber humidity + ambient temp"]
        DS["DS18B20 — heater-zone temp (safety signal)"]
    end

    subgraph L2["LAYER 2 — Actuation"]
        subgraph PTC_RELAYS["PTC heater relays ×3 (40A auto, NPN-driven)"]
            PR1["D4 → station 1 PTC"]
            PR2["D6 → station 2 PTC"]
            PR3["D8 → station 3 PTC"]
        end
        subgraph MOT_RELAYS["Motor relays ×3 (opto module, active-LOW)"]
            MR1["D5 → station 1 motor"]
            MR2["D7 → station 2 motor"]
            MR3["D9 → station 3 motor"]
        end
        FAN_BUS["Fan bus relay (D13 → 40A auto, NPN-driven)"]
        ESC_X["ESC PWM ×3 (D10–D12) — BLDC fan speed"]
    end

    subgraph L1["LAYER 1 — Power"]
        BANK["2× LiFePO4 12.8V 200Ah parallel<br/>BMS 200A per pack"]
        DISC["50A disconnect switch"]
        FUSE_MAIN["50A ANL main fuse"]
        DIST["12V DC distribution bus"]
        FUSE_PTC["30A fuse ×3<br/>(one per station PTC branch)"]
        FUSE_FAN["30A fan bus fuse"]
        FUSE_MOT["3A motor fuse ×3"]
        FUSE_LOGIC["3A logic fuse"]
        BUCK["LM2596S buck 12V → 5V"]
    end

    subgraph L0["LAYER 0 — Plant (mechanical + thermal)"]
        CH["3 drying stations"]
        PTC_ALL["PTC heaters 100W ×9<br/>(130°C thermal fuse per heater)"]
        FAN_ALL["BLDC fans ×9 (3 per station)"]
        MOT_ALL["SGM-370 worm motors ×3"]
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

Single domain: 12V DC throughout. The 50A main fuse allows one station at a time (~36A). Staged operation enforced by firmware.

```mermaid
flowchart LR
    BANK["LiFePO4 Bank<br/>2× 200Ah parallel<br/>400Ah / 5120Wh"]
    BMS["BMS 200A<br/>per pack"]
    DISC["50A disconnect"]
    FUSE_M["50A ANL<br/>main fuse"]
    BUS["12V DC bus"]

    BANK --> BMS --> DISC --> FUSE_M --> BUS

    BUS -->|"30A blade"| S1["Station 1<br/>PTC (30A) + Motor (3A)"]
    BUS -->|"30A blade"| S2["Station 2<br/>PTC (30A) + Motor (3A)"]
    BUS -->|"30A blade"| S3["Station 3<br/>PTC (30A) + Motor (3A)"]
    BUS -->|"30A blade"| FANS["Fan bus<br/>auto relay + 9× ESCs"]
    BUS -->|"3A blade"| LOGIC["5V buck<br/>Mega + sensors"]
```

### Per-station load budget

| Component | Qty | Voltage | Each | Total (station) |
|---|---|---|---|---|
| PTC heater | 3 | 12V | 100W / 8.3A | 300W / 25A |
| BLDC fan + ESC | 3 | 12V | ~30W / 3.2A | ~90W / 9.6A |
| SGM-370 motor | 1 | 12V | ~2.4W / 0.2A | ~2.4W / 0.2A |
| **Station total (peak)** | — | — | — | **~392W / ~35A** |

### System-wide fuse table

| Branch | Fuse | Consumers |
|---|---|---|
| Main | 50A ANL | Entire DC bus (one station at a time) |
| Station 1 PTC | 30A blade | 3× PTC heaters (~25A) |
| Station 2 PTC | 30A blade | 3× PTC heaters |
| Station 3 PTC | 30A blade | 3× PTC heaters |
| Motor 1 | 3A blade | 1× SGM-370 |
| Motor 2 | 3A blade | 1× SGM-370 |
| Motor 3 | 3A blade | 1× SGM-370 |
| Fan bus | 30A blade | 9× BLDC fans (28.8A) |
| Logic | 3A blade | Mega + LCD + DHT22 + DS18B20 via buck |

## 3. Control — pin mapping

| Arduino Pin | Function | Actuator | Drive | Active |
|---|---|---|---|---|
| D2 | DHT22 data | Chamber humidity sensor | 10kΩ pull-up | — |
| D3 | DS18B20 data | Temperature probe | 4.7kΩ pull-up | — |
| D4 | Station 1 PTC | 3× PTC (40A relay via NPN) | 2N2222 | HIGH |
| D5 | Station 1 motor | SGM-370 (opto module) | Optocoupler | LOW |
| D6 | Station 2 PTC | 3× PTC (40A relay via NPN) | 2N2222 | HIGH |
| D7 | Station 2 motor | SGM-370 (opto module) | Optocoupler | LOW |
| D8 | Station 3 PTC | 3× PTC (40A relay via NPN) | 2N2222 | HIGH |
| D9 | Station 3 motor | SGM-370 (opto module) | Optocoupler | LOW |
| D10 | Station 1 fan | ESC-1 PWM | Servo lib, 50 Hz | — |
| D11 | Station 2 fan | ESC-2 PWM | Servo lib, 50 Hz | — |
| D12 | Station 3 fan | ESC-3 PWM | Servo lib, 50 Hz | — |
| D13 | Fan bus enable | 40A auto relay via NPN | 2N2222 | HIGH |
| D14 | Start button | Push-button | INPUT_PULLUP | LOW |
| D15 | Red LED | Heating active | 220Ω | HIGH |
| D16 | Yellow LED | Cycle running / cooling | 220Ω | HIGH |
| D17 | Green LED | Ready / done | 220Ω | HIGH |
| D18 | Buzzer | Active buzzer | — | HIGH |
| 20 (SDA) | LCD I2C | 16×2 LCD | I2C | — |
| 21 (SCL) | LCD I2C | 16×2 LCD | I2C | — |

> **NPN driver stages (D4/D6/D8/D13):** 10kΩ base pull-downs hold relays OFF at boot.
> **Opto module (D5/D7/D9):** onboard pull-ups hold relays OFF (active-LOW) at boot.
> Firmware calls `allOff()` in `setup()` for an extra safety layer.

## 4. Safety layers

```mermaid
flowchart TD
    A["DS18B20 reads heater-zone temp"] --> B{"Temp > 65 C ?"}
    B -- Yes --> C["Firmware cuts ALL loads<br/>Latched until T < 50 C"]
    B -- No --> D["Normal operation"]

    C --> E{"Temp still rising ?"}
    E -- Yes --> F["130 C thermal fuse blows<br/>Per-heater, non-resettable"]
    E -- No --> G["PTC self-regulation<br/>Resistance rises with temp"]

    F --> H["Heater offline"]

    I["30A per-station blade fuse"] --> J{"Overcurrent ?"}
    J -- Yes --> K["Fuse blows<br/>Station isolated"]
    J -- No --> D

    L["BMS cell protection"] --> M{"Low V / over-current / over-temp ?"}
    M -- Yes --> N["Battery protected<br/>BMS disconnects"]
    M -- No --> O["Bank supplies bus"]
```

### Defense-in-depth thermal protection

| Layer | Mechanism | Trip point | Response time | Resettable? |
|---|---|---|---|---|
| **Firmware interlock** | DS18B20 + software cutoff | > 65 °C | < 1 s | Yes (auto when T < 50 °C) |
| **PTC self-regulation** | Resistance rises with temperature | ~150–200 °C | Passive / instant | Yes |
| **Thermal fuse** | One-shot bimetal (per heater) | 130 °C | Physical melt | **No** |
| **Branch blade fuse** | Overcurrent protection | 30A (PTC) / 30A (fan) / 3A (motor) | Current-dependent | Replace fuse |
| **BMS protection** | Cell-level hardware cutoff | Per-pack thresholds | Hardware | Auto (some conditions) |

> **Five independent thermal/electrical layers** protect against heater runaway.

## 5. One drying cycle — sequence

```mermaid
sequenceDiagram
    participant U as User
    participant FW as Mega 2560
    participant S as Sensors (DHT22 + DS18B20)
    participant R as Relays (D4–D13)
    participant E as ESCs (D10–D12)

    U->>FW: Press start (D14)
    FW->>S: Self-test read (humidity, temp)
    FW->>R: Fan bus ON (D13)
    FW->>E: Arm ESCs (min pulse on D10–D12)

    Note over FW,R: PREHEAT — staged: one station PTC at a time (30s each)

    loop Every 500 ms
        FW->>S: Read humidity H, zone temp T
        alt T > 65 °C (thermal alarm)
            FW->>R: ALL OFF — latched
            Note over FW: CUTOFF — retry only when T < 50 °C
        else H above threshold (wet)
            FW->>R: PTC ON for active station (rotates every 30s)
            FW->>E: Fan throttle FULL for active station
        else H below threshold for 5 min
            FW->>R: ALL OFF
            Note over FW: COMPLETE
        end
    end

    Note over FW: DRY phase — staged motor + PTC + fans, 15 min timer
    Note over FW: COOL phase — fans only, 2 min, then ALL OFF

    FW-->>U: COMPLETE on LCD + buzzer 3×
    U->>U: Unload umbrellas, empty drip tray
```

## 6. Design principles

| Principle | Realization |
|---|---|
| **No mains anywhere** | Entire system 12V DC — no RCD, no changeover, no AC wiring |
| **Defense in depth on heat** | DS18B20 → PTC self-regulation → 130°C thermal fuse (per heater) → branch fuses → BMS: five layers |
| **Staged operation** | Firmware rotates stations every 30s; only one station's heaters active at a time; keeps draw ~35.5A at 71% of the 50A main fuse |
| **Fault isolation** | Per-branch fuses: one station's fault doesn't affect the others |
| **ESC for fan speed** | BLDC fans with ESC PWM give variable speed; automotive relay on D13 gives instant all-fan kill |
| **Worm drive self-locking** | SGM-370 motors hold position when de-energized — no brake, no holding current |
| **Boot-safe relay states** | NPN pull-downs + opto pull-ups + firmware `allOff()` in `setup()` — triple guarantee |

## 7. Deliberate non-features

- **No mains connection** — Eliminates RCD, changeover switch, AC wiring
- **No per-station humidity sensor** — Single DHT22 is the shared control variable
- **No motor speed control** — 6 RPM fixed; ESC only for BLDC fans
- **No current sensing** — Jam detection via fuse + observation
- **No PID temperature control** — PTC self-regulation + firmware on/off hysteresis
