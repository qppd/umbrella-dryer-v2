# Electrical Block Diagram (Rev 4)

Canonical wiring map. Same content as `docs/BOM.md` §11, kept as a standalone printable sheet. All loads are 12V DC (extra-low voltage); all logic is 5V.

```mermaid
flowchart TB
    subgraph POWER["POWER DOMAIN — 12.8V LiFePO4 30Ah (BMS 30A)"]
        BAT["Battery<br/>12.8V 30Ah LiFePO4"]
        SW["Rocker switch<br/>main power (control side)"]
        F1["Fuse 25A<br/>main"]
        F2["Fuse 15A<br/>heater branch"]
        FA["Fuse 3A<br/>station 1"]
        FB["Fuse 3A<br/>station 2"]
        FC["Fuse 3A<br/>station 3"]
        BUCK["LM2596S buck<br/>12.8V -> 5V 3A"]
        FL["Fuse 3A<br/>logic branch"]
    end

    subgraph ACT["ACTUATION — relay modules, optocoupler isolated"]
        RH["30A 1-CH relay<br/>heater<br/>input: D4"]
        RM1["2-CH relay #1<br/>ch1: D5 st1<br/>ch2: D6 st2"]
        RM2["2-CH relay #2<br/>ch1: D7 st3<br/>ch2: D8 fan (optional purge)"]
    end

    subgraph LOADS["LOADS — 12V"]
        PTC["PTC heater 100W<br/>w/ blower"]
        M1["Worm motor 1<br/>60 kg-cm 16RPM"]
        M2["Worm motor 2<br/>60 kg-cm 16RPM"]
        M3["Worm motor 3<br/>60 kg-cm 16RPM"]
        FAN["120mm fan<br/>circulation"]
    end

    subgraph SENSE["SENSING"]
        DHT["DHT22<br/>chamber humidity + temp<br/>data: D2"]
        DS["DS18B20 waterproof<br/>heater-zone temp<br/>data: D3 + 4.7k pull-up"]
    end

    subgraph UI["USER INTERFACE"]
        LCD["LCD 16x2 I2C<br/>SDA 20 / SCL 21"]
        LED["LEDs G/Y/R<br/>D9 / D10 / D11"]
        BUZ["Active buzzer<br/>D12"]
        BTN["Start button<br/>D13 INPUT_PULLUP"]
    end

    MEGA["ARDUINO MEGA 2560<br/>5V rail from buck"]

    BAT --> SW --> F1
    F1 --> F2 --> RH --> PTC
    RH --> FAN
    F1 --> FA --> M1
    F1 --> FB --> M2
    F1 --> FC --> M3
    F1 --> FL --> BUCK --> MEGA
    RH -- "opto input" --> MEGA
    RM1 -- "opto inputs" --> MEGA
    RM2 -- "opto inputs" --> MEGA
    M1 -.-> RM1
    M2 -.-> RM1
    M3 -.-> RM2
    FAN -.-> RM2
    PTC -.-> RH
    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA --> LED
    MEGA --> BUZ
    BTN --> MEGA

    DRAIN["PASSIVE CONDENSATE<br/>sloped floor -> drain tube -> drip tray"]
    DRAIN -.-> PTC
```

## Wiring rules

1. **Relay coils** hang off the buck's 5V rail — never from Mega pins. Mega drives only the optocoupler LEDs (~2–5 mA).
2. **Wire gauge:** 16 AWG main + heater branch (incl. blower fan) · 18 AWG station branches · 22 AWG logic + chamber fan.
3. **Common ground:** battery −, buck −, all relay boards, sensors, Mega GND tied at the barrier block.
4. **Contacts are 30VDC-rated** — mains AC is prohibited by design.
5. **Slow duty cycling only** (2–5 s period) on the heater relay; fast PWM destroys mechanical contacts.
6. **Blower rides the heater branch:** the PTC's blower and the chamber fan are wired behind the same 15 A fuse as the heater — air always moves whenever heat is on. The D8 fan relay only adds post-cycle purge control (optional).
