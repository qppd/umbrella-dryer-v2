# Electrical Block Diagram (Rev 6: dual source + mains heat + 12V stations)

Canonical wiring map. Same content as `wiring/README.md`, printable sheet. Domains: **220V AC heat (wall outlet OR inverter via changeover)**, **12V DC stations + inverter feed**, **5V logic**. The Mega never touches mains or battery power.

```mermaid
flowchart TB
    subgraph AC["220V AC DOMAIN - dual source"]
        OUT["Wall outlet 220V"]
        INV["3000W pure sine inverter<br/>12V DC from battery bank"]
        CHO["CHANGEOVER 2P<br/>A: wall / B: inverter"]
        RCD["RCD/GFCI"]
        MSW["Mains rocker (2-gang)"]
        MF1["Fuse 10A line 1"]
        MF2["Fuse 10A line 2"]
        SSR1["Fotek SSR-40DA #1<br/>input: D4"]
        SSR2["Fotek SSR-40DA #2<br/>input: D5"]
        H1["PTC heater-fan 1500W #1"]
        H2["PTC heater-fan 1500W #2"]
        EFAN["12in Omni exhaust fan 220V"]
    end

    subgraph DC["12V DC DOMAIN - battery bank"]
        BAT["2x LiFePO4 12.8V 200Ah<br/>parallel, BMS 200A each"]
        IFUSE["ANL 250A<br/>inverter feed"]
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

    OUT --> CHO
    INV --> CHO
    CHO --> RCD
    RCD --> MSW
    MSW --> MF1 --> SSR1 --> H1
    MSW --> MF2 --> SSR2 --> H2
    MSW --> EFAN
    SSR1 -. "DC input 3-32V" .-> MEGA
    SSR2 -. "DC input" .-> MEGA
    BAT --> IFUSE --> INV
    CHO -. "mode sense D14" .-> MEGA
    CHO -. "remote pin gnd (wall mode)" .-> INV

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

1. **Four domains, protections at every level:** RCD + 10A branches (AC, either source) · 250A ANL (inverter feed) · 25A main + 3A stations (12V) · 3A + buck (5V).
2. **Two kill switches, clearly labeled:** mains rocker and DC rocker.
3. **The changeover is the only point where wall power and inverter output meet — and they never meet electrically.** In wall mode the inverter remote pin is grounded (inverter OFF).
4. **Mega inputs only:** SSR DC inputs (3–32V), D14 mode sense, and optocoupler LEDs (2–5 mA) — no power flows through the board.
5. **SSR heatsinks mandatory:** ~7–10 W dissipated per SSR at 6.8 A load; closed grounded metal box.
6. **Slow duty cycling (2–5 s)** on the SSRs; fast PWM is out.
7. **Wire gauge:** 2.0 mm² mains · **1/0 AWG inverter feed (≤ 1 m, 250A ANL at the battery end)** · 4 AWG battery links · 16 AWG battery main + logic feed · 18 AWG station branches · 22 AWG logic.
8. **Earthing:** electrical box, chamber frame, appliance chassis, inverter chassis — all earthed; RCD is the life-safety layer.
9. The exhaust fan has no Mega channel — it runs on the mains rocker (stage 1 airflow) on either source.
