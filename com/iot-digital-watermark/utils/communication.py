# utils/communication.py
import socket

class ClientCommunication:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '192.168.137.1'
        self.server_port = 12345
        self.ttl = 60

    def connect_to_server(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")
        return self.client_socket

    def send_data(self, client_socket, data):
        # Logic to send file to the client
        print(f"Sending file {data} to client...")
        client_socket.send(f"{data}".encode()) 

    def send_file(self, client_socket, file):
        print("Sending media")
        try:
            for chunk in file:
                client_socket.send(chunk)
                 
            print("file sent successfully")
        except Exception as e:
            print(f"Error sending file: {e}")

    def receive_data(self, client_socket):
        # Logic to send file to the client
        data = client_socket.recv(1024).decode()
        print(f"Received data {data} from server...")
        return data

    def receive_file(self, client_socket, file):
        print("Receiving media")
        # try:
        #     # for chunk in file:
        #     #     client_socket.send(chunk)
                 
        #     # print("file sent successfully")
        # except Exception as e:
        #     print(f"Error sending file: {e}")

    def close_client(self):
        self.client_socket.close()