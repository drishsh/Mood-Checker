# Mood Check Application - Intune Deployment Guide

## Required Files for Deployment
The following files must be included in the Intune package:
1. `deploy_mood_check.ps1` - The main deployment script
2. `main.py` - The main application
3. `requirements.txt` - Python package dependencies
4. `Shorthills Logo Light Bg.png` - Application logo

## Deployment Steps in Intune

1. Create a new Win32 App in Intune:
   - Go to Microsoft Endpoint Manager admin center
   - Navigate to Apps > Windows > Add
   - Select "Windows app (Win32)" as the app type

2. Prepare the installation package:
   - Create a folder with all required files listed above
   - Use the Microsoft Win32 Content Prep Tool to create the .intunewin file
   - Command: `IntuneWinAppUtil.exe -c <source_folder> -s deploy_mood_check.ps1 -o <output_folder>`

3. Configure the Win32 app in Intune:
   - Install command: `powershell.exe -ExecutionPolicy Bypass -File deploy_mood_check.ps1`
   - Uninstall command: `powershell.exe -ExecutionPolicy Bypass -File "%ProgramFiles%\MoodCheck\uninstall.ps1"`
   - Install behavior: System
   - Device restart behavior: No specific action

4. Detection Rules:
   Add these detection rules:
   - Rule type: File
   - Path: %ProgramFiles%\MoodCheck
   - File or folder: main.py
   - Detection method: File or folder exists
   
   AND
   
   - Rule type: Registry
   - Key path: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Schedule\TaskCache\Tree\MoodCheck
   - Value name: Id
   - Detection method: Key exists

5. Requirements:
   - Operating system architecture: x64
   - Minimum operating system: Windows 10 1903 or higher
   - Disk space required: 500 MB

6. Assignments:
   - Add the users or groups who should receive the application
   - Set the installation type as "Required"

## Post-Deployment Verification
After deployment, verify:
1. Python is installed correctly
2. The application starts automatically at user login
3. Data files are being created in %ProgramData%\MoodCheck
4. The system tray icon appears and notifications work

## Troubleshooting
Check the installation log at: `%ProgramData%\MoodCheck\install.log`

Common issues:
1. Python installation failure: Check internet connectivity and proxy settings
2. Missing dependencies: Verify requirements.txt installation
3. Startup task not running: Check Task Scheduler for errors

For support, contact: [Add your support contact information] 