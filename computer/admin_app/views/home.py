import tkinter as tk
from tkinter import ttk, messagebox
from config import APP_FONT
from .common import AbstractFrame


class HomeView(AbstractFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure main frame grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # Space above buttons
        self.rowconfigure(2, weight=0)  # First button
        self.rowconfigure(3, weight=0)  # Second button
        self.rowconfigure(4, weight=1)  # Space below buttons

        # Create three separate elements in the top bar
        # 1. Logout button on the left
        logout_btn = ttk.Button(
            self,
            text="← Wyloguj",
            style="SmallButton.TButton",
            command=lambda: controller.show_view("LoginView")
        )
        logout_btn.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # 2. Title in the center
        title_label = ttk.Label(
            self,
            text="Menu główne",
            font=APP_FONT
        )
        title_label.grid(row=0, column=0, pady=5, sticky="N")

        # Calculate button width (approximately 1/3 of window)
        button_width = 25  # Adjust this value as needed

        # Vehicle management button - centered
        vehicle_btn = ttk.Button(
            self,
            text="Zarządzanie pojazdami",
            style="HugeButton.TButton",
            width=button_width,
            command=lambda: controller.show_view("VehiclesView")
        )
        vehicle_btn.grid(row=2, column=0, pady=10)

        # Ticket validator management button - centered
        validator_btn = ttk.Button(
            self,
            text="Zarządzanie kasownikami",
            style="HugeButton.TButton",
            width=button_width,
            command=lambda: controller.show_view("TicketValidatorsView")
        )
        validator_btn.grid(row=3, column=0, pady=10)

        # Ticket validator management button - centered
        card_btn = ttk.Button(
            self,
            text="Zarządzanie kartami",
            style="HugeButton.TButton",
            width=button_width,
            command=lambda: controller.show_view("CardsView")
        )
        card_btn.grid(row=4, column=0, pady=10)

    def on_appear(self):
        print("Home view appeared")