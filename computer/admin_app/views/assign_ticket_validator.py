import tkinter as tk
from tkinter import ttk, messagebox
from func.ticket_validators import TicketValidatorData, update_ticket_validator
from func.vehicles import VehicleData, get_all_vehicles
from config import APP_FONT
from .common import AbstractFrame

class AssignTicketValidatorView(AbstractFrame):
    ticket_validator: TicketValidatorData
    vehicles: list[VehicleData]
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
        self.title_label = ttk.Label(
            self,
            text="Zmień pojazd kasownika",
            font=APP_FONT,
        )
        self.title_label.grid(row=0, column=0, pady=5, sticky="N")

        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, pady=20)
        
        ip_label = ttk.Label(
            form_frame,
            text="Pojazd:",
            font=APP_FONT
        )
        ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
        
        # self.ip_entry = ttk.Entry(
        #     form_frame,
        #     font=APP_FONT
        # )
        # self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")
        self.selected_text = tk.StringVar()
        self.vehicle_combo = ttk.Combobox(
            form_frame,
            textvariable=self.selected_text,
            values=[],
            state="readonly"  # User can't type in the combobox
        )
        self.vehicle_combo.grid(row=0, column=1, pady=20)
        
        add_btn = ttk.Button(
            form_frame,
            text="Dodaj do pojazdu",
            style="DefaultButton.TButton",
            command=self._update_ticket_validator
        )
        add_btn.grid(row=1, column=0, columnspan=2, pady=20)

    def _update_ticket_validator(self):
        vehicle = self.get_vehicle_by_registration_number(self.selected_text.get())
            
        if update_ticket_validator(self.ticket_validator.id, vehicle.id):
            messagebox.showinfo("Dodano do pojazdu", 
                              f"Kasownik o ip {self.ticket_validator.ip_adress} został dodany do {vehicle.registration_number}.")
            self.controller.show_view("TicketValidatorsView")
        else:
            messagebox.showerror("Błąd", 
                               f"Kasownik o ip {self.ticket_validator.ip_adress} nie został dodany do {vehicle.registration_number}.")

    def on_appear(self, validator: TicketValidatorData):
        self.ticket_validator = validator
        print(validator.id, validator.ip_adress)
        self.vehicles = [VehicleData(None, registration_number="Brak")] + get_all_vehicles()
        self.vehicle_combo["values"] = [vehicle.registration_number for vehicle in self.vehicles]
        self.selected_text.set(validator.vehicle_plate_number if validator.vehicle_plate_number else "Brak")
        self.title_label["text"] = f"Zmień pojazd kasownika {validator.ip_adress}"

    def get_vehicle_by_registration_number(self, registration_number: str) -> VehicleData:
        for vehicle in self.vehicles:
            if vehicle.registration_number == registration_number:
                return vehicle
        raise(ValueError(f"Vehicle with registration number {registration_number} not found"))