# Project Mood Check (v1.2)

A Python-based application built with Tkinter for tracking employee moods and generating notifications. This version uses Tkinter and Pillow for the GUI interface, providing a lightweight and native look and feel.

## Features

* Employee mood tracking with emoji-based selection
* Smooth circular buttons with hover effects
* CSV data storage for mood data
* Animated mood transitions
* Native GUI interface built with Tkinter
* Notification system
* Shorthills branding integration
* Cross-platform deployment support (Windows 11, Ubuntu 22.04, macOS M1)

## Requirements

* Python 3.x
* Tkinter (usually comes with Python)
* Pillow (for image handling)
* Additional dependencies listed in requirements.txt

## Local Setup

1. Clone the repository
2. Switch to version 1.2 branch:
   ```bash
   git checkout version-1.2
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python mood_checker_tkinter.py
   ```

## Enterprise Deployment

### Platform-Specific Deployment Scripts

The application includes deployment scripts for three major platforms:

#### Windows 11 Deployment
1. Open PowerShell as Administrator
2. Navigate to the project directory
3. Run the Windows deployment script:
   ```powershell
   .\platform_scripts\windows_11_deploy.ps1
   ```
- Installs Python 3.10 if not present
- Creates application directory in Program Files
- Sets up virtual environment
- Creates Start Menu and startup shortcuts
- Logs deployment process to `C:\ProgramData\MoodChecker\deployment.log`

#### Ubuntu 22.04 Deployment
1. Open Terminal
2. Navigate to the project directory
3. Run the Ubuntu deployment script:
   ```bash
   sudo bash platform_scripts/ubuntu_22_deploy.sh
   ```
- Installs system dependencies
- Creates application directory in /opt
- Sets up virtual environment
- Creates desktop entry and autostart
- Logs deployment process to `/var/log/mood_checker_deployment.log`

#### macOS M1 Deployment
1. Open Terminal
2. Navigate to the project directory
3. Run the macOS deployment script:
   ```bash
   sudo bash platform_scripts/macos_m1_deploy.sh
   ```
- Installs Homebrew and Python 3.10
- Creates application in /Applications
- Sets up virtual environment
- Creates launch agent for autostart
- Logs deployment process to `/var/log/mood_checker_deployment.log`

### Installation Locations

- Windows: `C:\Program Files\Project_Mood_Check`
- Ubuntu: `/opt/Project_Mood_Check`
- macOS: `/Applications/Project_Mood_Check`

### Logging

All deployment scripts include detailed logging:
- Windows: `C:\ProgramData\MoodChecker\deployment.log`
- Ubuntu: `/var/log/mood_checker_deployment.log`
- macOS: `/var/log/mood_checker_deployment.log`

### Troubleshooting

#### Windows
- Check Windows Event Viewer for Python installation issues
- Verify PowerShell execution policy allows script execution
- Ensure administrative privileges

#### Ubuntu
- Check system logs: `sudo journalctl -xe`
- Verify Python and Tkinter installation: `python3 -m tkinter`
- Check desktop entry permissions

#### macOS
- Check system logs: `console.app`
- Verify Homebrew installation: `brew doctor`
- Check launch agent status: `launchctl list | grep moodcheck`

## Project Structure

* `mood_checker_tkinter.py`: Main application file
* `platform_scripts/`: Platform-specific deployment scripts
  * `windows_11_deploy.ps1`: Windows 11 deployment script
  * `ubuntu_22_deploy.sh`: Ubuntu 22.04 deployment script
  * `macos_m1_deploy.sh`: macOS M1 deployment script
* `requirements.txt`: Python package dependencies
* `Shorthills Logo Light Bg.png`: Application logo
* `TESTING.md`: Testing documentation
* `test_mood_checker_tkinter.py`: Test suite

## Changes in v1.2

* Added cross-platform deployment scripts
* Migrated from PySide6 to Tkinter for better native integration
* Improved button aesthetics with perfect circular shapes
* Enhanced animation system
* Optimized performance with reduced dependencies
* Added hover effects and smooth color transitions

## License

MIT License 