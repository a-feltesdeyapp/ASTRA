# Wiring
- Wires connect the motor driver and the encoder to an Arduino Uno. There is one Arduino Uno per motor. The wiring setup is the same for each motor.
- Leads from the motor controller and encoders should already be installed but may come loose over time.
  - Check that leads are fully connected before use.

## 1) Motors 
- Leads should be coming off motor controller from ports SV, COM and F/R.
  - If they are not, please loosen screw with a small flat head screwdriver and replace lead, making sure that the black wire does not come out of port COM and that the yellow wire does not come out of port F/R
- Plug the lead from SV port into digital pin 9 – flagged with green tape
- Plug lead from F/R port into digital pin 12 – flagged with blue tape
- Plug lead from COM port into GND pin – flagged with white tape 

![Picture of wiring into Arduino](/../main/Images/Wiring1.jpg)
![Picture of wiring into motor controller](/../main/Images/Wiring2.jpg)
  

## 2) Encoders 
- The encoder has letters and numbers on the frame of the device: B, 5V, A, X, G
- Plug in the lead from A to digital pin 2
- Plug in the lead from B to digital pin 4
- Plug in the lead from X to digital pin 7
- Connect the 5V lead to the 5V output on the Arduino Uno 
- Connect the G lead to GND pin

![Picture of encoders being used](/../main/Images/Encoders.png)

# Software 

## 1) Install the following software 
- VS Code 
  - Python and C/C++ Extension Packs 
- pyserial, scipy, and numpy python libraries 
- Arduino IDE 
- ASTRA Game executable 
*If not using raw ASTRA Game code, reach out to DragonRuby Game Toolkit Developer Amir at amir@amirrajan.net to obtain a free student license to compile the game*

## 2) Code Setup  
- Install the pyserial, scipy, and numpy python libraries and make sure VSCode recognizes them  
- First adjust the COM ports in the cop_read.py file to match the COM ports being used for the Arduino  
- Make sure that the Wii Balance Board is connected and interacts with Wii Balance Walker correctly (Wii Balance Walker can be opened by running the python file)  
- When ready to actually run everything uncomment the serial communication lines (lines 29,30,75,76)  

## 3) Motor Setup  
- Use the motor correction scripts to make sure that both initial linkages point out horizontally from the center of the board  

## 4) Running the Code  
- Start running the Arduino code first, the python code will throw an error if it has nothing to send data to through the serial ports  
- Next run the python code and connect Wii Balance Walker to the Wii Balance Board. After completing this step, all control code should be functioning 
- When done, close Wii Balance Walker  

## 5) Possible Improvements  
- Unify the methods of dealing with minimum PWM  
- Maybe convert the original PWM signal into a percentage, then apply that percentage to the new range of PWM values (minimum PWM to 255 rather than 1 to 255)  
- Use the keyboard library to allow a key to end the main loop in the CoP code, this will provide a more elegant way to end the loop instead of closing Wii Balance Walker and letting the code throw an error 

# Common Errors 
- Game is not reacting to motion on Wii Balance Board 
  - Please verify that “Disable All Actions” option in wii_balance_walker is toggled off. 
- Motors are not responding to motion on Wii Balance Board 
  - Set motor switch to II

