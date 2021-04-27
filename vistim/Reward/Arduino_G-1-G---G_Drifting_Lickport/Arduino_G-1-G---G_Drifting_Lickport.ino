void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(7,OUTPUT);
  pinMode(2,OUTPUT);
}
  
void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available()>0){
      if (Serial.read()=='1'){
        delay(50); //the amount of time the light is off (milliseconds)
        digitalWrite(7,HIGH);
        digitalWrite(2,HIGH);
        delay(70);//he amount of time the light is on (milliseconds)
        digitalWrite(7,LOW);
        digitalWrite(2,LOW);
        delay(500); //the amount of time the light is off (milliseconds)
        Serial.write('2');//Just a number that closes the loop, clears the serial port of '1'
      }
      else{
        //digitalWrite(2,HIGH);
        //delay(3);//he amount of time the light is on (milliseconds)
        //digitalWrite(7,LOW);
        Serial.write('3');
      }
    }
}
