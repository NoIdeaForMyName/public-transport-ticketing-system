import tkinter as tk
from tkinter import ttk, messagebox
from func.login import check_login

from config import APP_FONT
from .common import AbstractFrame

class LoginView(AbstractFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Create a label for the settings view
        label = ttk.Label(self, text="Login View", font=APP_FONT)
        label.pack(pady=20)
        
        # Add some example settings
        settings_frame = ttk.Frame(self)
        settings_frame.pack(pady=20)

        # Configure grid columns to be equal width
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
        # Create and store references to Entry widgets
        ttk.Label(settings_frame, text="Login:", font=APP_FONT).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(settings_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Hasło:", font=APP_FONT).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(settings_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add login button - centered
        ttk.Button(
            settings_frame,
            text="Login",
            style="SmallButton.TButton",
            command=self.button_react
        ).grid(row=2, column=0, columnspan=2, pady=10, sticky="EW")


    def on_appear(self):
        print("Login view appeared")
        # Optionally clear entries when view appears
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def button_react(self):
        # Get values from entries
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        # Here you can add your login logic
        # For example:
        is_logged_in = check_login(username, password)
        if is_logged_in:
            print("Login successful")
            self.controller.show_view("HomeView")
        else:
            print("Login failed")
            # Optionally show an error message
            messagebox.showerror("Login Failed", "Invalid username or password")