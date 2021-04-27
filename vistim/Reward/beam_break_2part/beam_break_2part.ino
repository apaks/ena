/*
  IR Breakbeam sensor demo!
*/

#define LEDPIN 13
// Pin 13: Arduino has an LED connected on pin 13
// Pin 11: Teensy 2.0 has the LED on pin 11
// Pin  6: Teensy++ 2.0 has the LED on pin 6
// Pin 13: Teensy 3.0 has the LED on pin 13

#define SENSORPIN 4

String ts;
String time_st;

// variables will change:
int sensorState = 0, lastState = 0;       // variable for reading the pushbutton status
String flag;

void setup() {
  ts = String('u');
  flag = String('f');
  // initialize the LED pin as an output:
  pinMode(LEDPIN, OUTPUT);
  // initialize the sensor pin as an input:
  pinMode(SENSORPIN, INPUT);
  digitalWrite(SENSORPIN, HIGH); // turn on the pullup

  Serial.begin(9600);
  //Serial1.begin(9600);

}

void loop() {
  // read the state of the pushbutton value:
  sensorState = digitalRead(SENSORPIN);
  
  float _time = millis();
  time_st = String(_time / 1000);

  // check if the sensor beam is broken
  // if it is, the sensorState is LOW:
  if (sensorState == LOW) {
    flag = String('t');
    ts = ts + String(_time / 1000) + " ";
    delay(60);
    //Serial.println(flag);
    // turn LED on:
    digitalWrite(LEDPIN, HIGH);
  }
  else {
    // turn LED off:
    digitalWrite(LEDPIN, LOW);
  }
  int input = Serial.read();
  if (input == '3') {
        Serial.print(time_st);      //prints time stamp at beginning of each trial
        Serial.print('\t');         //print a tab
        Serial.print(ts);           //prints lick time
        Serial.print("\n");         //new line
        ts = String('u');           //prints a 'u' after all the times are recorded
        flag = String('f');
        delay(100);
        
  } else if (input == '5'){
        Serial.println(flag);  
        flag = String('f');
        delay(10);
  } else {
        //Serial.print('b');  
        flag = String('f');
        delay(10);
  }


  //  if (sensorState && !lastState) {
  //    Serial.println("Unbroken");
  //  }
  //  if (!sensorState && lastState) {
  //    Serial.println("Broken");
  //  }
  lastState = sensorState;
}
