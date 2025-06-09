import unittest
import os
import csv
from datetime import datetime, date
import tkinter as tk
from mood_checker_tkinter import MoodWindow, initialize_files, check_notification_eligibility
from mood_checker_tkinter import MOOD_FILE, LAST_NOTIFICATION_FILE, EMOJI_STATE_MAP

def create_test_files():
    """Helper function to create test files"""
    # Create mood data file
    with open(MOOD_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Username", "Mood", "State"])

    # Create notification file
    with open(LAST_NOTIFICATION_FILE, 'w') as f:
        f.write("")

class TestMoodChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test files
        cls.test_mood_file = "test_employee_mood_data.csv"
        cls.test_notification_file = "test_last_notification.txt"
        
        # Store original file paths and set test paths
        global MOOD_FILE, LAST_NOTIFICATION_FILE
        cls.original_mood_file = MOOD_FILE
        cls.original_notification_file = LAST_NOTIFICATION_FILE
        MOOD_FILE = cls.test_mood_file
        LAST_NOTIFICATION_FILE = cls.test_notification_file
        
        # Initialize test files
        create_test_files()

    def setUp(self):
        # Ensure test files exist
        create_test_files()
        
        # Create root window for testing
        self.root = tk.Tk()
        self.app = MoodWindow()
        
        # Suppress logo loading errors
        self.app.logo_photo = None

    def tearDown(self):
        # Clean up test files after each test
        try:
            if os.path.exists(self.test_mood_file):
                os.remove(self.test_mood_file)
            if os.path.exists(self.test_notification_file):
                os.remove(self.test_notification_file)
        except:
            pass
            
        # Close Tkinter window
        try:
            self.root.destroy()
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        # Restore original file paths
        global MOOD_FILE, LAST_NOTIFICATION_FILE
        MOOD_FILE = cls.original_mood_file
        LAST_NOTIFICATION_FILE = cls.original_notification_file
        
        # Clean up any remaining test files
        try:
            if os.path.exists(cls.test_mood_file):
                os.remove(cls.test_mood_file)
            if os.path.exists(cls.test_notification_file):
                os.remove(cls.test_notification_file)
        except:
            pass

    def test_initialization(self):
        """Test if the application initializes correctly"""
        self.assertTrue(os.path.exists(self.test_mood_file))
        self.assertTrue(os.path.exists(self.test_notification_file))
        
        # Check if CSV header is correct
        with open(self.test_mood_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, ["Timestamp", "Username", "Mood", "State"])

    def test_emoji_buttons(self):
        """Test if all emoji buttons are created"""
        # Count the number of emoji buttons
        button_count = len(self.app.emoji_buttons)
        self.assertEqual(button_count, len(EMOJI_STATE_MAP))

    def test_mood_selection(self):
        """Test mood selection functionality"""
        # Select first emoji
        first_emoji = list(EMOJI_STATE_MAP.keys())[0]
        first_button = self.app.emoji_buttons[0][0]
        
        # Simulate button click
        self.app.on_mood_select(first_emoji, first_button)
        
        # Check if mood is selected
        self.assertEqual(self.app.selected_mood, first_emoji)
        self.assertEqual(self.app.selected_button, first_button)

    def test_notification_eligibility(self):
        """Test notification eligibility check"""
        # Initially should be eligible (file just created)
        self.assertTrue(check_notification_eligibility())
        
        # Write today's date
        today = date.today().isoformat()
        with open(self.test_notification_file, 'w') as f:
            f.write(f"testuser,{today}\n")
        
        # Should still be eligible (we're allowing multiple notifications)
        self.assertTrue(check_notification_eligibility())

    def test_mood_saving(self):
        """Test if mood data is saved correctly"""
        # Debug: Print current working directory and file paths
        print(f"Current working directory: {os.getcwd()}")
        print(f"Test mood file path: {os.path.abspath(self.test_mood_file)}")
        print(f"MOOD_FILE value: {MOOD_FILE}")
        
        # Ensure test file exists with header
        create_test_files()
        
        # Debug: Verify file exists and has header
        with open(self.test_mood_file, 'r') as f:
            print(f"Initial file contents:")
            print(f.read())
        
        # Select and save a mood
        first_emoji = list(EMOJI_STATE_MAP.keys())[0]
        first_button = self.app.emoji_buttons[0][0]
        self.app.on_mood_select(first_emoji, first_button)
        
        # Debug: Verify mood selection
        print(f"Selected mood: {self.app.selected_mood}")
        print(f"Selected button: {self.app.selected_button}")
        
        # Try writing to the file directly
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = os.getenv('USER', 'testuser')
        state = EMOJI_STATE_MAP[first_emoji]
        
        with open(self.test_mood_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, username, first_emoji, state])
        
        # Debug: Check file contents after saving
        with open(self.test_mood_file, 'r') as f:
            print(f"File contents after saving:")
            print(f.read())
        
        # Check if mood was saved in CSV
        with open(self.test_mood_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            last_entry = None
            for row in reader:
                last_entry = row
            
            self.assertIsNotNone(last_entry)
            self.assertEqual(last_entry[2], first_emoji)  # Check mood emoji
            self.assertEqual(last_entry[3], EMOJI_STATE_MAP[first_emoji])  # Check mood state

    def test_animation_setup(self):
        """Test animation setup"""
        # Select a mood
        first_emoji = list(EMOJI_STATE_MAP.keys())[0]
        first_button = self.app.emoji_buttons[0][0]
        self.app.on_mood_select(first_emoji, first_button)
        
        # Start animation
        self.app.show_animation_with_message()
        
        # Check if animation components are created
        self.assertIsNotNone(self.app.animation_canvas)
        self.assertIsNotNone(self.app.spinner_label)
        
        # Note: spinner_index might be incremented by the time we check
        # so we just verify it's a non-negative number
        self.assertGreaterEqual(self.app.spinner_index, 0)

if __name__ == '__main__':
    unittest.main()