"""
Controlador para gestión de pedidos
"""
from tkinter import messagebox
from models.pedido_model import PedidoModel
from models.cliente_model import ClienteModel
from models.producto_model import ProductoModel
from utils.exporters import Exporters


class PedidoController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = PedidoModel()
        self.cliente_model = ClienteModel()
        self.producto_model = ProductoModel()
        self.view = None

    def set_view(self, view):
        self.view = view

    def cargar_datos(self):
        if self.view:
            pedidos = self.model.listar_todos()
            self.view.actualizar_tabla(pedidos)

            # Cargar combos
            clientes = self.cliente_model.listar_todos()
            productos = self.producto_model.listar_todos()
            self.view.cargar_combo_clientes(clientes)
            self.view.cargar_combo_productos(productos)

    def obtener_por_id(self, id):
        return self.model.obtener_por_id(id)

    def guardar(self, datos, actual=None):
        # Validaciones
        if not datos.get('cliente_id'):
            messagebox.showerror("Error", "Seleccione un cliente")
            return False

        if not datos.get('producto_id'):
            messagebox.showerror("Error", "Seleccione un producto")
            return False

        if int(datos.get('cantidad', 0)) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return False

        if actual and actual.get('id'):
            exito = self.model.actualizar(
                actual['id'],
                datos['cliente_id'],
                datos['producto_id'],
                int(datos['cantidad']),
                datos.get('fecha_entrega', ''),
                datos['estado']
            )
            if exito:
                messagebox.showinfo("Éxito", "Pedido actualizado correctamente")
        else:
            id = self.model.insertar(
                datos['cliente_id'],
                datos['producto_id'],
                int(datos['cantidad']),
                datos['fecha_pedido'],
                datos.get('fecha_entrega', '')
            )
            if id:
                messagebox.showinfo("Éxito", f"Pedido guardado con ID: {id}")

        self.cargar_datos()
        return True

    def eliminar(self, id):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este pedido?"):
            if self.model.eliminar(id):
                messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
                self.cargar_datos()
                return True
        return False

    def buscar(self, busqueda):
        if self.view:
            resultados = self.model.buscar(busqueda)
            self.view.actualizar_tabla(resultados)

    def exportar_excel(self):
        datos = self.model.listar_todos()
        if datos:
            columnas = ['ID', 'Cliente', 'Producto', 'Cantidad', 'Fecha Pedido', 'Fecha Entrega', 'Estado']
            Exporters.exportar_excel(datos, columnas, "Pedidos")
        else:
            messagebox.showwarning("Sin datos", "No hay pedidos para exportar")

    def exportar_pdf(self):
        datos = self.model.listar_todos()
        if datos:
            columnas = ['ID', 'Cliente', 'Producto', 'Cantidad', 'Fecha Pedido', 'Fecha Entrega', 'Estado']
            Exporters.exportar_pdf(datos, columnas, "Pedidos")
        else:
            messagebox.showwarning("Sin datos", "No hay pedidos para exportar")

    def apply_theme(self, theme):
        if self.view:
            self.view.apply_theme(theme)