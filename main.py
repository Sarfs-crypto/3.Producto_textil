
import tkinter as tk
from controllers.main_controller import MainController
import os


class TextilProApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TextilPro - Sistema de Gestión Textil Profesional")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 600)

        # Configurar favicon (si existe)
        if os.path.exists("assets/favicon.ico"):
            try:
                self.root.iconbitmap("assets/favicon.ico")
            except:
                pass

        # Inicializar controlador principal
        self.controller = MainController(self.root)

        # Configurar cierre limpio
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Cerrar la aplicación limpiamente"""
        if tk.messagebox.askyesno("Salir", "¿Está seguro de salir?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TextilProApp()
    app.run()