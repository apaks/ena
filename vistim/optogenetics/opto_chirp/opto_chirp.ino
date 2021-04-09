#include <Cyclops.h>
#define PI_CONST 3.14159265358979323846
// Parameters of the chirp waveform
#define CHIRP_TIME_MS 5000 // Length of chirp waveform in msec
#define FREQ_START 0.5f // Start frequency in Hz
#define FREQ_END 10.0f // End frequency in Hz
// Create a single cyclops object. CH0 corresponds to a physical board with
// jumper pads soldered so that OC0, CS0, TRIG0, and A0 are used. Set the
// current limit to 1A on this channel.
Cyclops cyclops0(CH0, 1000);
// Chirp frequency ramp parameter
float beta = 1.0;
int prev = 0;
void setup()
{
  Serial.begin(9600);
  // Chirp parameter
  beta = (FREQ_END - FREQ_START) / (((float)CHIRP_TIME_MS) / 1000.0);
  // Start the device and zero out its DAC
  Cyclops::begin();
  cyclops0.dac_load_voltage(0);
}
void loop()
{ if (Serial.available() > 0) {
    if (Serial.read() == '1') {
      // Calculate current chirp amplitude
      prev = millis();
      delay(1);
      while (1) {
        float now = ((float)((millis() - prev) % CHIRP_TIME_MS)) / 1000.0;
        Serial.println(now);
        float freq
          = 2.0 * PI_CONST * (FREQ_START * now + (beta / 2.0) * pow(now, 2));
        unsigned int voltage = (unsigned int)(4095.0 * (sin(freq) / 2.0 + 0.5));
        // Program the DAC and load the voltage
        cyclops0.dac_load_voltage(voltage);
        Serial.println(freq);
        if (now == 0) {
          cyclops0.dac_load_voltage(0);
          break;
        }
      }

    }
    else {
      Serial.write('3');
      cyclops0.dac_load_voltage(0);
    }
  }
}

