import socket
import subprocess
from time import sleep
def execute_shell_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        return str(e.output)
    
def send_message_to_server(message, host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    while True:
        flag = input("File already exists? yes/no ")
        if flag =='yes':
            msg = input("enter the file to broadcast  ")
            #cmd = f"scp {msg} amrita2023@192.168.114.79:/home/amrita2023/radio/fm_transmitter-master"
            #execute_shell_command(cmd)
            #sleep(1)
            message = message+msg
            client_socket.sendall(message.encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")
            print(f"Server response: {response}")

        if flag =='no':
            msg = input("enter the file to transmit and broadcast ")
            cmd = f"scp {msg} LAPTOP-1P94RCJ2@192.168.114.79:/home/amrita2023/radio/fm_transmitter-master"
            execute_shell_command(cmd)
            sleep(1)
            message = message+msg
            client_socket.sendall(message.encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")
            print(f"Server response: {response}")
        

       # client_socket.close()

if __name__ == "__main__":
    HOST = "192.168.114.79"
    PORT = 54545
    message_to_send = "sudo ./fm_transmitter -f 89.9 "  
    send_message_to_server(message_to_send, HOST, PORT)
