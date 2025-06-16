# Windows 11 Deployment Script for Project Mood Check
# Run as Administrator

# Enable logging
$LogFile = "C:\ProgramData\MoodChecker\deployment.log"
$LogDir = Split-Path $LogFile -Parent
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}
Start-Transcript -Path $LogFile -Append

Write-Host "Starting Project Mood Check Deployment for Windows 11..."

# Check for Python installation and install if needed
$pythonUrl = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
$pythonInstaller = "$env:TEMP\python-3.10.0-amd64.exe"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Python 3.10..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    Remove-Item $pythonInstaller
}

# Create application directory
$AppDir = "C:\Program Files\Project_Mood_Check"
if (-not (Test-Path $AppDir)) {
    New-Item -ItemType Directory -Path $AppDir | Out-Null
}

# Copy application files
Write-Host "Copying application files..."
Copy-Item "mood_checker_tkinter.py", "requirements.txt", "Shorthills Logo Light Bg.png" -Destination $AppDir

# Set up virtual environment
Write-Host "Setting up virtual environment..."
Set-Location $AppDir
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Create shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Project Mood Check.lnk")
$Shortcut.TargetPath = "$AppDir\venv\Scripts\pythonw.exe"
$Shortcut.Arguments = "$AppDir\mood_checker_tkinter.py"
$Shortcut.WorkingDirectory = $AppDir
$Shortcut.IconLocation = "$AppDir\Shorthills Logo Light Bg.png"
$Shortcut.Save()

# Create startup shortcut for all users
Copy-Item "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Project Mood Check.lnk" `
          "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"

Write-Host "Windows deployment completed successfully!"
Stop-Transcript 