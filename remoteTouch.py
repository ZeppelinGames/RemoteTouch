from flask import Flask, render_template, request,redirect
import mimetypes
import os
import math
from qrcodegen import QrCode, QrSegment
import random
import logging
import click
from getmac import get_mac_address
import socket

import pyautogui

pyautogui.FAILSAFE = True

connected = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while not connected:
    try:
        s.connect(("8.8.8.8", 80))
        connected = True
    except:
        pass
hostIP = s.getsockname()[0]
s.close()

prevMouseX = 0
prevMouseY = 0

keyConvDict = {
    '{bksp}':'BackSpace',
   '{enter}':'Return',
   '{shift}':'Shift',
   '{tab}':'Tab',
   '{lock}':'Caps_Lock',
   '{space}':'space',
   '{ctrl}':'Control_L',
   '{alt}':'Alt_L',
   '{esc}':'Escape',
   '{f1}':'F1',
   '{f2}':'F2',
   '{f3}':'F3',
   '{f4}':'F4',
   '{f5}':'F5',
   '{f6}':'F6',
   '{f7}':'F7',
   '{f8}':'F8',
   '{f9}':'F9',
   '{f10}':'F10',
   '{f11}':'F11',
   '{f12}':'F12',
}

def print_qr(qrcode: QrCode) -> None:
    """Prints the given QrCode object to the console."""
    border = 1
    sizeRange = qrcode.get_size() + border
    for y in range(-border, sizeRange):
        for x in range(-border, sizeRange):
            print("\u2588 "[1 if qrcode.get_module(x,y) else 0] * 2, end="")
        if(x <= sizeRange-border):
            print()
    if(y <= (sizeRange-border) - 1):
        print()

def processData(data):
    global prevMouseX
    global prevMouseY
    
    splitData = data.split(":")

    print("Raw: " + data + " | split: ",end='')
    print(splitData)
    
    if (len(splitData) > 1):
        if 'mm' in str(splitData[0]): #Mouse move
            if(len(splitData) > 2):
                currX = int(splitData[1])
                currY = int(splitData[2])

                moveX = currX - prevMouseX
                moveY = currY - prevMouseY
                dist = math.sqrt(math.pow(moveX,2) + math.pow(moveY,2))

                moveX = math.ceil(moveX / dist) * 10
                moveY = math.ceil(moveY / dist) * 10

                #print("Moving: " + str(moveX) + ", " + str(moveY))

                #subS.sendline("xterm -iconic -e 'xdotool mousemove_relative " + str(moveX) + " " + str(moveY) + "'")
                #subS.expect('')
                pyautogui.move(moveX,moveY)

                prevMouseX = currX
                prevMouseY = currY
        if 'kd' in str(splitData[0]): #Key down
            key = str(splitData[1])
            if(key in keyConvDict):
                key = keyConvDict[key]
            pyautogui.keyDown(key)
               # subS.sendline("xterm -iconic -e 'xdotool keydown " + key + "'")
                #subS.expect('')
            print("Pressed: "+ key)
        if 'ku' in str(splitData[0]): #Key up
            key = str(splitData[1])
            if(key in keyConvDict):
                key = keyConvDict[key]

            pyautogui.keyUp(key)
           # subS.sendline("xterm -iconic -e 'xdotool keyup " + key + "'")
           # subS.expect('')
    if(len(splitData) > 0):
        if 'lmbd' in splitData[0]: #LMB Down
           # subS.sendline("xterm -iconic -e 'xdotool mousedown 1'")
           # subS.expect('')
           #print("LMBD")
           
           pyautogui.mouseDown()
           #pyautogui.move(10,0)
        if 'lmbu' in splitData: #LMB up
          #  subS.sendline("xterm -iconic -e 'xdotool mouseup 1'")
           # subS.expect('')
           pyautogui.mouseUp()
           
        if 'rmbd' in str(splitData[0]): #RMB Down
           # subS.sendline("xterm -iconic -e 'xdotool mousedown 3'")
           # subS.expect('')
           pyautogui.mouseDown(button='right')
        if 'rmbu' in splitData: #RMB up
           # subS.sendline("xterm -iconic -e 'xdotool mouseup 3'")
           # subS.expect('')
           pyautogui.mouseUp(button='right')
        
authKey = random.randint(1000,9999)
currConnectionMAC = ""

qr0 = QrCode.encode_text("http://" + str(hostIP) + ":5000/params?key=" + str(authKey), QrCode.Ecc.LOW)
print_qr(qr0)

mimetypes.add_type('text/css', '.css')
app = Flask(__name__)

print("Auth: " + str(authKey))
print("Started webserver at " + str(hostIP))

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global currConnectionMAC
    
    authIP = request.remote_addr
    authMAC = str(get_mac_address(ip=authIP))

    if(request.method == 'POST'):
        if(authMAC == currConnectionMAC):
            try:
                inputData = request.form['inputData']
                processData(inputData)
            except:
                print("Bad data: " + str(request.form['inputData']))
    return render_template("index.html", data=0)

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.route('/params')
def auth():
    key = request.args.get('key')
    if(key == str(authKey)):
        global currConnectionMAC
        
        #store mac for auth
        authIP = request.remote_addr
        authMACAddr = str(get_mac_address(ip=authIP))
        currConnectionMAC = authMACAddr
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
