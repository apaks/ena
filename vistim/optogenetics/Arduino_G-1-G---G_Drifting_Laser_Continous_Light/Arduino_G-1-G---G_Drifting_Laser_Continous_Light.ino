void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(3,OUTPUT);
}
  
void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available()>0){
      if (Serial.read()=='1'){
          //delay(2700); //the amount of time the light is off (milliseconds)
          delay(1000);
          digitalWrite(3,HIGH);
          //delay(1800000);
          delay(1000);//1800000 for 30min continuous laser
          digitalWrite(3,LOW);
          delay(500);
          Serial.write('2');//Just a number that closes the loop, clears the serial port of '1'
        }
        else{
          Serial.write('3');
        }
      }
  }
