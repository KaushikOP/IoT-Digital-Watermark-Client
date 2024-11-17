# utils/communication.py
import socket

class ClientCommunication:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '192.168.1.41'
        self.server_port = 12345
        self.ttl = 60

    def connect_to_server(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")

    def send_file(self, file_path):
        # Logic to send file to the server
        print(f"Sending file {file_path} to server")
        # Implementation to send file data over socket
        pass

    def receive_file(self):
        # Logic to receive file from the server
        print("Receiving file from server...")
        # Implementation to receive file data over socket
        return "path/to/received/file"  # Replace with actual received file path

    def close_client(self):
        self.client_socket.close()