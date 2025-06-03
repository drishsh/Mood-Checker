# Mood Check Application Deployment Script for Intune
# This script installs and configures the Mood Check application

# Error handling
$ErrorActionPreference = "Stop"
$LogFile = "$env:ProgramData\MoodCheck\install.log"

function Write-Log {
    param($Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogFile -Value $LogMessage
    Write-Host $LogMessage
}

try {
    # Create installation directory
    $InstallDir = "$env:ProgramFiles\MoodCheck"
    $DataDir = "$env:ProgramData\MoodCheck"
    
    Write-Log "Creating installation directories..."
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

    # Install Python if not present
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Log "Installing Python..."
        $PythonUrl = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
        $PythonInstaller = "$env:TEMP\python-installer.exe"
        Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonInstaller
        Start-Process -FilePath $PythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        Remove-Item $PythonInstaller
    }

    # Copy application files
    Write-Log "Copying application files..."
    $RequiredFiles = @(
        "pyside6new.py",
        "requirements.txt",
        "Shorthills Logo Light Bg.png"
    )

    foreach ($file in $RequiredFiles) {
        Copy-Item -Path "$PSScriptRoot\$file" -Destination "$InstallDir\" -Force
    }

    # Install Python dependencies
    Write-Log "Installing Python dependencies..."
    Start-Process -FilePath "python" -ArgumentList "-m", "pip", "install", "-r", "$InstallDir\requirements.txt" -Wait

    # Create startup task
    Write-Log "Creating startup task..."
    $Action = New-ScheduledTaskAction -Execute "pythonw.exe" -Argument "`"$InstallDir\main.py`""
    $Trigger = New-ScheduledTaskTrigger -AtLogOn
    $Principal = New-ScheduledTaskPrincipal -GroupId "BUILTIN\Users" -RunLevel Highest
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden
    
    Register-ScheduledTask -TaskName "MoodCheck" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force

    # Create data files if they don't exist
    $DataFiles = @(
        @{
            Name = "employee_mood_data.csv"
            Content = "Timestamp,Username,Mood,State`n"
        },
        @{
            Name = "last_notification.txt"
            Content = ""
        }
    )

    foreach ($file in $DataFiles) {
        $FilePath = Join-Path $DataDir $file.Name
        if (-not (Test-Path $FilePath)) {
            $file.Content | Out-File -FilePath $FilePath -Encoding UTF8
        }
    }

    # Create uninstall script
    $UninstallScript = @"
Remove-Item -Path "$InstallDir" -Recurse -Force
Remove-Item -Path "$DataDir" -Recurse -Force
Unregister-ScheduledTask -TaskName "MoodCheck" -Confirm:`$false
"@
    $UninstallScript | Out-File -FilePath "$InstallDir\uninstall.ps1" -Encoding UTF8

    Write-Log "Installation completed successfully!"
    exit 0
} catch {
    Write-Log "Error: $_"
    exit 1
} 