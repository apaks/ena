#include <CapacitiveSensor.h>

CapacitiveSensor cs = CapacitiveSensor (4, 2);
long th = 500;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(7,OUTPUT);
  
}
  
void loop() {
  // put your main code here, to run repeatedly:

        long val = cs.capacitiveSensor(30);
        
        if (val >= th) {
        
        digitalWrite(7,HIGH);
        Serial.println(val);
        delay(20); //the amount of time the light is on (milliseconds)
        digitalWrite(7,LOW);
        
   
    }
}
