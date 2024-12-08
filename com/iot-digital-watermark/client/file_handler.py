# client/file_handler.py
import os

class FileHandler:

    def process_and_store(self, dir_name):
        # Logic to move processed data to another directory
        print(f"Processing and storing {dir_name}...")

    def load_media(self, file_path):
        if not os.path.exists(file_path):
            print("file does not exist")
            return None
        
        try:
            file_size = os.path.getsize(file_path)
            media_to_send = []
            # Send file data in chunks
            with open(file_path, "rb") as file:
                while chunk := file.read(1024):
                    media_to_send.append(chunk)
            
            return file_size,media_to_send
        except Exception as e:
            print(f"Error: {e}")
        finally:
            file.close()

    def save_media(self, file, file_path):
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save chunks to the destination file
            with open(file_path, "wb") as file:
                total_written = 0
                for chunk in file:
                    file.write(chunk)
                    total_written += len(chunk)
                
                print(f"\nFile successfully saved to {file_path}.")
            
            # # Verify if the total written size matches the expected file size
            # if total_written != file_size:
            #     print("Warning: File size mismatch! File may be incomplete.")
            #     return False
            
            return True
        except Exception as e:
            print(f"Error saving media: {e.with_traceback()}")
            return False


    
    def read_files_from_directory(dir_path):
        print("Reading files from "+ dir_path)
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.mp3', '.wav']
        if not os.path.exists(dir_path):
            print(f"Directory '{dir_path}' does not exist.")
            return []
        # Get a list of all files in the directory
        media_files = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                # If extensions are specified, filter by them
                if allowed_extensions:
                    if file.lower().endswith(tuple(allowed_extensions)):
                        media_files.append( file)
                else:
                    media_files.append( file)
        
        return media_files

    # Additional file handling logic as needed
