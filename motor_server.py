import RPi.GPIO as GPIO
from time import sleep



import socket

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
#GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
#GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
#GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse


def stop():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    GPIO.output(17, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.cleanup()

def backward():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    sleep(1)
    GPIO.cleanup()
    stop()

def forward():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    GPIO.output(17, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    sleep(1)
    GPIO.cleanup()
    stop()
    
def right():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    #GPIO.output(17, GPIO.LOW)
    #GPIO.output(23, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    sleep(1)
    GPIO.cleanup()
    stop()
    
def left():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    #GPIO.output(17, GPIO.HIGH)
    #GPIO.output(23, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    sleep(1)
    GPIO.cleanup()
    stop()

def complement_left():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    GPIO.output(17, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)
    sleep(1)
    GPIO.cleanup()
    stop()

def complement_right():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Motor 1 - Forward
    GPIO.setup(23, GPIO.OUT)  # Motor 1 - Reverse
    GPIO.setup(27, GPIO.OUT)  # Motor 2 - Forward
    GPIO.setup(22, GPIO.OUT)  # Motor 2 - Reverse
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)
    sleep(1)
    GPIO.cleanup()
    stop()



all_commands=[]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.5.79'  
port = 12347


server_socket.bind((host, port))


server_socket.listen()

print('Server is listening for incoming connections...')
stop()
while True:
  
    client_socket, address = server_socket.accept()
    print('Connected to', address)

    while True:
        data = client_socket.recv(1024).decode()
        print('Received data:', data)
        all_commands.append(data)

        if data == 'F':
            forward()
        elif data == 'B':
            backward()
        elif data == 'R':
            right()
        elif data == 'L':
            left()
        elif data == 'S':
            stop()
        elif data=="panic":
            for i in range(len(all_commands)-1,-1,-1):
                if all_commands[i]=="F":
                    backward()
                if all_commands[i]=="B":
                    forward()
                if all_commands[i]=="R":
                    complement_right()
                if all_commands[i]=="L":
                    complement_left()

            all_commands.clear()
            

        elif data == 'SHUTDOWN':
            break

client_socket.close()