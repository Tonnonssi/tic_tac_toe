// Define pins for the stepper motor
#define IN1 3
#define IN2 4
#define IN3 5
#define IN4 6

#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

// Declare global variables
int Steps = 0;
boolean Direction = true;
unsigned long last_time;
unsigned long currentMillis;
int steps_left = 4095;
long time;

void setup() {
    Serial.begin(115200);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
}

void loop() {
    while(steps_left > 0) {
        currentMillis = micros();
        if(currentMillis - last_time >= 800) {
            stepper(1);
            time = time + micros() - last_time;
            last_time = micros();
            steps_left--;
        }
    }
    Serial.println(time);
    Serial.println("Wait...!");
    delay(2000);
    Direction = !Direction;
    steps_left = 4095;
}

// Function to set the step direction based on Direction flag
void SetDirection() {
    if (Direction == 1) {
        Steps++;
    }
    if (Direction == 0) {
        Steps--;
    }
    if (Steps > 7) {
        Steps = 0;
    }
    if (Steps < 0) {
        Steps = 7;
    }
}

// Function to control the stepper motor based on Steps variable
void stepper(int xw) {
    for (int x = 0; x < xw; x++) {
        switch(Steps) {
            case 0:
                digitalWrite(IN1, LOW);  // blue
                digitalWrite(IN2, LOW);  // pink
                digitalWrite(IN3, LOW);  // yellow
                digitalWrite(IN4, HIGH); // orange
                break;
            case 1:
                digitalWrite(IN1, LOW);
                digitalWrite(IN2, LOW);
                digitalWrite(IN3, HIGH);
                digitalWrite(IN4, HIGH);
                break;
            case 2:
                digitalWrite(IN1, LOW);
                digitalWrite(IN2, LOW);
                digitalWrite(IN3, HIGH);
                digitalWrite(IN4, LOW);
                break;
            case 3:
                digitalWrite(IN1, LOW);
                digitalWrite(IN2, HIGH);
                digitalWrite(IN3, HIGH);
                digitalWrite(IN4, LOW);
                break;
            case 4:
                digitalWrite(IN1, LOW);
                digitalWrite(IN2, HIGH);
                digitalWrite(IN3, LOW);
                digitalWrite(IN4, LOW);
                break;
            case 5:
                digitalWrite(IN1, HIGH);
                digitalWrite(IN2, HIGH);
                digitalWrite(IN3, LOW);
                digitalWrite(IN4, LOW);
                break;
            case 6:
                digitalWrite(IN1, HIGH);
                digitalWrite(IN2, LOW);
                digitalWrite(IN3, LOW);
                digitalWrite(IN4, LOW);
                break;
            case 7:
                digitalWrite(IN1, HIGH);
                digitalWrite(IN2, LOW);
                digitalWrite(IN3, LOW);
                digitalWrite(IN4, HIGH);
                break;
            default:
                digitalWrite(IN1, LOW);
        }
        SetDirection();
    }
}