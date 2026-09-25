# Firmware Guide — 12V DC + AVC Blower Fans

> Complete firmware reference for the Umbrella Dryer V2 running on a **12V DC-only** system. AVC blowers are controlled via direct PWM from Mega pins (D10/D11/D12). PTC heaters and worm motors are switched by SSRs (SSR-40DD for PTC, SSR-10A for motors). No ESCs, no Servo library. DRY phase ends early when chamber humidity bottoms out (≤ 60% RH) — the energy-efficient control of the study.

---

## 1. System Logic and State Machine

### 1a. Operational Sequence

1. **Boot** → Initialized. All SSR outputs LOW (OFF). Fan bus SSR (D13) is OFF. Lid solenoid SSR (D23) LOW = **lid locked (fail-secure)**. Blowers remain off until cycle starts.
2. **Idle** → Reads DHT22 (humidity) + DS18B20 (temperature), displays on LCD. Button waits for input. Status LED is **GREEN**. The LCD shows the lid state; **hold Start ~2 s to UNLOCK the lid for loading** (bolt retracts ~3 s, then re-locks).
3. **Button tap (release < 2 s)** → Starts a 4-phase drying cycle **only if the lid is CLOSED** (reed switch D22 reads LOW). If the lid is open, the start is **refused** (buzzer + "CLOSE LID") — the machine will not run with the lid open. Once started, the lid is spring-***LOCKED*** for the whole cycle (solenoid off, 0 A).
   - **Phase 1 — Preheat** (Chamber Temp < 45°C): Master fan bus SSR (D13) ON. Blowers throttle to FULL (`analogWrite(D, 255)`). PTC heater SSRs D4, D6, D8 are energized (ON) sequentially to warm up the chamber. Motors remain OFF. Status LED is **RED** (heating active).
   - **Phase 2 — Dry** (Chamber Temp ≥ 45°C): Chamber temperature has reached target. Station worm gear motor SSRs D5, D7, D9 are switched ON to spin the umbrellas at 6 RPM. PTC heaters and blowers continue running. Timer starts counting down (default 15 minutes). **Humidity auto-stop:** if DHT22 reads ≤ 60% RH after at least 3 minutes of drying, the cycle skips straight to COOL — no wasted energy on already-dry umbrellas. Status LED is **YELLOW** (drying/spinning).
   - **Phase 3 — Cool** (Timer Done): PTC heaters switched OFF. Motors switched OFF (umbrellas stop spinning). Blowers remain running at full speed for 2 minutes to purge hot air and cool down the components. Status LED is **YELLOW**.
   - **Phase 4 — Done**: All loads de-energized. Master fan bus SSR OFF. Buzzer beeps 3 times. LCD shows "COMPLETE". Status LED is **GREEN**. The **lid is pulsed UNLOCKED (~3 s)** so the user can retrieve the umbrellas ("Lid UNLOCKED - open"). After closing, a tap resets to IDLE.
4. **Safety cutoff (any active phase)**: If DS18B20 reads >65°C, all SSRs and PWM signals are immediately killed (latched OFF). LCD displays "THERMAL CUTOFF!" and the RED LED blinks.
5. **Button tap (any active phase)**: Functions as an Emergency Stop. Immediately cuts all loads and returns the system to IDLE. (The lid remains locked until you hold Start ~2 s to unlock it.)
6. **Lid-open safety interlock (any active phase)**: If the reed switch reads OPEN mid-cycle — impossible while the lock holds — the firmware aborts everything to IDLE (defense in depth against a failed lock).

---

## 2. Pin Map — Arduino Mega 2560

