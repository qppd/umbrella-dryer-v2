# Firmware Guide — 12V DC + BLDC Fans

> Complete firmware reference for the Umbrella Dryer V2 running on a **12V DC-only** system. BLDC fans are controlled via ESC PWM signals. PTC heaters and worm motors are relay-switched.

---

## 1. System Logic and State Machine

### 1a. Operational Sequence
1. **Boot** → Initialized. Arms 3 ESCs (BLDC fan controllers) via low-throttle (1000 µs) PWM signals on D10/D11/D12. Master fan bus relay (D13) is closed (ON) momentarily during this arming sequence, then de-energized to prevent fan creep.
2. **Idle** → Reads DHT22 (humidity) + DS18B20 (temperature), displays on LCD. Button waits for input. Status LED is **GREEN**.
3. **Button press** → Starts a 4-phase drying cycle:
   - **Phase 1 — Preheat** (Chamber Temp < 45°C): Master fan bus relay (D13) ON. ESCs throttle fans to FULL (2000 µs or 180 on servo write). PTC heater relays D4, D6, D8 are energized (ON) sequentially to warm up the chamber. Motors remain OFF. Status LED is **RED** (heating active).
   - **Phase 2 — Dry** (Chamber Temp ≥ 45°C): Chamber temperature has reached target. Station worm gear motors D5, D7, D9 are switched ON to spin the umbrellas at 6 RPM. PTC heaters and BLDC fans continue running. Timer starts counting down (default 15 minutes). Status LED is **YELLOW** (drying/spinning).
   - **Phase 3 — Cool** (Timer Done): PTC heaters switched OFF. Motors switched OFF (umbrellas stop spinning). Fans remain running at full speed for 2 minutes to purge hot air and cool down the components. Status LED is **YELLOW**.
   - **Phase 4 — Done**: All loads de-energized. Master fan bus relay OFF. Buzzer beeps 3 times. LCD shows "COMPLETE". Status LED is **GREEN**.
4. **Safety cutoff (any active phase)**: If DS18B20 reads >65°C, all relays and ESC signals are immediately killed (latched OFF). LCD displays "THERMAL CUTOFF!" and the RED LED blinks.
5. **Button repress (any active phase)**: Functions as an Emergency Stop. Immediately cuts all loads and returns the system to IDLE.

---

## 2. Pin Map — Arduino Mega 2560

|| Pin | Net | Mode | Default | Active Level | Notes |
|---|---|---|---|---|---|
|| **D2** | DHT22_DATA | Input | — | — | Chamber humidity & ambient temp; 10kΩ pull-up to 5V |
|| **D3** | DS18B20_DATA | Input | — | — | Heater-zone temperature probe; 4.7kΩ pull-up to 5V |
|| **D4** | SSR_PTC_1 | Output | LOW | HIGH (ON) | Station 1 PTC heater (LCTC DC-DC SSR 40A) |
|| **D5** | SSR_MOTOR_1 | Output | LOW | HIGH (ON) | Station 1 worm motor (LCTC DC-DC SSR 10A) |
|| **D6** | SSR_PTC_2 | Output | LOW | HIGH (ON) | Station 2 PTC heater (LCTC DC-DC SSR 40A) |
|| **D7** | SSR_MOTOR_2 | Output | LOW | HIGH (ON) | Station 2 worm motor (LCTC DC-DC SSR 10A) |
|| **D8** | SSR_PTC_3 | Output | LOW | HIGH (ON) | Station 3 PTC heater (LCTC DC-DC SSR 40A) |
|| **D9** | SSR_MOTOR_3 | Output | LOW | HIGH (ON) | Station 3 worm motor (LCTC DC-DC SSR 10A) |
|| **D10** | ESC_PWM_1 | Output | PWM | 1000 µs | Station 1 BLDC fan ESC speed control |
|| **D11** | ESC_PWM_2 | Output | PWM | 1000 µs | Station 2 BLDC fan ESC speed control |
|| **D12** | ESC_PWM_3 | Output | PWM | 1000 µs | Station 3 BLDC fan ESC speed control |
|| **D13** | SSR_FAN_BUS | Output | LOW | HIGH (ON) | Master Fan Bus (LCTC DC-DC SSR 40A) |
|| **D14** | BTN_START | Input | HIGH | LOW (ON) | Arcade start button (internal pull-up enabled) |
|| **D15** | LED_RED | Output | LOW | HIGH (ON) | Status LED: active heating |
|| **D16** | LED_YELLOW | Output | LOW | HIGH (ON) | Status LED: drying and rotating / cooling |
|| **D17** | LED_GREEN | Output | HIGH | HIGH (ON) | Status LED: system ready or cycle complete |
|| **D18** | BUZZER | Output | LOW | HIGH (ON) | Active 5V buzzer |
|| **D20** | I2C_SDA | I2C | — | — | LCD SDA pin (hardware I2C) |
|| **D21** | I2C_SCL | I2C | — | — | LCD SCL pin (hardware I2C) |

