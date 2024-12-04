#include <Servo.h>
Servo myservo;

int lastServoPosition = -1;

void setup() {
  myservo.attach(9); // Ensure servo attached on pin 9
  Serial.begin(9600); 
  Serial.println("Arduino ready to receive weather data");
}

void loop() {
  if (Serial.available()) {
    String weather = Serial.readStringUntil('\n');
    Serial.println("Weather received: " + weather);

    int newServoPosition = 45; // Default

    // Determine the new position based on the weather
    if (weather.indexOf("Clear") >= 0) {
      newServoPosition = 0; // Clear
    } else if (weather.indexOf("Rain") >= 0) {
      newServoPosition = 90; // Rain
    } else if (weather.indexOf("Snow") >= 0) {
      newServoPosition = 180; // Snow
    }

    // Only move the servo if the position has changed
    if (newServoPosition != lastServoPosition) {
      myservo.write(newServoPosition);
      lastServoPosition = newServoPosition;
      Serial.println("Servo moved to " + String(newServoPosition) + " degrees");
    } else {
      Serial.println("Servo position unchanged");
    }
  }
}



  

