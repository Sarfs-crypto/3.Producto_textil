"""
Controlador para gestión de proveedores
"""
from tkinter import messagebox
from models.proveedor_model import ProveedorModel
from utils.validators import Validators
from utils.exporters import Exporters
from utils.image_handler import ImageHandler
from datetime import datetime


class ProveedorController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = ProveedorModel()
        self.image_handler = ImageHandler()
        self.view = None
        self.proveedor_actual = None
        self.imagen_actual = None

    def set_view(self, view):
        self.view = view

    def cargar_datos(self):
        if self.view:
            proveedores = self.model.listar_todos()
            self.view.actualizar_tabla(proveedores)

    def guardar_proveedor(self, datos):
        # Validaciones
        if not Validators.validar_ruc(datos['ruc']):
            messagebox.showerror("Error", "RUC inválido (debe tener 11 dígitos)")
            return False

        if not Validators.validar_longitud_texto(datos['nombre'], 3, 200):
            messagebox.showerror("Error", "El nombre debe tener entre 3 y 200 caracteres")
            return False

        if datos['email'] and not Validators.validar_email(datos['email']):
            messagebox.showerror("Error", "Email inválido")
            return False

        if datos['telefono'] and not Validators.validar_telefono(datos['telefono']):
            messagebox.showerror("Error", "Teléfono inválido (debe tener 7-15 dígitos)")
            return False

        # Procesar imagen
        imagen_path = None
        if self.imagen_actual:
            imagen_path = self.image_handler.procesar_imagen(
                self.imagen_actual,
                nombre_archivo=f"prov_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
        elif self.proveedor_actual and self.proveedor_actual.get('imagen_path'):
            imagen_path = self.proveedor_actual['imagen_path']

        datos['imagen_path'] = imagen_path

        if self.proveedor_actual:
            exito = self.model.actualizar(self.proveedor_actual['id'], datos)
            if exito:
                messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
        else:
            proveedor_id = self.model.insertar(datos)
            if proveedor_id:
                messagebox.showinfo("Éxito", "Proveedor guardado correctamente")

        self.limpiar_formulario()
        self.cargar_datos()
        return True

    def eliminar_proveedor(self, proveedor_id):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?"):
            exito = self.model.eliminar(proveedor_id)
            if exito:
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
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
        self.proveedor_actual = None
        self.imagen_actual = None
        if self.view:
            self.view.limpiar_formulario()

    def exportar_excel(self):
        proveedores = self.model.listar_todos()
        if proveedores:
            columnas = ['ID', 'RUC', 'Nombre', 'Contacto', 'Teléfono', 'Email', 'Dirección']
            Exporters.exportar_a_excel(proveedores, columnas, "TextilPro_Proveedores")

    def exportar_pdf(self):
        proveedores = self.model.listar_todos()
        if proveedores:
            columnas = ['ID', 'RUC', 'Nombre', 'Contacto', 'Teléfono']
            Exporters.exportar_a_pdf(proveedores, columnas, "TextilPro_Proveedores")

    def cargar_proveedor_para_editar(self, proveedor):
        self.proveedor_actual = proveedor
        if self.view:
            self.view.cargar_datos_formulario(proveedor)

    def apply_theme(self, theme):
        if self.view:
            self.view.apply_theme(theme)

def cargar_proveedor_para_editar(self, proveedor):
    """Cargar proveedor para editar"""
    self.proveedor_actual = proveedor
    if self.view:
        self.view.cargar_datos_formulario(proveedor)