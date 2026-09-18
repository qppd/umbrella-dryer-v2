# Flowcharts — Control Loop & Safety Interlocks — 12V DC

> Firmware behavior reference. Pin assignments per `wiring/README.md`; state machine per `docs/FIRMWARE-GUIDE.md`.

---

## 1. Main control loop

```mermaid
flowchart TD
    PWR([Power on]) --> INIT["Init: all SSRs LOW<br/>blower PWM 0 (D10–D12)<br/>LCD hello, sensor probe"]
    INIT --> SELF{Self-test pass?<br/>DHT22 + DS18B20 valid}
    SELF -- no --> FAULT["FAULT state<br/>red LED + long beeps"]
    SELF -- yes --> IDLE["IDLE<br/>green LED<br/>All loads OFF<br/>LCD: READY"]

    IDLE -- "button (D14)" --> PREHEAT["PREHEAT<br/>red LED<br/>Fan bus ON (D13)<br/>Blowers FULL (D10–D12)<br/>PTC ON for station 1 (D4)<br/>Staged: rotate 30s"]

    PREHEAT --> READ["Read DHT22 humidity<br/>read DS18B20 temp"]
    READ --> TOVER{T > 65°C?}
    TOVER -- yes --> CUTOFF["THERMAL CUTOFF<br/>ALL OFF<br/>red LED blink + error on LCD"]
    TOVER -- no --> TEMP_OK{T ≥ 45°C?}
    TEMP_OK -- no --> PREHEAT
    TEMP_OK -- yes --> DRY["DRY<br/>yellow LED<br/>PTC + motor ON<br/>Staged: rotate 30s<br/>15 min timer"]

    DRY --> READ2["Read sensors"]
    READ2 --> TOVER2{T > 65°C?}
    TOVER2 -- yes --> CUTOFF
    TOVER2 -- no --> TIMER{15 min done?}
    TIMER -- no --> DRY
    TIMER -- yes --> COOL["COOL<br/>PTC OFF, motor OFF<br/>Blowers stay ON<br/>2 min timer"]

    COOL --> COOL_TIMER{2 min done?}
    COOL_TIMER -- no --> COOL
    COOL_TIMER -- yes --> DONE["COMPLETE<br/>All OFF<br/>green LED + 3 beeps"]
    DONE --> IDLE

    FAULT --> IDLE
    CUTOFF --> IDLE
```

---

## 2. Safety interlock (inner loop, runs every 500ms)

```mermaid
flowchart TD
    TICK([Control tick]) --> T1{DS18B20 read OK?}
    T1 -- "fail x3" --> SERR["Sensor fault → FAULT"]
    T1 -- ok --> T2{T > 65°C?}
    T2 -- yes --> OFF1["ALL OFF<br/>PTC SSRs LOW (D4/D6/D8)<br/>Motor SSRs LOW (D5/D7/D9)<br/>Fan bus SSR LOW (D13)<br/>Blower PWM 0 (D10–D12)"]
    T2 -- no --> T3{Cycle active?}
    T3 -- no --> OFF2["All actuators OFF"]
    T3 -- yes --> OK["System OK — continue phase"]

    OFF1 --> WRITE["Write pins D4–D18"]
    OFF2 --> WRITE
    OK --> WRITE
    SERR --> WRITE
```

> **Defense in depth:** DS18B20 firmware cutoff (65°C) → PTC self-regulation → BMS 200A. Three independent layers.

---

## 3. Per-station fault handling

```mermaid
flowchart TD
    RUN(["Station n running"]) --> JAM{Umbrella jammed?<br/>stall noise}
    JAM -- yes --> STALL["Motor stalls<br/>SGM-370 stall current ~0.8A<br/>self-locking worm holds the load"]
    STALL --> USER["User clears the jam<br/>restarts the cycle"]
    USER --> RUN
    JAM -- no --> RUN
```

> **Design note:** stations are not sensor-monitored (no current-sense path). A stalled motor is detected by ear — hum without rotation — see `docs/TROUBLESHOOTING.md`.

---

## 4. Fan control on boot

No ESC arming needed — blowers take duty-cycle PWM directly from Mega pins.

```mermaid
flowchart LR
    BOOT([Boot]) --> SAFE["All SSRs LOW<br/>PWM pins 0 (D10–D12)"]
    SAFE --> IDLE["IDLE<br/>blowers off until PREHEAT"]
```

---

## 5. State summary

| State | PTC SSRs | Motor SSRs | Fan Bus + Blower PWM | LED | Buzzer |
|---|---|---|---|---|---|
| IDLE | OFF | OFF | OFF | Green | — |
| PREHEAT | Staged (1 at a time) | OFF | ON (full speed) | Red | — |
| DRY | Staged (1 at a time) | Staged (1 at a time) | ON (full speed) | Yellow | — |
| COOL | OFF | OFF | ON (full speed) | Yellow | — |
| COMPLETE | OFF | OFF | OFF | Green | 3 beeps |
| THERMAL CUTOFF | OFF | OFF | OFF | Red (blink) | 1 chirp (on failed reset) |
| FAULT | OFF | OFF | OFF | Red | long beeps |
