"""
Controlador para gestión de clientes
Cumple con: Validaciones, confirmación antes de eliminar
"""
from tkinter import messagebox
from models.cliente_model import ClienteModel
from utils.validators import Validators
from utils.exporters import Exporters
from utils.image_handler import ImageHandler


class ClienteController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = ClienteModel()
        self.image_handler = ImageHandler()
        self.view = None
        self.imagen_actual = None

    def set_view(self, view):
        self.view = view

    def cargar_datos(self):
        if self.view:
            datos = self.model.listar_todos()
            self.view.actualizar_tabla(datos)

    def obtener_por_id(self, id):
        return self.model.obtener_por_id(id)

    def guardar(self, datos, actual=None):
        # Validaciones
        if not Validators.validar_longitud(datos.get('nombre', ''), 3, 100):
            messagebox.showerror("Error", "El nombre debe tener entre 3 y 100 caracteres")
            return False

        if datos.get('email') and not Validators.validar_email(datos['email']):
            messagebox.showerror("Error", "Formato de email inválido.\nEjemplo: usuario@dominio.com")
            return False

        # Procesar imagen
        imagen_path = None
        if self.imagen_actual:
            imagen_path = self.image_handler.procesar_imagen(self.imagen_actual)

        if actual and actual.get('id'):
            exito = self.model.actualizar(
                actual['id'],
                datos['nombre'],
                datos.get('telefono', ''),
                datos.get('email', ''),
                datos.get('direccion', ''),
                imagen_path
            )
            if exito:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
            id = self.model.insertar(
                datos['nombre'],
                datos.get('telefono', ''),
                datos.get('email', ''),
                datos.get('direccion', ''),
                imagen_path
            )
            if id:
                messagebox.showinfo("Éxito", f"Cliente guardado con ID: {id}")

        self.imagen_actual = None
        self.cargar_datos()
        return True

    def eliminar(self, id):
        """Eliminar cliente con confirmación"""
        if messagebox.askyesno("Confirmar eliminación",
                               "¿Está SEGURO de eliminar este cliente?\nEsta acción no se puede deshacer."):
            if self.model.eliminar(id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargar_datos()
                return True
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")
        return False

    def buscar(self, busqueda):
        if self.view:
            resultados = self.model.buscar(busqueda)
            self.view.actualizar_tabla(resultados)

    def exportar_excel(self):
        datos = self.model.listar_todos()
        if datos:
            columnas = ['ID', 'Nombre', 'Teléfono', 'Email', 'Dirección']
            Exporters.exportar_excel(datos, columnas, "Clientes")
        else:
            messagebox.showwarning("Sin datos", "No hay clientes para exportar")

    def exportar_pdf(self):
        datos = self.model.listar_todos()
        if datos:
            columnas = ['ID', 'Nombre', 'Teléfono', 'Email', 'Dirección']
            Exporters.exportar_pdf(datos, columnas, "Clientes")
        else:
            messagebox.showwarning("Sin datos", "No hay clientes para exportar")

    def apply_theme(self, theme):
        if self.view:
            self.view.apply_theme(theme)