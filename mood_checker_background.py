import time
import subprocess
import sys
import os
from datetime import datetime, timedelta
import getpass
from mood_checker_tkinter import (
    get_last_close_time,
    has_mood_saved_today,
    initialize_files
)

def run_mood_checker():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mood_checker_tkinter.py')
    subprocess.Popen([sys.executable, script_path])

def check_and_show_window():
    last_close = get_last_close_time()
    if last_close is None:
        return
    
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    # If it's been 3 hours since last close and no mood saved today
    if (current_time - last_close) >= three_hours_in_seconds and not has_mood_saved_today():
        run_mood_checker()
        time.sleep(1)  # Wait a bit to avoid multiple instances

def main():
    initialize_files()
    
    print("Starting mood checker background service...")
    
    while True:
        try:
            check_and_show_window()
            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            print(f"Error in background service: {e}")
            time.sleep(300)  # Continue checking even if there's an error

if __name__ == "__main__":
    main() 