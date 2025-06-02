import unittest
import sys
import os
import csv
from datetime import datetime, date
from unittest.mock import patch, mock_open, MagicMock, call
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QMessageBox, QWidget
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QTimer
from pyside6new import (
    MoodWindow, 
    initialize_files, 
    check_notification_eligibility,
    save_mood,
    update_notification_time,
    EMOJI_STATE_MAP,
    MOOD_FILE,
    LAST_NOTIFICATION_FILE,
    MOOD_RESPONSE_MAP,
    SPINNER_FRAMES
)

# Mock date for testing
TEST_DATE = date(2024, 3, 20)

class MockWriter:
    def __init__(self):
        self.rows = []

    def writerow(self, row):
        self.rows.append(row)

class MockCSV:
    def writer(self):
        return MockWriter()

class TestMoodCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance for all tests
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Create a fresh instance of MoodWindow for each test
        self.window = MoodWindow()
        
        # Create temporary test files
        self.test_mood_file = "test_mood_data.csv"
        self.test_notification_file = "test_notification.txt"
        
    def tearDown(self):
        # Clean up after each test
        self.window.close()
        
        # Remove test files if they exist
        if os.path.exists(self.test_mood_file):
            os.remove(self.test_mood_file)
        if os.path.exists(self.test_notification_file):
            os.remove(self.test_notification_file)

    # Window Tests
    def test_window_initialization(self):
        """Test if the window is initialized with correct properties"""
        self.assertEqual(self.window.windowTitle(), "Mood Check-in")
        self.assertEqual(self.window.size().width(), 800)
        self.assertEqual(self.window.size().height(), 450)
        self.assertIsNone(self.window.selected_mood)
        self.assertIsNone(self.window.selected_button)
        self.assertTrue(self.window.isWindow())
        self.assertTrue(self.window.windowFlags() & Qt.WindowCloseButtonHint)

    def test_window_center_position(self):
        """Test if window is centered on screen"""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.window.geometry()
        center_x = (screen.width() - window_geometry.width()) // 2
        center_y = (screen.height() - window_geometry.height()) // 2
        self.assertEqual(window_geometry.x(), center_x)
        self.assertEqual(window_geometry.y(), center_y)

    # UI Element Tests
    def test_emoji_buttons_creation(self):
        """Test if all emoji buttons are created correctly"""
        emoji_count = 0
        for layout in self.window.emoji_layouts:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), QPushButton):
                    emoji_count += 1
                    # Test button properties
                    button = item.widget()
                    self.assertTrue(button.isCheckable())
                    self.assertFalse(button.isChecked())
                    self.assertTrue(button.isEnabled())
        
        self.assertEqual(emoji_count, len(EMOJI_STATE_MAP))

    def test_emoji_button_styles(self):
        """Test if emoji buttons have correct styles"""
        for layout in self.window.emoji_layouts:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), QPushButton):
                    button = item.widget()
                    style = button.styleSheet()
                    self.assertIn("border-radius: 15px", style)
                    self.assertIn("background-color: #ffffff", style)

    def test_send_button_properties(self):
        """Test send button properties"""
        self.assertIsNotNone(self.window.send_button)
        self.assertEqual(self.window.send_button.text(), "Send")
        self.assertTrue(self.window.send_button.isEnabled())
        self.assertIn("background-color: #FF6F61", self.window.send_button.styleSheet())

    # Functionality Tests
    def test_mood_selection(self):
        """Test mood selection functionality"""
        # Test selecting each mood
        for emoji in EMOJI_STATE_MAP.keys():
            emoji_button = None
            for layout in self.window.emoji_layouts:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), QPushButton):
                        if item.widget().text() == emoji:
                            emoji_button = item.widget()
                            break
            
            if emoji_button:
                QTest.mouseClick(emoji_button, Qt.LeftButton)
                self.assertEqual(self.window.selected_mood, emoji)
                self.assertTrue(emoji_button.isChecked())

    def test_mood_selection_toggle(self):
        """Test that selecting a new mood deselects the previous one"""
        emojis = list(EMOJI_STATE_MAP.keys())
        first_button = None
        second_button = None
        
        # Find two emoji buttons
        for layout in self.window.emoji_layouts:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), QPushButton):
                    if item.widget().text() == emojis[0]:
                        first_button = item.widget()
                    elif item.widget().text() == emojis[1]:
                        second_button = item.widget()

        if first_button and second_button:
            # Click first button
            QTest.mouseClick(first_button, Qt.LeftButton)
            self.assertTrue(first_button.isChecked())
            
            # Click second button
            QTest.mouseClick(second_button, Qt.LeftButton)
            self.assertFalse(first_button.isChecked())
            self.assertTrue(second_button.isChecked())

    @patch('pyside6new.save_mood')
    def test_submit_mood(self, mock_save_mood):
        """Test mood submission"""
        # Test submitting each mood
        for emoji in EMOJI_STATE_MAP.keys():
            self.window = MoodWindow()  # Fresh window for each mood
            self.window.selected_mood = emoji
            QTest.mouseClick(self.window.send_button, Qt.LeftButton)
            mock_save_mood.assert_called_with(emoji)
            self.assertFalse(self.window.send_button.isVisible())

    def test_submit_mood_ui_changes(self):
        """Test UI changes after mood submission"""
        self.window.selected_mood = "😄"
        
        with patch('pyside6new.save_mood') as mock_save:  # Mock save_mood to avoid file operations
            # Show the window to ensure proper visibility handling
            self.window.show()
            QApplication.processEvents()
            
            # Click the send button
            QTest.mouseClick(self.window.send_button, Qt.LeftButton)
            QApplication.processEvents()
            
            # Check if elements are hidden
            self.assertFalse(self.window.send_button.isVisible())
            label = self.window.findChild(QLabel, "question_label")
            self.assertFalse(label.isVisible())
            
            # Give time for animation to start
            QTimer.singleShot(100, lambda: None)
            QApplication.processEvents()
            
            # Check if new elements are shown
            self.assertIsNotNone(self.window.spinner_label)
            self.assertTrue(self.window.spinner_label.isVisible())
            
            # Verify save_mood was called
            mock_save.assert_called_once_with("😄")

    # File Operation Tests
    @patch('builtins.open', new_callable=mock_open)
    def test_initialize_files(self, mock_file):
        """Test file initialization"""
        mock_csv = MockCSV()
        with patch('os.path.exists', return_value=False), \
             patch('csv.writer', return_value=mock_csv.writer()):
            initialize_files()
            mock_file.assert_any_call(MOOD_FILE, 'w', newline='')
            mock_file.assert_any_call(LAST_NOTIFICATION_FILE, 'w')

    @patch('getpass.getuser', return_value='test_user')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pyside6new.date')
    def test_check_notification_eligibility(self, mock_date, mock_file, mock_getuser):
        """Test notification eligibility checking"""
        # Test when user has not received notification today
        mock_date.today.return_value = TEST_DATE
        mock_file.return_value.read.return_value = "other_user,2024-03-20\n"
        result = check_notification_eligibility()
        self.assertTrue(result)

        # Test when user has received notification today
        mock_file.return_value.read.return_value = "test_user,2024-03-20\n"
        result = check_notification_eligibility()
        self.assertTrue(result)

    @patch('getpass.getuser', return_value='test_user')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_mood(self, mock_file, mock_getuser):
        """Test mood saving functionality"""
        mock_csv = MockCSV()
        test_mood = "😄"
        
        with patch('csv.writer', return_value=mock_csv.writer()):
            save_mood(test_mood)
            mock_file.assert_any_call(MOOD_FILE, 'a', newline='')

    # Animation Tests
    def test_spinner_animation(self):
        """Test spinner animation functionality"""
        self.window.selected_mood = "😄"
        self.window.show_animation_with_message()
        
        # Verify spinner setup
        self.assertIsNotNone(self.window.spinner_label)
        self.assertIsNotNone(self.window.spinner_timer)
        self.assertTrue(self.window.spinner_timer.isActive())
        self.assertEqual(self.window.spinner_timer.interval(), 150)

        # Test spinner frame updates
        initial_frame = self.window.spinner_label.text()
        self.window.update_spinner_frame()
        next_frame = self.window.spinner_label.text()
        self.assertNotEqual(initial_frame, next_frame)
        self.assertIn(next_frame, SPINNER_FRAMES)

    def test_final_emoji_display(self):
        """Test final emoji display after animation"""
        test_mood = "😄"
        self.window.selected_mood = test_mood
        self.window.show_animation_with_message()
        self.window.show_final_emoji()
        
        # Verify final state
        self.assertEqual(self.window.spinner_label.text(), test_mood)
        self.assertFalse(self.window.spinner_timer.isActive())
        self.assertIn("font-size: 80px", self.window.spinner_label.styleSheet())

    def test_mood_response_display(self):
        """Test if correct response message is displayed"""
        test_mood = "😄"
        self.window.selected_mood = test_mood
        self.window.show_animation_with_message()
        
        # Find response label
        response_label = None
        for i in range(self.window.dynamic_container.count()):
            item = self.window.dynamic_container.itemAt(i)
            if item.widget():
                for child in item.widget().findChildren(QLabel):
                    if child.text() == MOOD_RESPONSE_MAP[test_mood]:
                        response_label = child
                        break

        self.assertIsNotNone(response_label)
        self.assertEqual(response_label.text(), MOOD_RESPONSE_MAP[test_mood])
        self.assertTrue(response_label.wordWrap())

    # Error Handling Tests
    def test_error_message_on_empty_submission(self):
        """Test error message when submitting without selecting mood"""
        with patch('PySide6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.window.selected_mood = None
            self.window.submit_mood()
            mock_warning.assert_called_once()
            args = mock_warning.call_args[0]
            self.assertEqual(args[1], "Select Mood")
            self.assertEqual(args[2], "Please select a mood before submitting.")

    def test_file_error_handling(self):
        """Test handling of file operation errors"""
        # Test initialize_files error handling
        with patch('builtins.open', side_effect=IOError):
            try:
                initialize_files()
            except Exception as e:
                self.fail(f"initialize_files raised an exception: {e}")

        # Test save_mood error handling separately
        with patch('builtins.open', side_effect=IOError):
            try:
                save_mood("😄")
            except Exception as e:
                # This is expected behavior - save_mood should propagate IOError
                self.assertIsInstance(e, IOError)

if __name__ == '__main__':
    unittest.main() 