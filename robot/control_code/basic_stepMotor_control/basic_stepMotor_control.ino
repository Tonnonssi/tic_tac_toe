#include <Stepper.h>
#define STEPS 100
Stepper stepper_1(STEPS, 4,3,5,6);
Stepper stepper_2(STEPS, 8,9,10,11);
Stepper stepper_3(STEPS, A5,A3,A4,A2);

int previous = 0;

void setup() {
  pinMode(A3, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);

  stepper_1.setSpeed(200);
  stepper_2.setSpeed(200);
  stepper_3.setSpeed(200);
}

void loop() {
  int val = analogRead(0);

  stepper_1.step(200);
  stepper_2.step(200);
  stepper_3.step(200);

  previous = val;
}
