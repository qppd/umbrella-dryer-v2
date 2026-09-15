# Electrical Block Diagram — 12V DC Umbrella Dryer

> **Pure 12V DC system.** No mains voltage. No inverter. No RCD/GFCI.
> All heating, motor, and fan loads run from a 12 V LiFePO4 battery bank
> through fused DC distribution. Arduino Mega 2560 provides closed-loop
> temperature and humidity control with relay-switched heaters/motors
> and ESC-driven BLDC fans.

---

## 1. System Overview

```mermaid
flowchart TB
    BAT["12V LiFePO4<br/>Battery Bank<br/>BMS Protected"]

    MSW["DC Master Switch"]
    FMAIN["25A Main Fuse"]
    BUS["12V DC Bus"]

    FS1["20A Fuse<br/>Station 1"]
    FS2["20A Fuse<br/>Station 2"]
    FS3["20A Fuse<br/>Station 3"]
    FF["10A Fuse<br/>Fan Bus"]
    FL["3A Fuse<br/>Logic"]

    ST1["Station 1<br/>3x PTC + Motor"]
    ST2["Station 2<br/>3x PTC + Motor"]
    ST3["Station 3<br/>3x PTC + Motor"]
    FBUS["Automotive Relay Bus<br/>9x BLDC Fan Power"]

    BUCK["Buck Converter<br/>12V to 5V"]
    MEGA["Arduino Mega 2560"]
    DHT["DHT22<br/>Ambient T/RH"]
    DS["DS18B20<br/>Surface T"]
    LCD["LCD 16x2<br/>I2C Status"]

    BAT --> MSW --> FMAIN --> BUS
    BUS --> FS1 --> ST1
    BUS --> FS2 --> ST2
    BUS --> FS3 --> ST3
    BUS --> FF --> FBUS
    BUS --> FL --> BUCK --> MEGA
    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA -. "Relay Modules<br/>D4-D9" .-> ST1
    MEGA -. "Relay Modules<br/>D4-D9" .-> ST2
    MEGA -. "Relay Modules<br/>D4-D9" .-> ST3
    MEGA -. "ESC PWM<br/>D10-D12" .-> FBUS
```

---

## 2. Power Distribution Tree

Detailed power path from battery through fuses to individual loads.
Three identical station branches share the DC bus. The fan bus is a
separate fused branch feeding all BLDC ESCs through an automotive-grade
relay bus (spade terminals, blade fuses, high-current bus bar).

```mermaid
flowchart TB
    BAT["12V LiFePO4<br/>Battery Bank"]
    MSW["DPST Master Switch<br/>30A Rated"]
    FMAIN["ANL Fuse<br/>25A Main"]
    BUS["12V DC Bus<br/>Terminal Strip"]

    subgraph STA["STATION BRANCH - x3 IDENTICAL"]
        direction TB
        FS["ATO Blade Fuse<br/>20A per Station"]
        RM["2-Ch Relay Module<br/>Optoisolated"]
        RH["CH1: 30A Relay<br/>PTC Heaters"]
        RMOT["CH2: 10A Relay<br/>Worm Motor"]
        PTC["3x PTC Heater<br/>12V 100W each<br/>Parallel: 300W total"]
        MOT["SGM-370 Worm Motor<br/>12V 6RPM 14 kg-cm"]
    end

    subgraph FANBUS["BLDC FAN BUS"]
        direction TB
        FF["ATO Blade Fuse<br/>10A"]
        ARB["Automotive Relay Bus<br/>Spade Terminal Dist"]
        ESC["3x ESC Module<br/>per Station"]
        BLDC["3x 50mm Ducted<br/>BLDC Fan per Station"]
    end

    subgraph LOGIC["LOGIC FEED"]
        direction TB
        FL["ATO Blade Fuse<br/>3A"]
        BUCK["LM2596S Buck<br/>12V to 5V 3A"]
        MEGA["Arduino Mega 2560"]
    end

    BAT --> MSW --> FMAIN --> BUS
    BUS --> FS --> RH --> PTC
    FS --> RMOT --> MOT
    BUS --> FF --> ARB --> ESC --> BLDC
    BUS --> FL --> BUCK --> MEGA
```

