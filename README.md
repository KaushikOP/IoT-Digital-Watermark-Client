# IoT-Digital-Watermark-Client

Project: IoT-Digital-Watermark-Client
com/iot-digital-watermark/
│
├── client/
│   ├── __init__.py
│   ├── client.py               # Main entry point for the client
│   └── file_handler.py         # Handles file operations (retrieving, organizing)
│
├── utils/
│   ├── __init__.py
│   ├── communication.py        # Handles socket communication
│   ├── constants.py            # Stores constants (like IP, port, paths)
│   └── encryption.py           # Handles encryption/decryption logic
│
├── watermark/
│   ├── __init__.py
│   ├── embedding.py            # Logic for embedding watermark
│
├── setup.py                    # Setup script for package installation
├── requirements.txt            # List of Python dependencies
├── README.md                   # Documentation for the project
└── main.py                     # Runs the client
