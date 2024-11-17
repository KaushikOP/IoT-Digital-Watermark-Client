# client/client.py

import sys
import os

# Add the root of the project (iot-digital-watermark) to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from utils.communication import ClientCommunication
from file_handler import FileHandler
from watermark.embedding import WatermarkEmbedding

class WatermarkClient:
    def __init__(self):
        self.communication = ClientCommunication()
        self.file_handler = FileHandler()
        self.embedding = WatermarkEmbedding()

    def start(self):
        print("Starting Watermark Client...")
        self.communication.connect_to_server()

        try:
            while True:
                # Optionally receive data from the server
                self.receive_data_from_server()

                # Send data to the server
                self.send_data_to_server()

            
        except KeyboardInterrupt:
            print("\nClient stopped by user.")
        finally:
            self.communication.close_client()

    def send_data_to_server(self):
        self.communication.client_socket.send(b"Hello")
        # file_path = self.file_handler.get_host_media()
        # watermarked_file_path = self.embedding.embed_watermark(file_path)
        # self.communication.send_file(watermarked_file_path)

    def receive_data_from_server(self):
        #received_file_path = self.communication.receive_file()
        received_file_path = self.communication.client_socket.recv(1024).decode()
        if received_file_path:
            print(f"Received file from server: {received_file_path}")

if __name__ == "__main__":
    client = WatermarkClient()
    client.start()
