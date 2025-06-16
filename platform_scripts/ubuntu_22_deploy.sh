#!/bin/bash
set -e

# Log file setup
LOG_FILE="/var/log/mood_checker_deployment.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "Starting Project Mood Check Deployment for Ubuntu 22.04..."

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    python3-tk \
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

# Create application directory
APP_DIR="/opt/Project_Mood_Check"
sudo mkdir -p "$APP_DIR"

# Copy application files
echo "Copying application files..."
sudo cp mood_checker_tkinter.py requirements.txt "Shorthills Logo Light Bg.png" "$APP_DIR/"

# Set up virtual environment
echo "Setting up virtual environment..."
cd "$APP_DIR"
sudo python3.10 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Create desktop entry
DESKTOP_ENTRY="/usr/share/applications/mood-checker.desktop"
echo "Creating desktop entry..."
sudo tee "$DESKTOP_ENTRY" << EOF
[Desktop Entry]
Version=1.0
Name=Project Mood Check
Comment=Employee Mood Tracking Application
Exec=/opt/Project_Mood_Check/venv/bin/python3 /opt/Project_Mood_Check/mood_checker_tkinter.py
Icon=/opt/Project_Mood_Check/Shorthills Logo Light Bg.png
Terminal=false
Type=Application
Categories=Utility;
EOF

# Set up autostart for all users
sudo mkdir -p /etc/skel/.config/autostart
sudo cp "$DESKTOP_ENTRY" /etc/skel/.config/autostart/

# Set permissions
sudo chmod +x "$APP_DIR/mood_checker_tkinter.py"
sudo chmod 755 "$DESKTOP_ENTRY"

echo "Ubuntu deployment completed successfully!"
exit 0 