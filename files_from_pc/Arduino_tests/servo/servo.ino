#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVO_0  100 // This is the 'minimum' pulse length count (out of 4096)  0 degree
#define SERVO_180  600 // This is the 'maximum' pulse length count (out of 4096)  180 degree
#define SERVO_HALF  300 // 90 degree
#define USMIN  300 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  1200 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

// our servo # counter
uint8_t servonum = 0;

void base_servo(int angle);

void setup() {
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);

  pwm.setPWM(0, 0, SERVO_0);
  pwm.setPWM(1, 0, SERVO_0);
  pwm.setPWM(2, 0, SERVO_0);
  pwm.setPWM(3, 0, SERVO_0);
  //  for (uint16_t microsec = USMAX; microsec > USMIN; microsec--) {
  //    pwm.writeMicroseconds(3, microsec);
  //  }

}
//
//int mapping_degtopl(int angle):
//  int pulse_length = map(angle,0, 180, SERVO0, SERVO180)
//  return pulse_length


void loop() {

  //  Serial.println(servonum);
  //  base_servo(60,0);
  //  delay(500);
  //  base_servo(0,1);
  //  delay(0);

//  pwm.setPWM(1, 0, SERVO_0);
//  delay(500);
//  pwm.setPWM(1, 0, SERVO_HALF);
//  delay(500);
  //  pwm.setPWM(1, 0, SERVO_0);
  //  delay(500);
  //  pwm.setPWM(1, 0, SERVO_180);
//  //  delay(500);


  pwm.setPWM(0, 0, SERVO_HALF);
  delay(500);

  for (uint16_t pulselen = SERVO_0; pulselen < 200; pulselen++) {
    pwm.setPWM(1, 0, pulselen);
    delay(5);
  }
  delay(500);

  pwm.setPWM(0, 0, SERVO_0);
  delay(500);

  for (uint16_t microsec = 300; microsec < 1200; microsec++) {
    pwm.writeMicroseconds(2, microsec);
  }
  delay(500);

  for (uint16_t pulselen = 200; pulselen > SERVO_0; pulselen--) {
    pwm.setPWM(1, 0, pulselen);
    delay(5);
  }

  delay(500);

  for (uint16_t microsec = 1200; microsec > 300; microsec--) {
    pwm.writeMicroseconds(2, microsec);
  }
  delay(500);
  pwm.setPWM(0, 0, SERVO_HALF);
  delay(1500);

  pwm.setPWM(0, 0, SERVO_0);
  delay(500);


}
void base_servo(int angle, int rotation) {
  int ang = map(angle, 0, 180, 300, 2400);
  if (rotation == 0) {
    for (uint16_t microsec = USMIN; microsec < ang; microsec++) {
      pwm.writeMicroseconds(3, microsec);
    }
  } else if (rotation == 1) {
    for (uint16_t microsec = ang; microsec > USMIN; microsec--) {
      pwm.writeMicroseconds(3, microsec);
    }
  }

}
