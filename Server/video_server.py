import socket
import cv2
import pickle 
import struct
import imutils
from threading import Thread
from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import pyshine as ps

# Constants for video transfer
VIDEO_HOST = '192.168.90.79'
VIDEO_PORT = 54321

# Constants for command listening
COMMAND_HOST = '192.168.90.79'
COMMAND_PORT = 12345

# Constants for audio transfer
AUDIO_HOST = '192.168.90.79'
AUDIO_PORT = 49820

class VideoServer:
    def _init_(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((VIDEO_HOST, VIDEO_PORT))
        self.server_socket.listen(5)
        print("Video server listening on {}:{}".format(VIDEO_HOST, VIDEO_PORT))

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print("Video client connected from {}".format(addr))

            video_thread = Thread(target=self.handle_video, args=(client_socket,))
            video_thread.start()

    def handle_video(self, client_socket):
        vid = cv2.VideoCapture(0)

        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            
            # Serialize the frame using pickle
            frame_data = pickle.dumps(frame)

            # Get the size of the serialized frame
            frame_size = len(frame_data)

            # Pack the frame size as a 4-byte unsigned long long integer
            packed_frame_size = struct.pack("L", frame_size)

            # Send the packed frame size to the client
            client_socket.sendall(packed_frame_size)

            # Send the frame data to the client
            client_socket.sendall(frame_data)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        client_socket.close()

class CommandServer:
    def _init_(self):
        self.factory = PiGPIOFactory()

        self.servo = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=self.factory)
        self.host = '192.168.90.79'
        self.port = 12345
        self.angle = 0

    def rotate_servo(self):
        while True:
            self.servo.angle = self.angle
            sleep(0.1)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        server_socket.listen(5)
        print("Server listening on {}:{}".format(self.host, self.port))

        while True:
            client_socket, addr = server_socket.accept()
            print("Client connected from {}".format(addr))

            # Create a thread for handling the client's messages
            client_thread = Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
    
    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            if data == 'LEFT' and self.angle >= -0.95:
                self.angle -= 0.05
                self.servo.value = (self.angle)
                #self.servo.angle = self.angle
            
            elif data == 'RIGHT' and self.angle <=0.95:
                self.angle += 0.05
                self.servo.value = (self.angle)
                #self.servo.angle = self.angle
            
            #elif data == "F":
            #    forward()
            #elif data == "B":
            #    backward()
            #elif data == "L":
            #    left()
            #elif data == "R":
            #    right()
            else:
                continue

        # Close the connection with the client
        client_socket.close()

    def start(self):
        # Create a thread for rotating the servo
        #servo_thread = Thread(target=self.rotate_servo)
        #servo_thread.start()

        # Start the server
        self.start_server()

        #client_socket.close()

class AudioServer:
    def _init_(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((AUDIO_HOST, AUDIO_PORT))
        self.server_socket.listen(5)
        self.mode='send'
        print("Audio server listening on {}:{}".format(AUDIO_HOST, AUDIO_PORT))
        self.audio,self.context = ps.audioCapture(mode=self.mode)

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print("Audio client connected from {}".format(addr))

            audio_thread = Thread(target=self.handle_audio, args=(client_socket,))
            audio_thread.start()

    def handle_audio(self, client_socket):
        while True:
            audio_data = self.audio.get()
            audio_data_bytes = pickle.dumps(audio_data)

            # Pack the audio data size as a 4-byte unsigned long long integer
            audio_data_size = struct.pack("Q", len(audio_data_bytes))

            # Send the packed audio data size to the client
            client_socket.sendall(audio_data_size)

            # Send the audio data to the client
            client_socket.sendall(audio_data_bytes)

        client_socket.close()

# Create instances of the servers
video_server = VideoServer()
command_server = CommandServer()
audio_server = AudioServer()

# Start the servers in separate threads
video_thread = Thread(target=video_server.start)
command_thread = Thread(target=command_server.start)
audio_thread = Thread(target=audio_server.start)

video_thread.start()
command_thread.start()
audio_thread.start()