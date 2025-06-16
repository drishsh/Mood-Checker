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
* Microsoft Intune deployment support for enterprise-wide installation

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

## Enterprise Deployment with Microsoft Intune

### Prerequisites
* Microsoft Intune admin access
* Ubuntu Linux systems (target machines)
* Git installed on deployment machine

### Deployment Steps

1. **Prepare the Package**:
   ```bash
   # Clone the repository
   git clone https://github.com/drishsh/Mood-Checker.git
   cd Mood-Checker
   git checkout version-1.2
   ```

2. **In Microsoft Endpoint Manager Admin Center**:
   1. Go to Apps > All apps > Add
   2. Select "Line-of-business app" as the app type
   3. Select "Other" as the app type
   4. Upload the following files:
      * mood_checker_tkinter.py
      * Mood_checker_deployement.sh
      * requirements.txt
      * Shorthills Logo Light Bg.png

3. **Configure App Information**:
   * Name: Project Mood Check
   * Description: Employee Mood Tracking Application
   * Publisher: Your Company Name
   * App Version: 1.2
   * Category: Business

4. **Program Settings**:
   * Installation command: `sudo bash Mood_checker_deployement.sh`
   * Installation behavior: System
   * Device restart behavior: No restart required

5. **Requirements**:
   * Operating system architecture: 64-bit
   * Minimum operating system: Ubuntu 20.04 or later

6. **Detection Rules**:
   * Rule type: File exists
   * Path: /opt/Project_Mood_Check
   * File or folder: mood_checker_tkinter.py
   * Detection method: File or folder exists

7. **Assignments**:
   * Required: Select your target group of devices
   * Available for enrolled devices: Yes

### Post-Deployment

The application will:
* Install automatically on target systems
* Create desktop shortcuts for all users
* Auto-start with system boot
* Store data in `/opt/Project_Mood_Check`

### Troubleshooting

* Check logs at `/var/log/mood_checker_deployment.log`
* Verify installation at `/opt/Project_Mood_Check`
* Check desktop entry at `/usr/share/applications/mood-checker.desktop`

## Project Structure

* `mood_checker_tkinter.py`: Main application file with Tkinter implementation
* `Mood_checker_deployement.sh`: Enterprise deployment script
* `requirements.txt`: Python package dependencies
* `Shorthills Logo Light Bg.png`: Application logo
* `TESTING.md`: Testing documentation
* `test_mood_checker_tkinter.py`: Test suite

## Changes in v1.2

* Migrated from PySide6 to Tkinter for better native integration
* Improved button aesthetics with perfect circular shapes
* Enhanced animation system
* Optimized performance with reduced dependencies
* Added hover effects and smooth color transitions
* Added enterprise deployment support via Microsoft Intune

## License

MIT License 