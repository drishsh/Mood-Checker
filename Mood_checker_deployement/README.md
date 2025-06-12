# Mood Check Application (v1.2)

A Python-based application built with Tkinter for tracking employee moods and generating notifications. This version uses Tkinter and Pillow for the GUI interface, providing a lightweight and native look and feel.

## Features

* Employee mood tracking with emoji-based selection
* Smooth circular buttons with hover effects
* CSV data storage for mood data
* Animated mood transitions
* Native GUI interface built with Tkinter
* Notification system
* Shorthills branding integration

## Requirements

* Python 3.x
* Tkinter (usually comes with Python)
* Pillow (for image handling)
* Additional dependencies listed in requirements.txt

## Setup

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

## Project Structure

* `mood_checker_tkinter.py`: Main application file with Tkinter implementation
* `employee_mood_data.csv`: Data storage for employee moods
* `Shorthills Logo Light Bg.png`: Application logo
* `last_notification.txt`: Notification tracking file

## Changes in v1.2

* Migrated from PySide6 to Tkinter for better native integration
* Improved button aesthetics with perfect circular shapes
* Enhanced animation system
* Optimized performance with reduced dependencies
* Added hover effects and smooth color transitions

## License

MIT License 