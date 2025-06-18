# Meant to grab variables from console output from Wii Balance Walker and print them as a proof of concept
import subprocess
import sys
import os
import math
import KinematicsModel
import serial
import struct
import csv
import time

# set working path to path to script path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# initialize kinematics model
km = KinematicsModel.ASTRAKinematicsModel()



process = subprocess.Popen(['./WiiBalanceWalker-0.5/WiiBalanceWalker-0.5/WiiBalanceWalker/bin/x64/Release/WiiBalanceWalker.exe'], 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True)

# setup serial communication (chan)
#ser1 = serial.Serial('COM4',115200)
#ser2 = serial.Serial('COMX',115200)

def  convertPitchRoll(x,y):
    # converts WBW balance ratio value into pitch/roll
    # x is a 0-100 value with 0 being at the left and 100 being at the right
    # y is a 0-100 value with zero being at the top and 100 being at the bottom
    x = (x-50) * 2  # converts x value to -100 to 100 value with negative being to the left
    y = (y-50) * -2 # converts y value to -100 to 100 value with negative being at the bottom
    roll = x/100 * 10
    pitch = y/100 * 10
    return [pitch, roll]

target_angles = [math.nan, math.nan]

# set up data export

while True:
    output = process.stdout.readline()
    output_array=output.split(",")
    x = float(output_array[0])
    y= float(output_array[1])

    # convert NaNs that appear when there isn't enough weight to represent centered CoP
    if (math.isnan(x)):
        x=50
    if (math.isnan(y)):
        y=50
    pitchRoll = convertPitchRoll(x,y) # convert CoP into pitch/roll
    # put pitch and roll into from that kinematics model likes
    pitchRoll[0] = round(pitchRoll[0])
    pitchRoll[1] = round(pitchRoll[1])
    pitch = int(pitchRoll[0])
    roll = int(pitchRoll[1])

    target_angles = km.calculate(KinematicsModel.deg2rad(pitch),KinematicsModel.deg2rad(roll)) # get target angles from pitch/roll
    # convert angles into form useful for arduino code
    # theta2_t is already good to go
    target_angles[0]=180-target_angles[0]
    if target_angles[0]<0:
        target_angles[0]=360-target_angles[0]
    theta1_t = struct.pack('f',target_angles[0])
    theta2_t = struct.pack('f',target_angles[1])
    
    if(not math.isnan(target_angles[0]) and not math.isnan(target_angles[1])):
    
        #ser1.write(theta1_t)
        #ser2.write(theta2_t)
        "placeholder"
    print(target_angles)

