#!/bin/bash
set -e

# Log file setup
LOG_FILE="/var/log/mood_checker_deployment.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1

echo "Starting Project Mood Check Deployment for macOS M1..."

# Check for Homebrew and install if needed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python 3.10 for M1
echo "Installing Python 3.10..."
brew install python@3.10

# Install Tkinter for M1
echo "Installing Tkinter..."
brew install python-tk@3.10

# Create application directory
APP_DIR="/Applications/Project_Mood_Check"
sudo mkdir -p "$APP_DIR"

# Copy application files
echo "Copying application files..."
sudo cp mood_checker_tkinter.py requirements.txt "Shorthills Logo Light Bg.png" "$APP_DIR/"

# Set up virtual environment
echo "Setting up virtual environment..."
cd "$APP_DIR"
sudo /opt/homebrew/bin/python3.10 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Create application launcher
cat > "$APP_DIR/launch.command" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python3 mood_checker_tkinter.py
EOF

# Set permissions
sudo chmod +x "$APP_DIR/launch.command"
sudo chmod +x "$APP_DIR/mood_checker_tkinter.py"

# Create Applications shortcut
PLIST_FILE="$HOME/Library/LaunchAgents/com.project.moodcheck.plist"
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.project.moodcheck</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Applications/Project_Mood_Check/launch.command</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF

# Load the launch agent
launchctl load "$PLIST_FILE"

echo "macOS M1 deployment completed successfully!"
exit 0 