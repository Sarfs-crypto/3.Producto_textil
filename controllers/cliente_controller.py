"""
Controlador para gestión de clientes
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
            self.view.actualizar_tabla(datos if datos else [])

    def obtener_por_id(self, id):
        return self.model.obtener_por_id(id)

    def guardar(self, datos, actual=None):
        # Validar nombre
        nombre = datos.get('nombre', '').strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return False

        if not Validators.validar_longitud(nombre, 3, 100):
            messagebox.showerror("Error", "El nombre debe tener entre 3 y 100 caracteres")
            return False

        # Validar email
        email = datos.get('email', '').strip()
        if email and not Validators.validar_email(email):
            messagebox.showerror("Error", "Formato de email inválido.\nEjemplo: usuario@dominio.com")
            return False

        # Procesar imagen
        imagen_path = None
        if self.imagen_actual:
            imagen_path = self.image_handler.procesar_imagen(self.imagen_actual)
            print(f"DEBUG - Imagen procesada: {imagen_path}")

        try:
            if actual and actual.get('id'):
                # ACTUALIZAR
                print(f"DEBUG - Actualizando cliente ID: {actual['id']}")
                exito = self.model.actualizar(
                    actual['id'],
                    nombre,
                    datos.get('telefono', ''),
                    email,
                    datos.get('direccion', ''),
                    imagen_path
                )
                if exito:
                    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                    self.cargar_datos()
                    return True
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el cliente")
                    return False
            else:
                # INSERTAR NUEVO
                print("DEBUG - Insertando nuevo cliente")
                nuevo_id = self.model.insertar(
                    nombre,
                    datos.get('telefono', ''),
                    email,
                    datos.get('direccion', ''),
                    imagen_path
                )
                print(f"DEBUG - ID generado: {nuevo_id}")

                if nuevo_id:
                    messagebox.showinfo("Éxito", f"Cliente guardado con ID: {nuevo_id}")
                    self.cargar_datos()
                    self.limpiar_formulario()
                    return True
                else:
                    messagebox.showerror("Error", "No se pudo guardar el cliente. Verifique que el email no esté duplicado.")
                    return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
            return False
        finally:
            self.imagen_actual = None

    def limpiar_formulario(self):
        """Limpiar el formulario desde el controlador"""
        if self.view:
            self.view.limpiar()
        self.imagen_actual = None

    def eliminar(self, id):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            if self.model.eliminar(id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargar_datos()
                if self.view:
                    self.view.limpiar()
                return True
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")
        return False

    def buscar(self, busqueda):
        if self.view:
            resultados = self.model.buscar(busqueda)
            self.view.actualizar_tabla(resultados if resultados else [])

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