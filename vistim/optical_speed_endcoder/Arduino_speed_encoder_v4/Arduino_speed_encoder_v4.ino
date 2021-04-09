// brown = B, blue(white strips) = A
// 50.24 cm per 360 degree
// 400 cpr
// 1 tick = 0.1256 cm/tick
// 25 ms report time
//1 tick = 5 cm/s

#define outputA 6
#define outputB 7
String ts;
int counter = 0;
int aState;
int aLastState;
void setup() {
  pinMode (outputA, INPUT);
  pinMode (outputB, INPUT);
  ts = "";
  Serial.begin(9600);
  // Reads the initial state of the outputA
  aLastState = digitalRead(outputA);
}

void loop() {
  
  const unsigned long sampling = 25UL;
  static unsigned long lastSampleTime = 0 - sampling;  // initialize such that a reading is due the first time through loop()
  unsigned long now = millis(); 
  aState = digitalRead(outputA); // Reads the "current" state of the outputA
  // If the previous and the current state of the outputA are different, that means a Pulse has occured
  if (aState != aLastState) {
    // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
    if (digitalRead(outputB) != aState) {
      // clockwise movement
      counter ++;
    } else {
      // counter clockwise movement
      counter --;
    }
    aLastState = aState;
//    Serial.println(counter); 
  }

  if ((now - lastSampleTime) > sampling) {
    lastSampleTime = now;
    ts += counter;
    ts += ',';
//    counter = 0;
    // add code to take temperature reading here
  }
  if (Serial.available()>0){
    int input = Serial.read();
    if (input == '1') {
      ts = "";
      counter = 0;
    } else if (input == '2') {
      Serial.println(ts);      //prints time stamp at beginning of each trial
      delay(10);
    }
  }
}
