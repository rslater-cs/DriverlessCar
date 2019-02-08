import RPi.GPIO as gpio
import time
from threading import Thread
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
#create gpio and set pins to be output mode

path = 3
freq = 50
velocity = 50
currVelocity = velocity
acc = None
#set starting speed and direction to stop

wheel = [gpio.PWM(7, freq), gpio.PWM(11, freq), gpio.PWM(13, freq), gpio.PWM(15, freq)]
for x in range(4):
    wheel[x].start(0)

def forward(velocity):
    wheel[0].ChangeDutyCycle(currVelocity)
    wheel[1].ChangeDutyCycle(0)
    wheel[2].ChangeDutyCycle(0)
    wheel[3].ChangeDutyCycle(currVelocity)

def left(velocity):
    wheel[0].ChangeDutyCycle(currVelocity)
    wheel[1].ChangeDutyCycle(0)
    wheel[2].ChangeDutyCycle(currVelocity)
    wheel[3].ChangeDutyCycle(0)

def right(velocity):
    wheel[0].ChangeDutyCycle(0)
    wheel[1].ChangeDutyCycle(currVelocity)
    wheel[2].ChangeDutyCycle(0)
    wheel[3].ChangeDutyCycle(currVelocity)

def stop(velocity):
    for x in range(4):
        wheel[x].ChangeDutyCycle(currVelocity)
"""When a function runs it changes the voltage given to each motor to get the direction
needed and turns the motor off and on at a high frequancy to make the car move
different speeds"""

def accelerate(finalSpeed):
    global velocity, currVelocity
    changeInSpeed = int(finalSpeed - currVelocity)
    timeInterval = abs(1/changeInSpeed)
    print("time" + str(timeInterval))
    print("change" + str(changeInSpeed))
    interval = changeInSpeed / abs(changeInSpeed)
    for x in range(abs(changeInSpeed)):
        print("curr vel" + str(currVelocity))
        currVelocity += interval
        time.sleep(timeInterval)
    return

def setMovement():
    while True:
        global path
        global currVelocity
        if path == 0:
            forward(currVelocity)
        elif path == 1:
            left(currVelocity)
        elif path == 2:
            right(currVelocity)
        elif path == 3:
            stop(currVelocity)
    """Depending on the value of path, 1 of 4 functions are run and passed the speed"""

def setDirection(direction):
    global path
    path = direction

def setSpeed(speed):
    global velocity
    global acc
    if (speed is not None):
        speed = int(speed)
        if (speed is not velocity):
            if acc is not None:
                acc.join()
            velocity = speed
            print(velocity)
            acc = Thread(target = accelerate, args = [velocity])
            acc.start()
