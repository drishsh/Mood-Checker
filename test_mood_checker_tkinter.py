import unittest
import tkinter as tk
from tkinter import ttk
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from mood_checker_tkinter import (
    MoodWindow, 
    EMOJI_STATE_MAP
)

class TestMoodChecker(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create root window for testing
        self.root = tk.Tk()
        
        # Create app without logo
        self.app = MoodWindow()
        
        # Wait for UI to update and initialize
        self.app.update_idletasks()
        self.app.update()
        
        # Give time for emoji buttons to be created
        self.app.after(100)
        self.app.update()

    def tearDown(self):
        """Clean up after each test"""
        try:
            self.root.destroy()
        except:
            pass

    # Window Tests
    def test_window_initialization(self):
        """Test if window properties are correctly initialized"""
        self.assertEqual(self.app.title(), "Mood Check-in")
        self.assertEqual(self.app.winfo_width(), 800)
        self.assertEqual(self.app.winfo_height(), 450)
        self.assertEqual(self.app.cget('bg'), 'white')
        self.assertTrue(self.app._w)  # Check if window exists

    def test_window_center_position(self):
        """Test if window is centered on screen"""
        self.app.update_idletasks()
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        expected_x = (screen_width // 2) - (window_width // 2)
        expected_y = (screen_height // 2) - (window_height // 2)
        
        geometry = self.app.geometry()
        actual_x = int(geometry.split('+')[1])
        actual_y = int(geometry.split('+')[2])
        
        self.assertAlmostEqual(actual_x, expected_x, delta=1)
        self.assertAlmostEqual(actual_y, expected_y, delta=1)

    # UI Element Tests
    def test_emoji_buttons_creation(self):
        """Test if emoji buttons are created with correct properties"""
        # Find emoji buttons in the emoji_frame
        emoji_buttons = []
        for frame in self.app.emoji_frame.winfo_children():
            if isinstance(frame, ttk.Frame):
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Canvas):
                        emoji_buttons.append(widget)
        
        self.assertEqual(len(emoji_buttons), len(EMOJI_STATE_MAP))
        for button in emoji_buttons:
            self.assertEqual(int(button.cget('highlightthickness')), 0)
            self.assertEqual(int(button.cget('bd')), 0)
            self.assertEqual(button.cget('bg'), 'white')

    def test_emoji_button_styles(self):
        """Test emoji button styling"""
        emoji_buttons = [btn for btn in self.app.winfo_children() if isinstance(btn, tk.Canvas)]
        for button in emoji_buttons:
            # Check circle properties
            circle = button.find_withtag('oval')
            self.assertTrue(circle)
            self.assertEqual(button.itemcget(circle[0], 'fill'), '#ffd700')
            
            # Check text label
            text = button.find_withtag('text')
            self.assertTrue(text)

    def find_send_button(self):
        """Helper function to find the send button"""
        print("\nLooking for send button")
        send_button = self.app.send_button
        if send_button and isinstance(send_button, tk.Button) and send_button.cget('text') == 'Send':
            print("Found send button!")
            return send_button
        print("Send button not found!")
        return None

    def test_send_button_properties(self):
        """Test send button attributes"""
        send_button = self.find_send_button()
        self.assertIsNotNone(send_button, "Send button not found")
        self.assertEqual(send_button.cget('text'), "Send")
        self.assertEqual(send_button.cget('bg'), '#FF6F61')
        self.assertEqual(send_button.cget('fg'), 'white')

    # Error Handling Tests
    def test_error_message_on_empty_submission(self):
        """Test error handling for empty submissions"""
        # Try to submit without selecting mood
        self.app.submit_mood()
        
        # Verify error message
        self.assertEqual(self.app.selected_mood, None)
        self.assertTrue(self.app.winfo_children())  # Window still has widgets

    def test_mood_selection(self):
        """Test mood selection for all emojis"""
        for emoji in EMOJI_STATE_MAP.keys():
            button = None
            for frame in self.app.emoji_frame.winfo_children():
                if isinstance(frame, ttk.Frame):
                    for widget in frame.winfo_children():
                        if isinstance(widget, tk.Canvas):
                            for child in widget.winfo_children():
                                if isinstance(child, tk.Label) and child.cget('text') == emoji:
                                    button = widget
                                    break
            self.assertIsNotNone(button, f"Button not found for emoji {emoji}")
            self.app.on_mood_select(emoji, button)
            self.assertEqual(self.app.selected_mood, emoji)
            self.assertEqual(self.app.selected_button, button)

    def test_mood_selection_toggle(self):
        """Test toggling between different moods"""
        emojis = list(EMOJI_STATE_MAP.keys())
        first_emoji = emojis[0]
        second_emoji = emojis[1]
        
        first_button = None
        second_button = None
        
        # Find buttons
        for frame in self.app.emoji_frame.winfo_children():
            if isinstance(frame, ttk.Frame):
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Canvas):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Label):
                                if child.cget('text') == first_emoji:
                                    first_button = widget
                                elif child.cget('text') == second_emoji:
                                    second_button = widget
        
        self.assertIsNotNone(first_button, f"Button not found for emoji {first_emoji}")
        self.assertIsNotNone(second_button, f"Button not found for emoji {second_emoji}")
        
        # Select first mood
        self.app.on_mood_select(first_emoji, first_button)
        self.assertEqual(self.app.selected_mood, first_emoji)
        
        # Select second mood
        self.app.on_mood_select(second_emoji, second_button)
        self.assertEqual(self.app.selected_mood, second_emoji)

if __name__ == '__main__':
    unittest.main() 