"""
Controlador principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.main_view import MainView
from controllers.producto_controller import ProductoController
from controllers.proveedor_controller import ProveedorController
from controllers.venta_controller import VentaController
from utils.themes import Themes


class MainController:
    def __init__(self, root):
        self.root = root

        # Crear controladores secundarios
        self.producto_controller = ProductoController(self)
        self.proveedor_controller = ProveedorController(self)
        self.venta_controller = VentaController(self)

        # Crear vista principal
        self.view = MainView(self)

    def toggle_theme(self):
        """Cambiar tema de la aplicación"""
        theme = Themes.toggle_theme()
        self.view.apply_theme(theme)
        self.producto_controller.apply_theme(theme)
        self.proveedor_controller.apply_theme(theme)
        self.venta_controller.apply_theme(theme)

    def mostrar_productos(self):
        """Mostrar vista de productos"""
        self.view.mostrar_frame('productos')
        self.producto_controller.cargar_datos()

    def mostrar_proveedores(self):
        """Mostrar vista de proveedores"""
        self.view.mostrar_frame('proveedores')
        self.proveedor_controller.cargar_datos()

    def mostrar_ventas(self):
        """Mostrar vista de ventas"""
        self.view.mostrar_frame('ventas')
        self.venta_controller.cargar_datos()

    def exportar_todo_excel(self):
        """Exportar todos los datos"""
        from utils.exporters import Exporters

        # Productos
        productos = self.producto_controller.model.listar_todos()
        if productos:
            columnas = ['ID', 'Código', 'Nombre', 'Categoría', 'Talla', 'Color', 'Precio Venta', 'Stock']
            Exporters.exportar_a_excel(productos, columnas, "TextilPro_Productos")

        # Proveedores
        proveedores = self.proveedor_controller.model.listar_todos()
        if proveedores:
            columnas = ['ID', 'RUC', 'Nombre', 'Contacto', 'Teléfono', 'Email']
            Exporters.exportar_a_excel(proveedores, columnas, "TextilPro_Proveedores")