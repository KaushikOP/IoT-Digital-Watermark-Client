# server/file_handler.py

class FileHandler:
    def receive_file(self, client_socket):
        file_name = 'data/received_file'
        with open(file_name, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        return file_name

    def process_and_store(self, file_name):
        # Logic to move processed data to another directory
        print(f"Processing and storing {file_name}...")

# client/file_handler.py

class FileHandler:
    def get_host_media_path(self):
        return 'data/host_media/sample_file.jpg'

    # Additional file handling logic as needed
