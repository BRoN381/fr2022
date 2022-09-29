#include <LiquidCrystal.h> 
#include <Servo.h>
int rpwm, lpwm, sign, stepm, water, servom, color;

const int inputPinLoc[4] = {38,39};  //tba
const int outputPinLoc[9] = {A0,2,3,4,5,6,7,8,9};   //A0 servo, 2~5 main motor, 6~9 step motor
const int buttonPin[5] = {34,35,36,37,38}; //34 state lock, 35~38 four states
const int motorPin[4] = {2,3,4,5}; //left forward, left backward, right forward, right backward
const int motorSpeed = 150; //default speed before p-control
const int triangleTurnSpeed[6] = {150,150,150,150,1000,1000}; //left forward, left backward, right forward, right backward, left turn time, right turn time
const int squareTurnSpeed[3] = {150,150,1000}; //left forward, right backward, turn time
const int circleTurnSpeed[3] = {150,150,2000}; //left forward, right backward, turn time

LiquidCrystal lcd(1,2,3,4,5,6);//to be asure
Servo clawServo;

void readSerial();
void stopMotor();
void moveMotor(int left, int right);  //main moving code
void readSign();
void sign0(); //move while checking claw code
void triangleTurn(bool type); //triangle sign, true for left, false for right
void squareTurn();  //90 degree turn
void circleTurn();  //180 degree turn
void readStateButton(); //manual change state
void printLcd(String str1, String str2);

void setup() {
  for (int i = 0; i < 9; i++) pinMode(outputPinLoc[i], OUTPUT);
  for (int i = 0; i < 5; i++) pinMode(buttonPin[i], INPUT_PULLUP);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.clear();
  clawServo.attach(A0);
}

void loop() {
  readSerial();
  readSign();
  readStateButton();
    
}

void stopMotor(){
  for(int i = 0; i < 4; i++) analogWrite(motorPin[i], 0);
}

void moveMotor(int left, int right){  //main moving code
  analogWrite(motorPin[0], left);
  analogWrite(motorPin[2], right);
}

void triangleTurn(bool type){ //triangle sign, true for left, false for right
  if (type){  //turn left
    analogWrite(motorPin[1], triangleTurnSpeed[1]);
    analogWrite(motorPin[2], triangleTurnSpeed[2]);
    delay(triangleTurnSpeed[4]);
  }
  else{ //turn right
    analogWrite(motorPin[0], triangleTurnSpeed[0]);
    analogWrite(motorPin[3], triangleTurnSpeed[3]);
    delay(triangleTurnSpeed[5]);
  }
  stopMotor();
}

void squareTurn(){  //90 degree turn
  analogWrite(motorPin[0], squareTurnSpeed[0]);
  analogWrite(motorPin[3], squareTurnSpeed[1]);
  delay(squareTurnSpeed[2]);
  stopMotor();
}

void circleTurn(){  //180 degree turn
  analogWrite(motorPin[0], circleTurnSpeed[0]);
  analogWrite(motorPin[3], circleTurnSpeed[1]);
  delay(circleTurnSpeed[2]);
  stopMotor();
}

void readSerial(){
  if (Serial.available()){
    String str = Serial.readStringUntil('\n');
    rpwm = str.substring(0,3).toInt();
    lpwm = str.substring(3,6).toInt();
    sign = (int)str[6];
    stepm = (int)str[7];
    water = (int)str[8];
    servom = (int)str[9];
    color = (int)str[10];
  }
}

void sign0(){
  moveMotor(lpwm, rpwm);
  
}

void readSign(){
  switch(sign){ //0 none, 1 left triangle,2 right triangle, 3 square, 4 circle
    case 0:
      sign0();
      break;
    case 1:
      triangleTurn(true);
      break;
    case 2:
      triangleTurn(false);
      break;
    case 3:
      squareTurn();
      break;
    case 4:
      circleTurn();
      break;
  }
}

void readStateButton(){
  int stateInput = 0;
  if (buttonPin[0] == LOW){
    printLcd("state unlock", "plz input state");
    while(buttonPin[0] == LOW){ //while unlock
      for(int i = 1; i< 5; i++){
        if(buttonPin[i] == LOW){
          printLcd("input state "+(String)i, "comfirm?");
          stateInput = i;
        }
      }
    }
    lcd.clear();
  }
  Serial.write(stateInput);
}

void printLcd(String str1, String str2){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(str1);
  lcd.setCursor(0,1);
  lcd.print(str2);
}
