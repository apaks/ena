void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(7,OUTPUT);
}
  
void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available()>0){
      if (Serial.read()=='1'){
        //delay(2700); //the amount of time the light is off (milliseconds)
        delay(500); //the amount of time the light is off (milliseconds)
        for (int ii = 1; ii <= 2 ; ii++){
          
          
        
          for (int i =1 ; i <= 40 ; i++){//90 for 3s 600 for 20s, 900 for 30s, 9,000 for 5min
            digitalWrite(7,HIGH);
            delay(60); // the amount of time the light is on (milliseconds)  
            digitalWrite(7,LOW);
            delay(40);}
          delay(0);//do 250 for 4hz, 166 for 6hz, 125 for 8Hz
        }
        delay(50); //the amount of time the light is off (milliseconds)
        Serial.write('2');//Just a number that closes the loop, clears the serial port of '1'
      }
      else{
        Serial.write('3');
      }
    }
}