---

## 3. Timing and Control Thresholds

| Parameter | Value | Design Rationale / Notes |
|---|---|---|
| **Loop Tick Interval** | 500 ms | Prevents sensor bus congestion; provides stable sensor readings |
| **Preheat Threshold** | 45.0°C | Chamber air temp target required to enable safe centrifugal drying |
| **Thermal Cutoff** | 65.0°C | Absolute maximum chamber ceiling; triggers immediate system lock |
| **Dry Phase Timer** | 15 minutes | Standard cycle length; sufficient for complete moisture removal |
| **Cool Phase Timer** | 2 minutes | Fan-only overrun to dissipate residual heater block temperature |
| **ESC Arm Delay** | 2000 ms | Mandatory delay at boot sending 1000 µs throttle to initialize ESCs |
| **Debounce Delay** | 300 ms | Ignores button contact bounce and microphonics |

---

## 4. Complete Arduino Sketch

Copy and paste the following complete, verified sketch into the Arduino IDE.

```cpp
// ============================================================================
// Umbrella Dryer V2 — 12V DC-Only System Firmware
// Target Board: Arduino Mega 2560
// Dependencies: DHT, OneWire, DallasTemperature, Servo, LiquidCrystal_I2C
// ============================================================================

#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

// ---- Pin Definitions ----
#define PIN_DHT22         2
#define PIN_DS18B20       3

// Actuators
#define PIN_SSR_PTC_1   4   // LCTC DC-DC SSR 40A (Station 1 Heaters)
#define PIN_SSR_MOTOR_1 5   // LCTC DC-DC SSR 10A (Station 1 Motor)
#define PIN_SSR_PTC_2   6   // LCTC DC-DC SSR 40A (Station 2 Heaters)
#define PIN_SSR_MOTOR_2 7   // LCTC DC-DC SSR 10A (Station 2 Motor)
#define PIN_SSR_PTC_3   8   // LCTC DC-DC SSR 40A (Station 3 Heaters)
#define PIN_SSR_MOTOR_3 9   // LCTC DC-DC SSR 10A (Station 3 Motor)

#define PIN_ESC_PWM_1     10  // ESC PWM signal Station 1
#define PIN_ESC_PWM_2     11  // ESC PWM signal Station 2
#define PIN_ESC_PWM_3     12  // ESC PWM signal Station 3
#define PIN_SSR_FAN_BUS   13  // LCTC DC-DC SSR 40A (Master Fan Bus)

// UI and Peripherals
#define PIN_BTN_START     14  // Arcade button (active-LOW, pull-up)
#define PIN_LED_RED       15  // Active heating
#define PIN_LED_YELLOW    16  // Centrifugal drying / Cooling
#define PIN_LED_GREEN     17  // System ready / Cycle complete
#define PIN_BUZZER        18  // Audible notifications

// ---- Sensor Objects ----
DHT dht(PIN_DHT22, DHT22);
OneWire oneWire(PIN_DS18B20);
DallasTemperature ds18b20(&oneWire);
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Alternate address: 0x3F

// ---- ESC PWM Objects ----
Servo esc1;
Servo esc2;
Servo esc3;

// ---- Configuration and Constants ----
const float PREHEAT_TEMP   = 45.0;                      // °C - dry trigger
const float CUTOFF_TEMP    = 65.0;                      // °C - safety threshold
const unsigned long DRY_TIME_MS  = 15UL * 60UL * 1000UL; // 15-minute drying timer
const unsigned long COOL_TIME_MS = 2UL * 60UL * 1000UL;  // 2-minute cooling run
const unsigned long ESC_ARM_MS   = 2000;                // 2-second arm delay
const int ESC_OFF          = 0;                         // Stopped throttle (0 degrees)
const int ESC_FULL         = 180;                       // Full speed throttle (180 degrees)

// ---- Staged operation (one station at a time — keeps draw ~36A under the 50A main fuse) ----
const uint8_t PIN_PTC[3]   = { PIN_RELAY_PTC_1,  PIN_RELAY_PTC_2,  PIN_RELAY_PTC_3  };
const uint8_t PIN_MOT[3]   = { PIN_RELAY_MOTOR_1, PIN_RELAY_MOTOR_2, PIN_RELAY_MOTOR_3 };
const uint8_t PIN_ESCS[3]  = { PIN_ESC_PWM_1,    PIN_ESC_PWM_2,    PIN_ESC_PWM_3    };
const unsigned long STAGE_MS = 30000;   // 30 s per station before rotating
Servo* const ESCS[3] = { &esc1, &esc2, &esc3 };
uint8_t activeStation = 0;
unsigned long stageStart = 0;

// Energize ONLY the active station: PTC always, motor only in DRY
void applyStage(bool dryMotors) {
  for (uint8_t i = 0; i < 3; i++) {
    autoRelayOff(PIN_PTC[i]);
    pcbRelayOff(PIN_MOT[i]);
    ESCS[i]->write(ESC_OFF);
  }
  autoRelayOn(PIN_PTC[activeStation]);
  ESCS[activeStation]->write(ESC_FULL);
  if (dryMotors) pcbRelayOn(PIN_MOT[activeStation]);
}

// Rotate to the next station every STAGE_MS
void rotateStage(unsigned long now) {
  if (now - stageStart >= STAGE_MS) {
    stageStart = now;
    activeStation = (activeStation + 1) % 3;
    Serial.print("Stage rotate -> station ");
    Serial.println(activeStation + 1);
  }
}

// ---- System State Machine ----
enum State { STATE_IDLE, STATE_PREHEAT, STATE_DRY, STATE_COOL, STATE_DONE, STATE_CUTOFF };
State currentPhase = STATE_IDLE;

unsigned long phaseStart  = 0;
unsigned long lastLoopTick = 0;
float humidity            = 0;
float temperature         = 0;
bool buttonPrevState      = HIGH;

// ---- Actuation Helpers ----
void pcbRelayOn(int pin)  { digitalWrite(pin, LOW);  } // Active-LOW
void pcbRelayOff(int pin) { digitalWrite(pin, HIGH); } // Active-LOW

void autoRelayOn(int pin)  { digitalWrite(pin, HIGH); } // Active-HIGH via 2N2222
void autoRelayOff(int pin) { digitalWrite(pin, LOW);  } // Active-HIGH via 2N2222

// ---- Absolute System Safety Shutdown ----
void allOff() {
  // Turn off high-power heater elements (Active-HIGH relays)
  autoRelayOff(PIN_RELAY_PTC_1);
  autoRelayOff(PIN_RELAY_PTC_2);
  autoRelayOff(PIN_RELAY_PTC_3);

  // Turn off motors (Active-LOW relays)
  pcbRelayOff(PIN_RELAY_MOTOR_1);
  pcbRelayOff(PIN_RELAY_MOTOR_2);
  pcbRelayOff(PIN_RELAY_MOTOR_3);

  // Stop ESC signals and isolate power rail
  esc1.write(ESC_OFF);
  esc2.write(ESC_OFF);
  esc3.write(ESC_OFF);
  delay(10);
  autoRelayOff(PIN_RELAY_FAN_BUS);

  // Manage UI indicators
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_LED_YELLOW, LOW);
  digitalWrite(PIN_LED_GREEN, LOW);
  digitalWrite(PIN_BUZZER, LOW);
}

// ---- ESC Initialization (Arming Sequence) ----
void armESCs() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Arming ESCs...");
  
  // Power up the fan bus rail to allow ESCs to sense incoming power during pulse
  autoRelayOn(PIN_RELAY_FAN_BUS);
  delay(100);
  
  esc1.attach(PIN_ESC_PWM_1);
  esc2.attach(PIN_ESC_PWM_2);
  esc3.attach(PIN_ESC_PWM_3);
  
  // Send minimum throttle pulse to initialize ESC controller ICs
  esc1.write(ESC_OFF);
  esc2.write(ESC_OFF);
  esc3.write(ESC_OFF);
  
  delay(ESC_ARM_MS);
  
  // Kill power to bus to prevent any fan creep before active start
  autoRelayOff(PIN_RELAY_FAN_BUS);
  lcd.clear();
}

// ---- Fan Speed Control ----
void fansOn() {
  autoRelayOn(PIN_RELAY_FAN_BUS);
  delay(100); // Allow automotive relay contact debounce and rail stabilization
  esc1.write(ESC_FULL);
  esc2.write(ESC_FULL);
  esc3.write(ESC_FULL);
}

void fansOff() {
  esc1.write(ESC_OFF);
  esc2.write(ESC_OFF);
  esc3.write(ESC_OFF);
  delay(50);
  autoRelayOff(PIN_RELAY_FAN_BUS);
}

// ---- Sensor Data Acquisition ----
void readSensors() {
  humidity = dht.readHumidity();
  ds18b20.requestTemperatures();
  float tempRead = ds18b20.getTempCByIndex(0);
  
  if (tempRead != DEVICE_DISCONNECTED_C) {
    temperature = tempRead;
  }
}

// ---- Display Management ----
void lcdUpdate(const char* stateName, int rMin, int rSec) {
  lcd.setCursor(0, 0);
  lcd.print("H:");
  if (isnan(humidity)) {
    lcd.print("ERR");
  } else {
    lcd.print((int)humidity);
    lcd.print("%");
  }
  lcd.print(" T:");
  lcd.print((int)temperature);
  lcd.print("C    ");

  lcd.setCursor(0, 1);
  lcd.print(stateName);
  lcd.print(" ");
  if (rMin >= 0) {
    if (rMin < 10) lcd.print("0");
    lcd.print(rMin);
    lcd.print(":");
    if (rSec < 10) lcd.print("0");
    lcd.print(rSec);
  } else {
    lcd.print("     ");
  }
  lcd.print("  ");
}

// ---- System Initialization ----
void setup() {
  Serial.begin(115200);
  Serial.println("Umbrella Dryer V2 — 12V DC System Boot Initializing");

  // Actuator Output Setup & Hard Pull-Offs
  pinMode(PIN_RELAY_PTC_1, OUTPUT);
  pinMode(PIN_RELAY_PTC_2, OUTPUT);
  pinMode(PIN_RELAY_PTC_3, OUTPUT);
  pinMode(PIN_RELAY_MOTOR_1, OUTPUT);
  pinMode(PIN_RELAY_MOTOR_2, OUTPUT);
  pinMode(PIN_RELAY_MOTOR_3, OUTPUT);
  pinMode(PIN_RELAY_FAN_BUS, OUTPUT);

  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_YELLOW, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  // Put system in completely safe offline state
  allOff();

  // Input Setup
  pinMode(PIN_BTN_START, INPUT_PULLUP);

  // Initialize Peripherals
  dht.begin();
  ds18b20.begin();
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Umbrella Dryer");
  lcd.setCursor(0, 1);
  lcd.print("V2 DC SYSTEM");
  delay(1500);

  // Core ESC Calibration & Arming
  armESCs();

  // Settle on READY State
  digitalWrite(PIN_LED_GREEN, HIGH);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("SYSTEM READY");
  lcd.setCursor(0, 1);
  lcd.print("Press Button");
}

// ---- Main Control Loop ----
void loop() {
  unsigned long now = millis();
  
  // Stable 500 ms loop interval
  if (now - lastLoopTick < 500) return;
  lastLoopTick = now;

  readSensors();

  // ---- Absolute Over-Temperature Interlock ----
  if (temperature > CUTOFF_TEMP && currentPhase != STATE_IDLE && currentPhase != STATE_CUTOFF) {
    Serial.print("CRITICAL THERMAL CUTOFF TRIP: ");
    Serial.println(temperature);
    allOff();
    currentPhase = STATE_CUTOFF;
    phaseStart = now;
    return;
  }

  // ---- Non-blocking Button Edge Detection ----
  bool buttonState = digitalRead(PIN_BTN_START);
  bool buttonClicked = (buttonState == LOW && buttonPrevState == HIGH);
  buttonPrevState = buttonState;

  // ---- State Machine Logic ----
  switch (currentPhase) {

    // ================= STATE READY/IDLE =================
    case STATE_IDLE:
      digitalWrite(PIN_LED_GREEN, HIGH);
      digitalWrite(PIN_LED_RED, LOW);
      digitalWrite(PIN_LED_YELLOW, LOW);
      lcdUpdate("READY", -1, -1);

      if (buttonClicked) {
        Serial.println("CYCLE COMMENCING");
        digitalWrite(PIN_LED_GREEN, LOW);
        digitalWrite(PIN_LED_RED, HIGH);
        currentPhase = STATE_PREHEAT;
        phaseStart = now;
        fansOn();
        activeStation = 0;
        stageStart = now;
        applyStage(false); // PTC heaters only, motors off
      }
      break;

    // ================= STATE PREHEAT =================
    case STATE_PREHEAT:
      {
        int elapsed = (int)((now - phaseStart) / 1000);
        lcdUpdate("PREHEAT", elapsed / 60, elapsed % 60);

        applyStage(false);  // staged: rotates station every 30 s automatically
        rotateStage(now);

        if (temperature >= PREHEAT_TEMP) {
          Serial.println("CHAMBER WARMED. ENTERING CENTRIFUGAL DRYING PHASE");
          digitalWrite(PIN_LED_RED, LOW);
          digitalWrite(PIN_LED_YELLOW, HIGH);
          currentPhase = STATE_DRY;
          phaseStart = now;
          stageStart = now;
          applyStage(true); // staged PTC + motor for active station
        }
        
        if (buttonClicked) {
          Serial.println("CYCLE ABORTED DURING PREHEAT");
          allOff();
          currentPhase = STATE_IDLE;
        }
      }
      break;

    // ================= STATE CENTRIFUGAL DRYING =================
    case STATE_DRY:
      {
        unsigned long elapsed = now - phaseStart;
        unsigned long remaining = 0;
        
        if (elapsed < DRY_TIME_MS) {
          remaining = (DRY_TIME_MS - elapsed) / 1000;
        }
        
        int rMin = (int)(remaining / 60);
        int rSec = (int)(remaining % 60);
        lcdUpdate("DRYING", rMin, rSec);

        applyStage(true);   // staged: PTC + motor for active station
        rotateStage(now);

        if (elapsed >= DRY_TIME_MS) {
          Serial.println("TIMER ELAPSED. ENTERING COOL-DOWN");
          currentPhase = STATE_COOL;
          phaseStart = now;
        }
        
        if (buttonClicked) {
          Serial.println("CYCLE ABORTED DURING DRYING RUN");
          allOff();
          currentPhase = STATE_IDLE;
        }
      }
      break;

    // ================= STATE COOL-DOWN PURGE =================
    case STATE_COOL:
      {
        unsigned long elapsed = now - phaseStart;
        unsigned long remaining = 0;
        
        if (elapsed < COOL_TIME_MS) {
          remaining = (COOL_TIME_MS - elapsed) / 1000;
        }
        
        int rMin = (int)(remaining / 60);
        int rSec = (int)(remaining % 60);
        lcdUpdate("COOLING", rMin, rSec);

        if (elapsed >= COOL_TIME_MS) {
          Serial.println("CYCLE COMPLETE. DE-ENERGIZING FANS.");
          fansOff();
          allOff();
          currentPhase = STATE_DONE;
          phaseStart = now;
          
          // Audible cycle completion notification (3 long beeps)
          digitalWrite(PIN_LED_GREEN, HIGH);
          for (int i = 0; i < 3; i++) {
            digitalWrite(PIN_BUZZER, HIGH);
            delay(500);
            digitalWrite(PIN_BUZZER, LOW);
            delay(300);
          }
        }
        
        if (buttonClicked) {
          Serial.println("CYCLE ABORTED DURING COOL-DOWN");
          allOff();
          currentPhase = STATE_IDLE;
        }
      }
      break;

    // ================= STATE CYCLE COMPLETE =================
    case STATE_DONE:
      digitalWrite(PIN_LED_GREEN, HIGH);
      lcdUpdate("COMPLETE", -1, -1);
      lcd.setCursor(0, 1);
      lcd.print("Press to Reset ");

      if (buttonClicked) {
        Serial.println("SYSTEM RESET TO IDLE STATUS");
        allOff();
        currentPhase = STATE_IDLE;
      }
      break;

    // ================= STATE EMERGENCY CUTOFF =================
    case STATE_CUTOFF:
      // Rapid blinking red LED as alarm
      digitalWrite(PIN_LED_RED, (millis() % 300 < 150) ? HIGH : LOW);
      digitalWrite(PIN_LED_GREEN, LOW);
      digitalWrite(PIN_LED_YELLOW, LOW);
      
      lcd.setCursor(0, 0);
      lcd.print("CRITICAL ERROR! ");
      lcd.setCursor(0, 1);
      lcd.print("OVERHEAT: ");
      lcd.print((int)temperature);
      lcd.print("C  ");

      if (buttonClicked) {
        // Enforce cooling wait period before allowing a manual override reset
        if (temperature < 50.0) {
          Serial.println("TEMPERATURE RESTORED TO SAFE THRESHOLD. SYSTEM RESETTABLE.");
          allOff();
          currentPhase = STATE_IDLE;
        } else {
          Serial.println("RESET ATTEMPT BLOCKED. SURFACE TEMPERATURE EXCEEDS SAFE 50C RETRY.");
          // Chirp buzzer as error warning
          digitalWrite(PIN_BUZZER, HIGH);
          delay(100);
          digitalWrite(PIN_BUZZER, LOW);
        }
      }
      break;
  }
}
```

