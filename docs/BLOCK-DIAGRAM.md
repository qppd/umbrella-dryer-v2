# Electrical Block Diagram — 12V DC Umbrella Dryer

> **Pure 12V DC system.** No mains voltage. No inverter. No RCD/GFCI.
> All heating, motor, and fan loads run from a 12V LiFePO4 battery bank
> through fused DC distribution. Arduino Mega 2560 provides closed-loop
> control with NPN-driven 40A automotive relays for PTC heaters,
> optocoupler relays for worm motors, and ESC PWM for BLDC fans.
>
> **Rev 8:** Main fuse 50A ANL; PTC relays 40A automotive; per-heater 130°C thermal fuse;
> staged operation mandatory; LCD I2C on Mega pins 20/21.

---

## 1. System Overview

```mermaid
flowchart TB
    BAT["12V LiFePO4<br/>Battery Bank<br/>2× 200Ah, BMS Protected"]

    DISC["50A Disconnect<br/>Master Switch"]
    FMAIN["50A ANL<br/>Main Fuse"]
    BUS["12V DC Bus"]

    FS1["30A Fuse<br/>Station 1 PTC"]
    FS2["30A Fuse<br/>Station 2 PTC"]
    FS3["30A Fuse<br/>Station 3 PTC"]
    FM1["3A Fuse<br/>Motor 1"]
    FM2["3A Fuse<br/>Motor 2"]
    FM3["3A Fuse<br/>Motor 3"]
    FF["30A Fuse<br/>Fan Bus"]
    FL["3A Fuse<br/>Logic"]

    ST1["Station 1<br/>3x PTC + Motor"]
    ST2["Station 2<br/>3x PTC + Motor"]
    ST3["Station 3<br/>3x PTC + Motor"]
    FBUS["40A Auto Relay<br/>9x BLDC Fan Power"]

    BUCK["LM2596S Buck<br/>12V to 5V"]
    MEGA["Arduino Mega 2560"]
    DHT["DHT22<br/>Ambient T/RH"]
    DS["DS18B20<br/>Heater T"]
    LCD["LCD 16x2<br/>I2C (pins 20/21)"]

    BAT --> DISC --> FMAIN --> BUS
    BUS --> FS1 --> ST1
    BUS --> FS2 --> ST2
    BUS --> FS3 --> ST3
    BUS --> FM1
    BUS --> FM2
    BUS --> FM3
    BUS --> FF --> FBUS
    BUS --> FL --> BUCK --> MEGA
    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA -. "D4/D6/D8<br/>NPN→40A auto relay" .-> ST1
    MEGA -. "D4/D6/D8<br/>NPN→40A auto relay" .-> ST2
    MEGA -. "D4/D6/D8<br/>NPN→40A auto relay" .-> ST3
    MEGA -. "D13 NPN→40A auto relay" .-> FBUS
    MEGA -. "D5/D7/D9<br/>opto module (LOW=ON)" .-> ST1
    MEGA -. "D5/D7/D9<br/>opto module (LOW=ON)" .-> ST2
    MEGA -. "D5/D7/D9<br/>opto module (LOW=ON)" .-> ST3
    MEGA -. "D10-D12<br/>ESC PWM" .-> FBUS
```

---

## 2. Power Distribution Tree

```mermaid
flowchart TB
    BAT["12V LiFePO4<br/>Battery Bank"]
    DISC["50A Disconnect<br/>Master Switch"]
    FMAIN["50A ANL Fuse"]
    BUS["12V DC Bus<br/>Terminal Strip"]

    subgraph STA["STATION BRANCH - x3 IDENTICAL"]
        direction TB
        F_PTC["30A Blade Fuse<br/>(PTC heaters)"]
        RELAY_H["40A Auto Relay<br/>via 2N2222 NPN"]
        THF["130°C Thermal Fuse<br/>(per heater, ×3)"]
        PTC["3× PTC Heater<br/>12V 100W each<br/>Parallel: 300W"]
        F_MOT["3A Blade Fuse<br/>(worm motor)"]
        RELAY_M["Opto Module CH<br/>Active-LOW"]
        MOT["SGM-370<br/>Worm Motor"]
    end

    subgraph FANBUS["BLDC FAN BUS"]
        direction TB
        FF["30A Blade Fuse"]
        RELAY_F["40A Auto Relay<br/>via 2N2222 NPN"]
        ESC["3× ESC Module<br/>(per station, parallel)"]
        BLDC["3× 50mm Ducted<br/>BLDC Fan"]
    end

    subgraph LOGIC["LOGIC FEED"]
        direction TB
        FL["3A Blade Fuse"]
        BUCK["LM2596S Buck<br/>12V to 5V"]
        MEGA["Arduino Mega 2560"]
    end

    BAT --> DISC --> FMAIN --> BUS
    BUS --> F_PTC --> RELAY_H --> THF --> PTC
    BUS --> F_MOT --> RELAY_M --> MOT
    BUS --> FF --> RELAY_F --> ESC --> BLDC
    BUS --> FL --> BUCK --> MEGA
```

