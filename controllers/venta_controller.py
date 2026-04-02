"""
Controlador para gestión de ventas
"""
from tkinter import messagebox
from models.venta_model import VentaModel
from models.producto_model import ProductoModel
from utils.exporters import Exporters


class VentaController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.model = VentaModel()
        self.producto_model = ProductoModel()
        self.view = None
        self.carrito = []
        self.total = 0

    def set_view(self, view):
        self.view = view

    def cargar_datos(self):
        if self.view:
            ventas = self.model.listar_ventas()
            self.view.actualizar_tabla(ventas)

    def cargar_productos_para_venta(self):
        productos = self.producto_model.listar_todos()
        if self.view:
            self.view.cargar_productos(productos)

    def agregar_al_carrito(self, producto_id, cantidad):
        producto = self.producto_model.obtener_por_id(producto_id)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return False

        if producto['stock'] < cantidad:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
            return False

        precio = float(producto['precio_venta'])
        subtotal = precio * cantidad

        item = {
            'producto_id': producto['id'],
            'producto_nombre': producto['nombre'],
            'codigo': producto['codigo'],
            'cantidad': cantidad,
            'precio_unitario': precio,
            'subtotal': subtotal
        }

        self.carrito.append(item)
        self.total += subtotal

        if self.view:
            self.view.actualizar_carrito(self.carrito, self.total)

        return True

    def eliminar_del_carrito(self, index):
        if 0 <= index < len(self.carrito):
            self.total -= self.carrito[index]['subtotal']
            del self.carrito[index]
            if self.view:
                self.view.actualizar_carrito(self.carrito, self.total)

    def registrar_venta(self, cliente):
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "Agregue productos a la venta")
            return False

        if not cliente:
            cliente = "Cliente General"

        detalles = []
        for item in self.carrito:
            detalles.append({
                'producto_id': item['producto_id'],
                'cantidad': item['cantidad'],
                'precio_unitario': item['precio_unitario'],
                'subtotal': item['subtotal']
            })

        datos = {
            'cliente': cliente,
            'total': self.total,
            'detalles': detalles
        }

        venta_id = self.model.registrar_venta(datos)

        if venta_id:
            messagebox.showinfo("Éxito", f"Venta registrada correctamente\nTotal: ${self.total:,.2f}")
            self.carrito = []
            self.total = 0
            self.cargar_datos()
            if self.view:
                self.view.limpiar_venta()
                self.view.actualizar_carrito([], 0)
            return True
        else:
            messagebox.showerror("Error", "Error al registrar la venta")
            return False

    def ver_detalle_venta(self, venta_id):
        venta = self.model.obtener_por_id(venta_id)
        detalles = self.model.obtener_detalles_venta(venta_id)
        if self.view:
            self.view.mostrar_detalle_venta(venta, detalles)

    def exportar_excel(self):
        ventas = self.model.listar_ventas()
        if ventas:
            columnas = ['ID', 'Código Venta', 'Fecha', 'Cliente', 'Total']
            Exporters.exportar_a_excel(ventas, columnas, "TextilPro_Ventas")

    def exportar_pdf(self):
        ventas = self.model.listar_ventas()
        if ventas:
            columnas = ['ID', 'Código Venta', 'Fecha', 'Cliente', 'Total']
            Exporters.exportar_a_pdf(ventas, columnas, "TextilPro_Ventas")

    def apply_theme(self, theme):
        if self.view:
            self.view.apply_theme(theme)