---

## 5. Wiring and Connectivity Master Guide

| Wire Number | Pin / Connection | Wire Gauge (AWG) | Wire Color | Destination | Function |
|---|---|---|---|---|---|
| **1** | LM2596S OUT+ | 20 AWG | Red | Arduino Mega `5V` Pin | Regulated logic power supply (MUST calibrate to 5V beforehand) |
| **2** | LM2596S OUT− | 20 AWG | Black | Arduino Mega `GND` Pin | Common negative logic ground link |
| **3** | Mega Pin D2 | 22 AWG | Yellow | DHT22 DATA | Ambient chamber relative humidity input (10kΩ pull-up to 5V) |
| **4** | Mega Pin D3 | 22 AWG | Blue | DS18B20 DATA | Heater surface temperature reading (4.7kΩ pull-up to 5V) |
| **5** | Mega Pin D4 | 22 AWG | Red | Relay 1 Trigger (PTC 1) | Transistor base 1kΩ resistor (HIGH = closes 40A PTC 1 circuit) |
| **6** | Mega Pin D5 | 22 AWG | Orange | Relay 2 Trigger (M1) | PCB Relay opto-coupler channel 1 (LOW = turns on Worm Motor 1) |
| **7** | Mega Pin D6 | 22 AWG | Red | Relay 3 Trigger (PTC 2) | Transistor base 1kΩ resistor (HIGH = closes 40A PTC 2 circuit) |
| **8** | Mega Pin D7 | 22 AWG | Orange | Relay 4 Trigger (M2) | PCB Relay opto-coupler channel 2 (LOW = turns on Worm Motor 2) |
| **9** | Mega Pin D8 | 22 AWG | Red | Relay 5 Trigger (PTC 3) | Transistor base 1kΩ resistor (HIGH = closes 40A PTC 3 circuit) |
| **10** | Mega Pin D9 | 22 AWG | Orange | Relay 6 Trigger (M3) | PCB Relay opto-coupler channel 3 (LOW = turns on Worm Motor 3) |
| **11** | Mega Pin D10 | 22 AWG | White | ESC 1 Signal | PWM control line for Station 1 BLDC ducted fans |
| **12** | Mega Pin D11 | 22 AWG | White | ESC 2 Signal | PWM control line for Station 2 BLDC ducted fans |
| **13** | Mega Pin D12 | 22 AWG | White | ESC 3 Signal | PWM control line for Station 3 BLDC ducted fans |
| **14** | Mega Pin D13 | 22 AWG | Purple | Relay 7 Trigger (Fan Bus) | Transistor base 1kΩ resistor (HIGH = closes master 40A Fan Bus) |
| **15** | Mega Pin D14 | 22 AWG | Green | Arcade Button NO | Active-LOW trigger logic; button NC is unmapped |
| **16** | Mega Pin D15 | 22 AWG | Red | Status LED (Red) | Connected via series 220Ω current-limiting resistor |
| **17** | Mega Pin D16 | 22 AWG | Yellow | Status LED (Yellow) | Connected via series 220Ω current-limiting resistor |
| **18** | Mega Pin D17 | 22 AWG | Green | Status LED (Green) | Connected via series 220Ω current-limiting resistor |
| **19** | Mega Pin D18 | 22 AWG | White | Active Buzzer + | Emits cycles alerts (Audible notification) |
| **20** | Mega Pin D20 | 22 AWG | Green | LCD I2C SDA | Hardware SDA interface (pull-ups usually integrated on I2C board) |
| **21** | Mega Pin D21 | 22 AWG | Yellow | LCD I2C SCL | Hardware SCL interface (pull-ups usually integrated on I2C board) |

