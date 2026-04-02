import tkinter as tk
from controllers.main_controller import MainController

class TextilProApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TextilPro - Sistema de Gestión Textil")
        self.root.geometry("1400x800")
        self.controller = MainController(self.root)
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TextilProApp()
    app.run()