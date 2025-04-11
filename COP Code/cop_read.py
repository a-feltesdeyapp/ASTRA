# Meant to grab variables from console output from Wii Balance Walker and print them as a proof of concept
import subprocess
import sys
process = subprocess.Popen(['./WiiBalanceWalker-0.5/WiiBalanceWalker-0.5/WiiBalanceWalker/bin/x64/Release/WiiBalanceWalker.exe'], 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True)

while True:
    output = process.stdout.readline()
    print(output)
