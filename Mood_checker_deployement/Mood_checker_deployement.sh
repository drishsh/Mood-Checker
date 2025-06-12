#!/bin/bash
set -e

echo "Starting Mood Checker Tkinter Deployment..."

# Install system dependencies for Tkinter and Pillow
# (Tkinter is usually included with python3-tk, Pillow needs libjpeg, zlib, etc.)
echo "Installing system dependencies for Tkinter and Pillow..."
sudo apt-get update
sudo apt-get install -y \
    python3-tk \
    python3-venv \
    python3-pip \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "pillow" > requirements.txt
fi

# Install Python packages
echo "Installing Python packages..."
pip install -r requirements.txt

# Run the application
echo "Starting the application..."
python3 mood_checker_tkinter.py

# Deactivate virtual environment
deactivate

echo "Deployment complete!" 