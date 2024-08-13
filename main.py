import random
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, filedialog, font

# Ensure NLTK data is available
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Default response categories
default_responses = {
    'positive': [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes – definitely.", "You may rely on it.", "Outlook good.",
        "Yes.", "Signs point to yes."
    ],
    'neutral': [
        "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
        "Cannot predict now.", "Concentrate and ask again."
    ],
    'negative': [
        "Don't count on it.", "My reply is no.", "My sources say no.",
        "Outlook not so good.", "Very doubtful."
    ]
}

# Profile management
def load_profile(profile_name):
    profile_path = f"profiles/{profile_name}.pkl"
    if os.path.exists(profile_path):
        with open(profile_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {
            'responses': default_responses.copy(),
            'theme': {'bg_color': 'white', 'fg_color': 'black'},
            'font': {'family': 'Arial', 'size': 14},
            'history': {}
        }

def save_profile(profile_name, profile_data):
    if not os.path.exists("profiles"):
        os.makedirs("profiles")
    profile_path = f"profiles/{profile_name}.pkl"
    with open(profile_path, 'wb') as f:
        pickle.dump(profile_data, f)

# Main application class
class Magic8BallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic 8 Ball")
        self.current_profile = None
        self.profile_data = None

        # Load profile dialog
        self.load_profile_dialog()

        # Create menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Profile menu
        profile_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Profile", menu=profile_menu)
        profile_menu.add_command(label="Load Profile", command=self.load_profile_dialog)
        profile_menu.add_command(label="Save Profile", command=self.save_current_profile)
        profile_menu.add_command(label="New Profile", command=self.new_profile_dialog)

        # Customize menu
        customize_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Customize", menu=customize_menu)
        customize_menu.add_command(label="Add Custom Response", command=self.add_custom_response)
        customize_menu.add_command(label="Change Theme", command=self.change_theme)
        customize_menu.add_command(label="Change Font", command=self.change_font)
        customize_menu.add_command(label="Manage Categories", command=self.manage_categories)

        # User input and display area
        self.label = tk.Label(root, text="Enter your name:", font=self.get_font(), bg=self.profile_data['theme']['bg_color'], fg=self.profile_data['theme']['fg_color'])
        self.label.pack(pady=10)

        self.name_entry = tk.Entry(root, width=30, font=self.get_font())
        self.name_entry.pack(pady=5)

        self.question_label = tk.Label(root, text="Ask your question:", font=self.get_font(), bg=self.profile_data['theme']['bg_color'], fg=self.profile_data['theme']['fg_color'])
        self.question_label.pack(pady=10)

        self.question_entry = tk.Entry(root, width=50, font=self.get_font())
        self.question_entry.pack(pady=5)

        # Button to ask the Magic 8 Ball
        self.ask_button = tk.Button(root, text="Ask the Magic 8 Ball", command=self.ask_magic_8_ball, font=self.get_font())
        self.ask_button.pack(pady=10)

        # Display area for the Magic 8 Ball response
        self.response_label = tk.Label(root, text="", font=self.get_font(bold=True), wraplength=300, bg=self.profile_data['theme']['bg_color'], fg=self.profile_data['theme']['fg_color'])
        self.response_label.pack(pady=20)

    def get_font(self, bold=False):
        font_family = self.profile_data['font']['family']
        font_size = self.profile_data['font']['size']
        font_weight = "bold" if bold else "normal"
        return font.Font(family=font_family, size=font_size, weight=font_weight)

    def load_profile_dialog(self):
        profile_name = simpledialog.askstring("Load Profile", "Enter profile name:")
        if profile_name:
            self.current_profile = profile_name
            self.profile_data = load_profile(profile_name)
            self.update_ui()

    def save_current_profile(self):
        if self.current_profile:
            save_profile(self.current_profile, self.profile_data)
            messagebox.showinfo("Success", f"Profile '{self.current_profile}' saved successfully.")
        else:
            messagebox.showerror("Error", "No profile loaded.")

    def new_profile_dialog(self):
        profile_name = simpledialog.askstring("New Profile", "Enter new profile name:")
        if profile_name:
            self.current_profile = profile_name
            self.profile_data = {
                'responses': default_responses.copy(),
                'theme': {'bg_color': 'white', 'fg_color': 'black'},
                'font': {'family': 'Arial', 'size': 14},
                'history': {}
            }
            self.update_ui()

    def update_ui(self):
        self.label.config(font=self.get_font(), bg=self.profile_data['theme']['bg_color'], fg=self.profile_data['theme']['fg_color'])
        self.question_label.config(font=self.get_font(), bg=self.profile_data['theme']['bg_color'], fg=self.profile_data['theme']['fg_color'])
        self.response_label.config(font=self.get_font(bold=True), bg=self.profile_data['theme']['bg_color'], fg=self.profile_data['theme']['fg_color'])
        self.ask_button.config(font=self.get_font())

    def ask_magic_8_ball(self):
        user_name = self.name_entry.get().strip()
        question = self.question_entry.get().strip()

        if not user_name or not question:
            messagebox.showerror("Error", "Please enter both your name and a question.")
            return

        if user_name not in self.profile_data['history']:
            self.profile_data['history'][user_name] = []

        category = analyze_question(question)
        response = random.choice(self.profile_data['responses'][category])

        self.response_label.config(text=f"Magic 8 Ball says: {response}")

        # Save interaction
        self.profile_data['history'][user_name].append({'question': question, 'response': response})

    def add_custom_response(self):
        response = simpledialog.askstring("Input", "Enter your custom response:")
        if response:
            category = simpledialog.askstring("Input", "Enter the category:").lower()
            if category in self.profile_data['responses']:
                self.profile_data['responses'][category].append(response)
                messagebox.showinfo("Success", f"Custom response added to {category} category.")
            else:
                messagebox.showerror("Error", "Invalid category.")

    def change_theme(self):
        bg_color = colorchooser.askcolor(title="Choose Background Color")[1]
        fg_color = colorchooser.askcolor(title="Choose Text Color")[1]

        if bg_color and fg_color:
            self.profile_data['theme']['bg_color'] = bg_color
            self.profile_data['theme']['fg_color'] = fg_color
            self.update_ui()

    def change_font(self):
        font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
        font_size = simpledialog.askinteger("Font", "Enter font size (e.g., 14):")

        if font_family and font_size:
            self.profile_data['font']['family'] = font_family
            self.profile_data['font']['size'] = font_size
            self.update_ui()

    def manage_categories(self):
        category = simpledialog.askstring("Category", "Enter category name:")
        if category:
            if category not in self.profile_data['responses']:
                self.profile_data['responses'][category] = []
                messagebox.showinfo("Success", f"Category '{category}' created.")
            else:
                response = simpledialog.askstring("Response", f"Enter a response for '{category}':")
                if response:
                    self.profile_data['responses'][category].append(response)
                    messagebox.showinfo("Success", f"Response added to category '{category}'.")

# Run the Magic 8 Ball application
if __name__ == "__main__":
    root = tk.Tk()
    app = Magic8BallApp(root)
    root.mainloop()
