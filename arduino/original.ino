/* DOCS
 *  
 *  MOTOR - m
 *  > f - Forward
 *  > b - Backward
 *  > * (Any other) - Stop
 *  \ mf - Forward; mb - Backward; ms - Stop
 *  
 *  SERVO - s
 *  > o - Open
 *  > r - Right
 *  > l - Left
 *  >> 1 - Servo №1
 *  >> 2 - Servo №2
 *  >> 3 - Servo №3
 *  \ so1 - Open servo 1; sr1 - Right servo 1; sl1 - Left servo 1; so2 - Open servo 2; sr2 - Right servo 2; sl2 - Left servo 2; so3 - Open servo 3; sr3 - Right servo 3; sl3 - Left servo 3
 */

#include <Servo.h>

/* MOTOR */
#define MOTOR_1_FORWARD_PIN 5
#define MOTOR_1_BACKWARD_PIN 4
#define MOTOR_2_FORWARD_PIN 3
#define MOTOR_2_BACKWARD_PIN 2

#define MOTOR_KEY 109 //m

#define MOTOR_STATE_FORWARD_KEY 102 //f
#define MOTOR_STATE_BACKWARD_KEY 98 //b

/* SERVO */
#define SERVO_1_PIN OUT1
#define SERVO_2_PIN OUT2
#define SERVO_3_PIN OUT3

#define SERVO_KEY 115 //s

#define SERVO_OPEN_KEY 111 //o
#define SERVO_RIGHT_KEY 114 //r
#define SERVO_LEFT_KEY 108 //l

#define SERVO_1_KEY 49 //1
#define SERVO_2_KEY 50 //2
#define SERVO_3_KEY 51 //3

#define SERVO_OPEN_DEGREE 0
#define SERVO_RIGHT_DEGREE 135
#define SERVO_LEFT_DEGREE 45

Servo servo1;
Servo servo2;
Servo servo3;

/* VARIABLES */
int incomingByte = 0;
int mode = 0; //0 = blank; 1 = motor; 2 = servo

int servoState = 0; //SERVO_*_KEY; 0 = blank

void setup() {
  Serial.begin(115200);

  pinMode(MOTOR_1_FORWARD_PIN, OUTPUT);
  pinMode(MOTOR_1_BACKWARD_PIN, OUTPUT);
  pinMode(MOTOR_2_FORWARD_PIN, OUTPUT);
  pinMode(MOTOR_2_BACKWARD_PIN, OUTPUT);

  motor(0);

  servo1.attach(SERVO_1_PIN);
  servo2.attach(SERVO_2_PIN);
  servo3.attach(SERVO_3_PIN);

  servo1.write(SERVO_OPEN_DEGREE);
  servo2.write(180-SERVO_OPEN_DEGREE);
  servo3.write(SERVO_OPEN_DEGREE);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    if (incomingByte != 10) {
      if (!mode) {
        switch (incomingByte) {
          case MOTOR_KEY:
            mode = 1;
            break;
          case SERVO_KEY:
            mode = 2;
            break;
        }
      } else {
        switch (mode) {
          case 1:
            motor(incomingByte);
            mode = 0;
            break;
          case 2:
            if (!servoState)
            {
              servoState = incomingByte;
            } else {
              switch (servoState) {
                case SERVO_OPEN_KEY:
                  switch (incomingByte) {
                    case SERVO_1_KEY:
                      servo1.write(SERVO_OPEN_DEGREE);
                      break;
                    case SERVO_2_KEY:
                      servo2.write(180-SERVO_OPEN_DEGREE);
                      break;
                    case SERVO_3_KEY:
                      servo3.write(SERVO_OPEN_DEGREE);
                      break;
                  }
                  break;
                case SERVO_RIGHT_KEY:
                  switch (incomingByte) {
                    case SERVO_1_KEY:
                      servo1.write(SERVO_RIGHT_DEGREE);
                      break;
                    case SERVO_2_KEY:
                      servo2.write(180-SERVO_LEFT_DEGREE);
                      break;
                    case SERVO_3_KEY:
                      servo3.write(SERVO_RIGHT_DEGREE);
                      break;
                  }
                  break;
                case SERVO_LEFT_KEY:
                  switch (incomingByte) {
                    case SERVO_1_KEY:
                      servo1.write(SERVO_LEFT_DEGREE);
                      break;
                    case SERVO_2_KEY:
                      servo2.write(180-SERVO_RIGHT_DEGREE);
                      break;
                    case SERVO_3_KEY:
                      servo3.write(SERVO_LEFT_DEGREE);
                      break;
                  }
                  break;
              }
              mode = 0;
              servoState = 0;
            }
            break;
        }
      }
    }
  }
}

void motor(int direction)
{
  digitalWrite(MOTOR_1_FORWARD_PIN, LOW);
  digitalWrite(MOTOR_1_BACKWARD_PIN, LOW);
  digitalWrite(MOTOR_2_FORWARD_PIN, LOW);
  digitalWrite(MOTOR_2_BACKWARD_PIN, LOW);
  switch (direction) {
    case MOTOR_STATE_BACKWARD_KEY:
      digitalWrite(MOTOR_1_BACKWARD_PIN, HIGH);
      digitalWrite(MOTOR_2_BACKWARD_PIN, HIGH);
      break;
    case MOTOR_STATE_FORWARD_KEY:
      digitalWrite(MOTOR_1_FORWARD_PIN, HIGH);
      digitalWrite(MOTOR_2_FORWARD_PIN, HIGH);
      break;
  }
}
