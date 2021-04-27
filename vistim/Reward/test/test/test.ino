#include <CapacitiveSensor.h>

CapacitiveSensor cs = CapacitiveSensor (3, 2);

long th = 800;
String ts;
String time_st;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ts = String('u');
}

void loop() {

long val = cs.capacitiveSensor(30);
 float _time = millis(); 
 time_st = String(_time/1000);
  if(val>=th){
    
    
  // put your main code here, to run repeatedly:
      
                         // changed time to _time
      
      ts = ts + String(_time/1000) + ' ';     // convert _time to timeString formatted as seconds
      // *** long val = cs.capacitiveSensor(30);
     delay(100);
  }
if (Serial.read()=='3') {
  // print to serial

  Serial.print(time_st);
  Serial.print('\t');
  
  Serial.print(ts);
  Serial.print("\n");
  ts = String('u');
  // wait 
}
  //delay(500);
}