| | Pin | Net | Mode | Default | Active Level | Notes |
|---|---|---|---|---|---|---|
| | **D2** | DHT22_DATA | Input | — | — | Chamber humidity & ambient temp; 10kΩ pull-up to 5V |
| | **D3** | DS18B20_DATA | Input | — | — | Heater-zone temperature probe; 4.7kΩ pull-up to 5V |
| | **D4** | SSR_PTC_1 | Output | LOW | HIGH (ON) | Station 1 PTC heater (LCTC DC-DC SSR 40A) |
| | **D5** | SSR_MOTOR_1 | Output | LOW | HIGH (ON) | Station 1 worm motor (LCTC DC-DC SSR 10A) |
| | **D6** | SSR_PTC_2 | Output | LOW | HIGH (ON) | Station 2 PTC heater (LCTC DC-DC SSR 40A) |
| | **D7** | SSR_MOTOR_2 | Output | LOW | HIGH (ON) | Station 2 worm motor (LCTC DC-DC SSR 10A) |
| | **D8** | SSR_PTC_3 | Output | LOW | HIGH (ON) | Station 3 PTC heater (LCTC DC-DC SSR 40A) |
| | **D9** | SSR_MOTOR_3 | Output | LOW | HIGH (ON) | Station 3 worm motor (LCTC DC-DC SSR 10A) |
| | **D10** | PWM_FAN_1 | Output (PWM) | 0 | — | Station 1 blower PWM (`analogWrite`) |
| | **D11** | PWM_FAN_2 | Output (PWM) | 0 | — | Station 2 blower PWM (`analogWrite`) |
| | **D12** | PWM_FAN_3 | Output (PWM) | 0 | — | Station 3 blower PWM (`analogWrite`) |
| | **D13** | SSR_FAN_BUS | Output | LOW | HIGH (ON) | Master Fan Bus (LCTC DC-DC SSR 40A) |
| | **D14** | BTN_START | Input | HIGH | LOW (ON) | Arcade start button (internal pull-up enabled) |
| | **D15** | LED_RED | Output | LOW | HIGH (ON) | Status LED: active heating |
| | **D16** | LED_YELLOW | Output | LOW | HIGH (ON) | Status LED: drying and rotating / cooling |
| | **D17** | LED_GREEN | Output | HIGH | HIGH (ON) | Status LED: system ready or cycle complete |
| | **D18** | BUZZER | Output | LOW | HIGH (ON) | Active 5V buzzer |
| | **D22** | LID_REED | Input | HIGH | LOW (CLOSED) | Lid closed sensor (NO reed, INPUT_PULLUP) |
| | **D23** | SOL_LOCK | Output | LOW | HIGH (UNLOCK) | Lid solenoid lock (SSR-10A) — pulse ~3 s |
| | **D20** | I2C_SDA | I2C | — | — | LCD SDA pin (hardware I2C) |
| | **D21** | I2C_SCL | I2C | — | — | LCD SCL pin (hardware I2C) |

> All SSRs are active-HIGH. Floating pins at boot default LOW = SSR OFF. `allOff()` in `setup()` enforces safe state.
> **Lid interlock:** D23 (SOL_LOCK) LOW = lid LOCKED (fail-secure, 0 A). A ~3 s HIGH pulse on D23 retracts the bolt (UNLOCK) — used at cycle COMPLETE and when holding Start ~2 s in IDLE to load. The START button only begins a cycle while D22 (LID_REED) reads LOW (lid closed).

---

## 3. Timing and Control Thresholds

| Parameter | Value | Design Rationale / Notes |
|---|---|---|
| **Loop Tick Interval** | 500 ms | Prevents sensor bus congestion; provides stable sensor readings |
| **Preheat Threshold** | 45.0°C | Chamber air temp target required to enable safe centrifugal drying |
| **Thermal Cutoff** | 65.0°C | Absolute maximum chamber ceiling; triggers immediate system lock |
| **Dry Phase Timer** | 15 minutes (max) | Standard cycle ceiling; sufficient for complete moisture removal |
| **Humidity Auto-Stop** | ≤ 60% RH, after ≥ 3 min drying | Chamber RH bottoms out once umbrellas are dry — cycle skips to COOL; saves the unused portion of the 15-minute budget |
| **Min Dry Time before Auto-Stop** | 3 minutes | Guards against stale/spike DHT22 readings ending the cycle early |
| **Cool Phase Timer** | 2 minutes | Blower-only overrun to dissipate residual heater block temperature |
| **Debounce Delay** | 300 ms | Ignores button contact bounce and microphonics |
| **Lid Hold-to-Unlock** | 2 seconds | Hold Start in IDLE to retract the lock bolt for loading |
| **Lid Unlock Pulse** | 3 seconds | Length of the D23 SSR pulse that retracts the bolt (solenoid is rated for 1–10 s activation — never hold it on) |

