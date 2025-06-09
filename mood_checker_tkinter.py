import os
import getpass
from datetime import datetime, date
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys

# File paths
MOOD_FILE = "employee_mood_data.csv"
LAST_NOTIFICATION_FILE = "last_notification.txt"

# Emojis and their corresponding states
EMOJI_STATE_MAP = {
    "\U0001F604": "Thrivin'",  # 😄
    "\U0001F60A": "Chillin'",  # 😊
    "\U0001F610": "Meh!",      # 😐
    "\U0001F614": "Low Key",   # 😔
    "\U0001F61E": "Cooked >_>" # 😞
}
EMOJIS = list(EMOJI_STATE_MAP.keys())

# Define colors for each mood
EMOJI_COLOR_MAP = {
    "\U0001F604": {"hover": "#90f090", "normal": "#ffd700", "pressed": "#70e000"},  # 😄 - green when selected
    "\U0001F60A": {"hover": "#a8e8ff", "normal": "#ffd700", "pressed": "#00b4d8"},  # 😊 - blue when selected
    "\U0001F610": {"hover": "#fff4b5", "normal": "#ffd700", "pressed": "#fff4b5"},  # 😐 - light yellow when selected
    "\U0001F614": {"hover": "#ffd4b0", "normal": "#ffd700", "pressed": "#FFA07A"},  # 😔 - orange when selected
    "\U0001F61E": {"hover": "#ffccd4", "normal": "#ffd700", "pressed": "#FF6347"},  # 😞 - red when selected
}

SPINNER_DURATION_MS = 2000
SPINNER_FRAMES = ["\U0001F604", "\U0001F60A", "\U0001F610", "\U0001F614", "\U0001F61E"]

