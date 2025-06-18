// PID Variables
double theta;  // current detected angle
int control; // control signal
double theta_t; // desired angle
byte buffer[4];
double Kp = 4.5; //proportional gain
double Ki = 0; //integral gain
double Kd = 0; //derivative gain
int T = 10; //sample time in milliseconds (ms)
unsigned long last_time=0;
double total_error, last_error;
int max_control = 255;
int min_control = -255;
float recievedFloat;
// Motor Communication
const int MOTOR_PWM = 9;  // PWM output for speed for motor 1
const int MOTOR_FR = 12;   // Forward/Reverse control for motor 1
// Encoder Communication
#define ENC_A 2  // Encoder Channel A
#define ENC_B 4  // Encoder Channel B
#define ENC_X 7  // Encoder Index (X) Channel
volatile long encoderPosition = 0;  // Position count
volatile bool aLastState;
volatile bool indexEvent = false;   // Flag to indicate an index event
const int ppr = 2048;  // Pulses Per Revolution (set via DIP switches)
const int countsPerRev = ppr * 2;  // Using 2 counts per pulse (from channel A only)
const float degreesPerCount = 360.0 / countsPerRev;  // Conversion factor from count to degrees
float offset; // initial encoder position for zeroing
float pwm;
float min_pwm = 10;
void setup(){
  // Control
  pinMode(MOTOR_PWM, OUTPUT);
  pinMode(MOTOR_FR, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(1);
  // Encoder
  pinMode(ENC_A, INPUT_PULLUP);
  pinMode(ENC_B, INPUT_PULLUP);
  pinMode(ENC_X, INPUT_PULLUP);
  // Attach interrupt for channel A on any change
  attachInterrupt(digitalPinToInterrupt(ENC_A), readEncoder, CHANGE);
  // Attach interrupt for index channel (X); using FALLING edge as an example
  attachInterrupt(digitalPinToInterrupt(ENC_X), indexHandler, FALLING);
  aLastState = digitalRead(ENC_A);
  // establish offset
  readEncoder();
  offset = encoderPosition * degreesPerCount;
}
void loop(){
readEncoder();
theta = encoderPosition * degreesPerCount-offset;
theta = fmod(theta,360);
PID_Control(); //calls the PID function every T interval and outputs a control signal
sendControl(); // sends control signals to motors
}
void PID_Control(){
unsigned long current_time = millis(); //returns the number of milliseconds passed since the Arduino started running the program
int delta_time = current_time - last_time; //delta time interval
if (delta_time >= T){ // only update control signal at set interval
// update target angles
updateTarget();
// proportional error
double error = theta_t-theta;
// integral error
total_error+=error; // accumulates error for integral term for motor 1
if (total_error >= max_control) total_error = max_control;
else if (total_error <= min_control) total_error = min_control;
// derivative error
double delta_error = error - last_error; //difference of error for derivative term
// control signal generation
control = Kp*error + (Ki*T)*total_error + (Kd/T)*delta_error; //PID control compute
if (control >= max_control) control = max_control;
else if (control <= min_control) control = min_control;
// update previous error
last_error = error;
}
}
void readEncoder() {
  bool aState = digitalRead(ENC_A);
  bool bState = digitalRead(ENC_B);
  // Check for change on channel A and update count based on the state of B
  if (aState != aLastState) {
    if (bState != aState) {
      encoderPosition++;  // Clockwise rotation
    } else {
      encoderPosition--;  // Counterclockwise rotation
    }
  }
  aLastState = aState;
}
void updateTarget(){
  // serial communication
  if (Serial.available() >=4){
    Serial.readBytes(buffer, 4);
    memcpy(&recievedFloat, buffer,sizeof(buffer));
    theta_t = recievedFloat;
  }
}
void sendControl(){
  // set motor direction and output pwm
  if(control>0)
  {
    digitalWrite(MOTOR_FR, HIGH);
  }
  else
  {
    digitalWrite(MOTOR_FR, LOW);
  }
  pwm = abs(control);
  if (pwm < min_pwm && pwm >0)
  {
    pwm = min_pwm;
  }
  analogWrite(MOTOR_PWM, pwm);
}
void indexHandler() {
  // Index pulse detected – reset the encoder count
  encoderPosition = 0;
  indexEvent = true;
}