---

## 3. Per-Station Architecture

One drying station in full detail. All three stations are electrically identical.

```mermaid
flowchart TB
    FUSE_PTC["30A Blade Fuse<br/>from DC Bus"]
    FUSE_MOT["3A Blade Fuse<br/>from DC Bus"]

    subgraph NPN_DRV["2N2222 NPN Driver"]
        R_BASE["1kΩ base<br/>from Mega D4/D6/D8"]
        R_PULL["10kΩ pull-down<br/>to GND"]
        D_FLY["1N4007 flyback<br/>across coil"]
    end

    subgraph RELAY_H["40A Automotive Relay"]
        COIL["Coil: +12V → 86<br/>-85 → NPN collector"]
        CONTACTS["30: fused 12V<br/>87: to PTC heaters"]
    end

    subgraph HEATERS["PTC Heater Array - 300W"]
        THF1["130°C fuse"]
        H1["PTC 1<br/>12V 100W"]
        THF2["130°C fuse"]
        H2["PTC 2<br/>12V 100W"]
        THF3["130°C fuse"]
        H3["PTC 3<br/>12V 100W"]
    end

    subgraph OPTO["Opto Module CH"]
        OPTO_COIL["5V coil (buck rail)<br/>10kΩ pull-up (boot-safe)"]
        OPTO_CONTACTS["COM: fused 12V<br/>NO: to motor +"]
    end

    MOTOR["SGM-370<br/>12V 6RPM<br/>Motor − to GND"]

    subgraph FANS["BLDC Fans ×3 (parallel)"]
        ESC_S["ESC signal<br/>from Mega D10/D11/D12"]
        ESC_V["ESC VIN<br/>from fan bus relay"]
        BLDC_F["50mm ducted<br/>BLDC fans"]
    end

    FUSE_PTC --> NPN_DRV --> RELAY_H --> THF1 --> H1
    RELAY_H --> THF2 --> H2
    RELAY_H --> THF3 --> H3

    FUSE_MOT --> OPTO --> OPTO_CONTACTS --> MOTOR
    MOTOR -. "− lead" .-> GND["Common GND"]

    FANS
    ESC_V -->|"from D13 fan relay"| ESC_S --> BLDC_F
```

---

## 4. Controller I/O Map — Arduino Mega 2560