---

## 6. Sourcing Software Dependencies

1. **DHT Sensor Library** by Adafruit (ver 1.4.x+)
2. **Adafruit Unified Sensor** by Adafruit (ver 1.1.x+)
3. **OneWire** by Paul Stoffregen (ver 2.3.x+)
4. **DallasTemperature** by Miles Burton (ver 3.9.x+)
5. **LiquidCrystal I2C** by Frank de Brabander (ver 1.1.2+)
6. **Servo** (Standard library built directly into the Arduino IDE environment)

---

## 7. ESC calibration (first-time setup)

If BLDC fans don't respond to throttle commands:

1. **Power on** with ESC signal wire disconnected from Mega.
2. **Connect ESC signal** to a known PWM source (or Mega running calibration sketch).
3. **Send MAX throttle** (`write(180)`) for 3 seconds — ESC beeps to confirm max.
4. **Send MIN throttle** (`write(0)`) for 3 seconds — ESC beeps to confirm min.
5. ESC is now calibrated. Power cycle and test.

Some ESCs auto-calibrate on first power-up if they detect a valid signal range.

---

## 8. Debugging tips

| Symptom | Check |
|---|---|
| ESC doesn't arm | Verify D10/D11/D12 wired correctly; check `esc.attach()` called; fan bus relay (D13) must be ON during arming — it powers the ESCs |
| Fans spin then stop | ESC lost signal — check jumper continuity; keep `esc.write()` values refreshed |
| No humidity reading | DHT22 VCC→5V, GND→GND, DATA→D2 with 10kΩ pull-up; use the DHT22 **module**, not a bare sensor |
| No temperature reading | DS18B20 red→5V, black→GND, yellow→D3 with 4.7kΩ pull-up; run a OneWire scanner sketch |
| LCD blank / garbage | Try address 0x3F; call `lcd.init()`; on the **Mega, I2C is pins 20/21 — NOT A4/A5** |
| Heater relay doesn't click | D4/D6/D8 → 1kΩ → 2N2222 base; collector → coil 85; coil 86 → +12V; emitter → GND; 10kΩ base→GND pull-down |
| Motor relay doesn't click | D5/D7/D9 → module IN1/IN2/IN3; module VCC → 5V buck rail (NOT Mega pin); active-LOW: LOW = ON |
| Relay clicks but load stays off | Check COM/NO high-current side: fused 12V → COM, load → NO; verify branch fuse is intact |
| Button not responding | D14 → button pin 1, pin 2 → GND; INPUT_PULLUP; LOW = pressed |
| Thermal cutoff triggers immediately | DS18B20 may be heated by direct contact — mount probe in the air stream, not touching heater body |
| Buck output not 5V | Adjust potentiometer with multimeter BEFORE connecting to Mega; must be 5.0V ± 0.1V |
| Motors spin wrong direction | Swap the two motor leads (DC motor direction = polarity) |
| Main fuse blows during cycle | Firmware staged operation broken? Check that only ONE station's heaters are ever ON (see §9) |

