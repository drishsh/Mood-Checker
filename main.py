import os
import getpass
from datetime import datetime, date
import csv
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QSystemTrayIcon, QMessageBox, QSizePolicy)
from PySide6.QtGui import QLinearGradient, QPainter, QColor, QIcon, QPixmap
from PySide6.QtCore import Qt, QTimer
import sys
 
# File paths
MOOD_FILE = "employee_mood_data.csv"
LAST_NOTIFICATION_FILE = "last_notification.txt"
 
# Emojis and their corresponding states
EMOJI_STATE_MAP = {
    "😄": "Thrivin'",
    "😊": "Chillin'",
    "😐": "Meh!",
    "😔": "Low Key",
    "😞": "Cooked >_>"
}
EMOJIS = list(EMOJI_STATE_MAP.keys())
 
# Define colors for each mood
EMOJI_COLOR_MAP = {
    "😄": {"hover": "#90EE90", "pressed": "#70e000", "checked": "#9ef01a"},
    "😊": {"hover": "#ADD8E6", "pressed": "#00b4d8", "checked": "#56cfe1"},
    "😐": {"hover": "#D3D3D3", "pressed": "#A9A9A9", "checked": "#ced4da"},
    "😔": {"hover": "#FFDAB9", "pressed": "#FFA07A", "checked": "#FF7F50"},
    "😞": {"hover": "#FFB6C1", "pressed": "#FF6347", "checked": "#FF4500"},
}
 
SPINNER_DURATION_MS = 2000
 
SPINNER_FRAMES = ["😄", "😊", "😐", "😔", "😞"]
 
MOOD_RESPONSE_MAP = {
    "😄": "Yaaas! Love to see you thriving! Keep that energy up!",
    "😊": "Smooth sailing. Glad you're vibing. Keep it mellow!",
    "😐": "Fair enough. Not every day's a banger. Tomorrow's a reset.",
    "😔": "Aww, sending a little sunshine your way. Hope today feels lighter.",
    "😞": "Oh no, you got roasted by the day! Hope today serves better vibes."
}
 
def initialize_files():
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Username", "Mood", "State"])
    if not os.path.exists(LAST_NOTIFICATION_FILE):
        with open(LAST_NOTIFICATION_FILE, 'w') as f:
            f.write("")
 
