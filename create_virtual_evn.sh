#!/bin/bash

# Get the current working directory
CURRENT_DIR=$(pwd)

# Extract the folder name from the current directory path
FOLDER_NAME=$(basename "${CURRENT_DIR}_venv")

# Create a virtual environment with the name of the folder
python3 -m venv "${FOLDER_NAME}"

# Activate the virtual environment
source "${FOLDER_NAME}/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install required libraries
pip install requests numpy pandas ipykernel

# Deactivate the virtual environment (optional)
deactivate

echo "Virtual environment '$FOLDER_NAME' created and libraries installed."
