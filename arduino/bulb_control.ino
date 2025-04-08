const int greenLed = 9;  // Pin para el bombillo verde
const int redLed = 10;   // Pin para el bombillo rojo

void setup() {
    pinMode(greenLed, OUTPUT);
    pinMode(redLed, OUTPUT);
    Serial.begin(9600);  // Iniciar comunicación serial
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        if (command == 'G') {
            digitalWrite(greenLed, HIGH);
            digitalWrite(redLed, LOW);
        } else if (command == 'R') {
            digitalWrite(greenLed, LOW);
            digitalWrite(redLed, HIGH);
        }
    }
}
