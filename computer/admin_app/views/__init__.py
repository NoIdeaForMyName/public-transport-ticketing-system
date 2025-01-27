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






# from abc import ABC, abstractmethod
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk

# from .common import setup_styles
# from config import APP_SIZE, APP_TITLE

# from .login import LoginView
# from .home import HomeView
# from .vehicles import VehiclesView
# from .add_vehicle import AddVehicleView
# from .ticket_validators import TicketValidatorsView
# from .add_ticket_validator import AddTicketValidatorView
# from .assign_ticket_validator import AssignTicketValidatorView
# from .cards import CardsView
# from .add_card import AddCardView

# frame_classes = [
#     LoginView,
#     HomeView,
#     VehiclesView,
#     AddVehicleView,
#     TicketValidatorsView,
#     AddTicketValidatorView,
#     AssignTicketValidatorView,
#     CardsView,
#     AddCardView
# ]

# class MainApplication(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         # Configure the main window
#         self.title(APP_TITLE)
#         self.geometry(APP_SIZE)

#         setup_styles()
        
#         # Create a canvas for background
#         self.canvas = tk.Canvas(self, highlightthickness=0)
#         self.canvas.pack(side="top", fill="both", expand=True)
        
#         # Load and set the background image
#         try:
#             # Assuming the image is in an 'assets' folder
#             image = Image.open("assets/background.png")
            
#             # Bind resize event to update background
#             self.bind("<Configure>", self._resize_background)
            
#             # Store the original image for resizing
#             self.background_image = image
            
#             # Create the initial photo image
#             self._resize_background(None)
            
#         except Exception as e:
#             print(f"Could not load background image: {e}")
#             # Create a fallback gradient background
#             self.canvas.configure(bg="white")
            
#         # Add semi-transparent white overlay
#         self.canvas.create_rectangle(
#             0, 0, 
#             self.winfo_width(), self.winfo_height(),
#             fill="white",
#             stipple="gray50",  # Creates a semi-transparent effect
#             tags=("overlay",)
#         )
        
#         # Create a container to hold all the views
#         self.container = ttk.Frame(self.canvas, style="Transparent.TFrame")
#         self.canvas.create_window(
#             0, 0,
#             anchor="nw",
#             window=self.container,
#             width=self.winfo_width(),
#             height=self.winfo_height(),
#             tags=("container",)
#         )
        
#         self.container.grid_rowconfigure(0, weight=1)
#         self.container.grid_columnconfigure(0, weight=1)

#         # Dictionary to store our views
#         self.frames = {}
        
#         # Create and add all views to the frames dictionary
#         for ViewClass in frame_classes:
#             frame = ViewClass(parent=self.container, controller=self)
#             self.frames[ViewClass.__name__] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         # Show the initial view
#         self.show_view("LoginView")
    
#     def _resize_background(self, event):
#         """Resize background image to fit window"""
#         if hasattr(self, 'background_image'):
#             # Get window size
#             width = self.winfo_width()
#             height = self.winfo_height()
            
#             if width > 1 and height > 1:  # Ensure valid dimensions
#                 # Resize image to fit window
#                 resized_image = self.background_image.resize(
#                     (width, height),
#                     Image.Resampling.LANCZOS
#                 )
                
#                 # Store the PhotoImage to prevent garbage collection
#                 self.background_photo = ImageTk.PhotoImage(resized_image)
                
#                 # Update canvas background
#                 self.canvas.delete("background")
#                 self.canvas.create_image(
#                     0, 0,
#                     anchor="nw",
#                     image=self.background_photo,
#                     tags=("background",)
#                 )
                
#                 # Ensure background is behind everything
#                 self.canvas.tag_lower("background")
                
#                 # Update overlay size
#                 self.canvas.coords(
#                     "overlay",
#                     0, 0, width, height
#                 )
                
#                 # Update container size
#                 self.canvas.itemconfig(
#                     "container",
#                     width=width,
#                     height=height
#                 )
    
#     def show_view(self, view_name, *args, **kwargs):
#         """Switch to the specified view"""
#         frame = self.frames[view_name]
#         frame.on_appear(*args, **kwargs)
#         frame.tkraise()