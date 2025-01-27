import tkinter as tk
from tkinter import ttk, messagebox
import func.cards as cards
from config import APP_FONT
from .common import AbstractFrame


class CardsView(AbstractFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure main frame grid
        self.grid(row=0, column=0, sticky="NSEW")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Make the parent window expand
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Top navigation bar
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=0, column=0, sticky="EW", padx=10, pady=5)
        nav_frame.grid_columnconfigure(1, weight=1)  # Make title expand
        
        # Back button
        back_btn = ttk.Button(
            nav_frame,
            text="← Wstecz",
            style="SmallButton.TButton",
            command=lambda: controller.show_view("HomeView")
        )
        back_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Title (centered)
        title_label = ttk.Label(
            nav_frame,
            text="Zarządzanie kartami",
            font=APP_FONT,
            anchor="center"
        )
        title_label.grid(row=0, column=1)
        
        # Add Card button
        add_btn = ttk.Button(
            nav_frame,
            text="Dodaj Kartę",
            style="SmallButton.TButton",
            command=self.add_card
        )
        add_btn.grid(row=0, column=2, padx=(10, 0))

        # Table frame with scrollbar
        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="NSEW", padx=10, pady=5)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(table_frame)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"),
                width=self.canvas.winfo_width()
            )
        )
        
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window,
                width=e.width
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.grid(row=0, column=0, sticky="NSEW")
        scrollbar.grid(row=0, column=1, sticky="NS")
        
        # Configure columns
        self.scrollable_frame.grid_columnconfigure(0, weight=2)  # RFID
        self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Balance
        self.scrollable_frame.grid_columnconfigure(2, weight=2)  # Actions

        self.on_appear()

    def on_appear(self):
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Add headers
        ttk.Label(
            self.scrollable_frame,
            text="RFID",
            font=APP_FONT,
            anchor="center"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        
        ttk.Label(
            self.scrollable_frame,
            text="Saldo",
            font=APP_FONT,
            anchor="center"
        ).grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        
        ttk.Label(
            self.scrollable_frame,
            text="Akcja",
            font=APP_FONT,
            anchor="center"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="EW")
        
        # Add main separator after headers
        separator = ttk.Separator(self.scrollable_frame, orient="horizontal", style="MainSeparator.TSeparator")
        separator.grid(row=1, column=0, columnspan=3, sticky="EW", pady=2)
        
        # Add data rows
        cards_data = cards.get_all_cards()
        for i, card in enumerate(cards_data):
            draw_at_row = i * 2 + 2  # Account for separators
            
            # RFID (centered)
            ttk.Label(
                self.scrollable_frame,
                text=card.rfid,
                font=APP_FONT,
                anchor="center"
            ).grid(row=draw_at_row, column=0, padx=5, pady=5, sticky="EW")

            # Balance (centered)
            ttk.Label(
                self.scrollable_frame,
                text=f"{card.balance:.2f} zł",
                font=APP_FONT,
                anchor="center"
            ).grid(row=draw_at_row, column=1, padx=5, pady=5, sticky="EW")

            # Actions frame (centered)
            actions_frame = ttk.Frame(self.scrollable_frame)
            actions_frame.grid(row=draw_at_row, column=2, padx=5, pady=5, sticky="EW")
            actions_frame.grid_columnconfigure(0, weight=1)  # Left padding
            actions_frame.grid_columnconfigure(2, weight=1)  # Right padding
            
            # Delete button
            ttk.Button(
                actions_frame,
                text="Usuń",
                style="SmallButton.TButton",
                command=lambda c=card: self.delete_card(c)
            ).grid(row=0, column=1, padx=2)
            
            # Add separator after each row (except the last one)
            if i < len(cards_data):
                separator = ttk.Separator(self.scrollable_frame, orient="horizontal", style="SmallSeparator.TSeparator")
                separator.grid(row=draw_at_row+1, column=0, columnspan=3, sticky="EW", pady=1)

    def add_card(self):
        self.controller.show_view("AddCardView")
        
    def delete_card(self, card: cards.CardData):
        if messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć kartę {card.rfid}?"):
            if cards.delete_card(card.id):
                messagebox.showinfo("Informacja", "Karta została usunięta")
                self.on_appear()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć karty")