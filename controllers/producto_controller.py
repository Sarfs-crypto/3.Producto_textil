"""
Controlador para gestión de productos
"""
import tkinter as tk
from tkinter import messagebox
from models.producto_model import ProductoModel
from utils.validators import Validators
from utils.exporters import Exporters
from utils.image_handler import ImageHandler
from datetime import datetime


class ProductoController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = ProductoModel()
        self.image_handler = ImageHandler()
        self.view = None
        self.producto_actual = None
        self.imagen_actual = None

    def set_view(self, view):
        self.view = view

    def cargar_datos(self):
        if self.view:
            productos = self.model.listar_todos()
            self.view.actualizar_tabla(productos)

    def guardar_producto(self, datos):
        # Validaciones
        if not Validators.validar_codigo(datos['codigo']):
            messagebox.showerror("Error", "El código debe tener al menos 3 caracteres")
            return False

        if not Validators.validar_longitud_texto(datos['nombre'], 3, 200):
            messagebox.showerror("Error", "El nombre debe tener entre 3 y 200 caracteres")
            return False

        if not Validators.validar_precio(datos['precio_compra']):
            messagebox.showerror("Error", "El precio de compra debe ser un número positivo")
            return False

        if not Validators.validar_precio(datos['precio_venta']):
            messagebox.showerror("Error", "El precio de venta debe ser un número positivo")
            return False

        if not Validators.validar_entero(datos['stock']):
            messagebox.showerror("Error", "El stock debe ser un número entero")
            return False

        if not Validators.validar_entero(datos['stock_minimo']):
            messagebox.showerror("Error", "El stock mínimo debe ser un número entero")
            return False

        # Procesar imagen
        imagen_path = None
        if self.imagen_actual:
            imagen_path = self.image_handler.procesar_imagen(
                self.imagen_actual,
                nombre_archivo=f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
        elif self.producto_actual and self.producto_actual.get('imagen_path'):
            imagen_path = self.producto_actual['imagen_path']

        datos['imagen_path'] = imagen_path

        if self.producto_actual:
            exito = self.model.actualizar(self.producto_actual['id'], datos)
            if exito:
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        else:
            producto_id = self.model.insertar(datos)
            if producto_id:
                messagebox.showinfo("Éxito", f"Producto guardado correctamente")

        self.limpiar_formulario()
        self.cargar_datos()
        return True

    def eliminar_producto(self, producto_id):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            exito = self.model.eliminar(producto_id)
            if exito:
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.limpiar_formulario()
                self.cargar_datos()

    def buscar(self, busqueda):
        resultados = self.model.buscar(busqueda)
        if self.view:
            self.view.actualizar_tabla(resultados)

    def seleccionar_imagen(self):
        imagen_path = self.image_handler.seleccionar_imagen()
        if imagen_path:
            self.imagen_actual = imagen_path
            imagen_tk = self.image_handler.cargar_imagen_para_tk(imagen_path)
            if imagen_tk and self.view:
                self.view.mostrar_imagen_preview(imagen_tk)

    def limpiar_formulario(self):
        self.producto_actual = None
        self.imagen_actual = None
        if self.view:
            self.view.limpiar_formulario()

    def exportar_excel(self):
        productos = self.model.listar_todos()
        if productos:
            columnas = ['ID', 'Código', 'Nombre', 'Categoría', 'Talla', 'Color', 'Precio Compra', 'Precio Venta',
                        'Stock']
            Exporters.exportar_a_excel(productos, columnas, "TextilPro_Productos")
        else:
            messagebox.showwarning("Sin datos", "No hay productos para exportar")

    def exportar_pdf(self):
        productos = self.model.listar_todos()
        if productos:
            columnas = ['ID', 'Código', 'Nombre', 'Categoría', 'Precio Venta', 'Stock']
            Exporters.exportar_a_pdf(productos, columnas, "TextilPro_Productos")

    def cargar_producto_para_editar(self, producto):
        self.producto_actual = producto
        if self.view:
            self.view.cargar_datos_formulario(producto)

    def apply_theme(self, theme):
        if self.view:
            self.view.apply_theme(theme)

def cargar_producto_para_editar(self, producto):
    """Cargar producto para editar"""
    self.producto_actual = producto
    if self.view:
        self.view.cargar_datos_formulario(producto)