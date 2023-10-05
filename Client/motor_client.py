import socket
import time
from pynput import keyboard
# from pynput.keyboard import Key, Controller
# keyboard=Controller()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.5.79'  
port = 12347

client_socket.connect((host, port))
print('Connected to the server.')


def on_key_press(key):
    try:
        if key == keyboard.Key.up:
            data = "F"
            client_socket.send(data.encode())
            print('Sent data:', data)  
        elif key == keyboard.Key.down:
            data = "B"
            client_socket.send(data.encode())
            print('Sent data:', data)  
        elif key == keyboard.Key.right:
            data = "R"
            client_socket.send(data.encode())
            print('Sent data:', data) 
        elif key == keyboard.Key.left:
            data = "L"
            client_socket.send(data.encode())
            print('Sent data:', data)
       
        elif key==keyboard.Key.space:
            data="panic"
            client_socket.send(data.encode())
            print("send data:",data)

        elif key == keyboard.char == 's':
            client_socket.send(data.encode())
            print('Sent data:', data) 
            return False
          
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_key_press)

listener.start()
listener.join()
client_socket.close()