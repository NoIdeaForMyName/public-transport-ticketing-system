from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk

from .common import setup_styles
from config import APP_SIZE, APP_TITLE

from .login import LoginView
from .home import HomeView
from .vehicles import VehiclesView
from .add_vehicle import AddVehicleView
from .ticket_validators import TicketValidatorsView
from .add_ticket_validator import AddTicketValidatorView
from .assign_ticket_validator import AssignTicketValidatorView
from .cards import CardsView
from .add_card import AddCardView

frame_classes = [
    LoginView,
    HomeView,
    VehiclesView,
    AddVehicleView,
    TicketValidatorsView,
    AddTicketValidatorView,
    AssignTicketValidatorView,
    CardsView,
    AddCardView
]

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)

        setup_styles()
        
        # Create a container to hold all the views
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to store our views
        self.frames = {}
        
        # Create and add all views to the frames dictionary
        for ViewClass in frame_classes:
            frame = ViewClass(parent=self.container, controller=self)
            self.frames[ViewClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial view
        self.show_view("LoginView")
    
    def show_view(self, view_name, *args, **kwargs):
        """Switch to the specified view"""
        frame = self.frames[view_name]
        frame.on_appear(*args, **kwargs)
        frame.tkraise()