---

## 3. Per-Station Architecture

One drying station in full detail. All three stations are electrically
identical. The relay module switches heater and motor loads; the ESCs
modulate fan speed from Mega PWM signals.

```mermaid
flowchart TB
    FUSE["ATO Blade Fuse 20A<br/>from DC Bus"]

    subgraph RELAYMOD["2-Ch Relay Module"]
        CH1["CH1: 30A Automotive Relay<br/>Coil 5V DC<br/>Mega Pin D4 / D6 / D8"]
        CH2["CH2: 10A PCB Relay<br/>Coil 5V DC<br/>Mega Pin D5 / D7 / D9"]
    end

    subgraph HEATERS["PTC Heater Array - 300W"]
        H1["PTC Heater 1<br/>12V 100W"]
        H2["PTC Heater 2<br/>12V 100W"]
        H3["PTC Heater 3<br/>12V 100W"]
    end

    MOTOR["SGM-370 Worm Motor<br/>12V 6RPM<br/>14 kg-cm Torque"]

    subgraph FANS["BLDC Fan Assembly"]
        E1["ESC 1<br/>Signal: D10 / D11 / D12"]
        E2["ESC 2<br/>Signal: D10 / D11 / D12"]
        E3["ESC 3<br/>Signal: D10 / D11 / D12"]
        F1["BLDC Fan 1<br/>50mm Ducted"]
        F2["BLDC Fan 2<br/>50mm Ducted"]
        F3["BLDC Fan 3<br/>50mm Ducted"]
    end

    BUS["12V DC Bus"]
    FBUS["Automotive<br/>Relay Bus"]
    MEGA["Arduino Mega 2560"]

    BUS --> FUSE --> CH1
    FUSE --> CH2
    CH1 --> H1
    CH1 --> H2
    CH1 --> H3
    CH2 --> MOTOR
    FBUS --> E1 --> F1
    FBUS --> E2 --> F2
    FBUS --> E3 --> F3
    MEGA -. "Relay Coils<br/>5V Signal" .-> RELAYMOD
    MEGA -. "PWM Signal<br/>1000-2000 us" .-> FANS
```

---

## 4. Controller I/O Map — Arduino Mega 2560

All digital pin assignments. The Mega runs at 5V from the buck converter.
No pins source or sink more than 40 mA. Relay coils draw ~70 mA each
(driven by the optoisolated relay module, not directly by the Mega).

```mermaid
flowchart LR
    subgraph IN["SENSOR INPUTS"]
        DHT["DHT22<br/>Ambient Temp + RH<br/>Data: D2"]
        DS["DS18B20<br/>Umbrella Surface Temp<br/>Data: D3 + 4.7k Pull-up"]
    end

    MEGA["Arduino Mega 2560<br/>ATmega2560 16MHz<br/>5V from Buck Converter"]

    subgraph I2C["I2C BUS"]
        LCD["LCD 16x2 I2C<br/>SDA: D20<br/>SCL: D21"]
    end

    subgraph OUT["ACTUATOR OUTPUTS"]
        R1["Station 1 Relays<br/>D4: Heaters 30A<br/>D5: Motor 10A"]
        R2["Station 2 Relays<br/>D6: Heaters 30A<br/>D7: Motor 10A"]
        R3["Station 3 Relays<br/>D8: Heaters 30A<br/>D9: Motor 10A"]
        E1["Station 1 Fan ESC<br/>D10: PWM 50Hz"]
        E2["Station 2 Fan ESC<br/>D11: PWM 50Hz"]
        E3["Station 3 Fan ESC<br/>D12: PWM 50Hz"]
    end

    DHT --> MEGA
    DS --> MEGA
    MEGA <--> LCD
    MEGA --> R1
    MEGA --> R2
    MEGA --> R3
    MEGA --> E1
    MEGA --> E2
    MEGA --> E3
```

---

## 5. Fuse and Wire Schedule