```mermaid
flowchart LR
    subgraph IN["SENSOR INPUTS"]
        DHT["DHT22<br/>Data: D2<br/>10kΩ pull-up"]
        DS["DS18B20<br/>Data: D3<br/>4.7kΩ pull-up"]
    end

    MEGA["Arduino Mega 2560<br/>ATmega2560 16MHz<br/>5V from LM2596S buck<br/>I2C on pins 20/21"]

    subgraph I2C["I2C BUS"]
        LCD["LCD 16x2<br/>SDA: D20<br/>SCL: D21"]
    end

    subgraph PTC_OUT["PTC HEATER RELAYS (40A auto, NPN-driven, active-HIGH)"]
        R1["D4: Station 1 PTC<br/>(~25A)"]
        R2["D6: Station 2 PTC<br/>(~25A)"]
        R3["D8: Station 3 PTC<br/>(~25A)"]
    end

    subgraph MOT_OUT["MOTOR RELAYS (opto module, active-LOW)"]
        M1["D5: Station 1 motor<br/>(~0.8A)"]
        M2["D7: Station 2 motor<br/>(~0.8A)"]
        M3["D9: Station 3 motor<br/>(~0.8A)"]
    end

    subgraph FAN_OUT["FAN BUS + ESC PWM"]
        FB["D13: Fan bus relay<br/>(40A auto, NPN, active-HIGH)"]
        E1["D10: ESC 1 PWM<br/>Station 1 fans"]
        E2["D11: ESC 2 PWM<br/>Station 2 fans"]
        E3["D12: ESC 3 PWM<br/>Station 3 fans"]
    end

    subgraph UI_OUT["UI OUTPUTS"]
        BTN["D14: Button<br/>(INPUT_PULLUP, LOW=ON)"]
        LED_R["D15: Red LED"]
        LED_Y["D16: Yellow LED"]
        LED_G["D17: Green LED"]
        BUZ["D18: Buzzer"]
    end

    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA --> PTC_OUT
    MEGA --> MOT_OUT
    MEGA --> FAN_OUT
    MEGA --> UI_OUT
```

---

## 5. Fuse and Wire Schedule

| Path | Fuse Rating | Fuse Type | Wire Gauge | Notes |
|------|-------------|-----------|------------|-------|
| Battery to disconnect | — | 50A switch | 8 AWG | Manual kill |
| Disconnect to main fuse | 50A | ANL | 8 AWG | Primary protection |
| Station 1 PTC branch | 30A | ATO blade | 10 AWG | 3× PTC heaters |
| Station 2 PTC branch | 30A | ATO blade | 10 AWG | 3× PTC heaters |
| Station 3 PTC branch | 30A | ATO blade | 10 AWG | 3× PTC heaters |
| Motor 1 | 3A | ATO blade | 18 AWG | SGM-370 |
| Motor 2 | 3A | ATO blade | 18 AWG | SGM-370 |
| Motor 3 | 3A | ATO blade | 18 AWG | SGM-370 |
| BLDC fan bus | 30A | ATO blade | 10 AWG | 9 ESCs, 18 AWG pigtails |
| Logic feed | 3A | ATO blade | 20 AWG | Buck converter input |
| Buck to Mega | — | PCB trace | 20 AWG | 5V regulated rail |
| PTC heater branch | 40A | Automotive relay | 10 AWG | Per relay COM→NO |
| Motor branch | 10A | Opto module | 18 AWG | Per module COM→NO |
| ESC power input | 3A per ESC | Bus bar | 18 AWG | From auto relay bus |
| ESC signal wire | Logic level | Jumper | 22 AWG | PWM from Mega |

## 6. Wire Gauge Rationale

| Run | Gauge | Rationale |
|---|---|---|
| Battery main + parallel links | 8 AWG | 50A main, <3% drop |
| Station PTC + fan branches | 10 AWG | 30A, short runs |
| Motor branches | 18 AWG | <1A |
| Logic feed | 20 AWG | <0.5A |
| Signal / LED / buzzer jumpers | 22 AWG | Logic-level only |

## 7. Design Notes

1. **Staged operation is mandatory.** One station draws ~36A; two stations ≈ 72A exceeds the 50A main fuse. Firmware enforces one station at a time with 30s rotation.
2. **PTC self-limiting.** PTC elements reduce current as temperature rises. Inrush is brief; steady-state per station ~15–20A.
3. **No mains voltage anywhere.** Entire system is 12V DC SELV.
4. **PTC relays are 40A automotive-grade** (not 10A PCB relays). Driven by 2N2222 NPN transistors with 10kΩ base pull-downs for boot-safety.
5. **Motor relays use a 4-CH optocoupler module** (10A channels — more than adequate for 0.8A motors).
6. **130°C thermal fuse per heater (9×).** Mounted in the + lead of each individual PTC heater. Rated 10A — safe for single-heater current (~8.3A).
7. **ESC PWM protocol.** 1000–2000 µs at 50 Hz. Fan bus relay (D13) must be ON for ESCs to receive power.
8. **LCD I2C is on Mega pins 20/21** (hardware I2C) — NOT A4/A5 (which are ADC on the Mega).
