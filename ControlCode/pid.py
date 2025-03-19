# PID controller
# _t denotes a target value
# theta1 and theta2 represent current motor position
# omega1 and omega2 represent current motor speed
import numpy as np
import time as t
import keyboard as k
class pidController:
    def __init__(self,Kp,Ki,Kd,setpoint):
        self.Kp=Kp
        self.Ki=Ki
        self.Kd=Kd
        self.setpoint=setpoint
        self.integralError = 0
        self.previousError = 0
    def update(self,setpoint,position,dt):
        # positional control
        self.setpoint = setpoint
        positionError = self.setpoint-position
        Pcontrol = positionError*self.Kp
        # derivative control
        derivativeError=(positionError-self.previousError)/dt
        Dcontrol = derivativeError*self.Kd
        # integral control
        self.integralError += positionError*dt
        Icontrol = self.integralError*self.Ki
        # full control
        Control= Pcontrol+Dcontrol+Icontrol

# main code body
Kp=1
Ki=1
Kd=1
theta1=0
theta2=0
theta1_t=0
theta2_t=0
pid1 = pidController(theta1,Kp,Ki,Kd,theta1_t)
pid2 = pidController(theta1,Kp,Ki,Kd,theta1_t)

active=True
dt = 0.001
end = 1000
n = end/dt
last_time = t.monotonic()

while True:
    # need this from magnetic encoders
    theta1=0
    theta2=0
    # need this from other functions
    theta1_t=0
    theta2_t=0
    current_time = t.monotonic()
    dt = current_time-last_time
    control1=pid1.update(theta1_t,dt)
    control2=pid2.update(theta2_t,dt)
    last_time=current_time
    if k.is_pressed('q'):
        print("Control terminated by user.")
        break
