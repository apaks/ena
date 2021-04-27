#include <CapacitiveSensor.h>

CapacitiveSensor cs = CapacitiveSensor (7, 4);

long th = 300;
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
      
      ts = ts + String(_time/1000) + " ";     // convert _time to timeString formatted as seconds
      // *** long val = cs.capacitiveSensor(30);
     delay(100);
  }
if (Serial.read()=='3') {
  // psychopy sends '3' to indicate trial start
  Serial.print(time_st);      //prints time stamp at beginning of each trial
  Serial.print('\t');         //print a tab
  Serial.print(ts);           //prints lick time
  Serial.print("\n");         //new line
  ts = String('u');           //prints a 'u' after all the times are recorded

}
  //delay(500);
}
