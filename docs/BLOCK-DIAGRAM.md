# Electrical Block Diagram (Rev 5: mains heat + 12V stations)

Canonical wiring map. Same content as `wiring/README.md`, printable sheet. Three separate domains: **220V AC heat**, **12V DC stations**, **5V logic**. The Mega never touches mains or battery power.

```mermaid
flowchart TB
    subgraph AC["220V AC DOMAIN - mains heat"]
        OUT["RCD/GFCI outlet"]
        MSW["Mains rocker (2-gang)"]
        MF1["Fuse 10A line 1"]
        MF2["Fuse 10A line 2"]
        SSR1["Fotek SSR-40DA #1<br/>input: D4"]
        SSR2["Fotek SSR-40DA #2<br/>input: D5"]
        H1["PTC heater-fan 1500W #1"]
        H2["PTC heater-fan 1500W #2"]
        EFAN["12in Omni exhaust fan 220V"]
    end

    subgraph DC["12V DC DOMAIN - battery"]
        BAT["LiFePO4 12.8V 30Ah BMS"]
        DSW["DC rocker"]
        F1["Fuse 25A main"]
        FA["Fuse 3A station 1"]
        FB["Fuse 3A station 2"]
        FC["Fuse 3A station 3"]
        FL["Fuse 3A logic"]
        BUCK["LM2596S buck 5V"]
    end

    subgraph ACT["ACTUATION"]
        RM["2x 2-CH relay (opto)<br/>D6 st1, D7 st2, D8 st3"]
    end

    subgraph LOADS12["LOADS 12V"]
        M1["Worm motor 1<br/>60 kg-cm 16RPM"]
        M2["Worm motor 2"]
        M3["Worm motor 3"]
    end

    subgraph SENSE["SENSING"]
        DHT["DHT22<br/>data: D2"]
        DS["DS18B20<br/>data: D3 + 4.7k pull-up"]
    end

    subgraph UI["USER INTERFACE"]
        LCD["LCD 16x2 I2C<br/>SDA 20 / SCL 21"]
        LED["LEDs G/Y/R<br/>D9 / D10 / D11"]
        BUZ["Buzzer<br/>D12"]
        BTN["Start button<br/>D13"]
    end

    MEGA["ARDUINO MEGA 2560<br/>5V rail from buck"]

    OUT --> MSW
    MSW --> MF1 --> SSR1 --> H1
    MSW --> MF2 --> SSR2 --> H2
    MSW --> EFAN
    SSR1 -. "DC input 3-32V" .-> MEGA
    SSR2 -. "DC input" .-> MEGA

    BAT --> DSW --> F1
    F1 --> FA --> M1
    F1 --> FB --> M2
    F1 --> FC --> M3
    F1 --> FL --> BUCK --> MEGA
    RM --> M1
    RM --> M2
    RM --> M3
    MEGA --> RM

    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA --> LED
    MEGA --> BUZ
    BTN --> MEGA

    HEATSINK["SSR heatsinks - 7-10W each - closed electrical box"]
    SSR1 -.-> HEATSINK
    SSR2 -.-> HEATSINK
    DRAIN["PASSIVE CONDENSATE<br/>sloped floor -> drain -> tray"]
    DRAIN -.-> H1
```

## Wiring rules

1. **Three domains, three protections:** RCD + 10A branches (AC) · 25A main + 3A stations (12V) · 3A + buck (5V).
2. **Two kill switches, clearly labeled:** mains rocker and DC rocker.
3. **Mega inputs only:** SSR DC inputs (3–32V) and optocoupler LEDs (2–5 mA) — no power flows through the board.
4. **SSR heatsinks mandatory:** ~7–10 W dissipated per SSR at 6.8 A load; closed grounded metal box.
5. **Slow duty cycling (2–5 s)** on the SSRs; fast PWM is out.
6. **Wire gauge:** 2.0 mm² mains · 16 AWG battery main + logic feed · 18 AWG station branches · 22 AWG logic.
7. **Earthing:** electrical box, chamber frame, appliance chassis — all earthed; RCD is the life-safety layer.
8. The exhaust fan has no Mega channel — it runs on the mains rocker (stage 1 airflow).
