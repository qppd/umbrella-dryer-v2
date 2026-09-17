# Electrical Block Diagram — 12V DC Umbrella Dryer

> **Pure 12V DC system.** No mains voltage. No inverter. No RCD/GFCI.
> All heating, motor, and fan loads run from a 12V LiFePO4 battery
> through direct DC distribution. Arduino Mega 2560 provides closed-loop
> control with LCTC DC-DC SSRs (40A for PTC/fan, 10A for motors),
> and Mega PWM for AVC blowers.
>
> staged operation mandatory; LCD I2C on Mega pins 20/21.

---

## 1. System Overview

```mermaid
flowchart TB
    BAT["12V LiFePO4<br/>Battery<br/>1× 200Ah, BMS Protected"]

    BUS_POS["12V Positive Bus Bar<br/>(10-Terminal Copper)"]
    BUS_NEG["12V Negative Bus Bar<br/>(10-Terminal Copper)"]

    ST1["Station 1<br/>3x PTC + 3x Blowers + Motor"]
    ST2["Station 2<br/>3x PTC + 3x Blowers + Motor"]
    ST3["Station 3<br/>3x PTC + 3x Blowers + Motor"]
    FBUS["DC SSR (SSR-40DD)<br/>9x AVC Blower Power"]

    BUCK["LM2596S Buck<br/>12V to 5V"]
    MEGA["Arduino Mega 2560"]
    DHT["DHT22<br/>Ambient T/RH"]
    DS["DS18B20<br/>Heater T"]
    LCD["LCD 16x2<br/>I2C (pins 20/21)"]

    BAT --> BUS_POS
    BAT --> BUS_NEG
    BUS_POS --> ST1
    BUS_POS --> ST2
    BUS_POS --> ST3
    BUS_POS --> FBUS
    BUS_POS --> BUCK --> MEGA
    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA -. "D4/D6/D8<br/>DC SSR (SSR-40DD)" .-> ST1
    MEGA -. "D4/D6/D8<br/>DC SSR (SSR-40DD)" .-> ST2
    MEGA -. "D4/D6/D8<br/>DC SSR (SSR-40DD)" .-> ST3
    MEGA -. "D13 DC SSR (SSR-40DD)" .-> FBUS
    MEGA -. "D5/D7/D9<br/>DC SSR (SSR-10A)" .-> ST1
    MEGA -. "D5/D7/D9<br/>DC SSR (SSR-10A)" .-> ST2
    MEGA -. "D5/D7/D9<br/>DC SSR (SSR-10A)" .-> ST3
    MEGA -. "D10/D11/D12<br/>PWM (analogWrite)" .-> FBUS
    ST1 -. "GND Return" .-> BUS_NEG
    ST2 -. "GND Return" .-> BUS_NEG
    ST3 -. "GND Return" .-> BUS_NEG
    FBUS -. "GND Return" .-> BUS_NEG
    MEGA -. "GND Return" .-> BUS_NEG
```

---

## 2. Power Distribution Tree

```mermaid
flowchart TB
    BAT["12V LiFePO4<br/>Battery"]
    BUS["12V Positive Bus Bar<br/>(10-Terminal Copper)"]

    subgraph STA["STATION BRANCH - x3 IDENTICAL"]
        direction TB
        SSR_H["DC SSR (SSR-40DD)<br/>Input: Mega pin<br/>Output: PTC heaters"]
        PTC["3× PTC Heater<br/>12V 100W each<br/>Parallel: 300W"]
        SSR_M["DC SSR (SSR-10A)<br/>Input: Mega pin<br/>Output: Motor"]
        MOT["SGM-370<br/>Worm Motor"]
    end

    subgraph FANBUS["AVC BLOWER BUS"]
        direction TB
        SSR_F["DC SSR (SSR-40DD)<br/>Input: Mega D13<br/>Output: 9 blowers"]
        BLOW["9× AVC Blower<br/>12V 4.5A each<br/>PWM via D10/D11/D12"]
    end

    subgraph LOGIC["LOGIC FEED"]
        direction TB
        BUCK["LM2596S Buck<br/>12V to 5V"]
        MEGA["Arduino Mega 2560"]
    end

    BAT --> BUS
    BUS --> SSR_H --> PTC
    BUS --> SSR_M --> MOT
    BUS --> SSR_F --> BLOW
    BUS --> BUCK --> MEGA
```

---

## 3. Per-Station Architecture

One drying station in full detail. All three stations are electrically identical.

