import subprocess
import sys
import os
import time

def start_background_service():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mood_checker_background.py')
    return subprocess.Popen([sys.executable, script_path])

def start_main_app():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mood_checker_tkinter.py')
    return subprocess.Popen([sys.executable, script_path])

def main():
    print("Starting Mood Checker application...")
    
    # Start the background service
    background_process = start_background_service()
    
    # Start the main application
    main_app = start_main_app()
    
    try:
        # Wait for the main app to finish
        main_app.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Cleanup
        if background_process.poll() is None:
            background_process.terminate()
        if main_app.poll() is None:
            main_app.terminate()

if __name__ == "__main__":
    main() 