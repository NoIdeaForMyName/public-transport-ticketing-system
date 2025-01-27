from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk

from config import APP_FONT


class AbstractFrame(tk.Frame, ABC):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    @abstractmethod
    def on_appear(self):
        pass

def setup_styles():
    styleHugeButton = ttk.Style()
    styleHugeButton.configure(
        "HugeButton.TButton",
        padding=20,
        font=APP_FONT,
    )

    styleSmallButton = ttk.Style()
    styleSmallButton.configure(
        "SmallButton.TButton",
        font=APP_FONT,
    )
    
    style = ttk.Style()
    
    # Configure Treeview style
    style.configure(
        "Custom.Treeview",
        font=APP_FONT,
        rowheight=40,
        background="white",
        fieldbackground="white",
        borderwidth=1,
        relief="solid"
    )
    
    # Configure Treeview heading style
    style.configure(
        "Custom.Treeview.Heading",
        font=APP_FONT,
        relief="flat",
        padding=5
    )

    # Configure selection colors
    style.map(
        "Custom.Treeview",
        background=[("selected", "#e6e6e6")],  # Light gray when selected
        foreground=[("selected", "black")]      # Keep text black when selected
    )

    styleMainSeparator = ttk.Style()
    styleMainSeparator.configure(
        "MainSeparator.TSeparator",
        background="black",
        thickness=2
    )

    styleSmallSeparator = ttk.Style()
    styleSmallSeparator.configure(
        "SmallSeparator.TSeparator",
        background="#d9d9d9",
        thickness=1
    )