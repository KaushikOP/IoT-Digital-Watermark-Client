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
from watermarking.embedding import WatermarkEmbedding
from utils import constants

class WatermarkClient:
    def __init__(self):
        self.communication = ClientCommunication()
        self.file_handler = FileHandler()
        self.embedding = WatermarkEmbedding()
        self.host_media = ''
        self.watermark = ''
        self.watermarked_media = ''

    def start(self):
        print("Starting Watermark Client...")
        client_socket = self.communication.connect_to_server()

        try:
            while True:
                print("\n\nWaiting for server...\n")
                command = self.receive_data_from_server(client_socket)
                if not command:
                    break  # Connection closed by server

                print(f"Command received from server: {command}")

                if command in ["c1","c2","c3"]:
                    if command == "c1":
                        print("Getting a new Host media")
                        file = self.receive_data_from_server(client_socket)
                        file_size = int(self.receive_data_from_server(client_socket))
                        print(file_size)
                        if file_size is not None:
                            self.send_data_to_server(client_socket,"ACK")
                        file_chunks =  self.communication.receive_file(client_socket,file_size)
                        if file_chunks is not None:
                            self.send_data_to_server(client_socket,"ACK")
                        self.file_handler.save_media(file_chunks, constants.HOST_MEDIA_DIR + file)
                        self.host_media = file

                    if command == "c2":
                        print("Getting a new watermark")
                        file = self.receive_data_from_server(client_socket)
                        file_size = int(self.receive_data_from_server(client_socket))
                        print(file_size)
                        if file_size is not None:
                             self.send_data_to_server(client_socket,"ACK")
                        file_chunks =  self.communication.receive_file(client_socket,file_size)
                        if file_chunks is not None:
                            self.send_data_to_server(client_socket,"ACK")
                        self.file_handler.save_media(file_chunks, constants.WATERMARK_DIR + file)
                        self.watermark = file

                    if command == "c3":
                        avail_host_media = FileHandler.read_files_from_directory(constants.HOST_MEDIA_DIR)
                        avail_watermark = FileHandler.read_files_from_directory(constants.WATERMARK_DIR)
                        if(self.host_media == ""):
                            self.host_media = avail_host_media[0]
                        if(self.watermark == ""):
                            self.watermark = avail_watermark[0]
                        
                        print("Performing Watermark Embedding using host media as " + self.host_media + " and watermark as " + self.watermark)
                        if(input("Press n to change... $..: ") in ['n','N']):
                            print(" Selecting a new file...")
                            try:
                                print(' '.join(f'{i} {item}' for i, item in enumerate(avail_host_media)))
                                tmp=int(input("Please input the number of media to be used...$..: "))
                                if(tmp <= len(avail_host_media)):
                                    self.host_media = avail_host_media[tmp]
                                
                                print(' '.join(f'{i} {item}' for i, item in enumerate(avail_watermark)))
                                tmp=int(input("Please input the media number to be used...$..: "))
                                if(tmp <= len(avail_watermark)):
                                    self.watermark = avail_watermark[tmp]

                            except Exception:
                                print(Exception.with_traceback())
                        
                        self.watermarked_media = WatermarkEmbedding.embedding(self, self.host_media, self.watermark)

                        self.send_data_to_server(client_socket, self.watermarked_media)
                        print("Sending file to server\n")
                        file = constants.WATERMARKED_MEDIA_DIR + self.watermarked_media
                        self.send_media_to_server(client_socket, file)

                        print("Now using host media as " + self.host_media + " and watermark as " + self.watermark)

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
        print("Receiving Media")
        
if __name__ == "__main__":
    client = WatermarkClient()
    client.start()