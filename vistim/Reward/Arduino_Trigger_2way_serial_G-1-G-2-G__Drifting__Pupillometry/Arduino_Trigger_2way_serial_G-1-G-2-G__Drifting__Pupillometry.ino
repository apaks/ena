void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(11,OUTPUT);
  pinMode(13,OUTPUT);
}
  
void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available()>0){
      if (Serial.read()=='1'){
        digitalWrite(11,HIGH);
        digitalWrite(13,HIGH);
        delay(4000); //the amount of time the light is on (milliseconds)
        digitalWrite(11,LOW);
        digitalWrite(13,LOW);
        delay(500); //the amount of time the light is off (milliseconds)
        Serial.write('2');
      }
      else{
        Serial.write('3');
      }
    }
}
