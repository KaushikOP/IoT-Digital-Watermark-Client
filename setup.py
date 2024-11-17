from setuptools import setup, find_packages

# Project name
project_name = "IoT-Digital-Watermark-Client"

# Author details
author = "Kaushik Talathi"
author_email = "kaushiktalathi@gmail.com"

# Short description of your project
description = "Project for handling digital watermarking on IoT devices using a client-server model"

# List of external libraries your code depends on
# Add packages as needed, for example, if you use 'requests', include it in the list
requirements = [
    "numpy",  # Add all necessary dependencies here
    "opencv-python",
    "pywavelets",
    "cryptography",
    # Add more libraries as per your project's requirements
]

setup(
    name=project_name,
    version="0.1.0",  # Update version number as needed
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),  # Automatically find packages
    author=author,
    author_email=author_email,
    description=description,
    install_requires=requirements,  # Dependencies to install
)
