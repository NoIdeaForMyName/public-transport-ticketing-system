import tkinter as tk
from tkinter import ttk, messagebox
from func.cards import add_card
from config import APP_FONT
from .common import AbstractFrame


class AddCardView(AbstractFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure main frame grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # Space above form
        self.rowconfigure(2, weight=0)  # Form elements
        self.rowconfigure(3, weight=1)  # Space below form

        # Back button on the left
        back_btn = ttk.Button(
            self,
            text="← Wstecz",
            style="SmallButton.TButton",
            command=lambda: controller.show_view("CardsView")
        )
        back_btn.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # Title in the center
        title_label = ttk.Label(
            self,
            text="Dodaj kartę",
            font=APP_FONT,
        )
        title_label.grid(row=0, column=0, pady=5, sticky="N")

        # Create a frame for the form elements
        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, pady=20)
        
        # RFID label and entry
        rfid_label = ttk.Label(
            form_frame,
            text="Numer RFID:",
            font=APP_FONT
        )
        rfid_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        
        self.rfid_entry = ttk.Entry(
            form_frame,
            font=APP_FONT
        )
        self.rfid_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")
        
        # Add card button
        add_btn = ttk.Button(
            form_frame,
            text="Dodaj kartę",
            style="DefaultButton.TButton",
            command=self._add_card
        )
        add_btn.grid(row=1, column=0, columnspan=2, pady=20)

    def _add_card(self):
        rfid = self.rfid_entry.get().strip()
        
        if not rfid:
            messagebox.showerror("Błąd", "Proszę wprowadzić numer RFID.")
            return
            
        if add_card(rfid):
            messagebox.showinfo("Dodano kartę", 
                              f"Karta o numerze RFID {rfid} została dodana.")
            self.rfid_entry.delete(0, tk.END)  # Clear the entry
            self.controller.show_view("CardsView")
        else:
            messagebox.showerror("Błąd", 
                               f"Karta o numerze RFID {rfid} nie została dodana. Już istnieje w bazie danych")

    def on_appear(self):
        self.rfid_entry.delete(0, tk.END)  # Clear RFID entry when view appears