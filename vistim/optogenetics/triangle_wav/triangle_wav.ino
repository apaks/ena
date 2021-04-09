#include <Cyclops.h>

// Create a single cyclops object. CH0 corresponds to a physical board with
// jumper pads soldered so that OC0, CS0, TRIG0, and A0 are used.
Cyclops cyclops0(CH0);

void setup()
{
    Serial.begin(9600);
    // Start the device
    Cyclops::begin();

    // Zero out the DAC
    cyclops0.dac_load_voltage(0);
}

// Each board includes an onboard 12-bit (4095 position) DAC spanning 0-5
// volts. The code function generates a triangle wave ranging fro 0 to full
// scale. The peak brightness of this triangle waveform can be scaled using the
// dial on the front of the device.
void loop()
{ if (Serial.available() > 0) {
    if (Serial.read() == '1') {
      uint16_t v_out = 0;
      delay(500);
      while (v_out < 4085) {
          v_out += 10;
          cyclops0.dac_load_voltage(v_out);
          //delayMicroseconds(500);
          delay(3);
      }
      //delay(600);
      cyclops0.dac_load_voltage(0);
      //delay(700);
//      while (v_out > 10) {
//          v_out -= 10;
//          cyclops0.dac_load_voltage(v_out);
//          delayMicroseconds(250);
//      }
  }  
  else {
    Serial.write('3');
    cyclops0.dac_load_voltage(0);
    }
   }
 }  
