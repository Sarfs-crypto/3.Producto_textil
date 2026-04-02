"""""
Controlador principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from controllers.cliente_controller import ClienteController
from controllers.producto_controller import ProductoController
from controllers.pedido_controller import PedidoController
from utils.themes import Themes

class MainController:
    def __init__(self, root):
        self.root = root
        self.current_theme = Themes.current

        # Inicializar controladores secundarios
        self.cliente_controller = ClienteController(self)
        self.producto_controller = ProductoController(self)
        self.pedido_controller = PedidoController(self)

        # Crear vista principal
        self.view = MainView(self)

        # Aplicar tema inicial
        self.root.configure(bg=self.current_theme['bg'])

    def toggle_theme(self):
        """Cambiar entre tema claro y oscuro"""
        self.current_theme = Themes.toggle()
        self.root.configure(bg=self.current_theme['bg'])
        self.view.apply_theme(self.current_theme)
        self.cliente_controller.apply_theme(self.current_theme)
        self.producto_controller.apply_theme(self.current_theme)
        self.pedido_controller.apply_theme(self.current_theme)

    def mostrar_clientes(self):
        self.view.mostrar_frame('clientes')
        self.cliente_controller.cargar_datos()

    def mostrar_productos(self):
        self.view.mostrar_frame('productos')
        self.producto_controller.cargar_datos()

    def mostrar_pedidos(self):
        self.view.mostrar_frame('pedidos')
        self.pedido_controller.cargar_datos()