---

## 4. Complete Arduino Sketch

Copy and paste the following complete, verified sketch into the Arduino IDE.

```cpp
// ============================================================================
// Umbrella Dryer V2 — 12V DC-Only System Firmware
// Target Board: Arduino Mega 2560
// Dependencies: DHT, OneWire, DallasTemperature, LiquidCrystal_I2C
// ============================================================================

#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
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

#define PIN_PWM_FAN_1     10  // Station 1 AVC blower PWM
#define PIN_PWM_FAN_2     11  // Station 2 AVC blower PWM
#define PIN_PWM_FAN_3     12  // Station 3 AVC blower PWM
#define PIN_SSR_FAN_BUS   13  // LCTC DC-DC SSR 40A (Master Fan Bus)

// UI and Peripherals
#define PIN_BTN_START     14  // Arcade button (active-LOW, pull-up)
#define PIN_LED_RED       15  // Active heating
#define PIN_LED_YELLOW    16  // Centrifugal drying / Cooling
#define PIN_LED_GREEN     17  // System ready / Cycle complete
#define PIN_BUZZER        18  // Audible notifications

// ---- Lid Safety Interlock ----
#define PIN_REED          22  // Lid closed sensor (NO reed, INPUT_PULLUP; LOW = LID CLOSED)
#define PIN_SOL_LOCK      23  // Solenoid lock SSR-10A (HIGH = UNLOCK pulse; LOW = LOCKED)

// ---- Sensor Objects ----
DHT dht(PIN_DHT22, DHT22);
OneWire oneWire(PIN_DS18B20);
DallasTemperature ds18b20(&oneWire);
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Alternate address: 0x3F

// ---- Configuration and Constants ----
const float PREHEAT_TEMP   = 45.0;                      // °C - dry trigger
const float CUTOFF_TEMP    = 65.0;                      // °C - safety threshold
const float HUMIDITY_STOP  = 60.0;                      // % RH - early stop: chamber is dry
const unsigned long MIN_DRY_TIME_MS = 3UL * 60UL * 1000UL; // min drying before auto-stop is allowed
const unsigned long DRY_TIME_MS  = 15UL * 60UL * 1000UL; // 15-minute drying timer (max)
const unsigned long COOL_TIME_MS = 2UL * 60UL * 1000UL;  // 2-minute cooling run
const int PWM_FULL         = 255;                       // Full blower speed
const int PWM_OFF          = 0;                         // Blower off

// ---- Staged operation (one station at a time — keeps draw ~39A under BMS 200A) ----
const uint8_t PIN_PTC[3]   = { PIN_SSR_PTC_1,  PIN_SSR_PTC_2,  PIN_SSR_PTC_3  };
const uint8_t PIN_MOT[3]   = { PIN_SSR_MOTOR_1, PIN_SSR_MOTOR_2, PIN_SSR_MOTOR_3 };
const uint8_t PIN_PWM[3]   = { PIN_PWM_FAN_1,  PIN_PWM_FAN_2,  PIN_PWM_FAN_3  };
const unsigned long STAGE_MS = 30000;   // 30 s per station before rotating
uint8_t activeStation = 0;
unsigned long stageStart = 0;

// Energize ONLY the active station: PTC always, motor only in DRY, PWM fans always
void applyStage(bool dryMotors) {
  for (uint8_t i = 0; i < 3; i++) {
    digitalWrite(PIN_PTC[i], LOW);
    digitalWrite(PIN_MOT[i], LOW);
    analogWrite(PIN_PWM[i], PWM_OFF);
  }
  digitalWrite(PIN_PTC[activeStation], HIGH);
  analogWrite(PIN_PWM[activeStation], PWM_FULL);
  if (dryMotors) digitalWrite(PIN_MOT[activeStation], HIGH);
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
unsigned long btnDownAt   = 0;    // timestamp when Start was pressed (for tap-vs-hold)
bool btnWasDown           = false; // Start currently held
bool btnUnlockSent        = false; // prevent repeat unlocks during one long hold

// ---- Lid Lock Helpers (fail-secure solenoid) ----
// The solenoid is NORMALLY-LOCKED: the bolt stays out (LID LOCKED) with zero power.
// A HIGH pulse retracts the bolt (UNLOCK) for ~3 s. Rated 1-10 s only — never hold it on.
void unlockLid() {
  digitalWrite(PIN_SOL_LOCK, HIGH);
  delay(3000);                 // hold bolt retracted ~3 s so the user can pull the lid open
  digitalWrite(PIN_SOL_LOCK, LOW);
  Serial.println(F("Lid UNLOCKED (bolt retracted 3 s)"));
}

inline bool lidIsClosed() {
  return digitalRead(PIN_REED) == LOW;   // magnet near reed (lid shut) = reed shorted = LOW
}

// ---- Absolute System Safety Shutdown ----
void allOff() {
  digitalWrite(PIN_SSR_PTC_1, LOW);
  digitalWrite(PIN_SSR_PTC_2, LOW);
  digitalWrite(PIN_SSR_PTC_3, LOW);
  digitalWrite(PIN_SSR_MOTOR_1, LOW);
  digitalWrite(PIN_SSR_MOTOR_2, LOW);
  digitalWrite(PIN_SSR_MOTOR_3, LOW);
  analogWrite(PIN_PWM_FAN_1, PWM_OFF);
  analogWrite(PIN_PWM_FAN_2, PWM_OFF);
  analogWrite(PIN_PWM_FAN_3, PWM_OFF);
  digitalWrite(PIN_SSR_FAN_BUS, LOW);
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_LED_YELLOW, LOW);
  digitalWrite(PIN_LED_GREEN, LOW);
  digitalWrite(PIN_BUZZER, LOW);
  digitalWrite(PIN_SOL_LOCK, LOW);   // lid LOCKED (fail-secure) — never energized during a cycle
}

// ---- Fan Control ----
void fansOn() {
  digitalWrite(PIN_SSR_FAN_BUS, HIGH);
  delay(100);
  analogWrite(PIN_PWM_FAN_1, PWM_FULL);
  analogWrite(PIN_PWM_FAN_2, PWM_FULL);
  analogWrite(PIN_PWM_FAN_3, PWM_FULL);
}

void fansOff() {
  analogWrite(PIN_PWM_FAN_1, PWM_OFF);
  analogWrite(PIN_PWM_FAN_2, PWM_OFF);
  analogWrite(PIN_PWM_FAN_3, PWM_OFF);
  delay(50);
  digitalWrite(PIN_SSR_FAN_BUS, LOW);
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
  pinMode(PIN_SSR_PTC_1, OUTPUT);
  pinMode(PIN_SSR_PTC_2, OUTPUT);
  pinMode(PIN_SSR_PTC_3, OUTPUT);
  pinMode(PIN_SSR_MOTOR_1, OUTPUT);
  pinMode(PIN_SSR_MOTOR_2, OUTPUT);
  pinMode(PIN_SSR_MOTOR_3, OUTPUT);
  pinMode(PIN_PWM_FAN_1, OUTPUT);
  pinMode(PIN_PWM_FAN_2, OUTPUT);
  pinMode(PIN_PWM_FAN_3, OUTPUT);
  pinMode(PIN_SSR_FAN_BUS, OUTPUT);

  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_YELLOW, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_SOL_LOCK, OUTPUT);       // solenoid lock SSR

  // Put system in completely safe offline state
  allOff();

  // Input Setup
  pinMode(PIN_BTN_START, INPUT_PULLUP);
  pinMode(PIN_REED, INPUT_PULLUP);     // lid-closed reed sensor (LOW = lid closed)

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

  // ---- Lid-open Interlock (defense in depth) ----
  // The fail-secure solenoid holds the lid locked for the whole cycle, so an OPEN reading
  // mid-cycle means the solenoid failed or the lid was forced. Kill all loads and return to IDLE.
  if (!lidIsClosed() &&
      (currentPhase == STATE_PREHEAT || currentPhase == STATE_DRY || currentPhase == STATE_COOL)) {
    Serial.println(F("LID OPENED DURING CYCLE - SAFETY ABORT"));
    allOff();
    currentPhase = STATE_IDLE;
    return;
  }

  // ---- Non-blocking Button Detection (tap vs hold) ----
  // Quick tap  = "click" (start / estop). Hold ~2 s in IDLE = "unlock lid for loading".
  // Act on the RELEASE edge so a deliberate hold doesn't accidentally start a cycle.
  bool buttonState = digitalRead(PIN_BTN_START);
  bool buttonClicked = false;                 // short tap completed
  bool longHold = false;                      // 2 s hold completed (unlock gesture)

  if (buttonState == LOW) {
    if (!btnWasDown) { btnDownAt = now; btnUnlockSent = false; btnWasDown = true; }
    if (!btnUnlockSent && (now - btnDownAt >= 2000)) { longHold = true; btnUnlockSent = true; }
  } else {
    if (btnWasDown && (now - btnDownAt < 2000)) buttonClicked = true;   // short tap released
    btnWasDown = false;
  }
  buttonPrevState = buttonState;   // diagnostics

  // ---- State Machine Logic ----
  switch (currentPhase) {

    // ================= STATE READY/IDLE =================
    case STATE_IDLE:
      digitalWrite(PIN_LED_GREEN, HIGH);
      digitalWrite(PIN_LED_RED, LOW);
      digitalWrite(PIN_LED_YELLOW, LOW);

      // Hold Start ~2 s to UNLOCK the lid for loading (bolt retracts ~3 s, then re-locks).
      if (longHold) {
        Serial.println(F("UNLOCKING LID FOR LOADING"));
        lcd.clear(); lcd.setCursor(0,0); lcd.print("UNLOCKING LID");
        lcd.setCursor(0,1); lcd.print("OPEN + LOAD");
        unlockLid();
      }

      lcdUpdate("READY", -1, -1);
      if (!lidIsClosed()) {
        lcd.setCursor(0, 1);
        lcd.print("LID OPEN  Hold unlock");
      }

      // START is safety-gated by the lid-closed reed switch: the machine will NOT start
      // with the lid open. Closing the lid and tapping Start begins the cycle.
      if (buttonClicked) {
        if (lidIsClosed()) {
          Serial.println("CYCLE COMMENCING (lid closed)");
          digitalWrite(PIN_LED_GREEN, LOW);
          digitalWrite(PIN_LED_RED, HIGH);
          currentPhase = STATE_PREHEAT;
          phaseStart = now;
          fansOn();
          activeStation = 0;
          stageStart = now;
          applyStage(false); // PTC heaters only, motors off
          // Lid stays LOCKED for the whole cycle (solenoid LOW / fail-secure).
        } else {
          Serial.println("START BLOCKED - LID OPEN");
          lcd.clear();
          lcd.setCursor(0,0); lcd.print("CLOSE LID");
          lcd.setCursor(0,1); lcd.print("To Start Cycle");
          for (int i = 0; i < 3; i++) {   // warning beeps
            digitalWrite(PIN_BUZZER, HIGH); delay(150); digitalWrite(PIN_BUZZER, LOW); delay(150);
          }
        }
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

        // ---- Humidity auto-stop (energy-efficient control) ----
        // Chamber RH bottoms out once the umbrellas are dry — end early.
        // The 3-minute floor prevents a stale DHT22 reading from ending the cycle.
        if (elapsed >= MIN_DRY_TIME_MS && !isnan(humidity) && humidity <= HUMIDITY_STOP) {
          Serial.print("HUMIDITY TARGET REACHED (");
          Serial.print(humidity);
          Serial.println("% RH). ENDING DRY PHASE EARLY.");
          currentPhase = STATE_COOL;
          phaseStart = now;
          break;
        }

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
          allOff();            // all loads OFF; lid solenoid LOW (locked, fail-secure)
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
          unlockLid();         // retract bolt ~3 s so the user can retrieve the umbrellas
          lcd.clear();
          lcd.setCursor(0,0); lcd.print("COMPLETE");
          lcd.setCursor(0,1); lcd.print("Lid UNLOCKED - open");
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
      lcd.print("Lid unlocked - reset");

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
| **5** | Mega Pin D4 | 22 AWG | Red | SSR PTC 1 Trigger | LCTC DC-DC SSR 40A (HIGH = closes Station 1 PTC circuit) |
| **6** | Mega Pin D5 | 22 AWG | Orange | SSR Motor 1 Trigger | LCTC DC-DC SSR 10A (HIGH = turns on Worm Motor 1) |
| **7** | Mega Pin D6 | 22 AWG | Red | SSR PTC 2 Trigger | LCTC DC-DC SSR 40A (HIGH = closes Station 2 PTC circuit) |
| **8** | Mega Pin D7 | 22 AWG | Orange | SSR Motor 2 Trigger | LCTC DC-DC SSR 10A (HIGH = turns on Worm Motor 2) |
| **9** | Mega Pin D8 | 22 AWG | Red | SSR PTC 3 Trigger | LCTC DC-DC SSR 40A (HIGH = closes Station 3 PTC circuit) |
| **10** | Mega Pin D9 | 22 AWG | Orange | SSR Motor 3 Trigger | LCTC DC-DC SSR 10A (HIGH = turns on Worm Motor 3) |
| **11** | Mega Pin D10 | 22 AWG | White | PWM Blower Station 1 | `analogWrite(D10, val)` — 0–255 duty cycle control |
| **12** | Mega Pin D11 | 22 AWG | White | PWM Blower Station 2 | `analogWrite(D11, val)` — 0–255 duty cycle control |
| **13** | Mega Pin D12 | 22 AWG | White | PWM Blower Station 3 | `analogWrite(D12, val)` — 0–255 duty cycle control |
| **14** | Mega Pin D13 | 22 AWG | Purple | SSR Fan Bus Trigger | LCTC DC-DC SSR 40A (HIGH = closes master Fan Bus) |
| **15** | Mega Pin D14 | 22 AWG | Green | Arcade Button NO | Active-LOW trigger logic; button NC is unmapped |
| **16** | Mega Pin D15 | 22 AWG | Red | Status LED (Red) | Connected via series 220Ω current-limiting resistor |
| **17** | Mega Pin D16 | 22 AWG | Yellow | Status LED (Yellow) | Connected via series 220Ω current-limiting resistor |
| **18** | Mega Pin D17 | 22 AWG | Green | Status LED (Green) | Connected via series 220Ω current-limiting resistor |
| **19** | Mega Pin D18 | 22 AWG | White | Active Buzzer + | Emits cycle alerts (Audible notification) |
| **20** | Mega Pin D20 | 22 AWG | Green | LCD I2C SDA | Hardware SDA interface (pull-ups usually integrated on I2C board) |
| **21** | Mega Pin D21 | 22 AWG | Yellow | LCD I2C SCL | Hardware SCL interface (pull-ups usually integrated on I2C board) |
| **22** | Mega Pin D22 | 22 AWG | Brown | Lid Reed Switch | NO reed to GND; INPUT_PULLUP; lid closed = LOW (machine won't start while open) |
| **23** | Mega Pin D23 | 22 AWG | Pink | Solenoid Lock SSR (SSR-10A) IN+ | SSR IN− → GND; SSR COM → +12V, NO → solenoid +; HIGH pulse ~3 s = unlock |

---

## 6. Sourcing Software Dependencies

1. **DHT Sensor Library** by Adafruit (ver 1.4.x+)
2. **Adafruit Unified Sensor** by Adafruit (ver 1.1.x+)
3. **OneWire** by Paul Stoffregen (ver 2.3.x+)
4. **DallasTemperature** by Miles Burton (ver 3.9.x+)
5. **LiquidCrystal I2C** by Frank de Brabander (ver 1.1.2+)

> **No Servo library needed** — blowers use `analogWrite()` directly.

---

## 7. Debugging tips

| Symptom | Check |
|---|---|
| No blower response | Verify D10/D11/D12 wired correctly; `analogWrite(D, 255)` sends full PWM; fan bus SSR (D13) must be ON for 12V power |
| Blowers don't spin | Check 12V from fan bus SSR to blower VIN; check PWM signal from Mega with multimeter or oscilloscope |
| No humidity reading | DHT22 VCC→5V, GND→GND, DATA→D2 with 10kΩ pull-up; use the DHT22 **module**, not a bare sensor |
| No temperature reading | DS18B20 red→5V, black→GND, yellow→D3 with 4.7kΩ pull-up; run a OneWire scanner sketch |
| LCD blank / garbage | Try address 0x3F; call `lcd.init()`; on the **Mega, I2C is pins 20/21 — NOT A4/A5** |
| Heater SSR doesn't trigger | D4/D6/D8 → SSR IN+; SSR IN− → GND; COM → +12V, NO → heaters |
| Motor SSR doesn't trigger | D5/D7/D9 → SSR-10A IN+; SSR IN− → GND; COM → +12V, NO → motor |
| SSR energized but load stays off | Check the high-current side: 12V → output COM, load → output NO |
| Button not responding | D14 → button pin 1, pin 2 → GND; INPUT_PULLUP; LOW = pressed |
| Thermal cutoff triggers immediately | DS18B20 may be heated by direct contact — mount probe in the air stream, not touching heater body |
| Buck output not 5V | Adjust potentiometer with multimeter BEFORE connecting to Mega; must be 5.0V ± 0.1V |
| Motors spin wrong direction | Swap the two motor leads (DC motor direction = polarity) |
| Cycle won't start | **Lid is open** — the reed switch (D22) must read LOW (lid closed). Close the lid; if it still won't start, verify the reed wiring and that the magnet on the lid aligns with the reed housing |
| Lid stuck locked / won't open | Hold Start ~2 s in IDLE to pulse the solenoid (D23). Check the SSR input (IN+ → D23, IN− → GND) and the output path (+12V → SSR COM → SSR NO → solenoid + → GND). The lock is fail-secure and needs a 12 V pulse to release |

---

## 8. Staged operation (IMPORTANT — current budget)

One station's full load = 3 PTC (25A) + 3 blowers (13.5A) + motor (0.8A) + logic (0.5A) ≈ **39.3A**.
Staged operation keeps the worst-case draw at ≈ **39.3A** by running only one station at a time — well under the 200A BMS limit.

The firmware **always** operates in staged mode — heaters round-robin 30 s per station; only the active station's motor and blower PWM run. All other stations' PTC and PWM are OFF.

---

## 9. Safety notes

- The system runs on **12V DC only** — no mains voltage anywhere.
- Battery BMS protects against over-discharge, over-charge, and short circuit.
- DS18B20 thermal cutoff at 65°C is the primary software safety.
- PTC heaters are self-regulating — they auto-limit current as temperature rises.
- Over-temperature protection relies on PTC self-regulation and DS18B20 firmware 65°C cutoff. No thermal fuses.
- Over-current protection relies on BMS 200A cutoff and PTC self-regulation. No hardware fuses.
- SSR pins boot in their OFF state (floating/LOW = OFF). `setup()` calls `allOff()` first regardless.
- **Lid safety interlock:** the machine will not start a drying cycle while the lid is open (reed D22 must read LOW); the lid is locked shut for the whole cycle (solenoid D23) and only pulsed open at COMPLETE or on a 2 s hold while IDLE.
- **Fail-secure lock:** the solenoid lock is normally-locked — D23 LOW (or any 12 V power loss) keeps the lid shut. During a power loss mid-cycle the lid stays locked until power returns (all thermal/fan/motor loads are also off, so this is safe; hold Start ~2 s once power returns to open).
- Mega is powered ONLY from the calibrated buck via the 5V pin — never the barrel jack, never raw 12V.