MOOD_RESPONSE_MAP = {
    "\U0001F604": "Yaaas! Love to see you thriving! Keep that energy up!",
    "\U0001F60A": "Smooth sailing. Glad you're vibing. Keep it mellow!",
    "\U0001F610": "Fair enough. Not every day's a banger. Tomorrow's a reset.",
    "\U0001F614": "Aww, sending a little sunshine your way. Hope today feels lighter.",
    "\U0001F61E": "Oh no, you got roasted by the day! Hope today serves better vibes."
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

class MoodWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.title("Mood Check-in")
        self.geometry("800x450")
        self.configure(bg='white')
        self.resizable(True, True)

        # Initialize variables
        self.selected_mood = None
        self.selected_button = None
        self.spinner_label = None
        self.spinner_timer = None
        self.spinner_index = 0

        # Create and configure the main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure style
        self.style = ttk.Style()
        self.style.configure('Main.TFrame', background='white')
        self.style.configure('TLabel', background='white')
        self.style.configure('TFrame', background='white')
        
        self.init_ui()
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def init_ui(self):
        # Top frame for logo and question
        top_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        top_frame.pack(fill=tk.X, pady=(20, 0))

        # Configure styles to ensure consistent background
        self.style.configure('Main.TFrame', background='white')
        self.style.configure('TLabel', background='white')
        self.style.configure('TFrame', background='white')

        # Question label
        question_label = ttk.Label(
            top_frame,
            text="How did yesterday treat you?",
            font=('Arial', 24, 'bold'),
            foreground='#003049'
        )
        question_label.pack(side=tk.LEFT, padx=(40, 0), pady=(10, 0))

        # Logo
        try:
            logo_img = Image.open("Shorthills Logo Light Bg.png")
            logo_img = logo_img.resize((80, 60), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(top_frame, image=self.logo_photo)
            logo_label.pack(side=tk.RIGHT, padx=20, pady=(10, 0))
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = ttk.Label(top_frame, text="")
            logo_label.pack(side=tk.RIGHT, padx=20, pady=(10, 0))

        # Frame for emoji buttons
        self.emoji_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.emoji_frame.pack(expand=True, fill=tk.BOTH, pady=(20, 0))

        # Create emoji buttons
        self.emoji_buttons = []
        for emoji, state in EMOJI_STATE_MAP.items():
            # Create custom button style for each emoji
            button_frame = ttk.Frame(self.emoji_frame, style='Main.TFrame')
            button_frame.pack(side=tk.LEFT, expand=True, padx=10)

            # First create a temporary label to measure the emoji size
            temp_label = tk.Label(
                button_frame,
                text=emoji,
                font=('TkDefaultFont', 48)
            )
            temp_label.pack()
            button_frame.update()
            
            # Get the emoji size
            emoji_width = temp_label.winfo_width()
            emoji_height = temp_label.winfo_height()
            canvas_size = max(emoji_width, emoji_height)
            temp_label.destroy()

            # Create circular canvas button exactly sized to the emoji
            canvas = tk.Canvas(
                button_frame,
                width=canvas_size,
                height=canvas_size,
                highlightthickness=0,
                bd=0,
                bg='white'
            )
            canvas.pack(pady=5)

            # Create the circular background
            circle = canvas.create_oval(
                0, 0,
                canvas_size, canvas_size,
                fill='#ffd700',
                outline='#ffd700',
                width=0
            )

            # Add emoji text
            text = tk.Label(
                canvas,
                text=emoji,
                font=('TkDefaultFont', 48),
                bg='#ffd700',
                bd=0,
                highlightthickness=0,
                padx=0,
                pady=0
            )
            text.place(relx=0.5, rely=0.5, anchor='center')

            # Store references
            button = canvas
            button.text = text
            button.emoji_code = emoji
            button.canvas_size = canvas_size
            button.circle = circle  # Store reference to circle for updates

            # Bind events to both canvas and text
            def handle_click(event, m=emoji, b=button):
                self.on_mood_select(m, b)

            def handle_enter(event, b=button):
                if b != self.selected_button:
                    colors = EMOJI_COLOR_MAP.get(b.emoji_code, {"hover": "#f0f9ff"})
                    b.itemconfig(b.circle, fill=colors['hover'], outline=colors['hover'])
                    b.text.configure(bg=colors['hover'])

            def handle_leave(event, b=button):
                if b != self.selected_button:
                    b.itemconfig(b.circle, fill='#ffd700', outline='#ffd700')
                    b.text.configure(bg='#ffd700')

            canvas.bind('<Button-1>', handle_click)
            text.bind('<Button-1>', handle_click)
            canvas.bind('<Enter>', handle_enter)
            canvas.bind('<Leave>', handle_leave)
            text.bind('<Enter>', handle_enter)
            text.bind('<Leave>', handle_leave)

            # Configure cursor
            canvas.configure(cursor='hand2')
            text.configure(cursor='hand2')

            # State label
            state_label = ttk.Label(
                button_frame,
                text=state,
                font=('Arial', 12, 'bold'),
                foreground='#003049',
                style='TLabel'
            )
            state_label.pack()

            self.emoji_buttons.append((button, state_label))

        # Send button
        self.send_button = tk.Button(
            self.main_frame,
            text="Send",
            font=('Arial', 16, 'bold'),
            bg='#FF6F61',
            fg='white',
            relief=tk.FLAT,
            command=self.submit_mood,
            padx=30,
            pady=10
        )
        self.send_button.pack(pady=(10, 20))

        # Bind hover events for send button
        self.send_button.bind('<Enter>', lambda e: self.send_button.configure(bg='#E65C50'))
        self.send_button.bind('<Leave>', lambda e: self.send_button.configure(bg='#FF6F61'))

    def on_hover_enter(self, button):
        emoji_code = button.emoji_code
        if button != self.selected_button:
            colors = EMOJI_COLOR_MAP.get(emoji_code, {"hover": "#f0f9ff"})
            if hasattr(button, 'mask'):
                button.mask.delete('all')
                button.mask.create_oval(0, 0, button.winfo_width(), button.winfo_height(),
                                      fill=colors['hover'], outline=colors['hover'])
                button.text.configure(bg=colors['hover'])
            button.configure(background=colors['hover'])

    def on_hover_leave(self, button):
        if button != self.selected_button:
            if hasattr(button, 'mask'):
                button.mask.delete('all')
                button.mask.create_oval(0, 0, button.winfo_width(), button.winfo_height(),
                                      fill='#fff4b5', outline='#fff4b5')
                button.text.configure(bg='#fff4b5')
            button.configure(background='#fff4b5')

    def on_mood_select(self, mood, button):
        # If there was a previously selected button, reset it to default yellow
        if self.selected_button:
            if isinstance(self.selected_button, tk.Canvas):
                self.selected_button.itemconfig(
                    self.selected_button.circle,
                    fill='#ffd700',
                    outline='#ffd700'
                )
                self.selected_button.text.configure(bg='#ffd700')
        
        # Update selection state
        self.selected_mood = mood
        self.selected_button = button
        
        # Set the selected button to its pressed color
        colors = EMOJI_COLOR_MAP.get(mood, {"pressed": "#d1e7ff"})
        if isinstance(button, tk.Canvas):
            button.itemconfig(
                button.circle,
                fill=colors['pressed'],
                outline=colors['pressed']
            )
            button.text.configure(bg=colors['pressed'])

    def submit_mood(self):
        if self.selected_mood:
            # Clear the window
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Show animation and message
            self.show_animation_with_message()
            
            # Save the mood
            save_mood(self.selected_mood)
        else:
            messagebox.showwarning("Select Mood", "Please select a mood before submitting.")

    def show_animation_with_message(self):
        # Create new frame for final display
        final_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        final_frame.pack(fill=tk.BOTH, expand=True)

        # Add logo at top right
        try:
            logo_frame = ttk.Frame(final_frame, style='Main.TFrame')
            logo_frame.pack(fill=tk.X, padx=20, pady=20)
            logo_label = ttk.Label(logo_frame, image=self.logo_photo)
            logo_label.pack(side=tk.RIGHT)
        except Exception as e:
            print(f"Error displaying logo: {e}")

        # Create container frame for animation
        animation_container = ttk.Frame(final_frame, style='Main.TFrame')
        animation_container.pack(expand=True)

        # Create temporary label to get emoji size
        temp_label = tk.Label(
            animation_container,
            text=self.selected_mood,
            font=('TkDefaultFont', 48)
        )
        temp_label.pack()
        animation_container.update()
        
        # Get the emoji size
        emoji_width = temp_label.winfo_width()
        emoji_height = temp_label.winfo_height()
        canvas_size = max(emoji_width, emoji_height)
        temp_label.destroy()

        # Get the color for the selected mood
        colors = EMOJI_COLOR_MAP.get(self.selected_mood, {"pressed": "#ffd700"})
        bg_color = colors['pressed']

        # Create circular canvas for animation
        self.animation_canvas = tk.Canvas(
            animation_container,
            width=canvas_size,
            height=canvas_size,
            highlightthickness=0,
            bd=0,
            bg='white'
        )
        self.animation_canvas.pack(expand=True)

        # Create the circular background
        self.animation_circle = self.animation_canvas.create_oval(
            0, 0,
            canvas_size, canvas_size,
            fill=bg_color,
            outline=bg_color,
            width=0
        )

        # Spinner label on top of canvas
        self.spinner_label = ttk.Label(
            self.animation_canvas,
            text=self.selected_mood,
            font=('TkDefaultFont', 48),
            background=bg_color
        )
        # Center the label in the canvas
        self.spinner_label.place(relx=0.5, rely=0.5, anchor='center')

        # Response text
        response = MOOD_RESPONSE_MAP.get(self.selected_mood, "")
        response_label = ttk.Label(
            final_frame,
            text=response,
            font=('Arial', 20, 'bold'),
            foreground='#003049',
            wraplength=600
        )
        response_label.pack(expand=True, pady=20)

        # Start animation
        self.spinner_index = 0
        self.update_spinner_frame()

    def update_spinner_frame(self):
        if self.spinner_index < len(SPINNER_FRAMES) * 2:  # Multiply by 2 for slower animation
            current_emoji = SPINNER_FRAMES[self.spinner_index % len(SPINNER_FRAMES)]
            self.spinner_label.configure(text=current_emoji)
            
            # Update circle color based on the current emoji
            colors = EMOJI_COLOR_MAP.get(current_emoji, {"pressed": "#ffd700"})
            self.animation_canvas.itemconfig(
                self.animation_circle,
                fill=colors['pressed'],
                outline=colors['pressed']
            )
            self.spinner_label.configure(background=colors['pressed'])
            
            self.spinner_index += 1
            self.after(150, self.update_spinner_frame)
        else:
            # Show final emoji
            self.spinner_label.configure(
                text=self.selected_mood,
                font=('TkDefaultFont', 48)
            )
            
            # Set final color
            colors = EMOJI_COLOR_MAP.get(self.selected_mood, {"pressed": "#ffd700"})
            self.animation_canvas.itemconfig(
                self.animation_circle,
                fill=colors['pressed'],
                outline=colors['pressed']
            )
            self.spinner_label.configure(background=colors['pressed'])

def show_notification():
    root = MoodWindow()
    root.mainloop()

def main():
    initialize_files()
    if check_notification_eligibility():
        show_notification()

if __name__ == "__main__":
    main() 