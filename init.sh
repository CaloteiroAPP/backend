#!/bin/bash

# Define the directory for the virtual environment
VENV_DIR=".venv"

# Check if .venv directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    virtualenv $VENV_DIR
else
    echo "Virtual environment detected."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install the requirements from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping installation of packages."
fi

echo "Setup complete."
