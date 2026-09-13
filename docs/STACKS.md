# Technology Stacks (Rev 6)

The full stack from silicon to tooling. Firmware behavior lives in `docs/FIRMWARE-GUIDE.md`; part ratings in `docs/HARDWARE.md`.

## 1. Firmware stack (bottom-up)

| Layer | Component | Version guidance | Role |
|---|---|---|---|
| Silicon | ATmega2560 (AVR 8-bit, 16 MHz, 256 KB flash / 8 KB SRAM / 4 KB EEPROM) | — | Bare-metal execution, no OS |
| Board package | **Arduino AVR Boards** core (Mega 2560 profile) | Latest stable | `digitalWrite`, `millis()`, Serial, I2C (Wire) |
| Library | `DHT sensor library` (Adafruit) **+** `Adafruit Unified Sensor` | Latest stable | DHT22 reads (≥2 s interval) |
| Library | `OneWire` (Paul Stoffregen) | Latest stable | DS18B20 bus |
| Library | `DallasTemperature` (Miles Burton) | Latest stable | DS18B20 high-level reads |
| Library | `LiquidCrystal I2C` (Frank de Brabander / marcoschwartz) | Latest stable | LCD @ 0x27/0x3F |
| Application | `umbrella-dryer.ino` (this repo) | Rev 6 | State machine + duty-cycle control |

**Toolchain:** Arduino IDE 2.x (Boards Manager → *Arduino Mega or Mega 2560*, Processor → *ATmega2560*) or `arduino-cli` for scripted builds. SRAM discipline: wrap LCD/Serial string literals in `F()` — 8 KB SRAM fills fast with menus.

**Reproducibility (for the capstone defense):** record core + library versions at flash time (`arduino-cli lib list`, IDE 2 shows them in Library Manager) and paste them into the paper's appendix.

## 2. Power stack (Rev 6)

| Stage | Component | In → Out |
|---|---|---|
| Source selection | **2P changeover switch** — wall outlet A / inverter B; 2nd pole grounds the inverter remote in wall mode | one source → RCD, never both |
| AC generation (battery mode) | **3000W pure sine inverter**, remote pin | 12.8 V → 220 V 60 Hz (stage-1 capped) |
| AC heat | RCD 30mA → mains rocker → 10A fuses → **2× SSR-40DA** | 220V → 2× 1500W heater-fans |
| AC exhaust | mains rocker gang | 220V → 12" Omni fan |
| Storage | 2× LiFePO4 12.8V 200Ah parallel w/ BMS 200 A each | — → 12.8 V bus (motors, control, inverter feed) |
| DC main | DC rocker + 25 A fuse | 12.8 V → station + logic branches |
| Actuation rail | 3 A ×3 station branches → 2× 2-CH relays | 3 worm motors |
| Logic rail | LM2596S buck + 3 A fuse | 12.8 V → **5.0 V @ 3 A** → Mega 5V pin + relay coils |
| Signal domain | Mega pins → SSR inputs (~12 mA) + optocoupler LEDs (2–5 mA) | Isolated triggers into both power domains |

## 3. Mechanical stack (per station)

```
Worm gear motor (60 kg·cm, 16 RPM, 8mm shaft)
   └─ 8×8 mm rigid coupling
        └─ 8mm × 300mm 304 SS shaft
             ├─ KP08 pillow block ×2 (supports)
             └─ umbrella holder (fabricated)
                  └─ umbrella (≤3 kg·cm load, ≥20× torque margin)
```

## 4. Development & docs tooling

| Purpose | Tool | Note |
|---|---|---|
| Firmware | Arduino IDE 2.x / `arduino-cli` | 115200 serial debug |
| Debugging | Serial Monitor prints @ state transitions | Per `docs/FIRMWARE-GUIDE.md` §8 |
| Version control | Git + GitHub (`qppd/umbrella-dryer-v2`) | `references/` is local-only |
| Diagrams | Mermaid (renders on GitHub) | FLOWCHART / BLOCK-DIAGRAM / SYSTEM-ARCHITECTURE |
| Procurement | Lazada PH + makerlab.ph | Cart: `docs/BOM.md` Appendix A |
| Electrical test | Multimeter (continuity/V/A) | Mandatory before first power-on (`docs/SETUP.md`) |

## 5. Optional / not used

- **PlatformIO (VS Code):** works with the same board core and libraries — optional, not required by the guide.
- **PWM speed control / BTS7960:** not in the stack (on/off control only) — see `docs/SYSTEM-ARCHITECTURE.md` §5.
- **SSR control of the exhaust fan:** not implemented — the fan is an appliance on the mains rocker.
- **RTC / EEPROM cycle logging:** not in scope; EEPROM counters are a possible future add-on for cycle-count analytics.
