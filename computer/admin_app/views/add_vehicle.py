import tkinter as tk
from tkinter import ttk, messagebox
from func.vehicles import add_vehicle
from config import APP_FONT
from .common import AbstractFrame

class AddVehicleView(AbstractFrame):
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
            command=lambda: controller.show_view("VehiclesView")
        )
        back_btn.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # Title in the center
        title_label = ttk.Label(
            self,
            text="Dodaj pojazd",
            style="SmallButton.TButton",
        )
        title_label.grid(row=0, column=0, pady=5, sticky="N")

        # Create a frame for the form elements
        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, pady=20)
        
        # Registration plate label and entry
        reg_label = ttk.Label(
            form_frame,
            text="Numer rejestracyjny:",
            font=APP_FONT
        )
        reg_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        
        self.reg_entry = ttk.Entry(
            form_frame,
            font=APP_FONT
        )
        self.reg_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")
        
        # Add vehicle button
        add_btn = ttk.Button(
            form_frame,
            text="Dodaj pojazd",
            style="DefaultButton.TButton",
            command=self._add_vehicle
        )
        add_btn.grid(row=1, column=0, columnspan=2, pady=20)

    def _add_vehicle(self):
        registration_plate = self.reg_entry.get().strip()
        
        if not registration_plate:
            messagebox.showerror("Błąd", "Proszę wprowadzić numer rejestracyjny.")
            return
            
        if add_vehicle(registration_plate):
            messagebox.showinfo("Dodano pojazd", 
                              f"Pojazd o numerze rejestracyjnym {registration_plate} został dodany.")
            self.reg_entry.delete(0, tk.END)  # Clear the entry
            self.controller.show_view("VehiclesView")
        else:
            messagebox.showerror("Błąd", 
                               f"Pojazd o numerze rejestracyjnym {registration_plate} nie został dodany. Już istnieje w bazie danych")

    def on_appear(self):
        self.reg_entry.delete(0, tk.END)  # Clear registration plate entry when view appears