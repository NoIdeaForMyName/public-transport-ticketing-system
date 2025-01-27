import tkinter as tk
from tkinter import ttk, messagebox
from func.ticket_validators import add_ticket_validator
from config import APP_FONT
from .common import AbstractFrame

class AddTicketValidatorView(AbstractFrame):
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
            command=lambda: controller.show_view("TicketValidatorsView")
        )
        back_btn.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        # Title in the center
        title_label = ttk.Label(
            self,
            text="Dodaj Kasownik",
            style="SmallButton.TButton",
        )
        title_label.grid(row=0, column=0, pady=5, sticky="N")

        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, pady=20)
        
        ip_label = ttk.Label(
            form_frame,
            text="Ip kasownika:",
            font=APP_FONT
        )
        ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        
        self.ip_entry = ttk.Entry(
            form_frame,
            font=APP_FONT
        )
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")
        
        add_btn = ttk.Button(
            form_frame,
            text="Dodaj kasownik",
            style="DefaultButton.TButton",
            command=self._add_ticket_validator
        )
        add_btn.grid(row=1, column=0, columnspan=2, pady=20)

    def _add_ticket_validator(self):
        ip_adress = self.ip_entry.get().strip()
        
        if not ip_adress:
            messagebox.showerror("Błąd", "Proszę wprowadzić numer ip.")
            return
            
        if add_ticket_validator(ip_adress):
            messagebox.showinfo("Dodano kasownik", 
                              f"Kasownik o ip {ip_adress} został dodany.")
            self.ip_entry.delete(0, tk.END)  # Clear the entry
            self.controller.show_view("TicketValidatorsView")
        else:
            messagebox.showerror("Błąd", 
                               f"Kasownik o ip {ip_adress} już istnieje.")

    def on_appear(self):
        self.ip_entry.delete(0, tk.END)  # Clear registration plate entry when view appears