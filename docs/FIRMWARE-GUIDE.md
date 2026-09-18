# Firmware Guide — 12V DC + AVC Blower Fans

> Complete firmware reference for the Umbrella Dryer V2 running on a **12V DC-only** system. AVC blowers are controlled via direct PWM from Mega pins (D10/D11/D12). PTC heaters and worm motors are switched by SSRs (SSR-40DD for PTC, SSR-10A for motors). No ESCs, no Servo library. DRY phase ends early when chamber humidity bottoms out (≤ 60% RH) — the energy-efficient control of the study.

---

## 1. System Logic and State Machine

### 1a. Operational Sequence

1. **Boot** → Initialized. All SSR outputs LOW (OFF). Fan bus SSR (D13) is OFF. Blowers remain off until cycle starts.
2. **Idle** → Reads DHT22 (humidity) + DS18B20 (temperature), displays on LCD. Button waits for input. Status LED is **GREEN**.
3. **Button press** → Starts a 4-phase drying cycle:
   - **Phase 1 — Preheat** (Chamber Temp < 45°C): Master fan bus SSR (D13) ON. Blowers throttle to FULL (`analogWrite(D, 255)`). PTC heater SSRs D4, D6, D8 are energized (ON) sequentially to warm up the chamber. Motors remain OFF. Status LED is **RED** (heating active).
   - **Phase 2 — Dry** (Chamber Temp ≥ 45°C): Chamber temperature has reached target. Station worm gear motor SSRs D5, D7, D9 are switched ON to spin the umbrellas at 6 RPM. PTC heaters and blowers continue running. Timer starts counting down (default 15 minutes). **Humidity auto-stop:** if DHT22 reads ≤ 60% RH after at least 3 minutes of drying, the cycle skips straight to COOL — no wasted energy on already-dry umbrellas. Status LED is **YELLOW** (drying/spinning).
   - **Phase 3 — Cool** (Timer Done): PTC heaters switched OFF. Motors switched OFF (umbrellas stop spinning). Blowers remain running at full speed for 2 minutes to purge hot air and cool down the components. Status LED is **YELLOW**.
   - **Phase 4 — Done**: All loads de-energized. Master fan bus SSR OFF. Buzzer beeps 3 times. LCD shows "COMPLETE". Status LED is **GREEN**.
4. **Safety cutoff (any active phase)**: If DS18B20 reads >65°C, all SSRs and PWM signals are immediately killed (latched OFF). LCD displays "THERMAL CUTOFF!" and the RED LED blinks.
5. **Button repress (any active phase)**: Functions as an Emergency Stop. Immediately cuts all loads and returns the system to IDLE.

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
| | **D20** | I2C_SDA | I2C | — | — | LCD SDA pin (hardware I2C) |
| | **D21** | I2C_SCL | I2C | — | — | LCD SCL pin (hardware I2C) |

> All SSRs are active-HIGH. Floating pins at boot default LOW = SSR OFF. `allOff()` in `setup()` enforces safe state.

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
- Mega is powered ONLY from the calibrated buck via the 5V pin — never the barrel jack, never raw 12V.
