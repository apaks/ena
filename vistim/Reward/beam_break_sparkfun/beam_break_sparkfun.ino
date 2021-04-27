/* Analog Read Interrupter
* -----------------------
*/

int ruptPin = 2; // select the input pin for the interrupter
int val = 0; // variable to store the value coming from the sensor

void setup()
{
    Serial.begin(9600); // set up Serial library at 9600 bps
}

void loop()
{
    val = analogRead(ruptPin); // read the value from the sensor
    if (val == 0){
      Serial.println(val); // print the sensor value to the serial monitor
      delay(10);
      }
     delay(10);
}
