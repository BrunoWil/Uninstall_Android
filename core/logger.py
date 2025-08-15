import tkinter as tk


class Logger:
    """Gerencia o log visual na interface."""

    def __init__(self, text_widget: tk.Text):
        self.text_widget = text_widget

    def log(self, texto: str):
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, texto + "\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")