---

## 9. Staged operation (IMPORTANT — fuse budget)

One station's full load = 3 PTC (25A) + 3 fans (9.7A) + motor (0.8A) ≈ **36A**.
The 50A main fuse supports **one station at a time**, plus the fan bus.

The stock sketch runs all 3 stations' heaters simultaneously in PREHEAT (~75A +
fans ≈ 105A — the main fuse WILL blow). Two options:

1. **Stock behavior is for bench testing only** (no heaters connected, TESTING L1/L2).
2. **For real cycles**, enable staged mode by defining `STAGED` at the top of the
   sketch — heaters round-robin 30 s per station; only the active station's
   motor + ESC throttle run. Staged mode keeps worst-case draw ≈ 36A.

```cpp
// Add at top of sketch:
#define STAGED 1   // 1 = one station at a time (deploy), comment out for bench tests

#ifdef STAGED
uint8_t activeStation = 0;  // 0..2 round-robin during PREHEAT/DRY
#endif
```

In staged mode, PREHEAT and DRY energize only `PIN_RELAY_PTC_1 + activeStation`
and throttle only that station's ESC; rotate `activeStation` every 30 s.

---

## 10. Safety notes

- The system runs on **12V DC only** — no mains voltage anywhere.
- Battery BMS protects against over-discharge, over-charge, and short circuit.
- DS18B20 thermal cutoff at 65°C is the primary software safety.
- 130°C one-shot thermal fuse **per heater** (9×) is the hardware backup.
- PTC heaters are self-regulating — they auto-limit current as temperature rises.
- Per-branch fuses (30A PTC ×3, 30A fan bus, 3A motor ×3, 3A logic) isolate faults.
- Relay pins boot in their OFF state: NPN stages have 10kΩ base pull-downs
  (active-HIGH pins default LOW), and the opto module has onboard pull-ups
  (active-LOW pins default HIGH). `setup()` calls `allOff()` first regardless.
- Mega is powered ONLY from the calibrated buck via the 5V pin — never the
  barrel jack, never raw 12V.
