import socket
import cv2
import pickle
import struct
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from threading import Thread
import pyshine as ps


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.114.79'  
video_port = 54321
command_port = 12345
client_socket.connect((host_ip, video_port))
client_socket1.connect((host_ip, command_port))


window = tk.Tk()
window.title("Video Streaming")


video_label = tk.Label(window)
video_label.pack(padx=10, pady=10)

def send_command(command):
    client_socket1.sendall(command.encode())

def left_button_click():
    send_command("RIGHT")

def right_button_click():
    send_command("LEFT")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14, "bold"), foreground="blue", background="#4CAF50")

left_button = ttk.Button(window, text="Left", command=left_button_click, width=10)
left_button.pack(side=tk.LEFT, padx=10, pady=10)

right_button = ttk.Button(window, text="Right", command=right_button_click, width=10)
right_button.pack(side=tk.RIGHT, padx=10, pady=10)

def receive_video():
    
    data = b""
    Data = struct.calcsize("L")

    while True:
        while len(data) < Data:
            packet = client_socket.recv(4*1024)  
            if not packet:
                break
            data += packet

        packed_msg_size = data[:Data]
        data = data[Data:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_scaled = cv2.resize(frame_rgb, (1024, 720))

        img = Image.fromarray(frame_scaled)
        img_tk = ImageTk.PhotoImage(image=img)
        video_label.configure(image=img_tk)
        video_label.image = img_tk

        window.update()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    client_socket.close()
def receive_audio():
    mode =  'get'
    name = 'CLIENT RECEIVING AUDIO'
    audio,context = ps.audioCapture(mode=mode)
    ps.showPlot(context,name)

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.114.79'

    port = 49820
    socket_address = (host_ip,port)
    client_socket.connect(socket_address)

    print("CLIENT CONNECTED TO",socket_address)

    data = b""
    Data = struct.calcsize("L")

    while True:
        while len(data) < Data:
            packet = client_socket.recv(8*1048) 
            if not packet:break
            data+=packet
        packed_msg_size = data[:Data]
        data = data[Data:]
        msg_size = struct.unpack("L",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(8*1048)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        audio.put(frame)

    client_socket.close()

audio_thread = Thread(target=receive_audio)
audio_thread.start()
video_thread = Thread(target=receive_video)
video_thread.start()

window.mainloop()
