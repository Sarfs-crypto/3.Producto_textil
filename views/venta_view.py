"""
Vista para gestión de ventas
"""
import tkinter as tk
from tkinter import ttk, messagebox


class VentaView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.productos = []

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Panel superior: Productos y carrito
        paned = ttk.PanedWindow(main_frame, orient='horizontal')
        paned.pack(fill='both', expand=True)

        # Izquierda: Productos disponibles
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Productos Disponibles", font=('Arial', 12, 'bold')).pack(pady=5)

        # Búsqueda
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(search_frame, text="Buscar:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.buscar_producto)
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)

        # Tabla de productos
        prod_container = ttk.Frame(left_frame)
        prod_container.pack(fill='both', expand=True, padx=5, pady=5)

        scroll_y = ttk.Scrollbar(prod_container)
        scroll_y.pack(side='right', fill='y')

        self.tabla_productos = ttk.Treeview(prod_container,
                                            columns=('id', 'codigo', 'nombre', 'precio', 'stock'),
                                            show='tree headings',
                                            yscrollcommand=scroll_y.set,
                                            height=15)
        self.tabla_productos.pack(fill='both', expand=True)
        scroll_y.config(command=self.tabla_productos.yview)

        self.tabla_productos.heading('#0', text='')
        self.tabla_productos.column('#0', width=0)
        self.tabla_productos.heading('id', text='ID')
        self.tabla_productos.column('id', width=40)
        self.tabla_productos.heading('codigo', text='Código')
        self.tabla_productos.column('codigo', width=80)
        self.tabla_productos.heading('nombre', text='Nombre')
        self.tabla_productos.column('nombre', width=200)
        self.tabla_productos.heading('precio', text='Precio')
        self.tabla_productos.column('precio', width=80)
        self.tabla_productos.heading('stock', text='Stock')
        self.tabla_productos.column('stock', width=60)

        self.tabla_productos.bind('<Double-Button-1>', self.agregar_al_carrito)

        # Derecha: Carrito de compras
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)

        ttk.Label(right_frame, text="Carrito de Compras", font=('Arial', 12, 'bold')).pack(pady=5)

        # Tabla del carrito
        cart_container = ttk.Frame(right_frame)
        cart_container.pack(fill='both', expand=True, padx=5, pady=5)

        scroll_y_cart = ttk.Scrollbar(cart_container)
        scroll_y_cart.pack(side='right', fill='y')

        self.tabla_carrito = ttk.Treeview(cart_container,
                                          columns=('producto', 'cantidad', 'precio', 'subtotal'),
                                          show='tree headings',
                                          yscrollcommand=scroll_y_cart.set,
                                          height=10)
        self.tabla_carrito.pack(fill='both', expand=True)
        scroll_y_cart.config(command=self.tabla_carrito.yview)

        self.tabla_carrito.heading('#0', text='')
        self.tabla_carrito.column('#0', width=0)
        self.tabla_carrito.heading('producto', text='Producto')
        self.tabla_carrito.column('producto', width=200)
        self.tabla_carrito.heading('cantidad', text='Cantidad')
        self.tabla_carrito.column('cantidad', width=70)
        self.tabla_carrito.heading('precio', text='Precio Unit.')
        self.tabla_carrito.column('precio', width=80)
        self.tabla_carrito.heading('subtotal', text='Subtotal')
        self.tabla_carrito.column('subtotal', width=80)

        # Panel inferior: Total y acciones
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill='x', padx=5, pady=10)

        ttk.Label(bottom_frame, text="Total:", font=('Arial', 14, 'bold')).pack(side='left', padx=10)
        self.total_label = ttk.Label(bottom_frame, text="$0.00", font=('Arial', 14, 'bold'))
        self.total_label.pack(side='left', padx=10)

        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.pack(side='right')

        ttk.Button(btn_frame, text="Eliminar del Carrito", command=self.eliminar_del_carrito).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Registrar Venta", command=self.registrar_venta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar Carrito", command=self.limpiar_carrito).pack(side='left', padx=5)

        # Panel de ventas registradas
        ventas_frame = ttk.LabelFrame(main_frame, text="Ventas Registradas", padding=5)
        ventas_frame.pack(fill='both', expand=True, pady=10)

        ventas_container = ttk.Frame(ventas_frame)
        ventas_container.pack(fill='both', expand=True)

        scroll_y_ventas = ttk.Scrollbar(ventas_container)
        scroll_y_ventas.pack(side='right', fill='y')

        self.tabla_ventas = ttk.Treeview(ventas_container,
                                         columns=('id', 'codigo', 'fecha', 'cliente', 'total'),
                                         show='tree headings',
                                         yscrollcommand=scroll_y_ventas.set,
                                         height=6)
        self.tabla_ventas.pack(fill='both', expand=True)
        scroll_y_ventas.config(command=self.tabla_ventas.yview)

        self.tabla_ventas.heading('#0', text='')
        self.tabla_ventas.column('#0', width=0)
        self.tabla_ventas.heading('id', text='ID')
        self.tabla_ventas.column('id', width=40)
        self.tabla_ventas.heading('codigo', text='Código')
        self.tabla_ventas.column('codigo', width=100)
        self.tabla_ventas.heading('fecha', text='Fecha')
        self.tabla_ventas.column('fecha', width=120)
        self.tabla_ventas.heading('cliente', text='Cliente')
        self.tabla_ventas.column('cliente', width=150)
        self.tabla_ventas.heading('total', text='Total')
        self.tabla_ventas.column('total', width=80)

        self.tabla_ventas.bind('<Double-Button-1>', self.ver_detalle)

    def cargar_productos(self, productos):
        self.productos = productos
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for p in productos:
            self.tabla_productos.insert('', 'end', values=(
                p['id'], p['codigo'], p['nombre'], f"${p['precio_venta']:.2f}", p['stock']
            ), iid=p['id'])

    def buscar_producto(self, *args):
        busqueda = self.search_var.get().lower()
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for p in self.productos:
            if busqueda in p['nombre'].lower() or busqueda in p['codigo'].lower():
                self.tabla_productos.insert('', 'end', values=(
                    p['id'], p['codigo'], p['nombre'], f"${p['precio_venta']:.2f}", p['stock']
                ), iid=p['id'])

    def agregar_al_carrito(self, event):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            return

        producto_id = seleccion[0]

        dialog = tk.Toplevel(self.parent)
        dialog.title("Cantidad")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()

        ttk.Label(dialog, text="Cantidad:").pack(pady=10)
        cantidad_var = tk.StringVar(value="1")
        ttk.Entry(dialog, textvariable=cantidad_var, width=20).pack(pady=5)

        def confirmar():
            try:
                cantidad = int(cantidad_var.get())
                if cantidad > 0:
                    self.controller.agregar_al_carrito(producto_id, cantidad)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida")

        ttk.Button(dialog, text="Agregar", command=confirmar).pack(pady=10)

    def actualizar_carrito(self, carrito, total):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        for i, item in enumerate(carrito):
            self.tabla_carrito.insert('', 'end', values=(
                item['producto_nombre'], item['cantidad'],
                f"${item['precio_unitario']:.2f}", f"${item['subtotal']:.2f}"
            ), iid=str(i))

        self.total_label.config(text=f"${total:.2f}")

    def eliminar_del_carrito(self):
        seleccion = self.tabla_carrito.selection()
        if seleccion:
            index = int(seleccion[0])
            self.controller.eliminar_del_carrito(index)

    def limpiar_carrito(self):
        if messagebox.askyesno("Limpiar", "¿Limpiar todo el carrito?"):
            for item in self.tabla_carrito.get_children():
                self.tabla_carrito.delete(item)
            self.total_label.config(text="$0.00")

    def registrar_venta(self):
        dialog = tk.Toplevel(self.parent)
        dialog.title("Registrar Venta")
        dialog.geometry("400x200")
        dialog.transient(self.parent)
        dialog.grab_set()

        ttk.Label(dialog, text="Cliente:").pack(pady=10)
        cliente_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=cliente_var, width=40).pack(pady=5)

        ttk.Label(dialog, text=f"Total: {self.total_label.cget('text')}", font=('Arial', 12, 'bold')).pack(pady=10)

        def confirmar():
            self.controller.registrar_venta(cliente_var.get())
            dialog.destroy()

        ttk.Button(dialog, text="Confirmar Venta", command=confirmar).pack(pady=10)

    def actualizar_tabla(self, ventas):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for v in ventas:
            self.tabla_ventas.insert('', 'end', values=(
                v['id'], v['codigo_venta'], v['fecha'][:16],
                v['cliente'], f"${v['total']:.2f}"
            ), iid=v['id'])

    def ver_detalle(self, event):
        seleccion = self.tabla_ventas.selection()
        if seleccion:
            self.controller.ver_detalle_venta(seleccion[0])

    def mostrar_detalle_venta(self, venta, detalles):
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Detalle de Venta - {venta['codigo_venta']}")
        dialog.geometry("600x400")
        dialog.transient(self.parent)

        ttk.Label(dialog, text=f"Venta: {venta['codigo_venta']}", font=('Arial', 12, 'bold')).pack(pady=5)
        ttk.Label(dialog, text=f"Fecha: {venta['fecha']}").pack()
        ttk.Label(dialog, text=f"Cliente: {venta['cliente']}").pack()
        ttk.Label(dialog, text=f"Total: ${venta['total']:.2f}", font=('Arial', 12, 'bold')).pack(pady=5)

        ttk.Separator(dialog, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(dialog, text="Productos:", font=('Arial', 10, 'bold')).pack()

        tabla = ttk.Treeview(dialog, columns=('producto', 'cantidad', 'precio', 'subtotal'), show='headings', height=10)
        tabla.pack(fill='both', expand=True, padx=10, pady=5)

        tabla.heading('producto', text='Producto')
        tabla.heading('cantidad', text='Cantidad')
        tabla.heading('precio', text='Precio Unit.')
        tabla.heading('subtotal', text='Subtotal')

        for d in detalles:
            tabla.insert('', 'end', values=(
                d['producto_nombre'], d['cantidad'], f"${d['precio_unitario']:.2f}", f"${d['subtotal']:.2f}"
            ))

        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def limpiar_venta(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)
        self.total_label.config(text="$0.00")

    def apply_theme(self, theme):
        pass