#include <StepMotor.h>
#define STEP4LAP 4095

StepMotor stepper_1(STEP4LAP, 3, 4, 5, 6);
StepMotor stepper_2(STEP4LAP, 8, 9, 10, 11);
StepMotor stepper_3(STEP4LAP, A5, A4, A3, A2);

bool firstRun = true; // loop에서 코드가 한 번만 실행되도록 제어하는 플래그

void setup() {
  Serial.begin(115200);
}

void loop() {

    // stepper_1.step(STEP4LAP);
    // stepper_2.step(STEP4LAP);
    // stepper_3.step(STEP4LAP);
    // delay(2000);
    stepper_1.step(STEP4LAP);
    stepper_2.step(STEP4LAP);
    stepper_3.step(-STEP4LAP);
    delay(2000);


}