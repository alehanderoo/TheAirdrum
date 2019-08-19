#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#include <Tone.h>

#define LED_PIN     10
#define LED_CNT     8
#define A_in        3
#define TxPin       11
#define EN_5V       2

Tone TxLed;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_CNT, LED_PIN, NEO_GRB + NEO_KHZ800);

typedef enum { 
    s_init,
    s_check,
    s_app
} sys_states_t;

sys_states_t fsm = s_init;
bool data_received = false;
uint8_t i2c_buf[64];
uint8_t i2c_cntr = 0;
uint16_t i2c_adr = 0;
uint8_t i2c_adr8 = 0;
uint8_t i2c_rnd = 0;
uint8_t hand_value = 0;
uint32_t start_millis = 0;
uint32_t led_millis = 0;
uint32_t system_color = 0;


void setup() {
  // debugging
  Serial.begin(115200);
  Serial.println("Starting...");

  // start led's
  pinMode(EN_5V, OUTPUT);       // 5V BUCK Pin
  digitalWrite(EN_5V, HIGH);    // 5V BUCK Enable
  strip.begin();
  strip.show();

  // Begin IR transmitting
  pinMode(TxPin, OUTPUT);       // IR transmitting LED pin
  TxLed.begin(TxPin);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  
}

void loop() {
  switch(fsm) {

      // initialize complete system
    case s_init:
      // analog 0 is unconnected and creates noise for a random seed
      randomSeed(analogRead(0));
      // reset variable
      data_received = false;
      // create address from random 16 bits. Convert to 7 bits (divide by 512)
      i2c_adr = random(65535);
      i2c_adr /= 512;
      i2c_adr8 = i2c_adr; // compiler wants 8 bits...
      // Start listening on this address
      Wire.begin(i2c_adr8);
      Wire.onRequest(request_event);
      Wire.onReceive(receive_event);
      // feedback
      Serial.print("Address: ");
      Serial.println(i2c_adr8);
      // check the if the given address is used
      fsm = s_check;
      // set the start value
      start_millis = millis();
      
      break;

      // After we are initialized, we want to wait and see if anybody
      // uses this address. This is done for a maximum of 1 second.
    case s_check:
      //Serial.println(system_color);
      if(millis() - start_millis > 1000) {
        fsm = s_app;
        Serial.println("Address can be used");
        digitalWrite(LED_BUILTIN, LOW);
      } 
      // Wait for 50msec before trying a new address. i2cdetect on Pi still busy scanning
      else if (data_received == true && millis() - start_millis > 50 ) {
        fsm = s_init;
        Serial.println("Address already used, retrying");
      }
      
      break;

      // Run the application
    case s_app:
      // get the hand value from the adc (8 bits instead of 10)
      hand_value = analogRead(A_in) >> 2;
      // new color given through i2c?
      if (i2c_cntr == 255) {
        system_color = strip.Color(200, 10, 100);
        //system_color = strip.Color(i2c_buf[0], i2c_buf[1], i2c_buf[2]);
        i2c_cntr = 0;
      }
      // update the LED's every 30ms
      if(millis() - led_millis > 30) {
        strip_set_color(system_color, hand_value);
        led_millis = millis();
      }
      
      break;
  }
}

void request_event() {
  // enable IR transmitting
  TxLed.play(25000);    //(32768);
  //Set the buffer up to send all 14 bytes of data
  Wire.write(&hand_value, 1);
  // disable IR transmitting
  TxLed.stop();
}

void receive_event(int len) {
  // in what state is the main loop?
  if (fsm == s_init || fsm == s_check) {
    // we received some data, aka address is already taken
    data_received = true;
  }
  else if (i2c_cntr != 255) {
    // place all incoming data in the global buffer
    while (Wire.available()) {
      i2c_buf[i2c_cntr] = Wire.read();
      i2c_cntr++;
    }
    //Serial.print(i2c_buf);
    for(int i = 0; i < 64; i++)
      {
        Serial.print(i2c_buf[i]);
        Serial.print('-');
      }
      Serial.println();
    // all data received, we dont want anymore
    i2c_cntr = 255;
  }
}



void strip_set_color(uint32_t color, uint8_t brightness) {
  // set brightness
  strip.setBrightness(brightness);
  // set colors in buffer
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, color);
  }
  // push buffer to LED's
  strip.show();
}