```mermaid
flowchart TB
    SSR_PTC["DC SSR (SSR-40DD)<br/>Input +: Mega D4/D6/D8<br/>Input −: GND<br/>Output: from 12V bus"]

    subgraph HEATERS["PTC Heater Array - 300W"]
        H1["PTC 1<br/>12V 100W"]
        H2["PTC 2<br/>12V 100W"]
        H3["PTC 3<br/>12V 100W"]
    end

    SSR_PTC --> H1 & H2 & H3

    SSR_MOT["DC SSR (SSR-10A)<br/>Input: Mega D5/D7/D9<br/>Input −: GND<br/>Output: to motor +"]

    MOTOR["SGM-370<br/>12V 6RPM<br/>Motor − to GND"]

    subgraph BLOWERS["AVC Blowers ×3 (parallel)"]
        BLOW_SIG["PWM signal<br/>from Mega D10/D11/D12"]
        BLOW_PWR["12V power<br/>from fan bus SSR"]
        BLOW_FAN["80mm AVC<br/>12V 4.5A blowers"]
    end

    SSR_MOT --> MOTOR
    MOTOR -. "− lead" .-> GND["Common GND"]

    BLOWERS
    BLOW_PWR -->|\"from D13 fan SSR\"| BLOW_SIG --> BLOW_FAN
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

    subgraph PTC_OUT["PTC HEATER SSRs (SSR-40DD, DC output, active-HIGH)"]
        R1["D4: Station 1 PTC<br/>(~25A)"]
        R2["D6: Station 2 PTC<br/>(~25A)"]
        R3["D8: Station 3 PTC<br/>(~25A)"]
    end

    subgraph MOT_OUT["MOTOR SSRs (SSR-10A, active-HIGH)"]
        M1["D5: Station 1 motor<br/>(~0.8A)"]
        M2["D7: Station 2 motor<br/>(~0.8A)"]
        M3["D9: Station 3 motor<br/>(~0.8A)"]
    end

    subgraph FAN_OUT["FAN BUS + BLower PWM"]
        FB["D13: Fan bus SSR<br/>(SSR-40DD, active-HIGH)"]
        E1["D10: PWM Station 1 blowers<br/>analogWrite(D10, val)"]
        E2["D11: PWM Station 2 blowers<br/>analogWrite(D11, val)"]
        E3["D12: PWM Station 3 blowers<br/>analogWrite(D12, val)"]
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

## 5. Wire Schedule

| Path | Wire Gauge | Notes |
|------|------------|-------|
| Battery to bus | 8 AWG | Direct connection |
| Station 1 PTC branch | 10 AWG | 3× PTC heaters via SSR |
| Station 2 PTC branch | 10 AWG | 3× PTC heaters via SSR |
| Station 3 PTC branch | 10 AWG | 3× PTC heaters via SSR |
| Station 1 Motor branch | 18 AWG | SGM-370 via SSR-10A |
| Station 2 Motor branch | 18 AWG | SGM-370 via SSR-10A |
| Station 3 Motor branch | 18 AWG | SGM-370 via SSR-10A |
| AVC blower bus | 10 AWG | 9 blowers, 18 AWG pigtails |
| Logic feed | 20 AWG | Buck converter input |
| Buck to Mega | 20 AWG | 5V regulated rail |
| BLOWER signal wires | 22 AWG | PWM from Mega (D10–D12) |

## 6. Wire Gauge Rationale

| Run | Gauge | Rationale |
|---|---|---|
| Battery main + main links | 8 AWG | 200A BMS peak, <3% drop |
| Station PTC + blower branches | 10 AWG | 40A, short runs |
| Motor branches | 18 AWG | <1A |
| Logic feed | 20 AWG | <0.5A |
| Signal / LED / buzzer jumpers | 22 AWG | Logic-level only |

## 7. Design Notes

1. **Staged operation is mandatory.** One station draws ~38.8A (3 PTC + 3 blowers + motor); two stations ≈ 77.6A. The BMS is rated 200A, so this is not a fuse limitation — staged operation preserves battery/BMS current budget and follows the study's energy-efficient control strategy. Firmware enforces one station at a time with 30s rotation.
2. **PTC self-limiting.** PTC elements reduce current as temperature rises. Inrush is brief; steady-state per station ~15–20A.
3. **No mains voltage anywhere.** Entire system is 12V DC SELV.
4. **PTC heaters and fan bus are switched by SSR-40DD solid-state relays** (input 3–32VDC, DC output, 40A rated). Driven directly from Mega digital pins — no NPN transistors, no base resistors, no flyback diodes needed. Active HIGH = ON; no input current = OFF (boot-safe).
5. **Motor SSRs are LCTC DC-DC SSR-10A** (DC output, active-HIGH). Direct drive from Mega pins — no optocoupler module needed. Active HIGH = ON; floating pin = OFF at boot.
6. **AVC blowers are PWM-controlled directly from Mega** (D10/D11/D12) using `analogWrite()`. No ESC needed. 5V logic compatible.
7. **No thermal fuses.** Over-temperature protection relies on PTC self-regulation and DS18B20 firmware 65 °C cutoff. Over-current protection relies on BMS 200A cutoff and PTC self-regulation. There is no hardware fuse backstop.
8. **Fan bus SSR (D13)** must be ON for blowers to receive 12V power. The PWM signal (D10/D11/D12) controls speed independently.
9. **LCD I2C is on Mega pins 20/21** (hardware I2C) — NOT A4/A5 (which are ADC on the Mega).