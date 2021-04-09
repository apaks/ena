float timer;
int numStim;
int byteAvail;
char tempIn;
String received;
int timeOn = 20; //seconds
int timeOff = 20; //seconds

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(7, OUTPUT);
  pinMode(2, OUTPUT);
}
  
void loop() {
  // put your main code here, to run repeatedly:
  byteAvail = Serial.available();
  if (byteAvail > 0){
    tempIn = Serial.read();
    if (tempIn == '\n'){
      timer = received.toInt() / 1000.0;
      received = "";
  
      if (timer < (timeOn + timeOff)){
        numStim = 0;
      }
  
      timer = timer - (numStim * (timeOn + timeOff));
      if (timer > (timeOn + timeOff)){
        numStim += 1;
        timer = timer - (timeOn + timeOff);
      }
      if (timer < timeOn){
        //delay(2700); //the amount of time the light is off (milliseconds)
        //Serial.write('1');
        digitalWrite(7, HIGH);
        delay(60); // the amount of time the light is on (milliseconds)  
        digitalWrite(7, LOW);
        delay(40);
      }
      else{
        digitalWrite(7, LOW);
      }
    }
    else{
      received += tempIn;
    }
  }
}