def check_notification_eligibility():
    username = getpass.getuser()
    today = date.today().isoformat()
    last_notifications = {}
    try:
        with open(LAST_NOTIFICATION_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        user, last_date = parts
                        last_notifications[user] = last_date
    except FileNotFoundError:
        pass
    if username in last_notifications and last_notifications[username] == today:
        return True
    return True
 
def update_notification_time():
    username = getpass.getuser()
    today = date.today().isoformat()
    last_notifications = {}
    try:
        with open(LAST_NOTIFICATION_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    user, last_date = line.strip().split(',')
                    last_notifications[user] = last_date
    except FileNotFoundError:
        pass
    last_notifications[username] = today
    with open(LAST_NOTIFICATION_FILE, 'w') as f:
        for user, last_date in last_notifications.items():
            f.write(f"{user},{last_date}\n")
 
def save_mood(mood):
    username = getpass.getuser()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = EMOJI_STATE_MAP.get(mood, "Unknown")
    with open(MOOD_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, username, mood, state])
    update_notification_time()
 
# (all imports and constants remain the same)
 
class MoodWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set window flags to show standard window decorations
        self.setWindowFlags(
            Qt.Window |  # Use Window to get standard title bar
            Qt.WindowTitleHint |  # Show title
            Qt.WindowSystemMenuHint |  # Show system menu
            Qt.WindowMinimizeButtonHint |  # Show minimize button
            Qt.WindowMaximizeButtonHint |  # Show maximize button
            Qt.WindowCloseButtonHint  # Show close button
        )
        # Set minimum size but allow resizing
        self.setMinimumSize(800, 450)
        self.setWindowTitle("Mood Check-in")
        self.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 20px;
            font-family: Arial, Helvetica, sans-serif;
        """)
        
        self.selected_mood = None
        self.selected_button = None
        self.spinner_label = None
        self.spinner_timer = None
        self.spinner_index = 0
        
        # Create a central container widget that can resize
        self.central_widget = QWidget(self)
        self.central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.central_widget.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 20px;
        """)
        
        self.init_ui()
        # Center window after showing it
        self.show()
        QApplication.processEvents()
        self.center_window()

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        # Make central widget fill the window
        self.central_widget.setGeometry(0, 0, event.size().width(), event.size().height())
        
        # Calculate new sizes based on window dimensions
        window_width = event.size().width()
        window_height = event.size().height()
        
        # Base size calculation that ensures scaling
        base_size = min(window_width // 8, window_height // 4)
        base_size = max(base_size, 80)  # Ensure minimum size
        
        # Update button sizes
        for layout in self.emoji_layouts:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item.widget(), QPushButton):
                    button = item.widget()
                    # Calculate sizes based on window dimensions
                    button_width = max(base_size, window_width // 8)
                    button_height = int(button_width * 1.1)  # Keep aspect ratio
                    font_size = max(30, min(50, button_width // 2))
                    
                    # Get the emoji for this button to determine colors
                    emoji = button.text()
                    colors = EMOJI_COLOR_MAP.get(emoji, {"hover": "#f0f9ff", "pressed": "#d1e7ff", "checked": "#d1e7ff"})
                    
                    # Create a properly formatted stylesheet
                    style = """
                        QPushButton {
                            font-size: %dpx;
                            background-color: #ffffff;
                            color: #2c3e50;
                            border: none;
                            border-radius: 15px;
                            padding: 15px;
                            min-width: %dpx;
                            min-height: %dpx;
                        }
                        QPushButton:hover {
                            background-color: %s;
                        }
                        QPushButton:pressed {
                            background-color: %s;
                        }
                        QPushButton:checked {
                            background-color: %s;
                            border: 3px solid %s;
                        }
                    """ % (
                        font_size,
                        button_width,
                        button_height,
                        colors['hover'],
                        colors['pressed'],
                        colors['checked'],
                        colors['pressed']
                    )
                    
                    button.setStyleSheet(style)
                    button.updateGeometry()

    def center_window(self):
        """Center the window on the screen"""
        # Get the screen geometry
        screen = QApplication.primaryScreen().availableGeometry()
        
        # Get the window geometry
        window_frame = self.frameGeometry()
        
        # Calculate the center point
        center_point = screen.center()
        
        # Move the window's center to the screen's center
        window_frame.moveCenter(center_point)
        
        # Use move instead of setGeometry to preserve size
        self.move(window_frame.x(), window_frame.y())
        
        # Process events to ensure the window is positioned
        QApplication.processEvents()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self.central_widget)  # Set layout on central widget
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Top layout for logo and label
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 30, 0, 0)  # Added 30px top margin
        top_layout.setSpacing(20)

        # Label
        label = QLabel("How did yesterday treat you?")
        label.setObjectName("question_label")
        label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #003049;
            background: transparent;
            margin-top: 10px;
            margin-left: 40px;  /* Added left margin to shift text right */
        """)
        label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(label, 1)

        # Logo
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("Shorthills Logo Light Bg.png")
        self.logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        top_layout.addWidget(self.logo_label)

        # Add top layout to main layout
        self.main_layout.addLayout(top_layout)

        # Add spacer to push content to center
        self.main_layout.addStretch(2)  # Increased weight for top stretch

        # Emoji buttons layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(30)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.emoji_layouts = []  # Initialize the list
        for emoji, state in EMOJI_STATE_MAP.items():
            emoji_layout = QVBoxLayout()
            emoji_layout.setSpacing(5)
            colors = EMOJI_COLOR_MAP.get(emoji, {"hover": "#f0f9ff", "pressed": "#d1e7ff", "checked": "#d1e7ff"})
            button_style = f"""
                QPushButton {{
                    font-size: 50px;
                    background-color: #ffffff;
                    color: #2c3e50;
                    border: none;
                    border-radius: 15px;
                    padding: 15px;
                    min-width: 80px;
                    min-height: 90px;
                }}
                QPushButton:hover {{
                    background-color: {colors['hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['pressed']};
                }}
                QPushButton:checked {{
                    background-color: {colors['checked']};
                    border: 3px solid {colors['pressed']};
                }}
            """
            btn = QPushButton(emoji)
            btn.setStyleSheet(button_style)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, e=emoji, b=btn: self.on_mood_select(e, b))
            emoji_layout.addWidget(btn, alignment=Qt.AlignCenter)
            text_label = QLabel(state)
            text_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #003049;
                background: transparent;
            """)
            text_label.setAlignment(Qt.AlignCenter)
            emoji_layout.addWidget(text_label, alignment=Qt.AlignCenter)
            self.button_layout.addLayout(emoji_layout)
            self.emoji_layouts.append(emoji_layout)

        self.main_layout.addLayout(self.button_layout)

        # Add spacer to push content to center
        self.main_layout.addStretch(3)  # Increased weight for bottom stretch

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                font-family: Helvetica;
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #FF6F61;
                border: 2px solid #283618;
                border-radius: 15px;
                padding: 8px;
                min-width: 100px;
                background-clip: padding-box;
            }
            QPushButton:hover {
                background-color: #E65C50;
            }
            QPushButton:pressed {
                background-color: #CC5247;
            }
        """)
        self.send_button.clicked.connect(self.submit_mood)
        self.main_layout.addWidget(self.send_button, alignment=Qt.AlignCenter)

        self.dynamic_container = QVBoxLayout()
        self.dynamic_container.setSpacing(20)
        self.main_layout.addLayout(self.dynamic_container)

    def on_mood_select(self, mood, button):
        if self.selected_button:
            self.selected_button.setChecked(False)
        self.selected_mood = mood
        self.selected_button = button
        button.setChecked(True)
 
    def submit_mood(self):
        if self.selected_mood:
            # Hide emoji buttons and the Send button immediately
            for layout in self.emoji_layouts:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.hide()

            # Hide the question label and all widgets in the top layout
            for child in self.findChildren(QWidget):
                if isinstance(child, QLabel):
                    child.hide()
            if self.send_button:
                self.send_button.hide()

            # Show animation and message together
            self.show_animation_with_message()
        else:
            QMessageBox.warning(self, "Select Mood", "Please select a mood before submitting.")

    def show_animation_with_message(self):
        self.clear_dynamic_container()

        # Create white background container
        final_widget = QWidget()
        final_widget.setStyleSheet("background-color: white;")
        final_layout = QVBoxLayout(final_widget)
        
        # Create top layout with logo only on the right
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(20)

        # Add stretch to push logo to the right
        top_layout.addStretch(1)

        # Logo on the right
        logo_label = QLabel()
        logo_pixmap = QPixmap("Shorthills Logo Light Bg.png")
        logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        top_layout.addWidget(logo_label)

        final_layout.addLayout(top_layout)
        
        # Add top spacing to move content slightly above center
        top_spacer = QWidget()
        top_spacer.setFixedHeight(20)  # Reduced top spacing to move content up
        final_layout.addWidget(top_spacer)

        # Spinner animation
        self.spinner_label = QLabel(self.selected_mood)
        self.spinner_label.setAlignment(Qt.AlignCenter)
        self.spinner_label.setStyleSheet("font-size: 50px; background-color: white;")  # Smaller size for animation
        final_layout.addWidget(self.spinner_label)

        # Display the mood response text immediately
        response = MOOD_RESPONSE_MAP.get(self.selected_mood, "")
        response_label = QLabel(response)
        response_label.setWordWrap(True)
        response_label.setAlignment(Qt.AlignCenter)
        response_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #003049;
            background: transparent;
            font-family: Arial, Helvetica, sans-serif;
            padding: 20px;
        """)
        final_layout.addWidget(response_label)
        
        # Add bottom spacing to balance the layout
        bottom_spacer = QWidget()
        bottom_spacer.setFixedHeight(180)  # Increased bottom spacing to push content up
        final_layout.addWidget(bottom_spacer)

        self.dynamic_container.addWidget(final_widget)

        # Start the animation
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self.update_spinner_frame)
        self.spinner_timer.start(150)

        # Show final emoji after animation
        QTimer.singleShot(SPINNER_DURATION_MS - 500, self.show_final_emoji)  # Show final emoji slightly before animation ends
        
        # Save the mood data
        save_mood(self.selected_mood)

    def update_spinner_frame(self):
        # Update the spinner frame
        self.spinner_index = (self.spinner_index + 1) % len(SPINNER_FRAMES)
        self.spinner_label.setText(SPINNER_FRAMES[self.spinner_index])

    def show_final_emoji(self):
        if self.spinner_timer:
            self.spinner_timer.stop()
        self.spinner_label.setStyleSheet("font-size: 80px; background-color: white;")  # Large size for final emoji
        self.spinner_label.setText(self.selected_mood)  # Show selected emoji

    def clear_dynamic_container(self):
        while self.dynamic_container.count():
            item = self.dynamic_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
 
# (rest of your file remains unchanged)
 
def show_notification():
    app = QApplication.instance() or QApplication(sys.argv)
    tray = QSystemTrayIcon(QIcon("Shorthills Logo Light Bg.png"))
    tray.show()
    tray.showMessage("Daily Mood Check", "Hey user, how was your day?",
                     QSystemTrayIcon.Information, 10000)
    window = MoodWindow()
    window.show()
    app.exec()
 
def main():
    initialize_files()
    if check_notification_eligibility():
        show_notification()
 
if __name__ == "__main__":
    main()