| Path | Fuse Rating | Fuse Type | Wire Gauge | Notes |
|------|-------------|-----------|------------|-------|
| Battery to DC Bus | 25 A | ANL | 10 AWG | Main system protection |
| Station 1 branch | 20 A | ATO blade | 12 AWG | 3x PTC + motor + ESCs |
| Station 2 branch | 20 A | ATO blade | 12 AWG | 3x PTC + motor + ESCs |
| Station 3 branch | 20 A | ATO blade | 12 AWG | 3x PTC + motor + ESCs |
| BLDC fan bus | 10 A | ATO blade | 14 AWG | All 9 ESCs in parallel |
| Logic feed | 3 A | ATO blade | 18 AWG | Buck converter input |
| Buck to Mega | 3 A | PCB trace | 22 AWG | 5V regulated rail |
| PTC heater branch | 30 A | Automotive relay | 12 AWG | Per relay CH1 output |
| Worm motor branch | 10 A | PCB relay | 16 AWG | Per relay CH2 output |
| ESC power input | 2 A per ESC | Bus bar | 18 AWG | From automotive relay bus |
| ESC signal wire | Logic level | Shielded | 22 AWG | PWM from Mega |

## 6. Relay and Pin Assignment

| Mega Pin | Function | Relay / Load | Current | Wire |
|----------|----------|-------------|---------|------|
| D2 | Sensor data | DHT22 | Logic | 22 AWG |
| D3 | Sensor data | DS18B20 + 4.7k | Logic | 22 AWG |
| D4 | Relay coil | Station 1 PTC heaters (30A) | ~70 mA | 22 AWG |
| D5 | Relay coil | Station 1 worm motor (10A) | ~70 mA | 22 AWG |
| D6 | Relay coil | Station 2 PTC heaters (30A) | ~70 mA | 22 AWG |
| D7 | Relay coil | Station 2 worm motor (10A) | ~70 mA | 22 AWG |
| D8 | Relay coil | Station 3 PTC heaters (30A) | ~70 mA | 22 AWG |
| D9 | Relay coil | Station 3 worm motor (10A) | ~70 mA | 22 AWG |
| D10 | PWM output | Station 1 fan ESCs x3 | Logic | 22 AWG |
| D11 | PWM output | Station 2 fan ESCs x3 | Logic | 22 AWG |
| D12 | PWM output | Station 3 fan ESCs x3 | Logic | 22 AWG |
| D20 (SDA) | I2C data | LCD 16x2 | Logic | 22 AWG |
| D21 (SCL) | I2C clock | LCD 16x2 | Logic | 22 AWG |

## 7. Design Notes

1. **Single-station operation recommended.** One station's 3x PTC heaters draw up to 25A at 12V (300W), which equals the main fuse rating. Run one station at a time, or reduce heater count when operating multiple stations simultaneously.
2. **PTC self-limiting.** Positive temperature coefficient heaters reduce current draw as they reach operating temperature. Inrush is brief; steady-state current per station is typically 15-20A.
3. **No mains voltage anywhere.** This system is entirely 12V DC. No inverter, no RCD/GFCI, no AC wiring. All user-accessible voltages are 12V DC or below.
4. **Relay module ratings.** Heater relay channels (CH1) must be 30A+ automotive-grade relays (not standard 10A PCB relays). Motor channels (CH2) can use standard 10A relays.
5. **Optoisolated relay modules.** The relay coil drive circuits are optoisolated from the Mega, providing galvanic isolation between the 5V logic and 12V power domains.
6. **ESC PWM protocol.** Standard 1-2 ms pulse width at 50 Hz. 1000 us = fans off; 2000 us = full speed. The Mega drives all three ESCs per station from a single PWM pin (parallel signal wiring).
7. **Automotive relay bus.** A high-current distribution bus using automotive blade fuses and spade terminals. All BLDC fan ESCs draw power from this bus, fused at 10A total.
8. **Wire gauge rationale.** 10 AWG for the main battery lead (25A with <3% drop over short runs). 12 AWG for station branches (20A). 14 AWG for fan bus (10A). 18 AWG for logic feed. 22 AWG for all signal/relay coil wires.
9. **LiFePO4 battery bank.** 12.8V nominal, BMS with over-voltage, under-voltage, over-current, and short-circuit protection. Recommended minimum 100Ah capacity for multi-station runtime.
10. **Condensate management.** Passive drainage — sloped chamber floor leads to collection tray. No pump required.
