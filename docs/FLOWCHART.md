# Flowcharts — Control Loop & Safety Interlocks (Rev 4)

Firmware behavior reference. Pin assignments per `docs/BOM.md` §15; control constants per `docs/FIRMWARE-GUIDE.md`.

## 1. Main control loop

```mermaid
flowchart TD
    PWR([Power on]) --> INIT[Init: safe relay states OFF<br/>LCD hello, sensor probe]
    INIT --> SELF{Self-test pass?<br/>DHT22 + DS18B20 valid}
    SELF -- no --> FAULT[FAULT state<br/>red LED + long beeps]
    SELF -- yes --> IDLE[IDLE<br/>green LED, heater OFF<br/>motors OFF, fan OFF]

    IDLE -- "start button (D13)" --> LOAD[Load umbrellas<br/>mark loaded stations 1-3]
    LOAD --> DRYING[DRYING<br/>yellow LED<br/>loaded station relays ON<br/>fan ON]

    DRYING --> READ[Read DHT22 humidity H<br/>read DS18B20 temp T]
    READ --> TOVER{T > 65 C?}
    TOVER -- yes --> CUT[HEATER CUTOFF<br/>heater relay OFF<br/>fan + motors keep running]
    CUT -- "T < 50 C" --> DRYING
    TOVER -- no --> DUTY[Duty cycle heater:<br/>duty = k x H error<br/>2-5 s time-proportional]
    DUTY --> HLOW{H below threshold<br/>for 5 min steady?}
    HLOW -- no --> READ
    HLOW -- yes --> DONE[COMPLETE<br/>heater OFF, stations OFF<br/>fan purge 2 min<br/>green LED + beeps]
    DONE --> IDLE

    FAULT --> IDLE
```

## 2. Heater safety interlock (inner loop, runs every cycle)

```mermaid
flowchart TD
    TICK([Control tick - every 500 ms]) --> T1{DS18B20 read OK?}
    T1 -- "fail x3" --> SERR[Sensor fault -> FAULT]
    T1 -- ok --> T2{T > 65 C?}
    T2 -- yes --> OFF1[Heater relay OFF<br/>latched until T < 50 C]
    T2 -- no --> T3{Cycle active?}
    T3 -- no --> OFF2[Heater OFF]
    T3 -- yes --> T4{H above threshold?}
    T4 -- no --> OFF2
    T4 -- yes --> PWM[Apply time-proportional duty<br/>ON window inside 4 s period]
    PWM --> RELAY[Write heater relay pin D4]
    OFF1 --> RELAY
    OFF2 --> RELAY
    SERR --> RELAY
```

## 3. Per-station fault handling

```mermaid
flowchart TD
    RUN([Station n running]) --> JAM{Umbrella jammed?<br/>stall noise / stall current}
    JAM -- yes --> FUSE[Station 3A fuse opens<br/>that motor stops]
    FUSE --> ISO[Other stations unaffected<br/>heater cycle continues]
    ISO --> USER[User removes jam<br/>replaces fuse<br/>restarts cycle]
    USER --> RUN
    JAM -- no --> RUN
```

> **Design note:** stations are fuse-isolated, not sensor-monitored (no current-sense path in Rev 4). A blown 3A fuse is detected at the UI as "station commanded ON but motion absent" — see `docs/TROUBLESHOOTING.md` §Motors.

## 4. State summary

| State | Heater | Stations | Fan / blower | LED | Buzzer |
|---|---|---|---|---|---|
| IDLE | OFF | OFF | OFF | Green | — |
| DRYING | duty-cycled | loaded ON | ON (heater branch) | Yellow | — |
| HEATER CUTOFF | OFF (latched) | ON | ON (purges heat) | Yellow (blink) | 1 chirp on entry |
| COMPLETE | OFF | OFF | 2-min purge (blower/heater branch) | Green | 3 beeps |
| FAULT | OFF | OFF | OFF | Red | long beeps until acknowledged |
