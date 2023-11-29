const int relay = 8;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    String incoming = Serial.readString();
    Serial.println("Typed: " + incoming);
    if (incoming.equals("on")) {
      Serial.println("Turn on");
      digitalWrite(relay, LOW);
    }
    else {
      Serial.println("Turn off");
      digitalWrite(relay, HIGH);
    }
  }
}
