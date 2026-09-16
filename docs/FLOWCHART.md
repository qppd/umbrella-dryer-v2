# Flowcharts — Control Loop & Safety Interlocks — 12V DC

> Firmware behavior reference. Pin assignments per `wiring/README.md` (canonical); state machine per `docs/FIRMWARE-GUIDE.md`.

---

## 1. Main control loop

```mermaid
flowchart TD
    PWR([Power on]) --> ARM["Arm ESCs<br/>D13 fan bus ON<br/>write 1000µs for 2s"]
    ARM --> INIT["Init: all relays OFF<br/>LCD hello, sensor probe"]
    INIT --> SELF{Self-test pass?<br/>DHT22 + DS18B20 valid}
    SELF -- no --> FAULT["FAULT state<br/>red LED + long beeps"]
    SELF -- yes --> IDLE["IDLE<br/>green LED<br/>All loads OFF<br/>LCD: READY"]

    IDLE -- "button (D14)" --> PREHEAT["PREHEAT<br/>red LED<br/>Fan bus ON (D13)<br/>ESC throttle FULL (D10–D12)<br/>PTC ON for station 1 (D4)<br/>Staged: rotate 30s"]

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
    TIMER -- yes --> COOL["COOL<br/>PTC OFF, motor OFF<br/>Fans stay ON<br/>2 min timer"]

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
    T2 -- yes --> OFF1["ALL OFF<br/>PTC relays LOW (via NPN: no base drive)<br/>Motor relays HIGH (opto: inactive)<br/>ESC write 0<br/>Fan bus relay LOW"]
    T2 -- no --> T3{Cycle active?}
    T3 -- no --> OFF2["All actuators OFF"]
    T3 -- yes --> OK["System OK — continue phase"]

    OFF1 --> RELAY["Write pins D4–D18"]
    OFF2 --> RELAY
    OK --> RELAY
    SERR --> RELAY
```

> **Defense in depth:** DS18B20 firmware cutoff (65°C) → PTC self-regulation → 130°C thermal fuse (per heater, 9×) → 30A branch fuses → BMS. Five independent layers.

---

## 3. Per-station fault handling

```mermaid
flowchart TD
    RUN(["Station n running"]) --> JAM{Umbrella jammed?<br/>stall noise}
    JAM -- yes --> FUSE["3A motor fuse opens<br/>that motor stops"]
    FUSE --> ISO["Other stations unaffected<br/>PTC + fan cycle continues"]
    ISO --> USER["User removes jam<br/>replaces fuse<br/>restarts cycle"]
    USER --> RUN
    JAM -- no --> RUN
```

> **Design note:** stations are fuse-isolated, not sensor-monitored (no current-sense path). A blown 3A fuse is detected at UI as "station commanded ON but motion absent" — see `docs/TROUBLESHOOTING.md`.

---

## 4. ESC arming sequence

```mermaid
flowchart LR
    BOOT([Boot]) --> BUS_ON["D13 fan bus relay ON<br/>(powers ESCs)"]
    BUS_ON --> ATTACH["esc.attach(pin)<br/>D10, D11, D12"]
    ATTACH --> ZERO["esc.writeMicroseconds(1000)<br/>min throttle pulse"]
    ZERO --> WAIT["delay 2000ms<br/>(ESC detects min)"]
    WAIT --> READY["ESCs armed"]
    READY --> BUS_OFF["D13 fan bus relay OFF<br/>(prevent fan creep)"]
    BUS_OFF --> IDLE["Enter IDLE state"]
```

---

## 5. State summary

| State | PTC Relays | Motor Relays | Fan Bus + ESCs | LED | Buzzer |
|---|---|---|---|---|---|
| IDLE | OFF | OFF | OFF | Green | — |
| PREHEAT | Staged (1 at a time) | OFF | ON (full speed) | Red | — |
| DRY | Staged (1 at a time) | Staged (1 at a time) | ON (full speed) | Yellow | — |
| COOL | OFF | OFF | ON (full speed) | Yellow | — |
| COMPLETE | OFF | OFF | OFF | Green | 3 beeps |
| THERMAL CUTOFF | OFF | OFF | OFF | Red (blink) | 1 chirp (on failed reset) |
| FAULT | OFF | OFF | OFF | Red | long beeps |
