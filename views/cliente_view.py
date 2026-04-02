import tkinter as tk
from tkinter import ttk, messagebox


class ClienteView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.crear_interfaz()

    def crear_interfaz(self):
        frame = ttk.Frame(self.parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Gestión de Clientes", font=('Arial', 14, 'bold')).pack(pady=10)
        ttk.Label(frame, text="Módulo en construcción").pack(pady=20)

    def actualizar_tabla(self, datos):
        pass

    def limpiar_formulario(self):
        pass

    def apply_theme(self, theme):
        pass