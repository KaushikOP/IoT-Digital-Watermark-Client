# client/client.py

import sys
import os
import time

# Add the root of the project (iot-digital-watermark) to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from utils.communication import ClientCommunication
from file_handler import FileHandler
from watermark.embedding import WatermarkEmbedding
from utils import constants

class WatermarkClient:
    def __init__(self):
        self.communication = ClientCommunication()
        self.file_handler = FileHandler()
        self.embedding = WatermarkEmbedding()

    def start(self):
        print("Starting Watermark Client...")
        client_socket = self.communication.connect_to_server()

        try:
            while True:
                command = self.receive_data_from_server(client_socket)
                if not command:
                    break  # Connection closed by server

                print(f"Command received from server: {command}")

                if command in ["c1","c2","c3"]:
                    if command == "c1":
                        print("Getting a new Host media")
                        file = self.receive_data_from_server(client_socket)
                        print(file)
                        exit()
                        file_size = self.receive_data_from_server(client_socket)
                        if file_size is not None:
                            self.send_data_to_server(client_socket,"ACK")
                        file_chunks =  self.file_handler.receive_file(client_socket,file_size)
                        if file_chunks is not None:
                            self.send_data_to_server(client_socket,"ACK")
                        self.file_handler.save_media(file_chunks, constants.HOST_MEDIA_DIR)

                    if command == "c2":
                        print("Getting a new watermark")
                    if command == "c3":
                        print("Performing Watermark Embedding")
                if command == "close_connection":
                    print("Closing connection as requested by server.")
                    break
                # else:
                #     #self.execute_command(command)

        except KeyboardInterrupt:
            print("\nClient stopped by user.")
        finally:
            self.communication.close_client()

    def send_data_to_server(self, client_socket, data=None):
        self.communication.send_data(client_socket, data)
        # file_path = self.file_handler.get_host_media()
        # watermarked_file_path = self.embedding.embed_watermark(file_path)
        # self.communication.send_file(watermarked_file_path)

    def send_media_to_server(self, client_socket, file):
        file_size,file = self.file_handler.load_media(file)
        self.communication.send_data(file_size)
        
        ack = self.communication.receive_data()
        if ack != "ACK":
            print("Acknowledgment not received. Terminating transfer.")
            ack=None
            exit
        self.communication.send_file(client_socket, file)
        ack = self.communication.receive_data()
        if ack != "ACK":
            print("Acknowledgment not received. Terminating transfer.")
            ack=None
            exit
        # file_path = self.file_handler.get_host_media()
        # watermarked_file_path = self.embedding.embed_watermark(file_path)
        # self.communication.send_file(watermarked_file_path)

    def receive_data_from_server(self, client_socket):
        #received_file_path = self.communication.receive_file()
        data = self.communication.receive_data(client_socket)
        return data

    def receive_media_from_server(self, client_socket, file_size):
        #received_file_path = self.communication.receive_file()
        

if __name__ == "__main__":
    client = WatermarkClient()
    client.start()
