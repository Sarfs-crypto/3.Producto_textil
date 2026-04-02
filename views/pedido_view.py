"""
Vista para gestión de pedidos
Cumple con: Selector de fecha con tkcalendar
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from utils.validators import Validators


class PedidoView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.pedido_actual = None
        self.clientes_dict = {}
        self.productos_dict = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Pedido", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)

        # Cliente
        ttk.Label(form_frame, text="Cliente (*):").grid(row=0, column=0, sticky='w', pady=5)
        self.cliente_combo = ttk.Combobox(form_frame, state='readonly', width=37)
        self.cliente_combo.grid(row=0, column=1, pady=5, padx=5)

        # Producto
        ttk.Label(form_frame, text="Producto (*):").grid(row=1, column=0, sticky='w', pady=5)
        self.producto_combo = ttk.Combobox(form_frame, state='readonly', width=37)
        self.producto_combo.grid(row=1, column=1, pady=5, padx=5)

        # Cantidad (solo números)
        ttk.Label(form_frame, text="Cantidad (*):").grid(row=2, column=0, sticky='w', pady=5)
        vcmd = (form_frame.register(Validators.solo_numeros), '%P')
        self.cantidad_var = tk.StringVar()
        self.cantidad_entry = ttk.Entry(form_frame, textvariable=self.cantidad_var,
                                        validate='key', validatecommand=vcmd, width=20)
        self.cantidad_entry.grid(row=2, column=1, pady=5, padx=5, sticky='w')

        # Fecha Pedido (con tkcalendar)
        ttk.Label(form_frame, text="Fecha Pedido (*):").grid(row=3, column=0, sticky='w', pady=5)
        self.fecha_pedido = DateEntry(form_frame, width=20, date_pattern='yyyy-mm-dd')
        self.fecha_pedido.grid(row=3, column=1, pady=5, padx=5, sticky='w')

        # Fecha Entrega (con tkcalendar)
        ttk.Label(form_frame, text="Fecha Entrega:").grid(row=4, column=0, sticky='w', pady=5)
        self.fecha_entrega = DateEntry(form_frame, width=20, date_pattern='yyyy-mm-dd')
        self.fecha_entrega.grid(row=4, column=1, pady=5, padx=5, sticky='w')

        # Estado
        ttk.Label(form_frame, text="Estado:").grid(row=5, column=0, sticky='w', pady=5)
        self.estado_combo = ttk.Combobox(form_frame, state='readonly', width=20)
        self.estado_combo['values'] = ('pendiente', 'en proceso', 'completado', 'cancelado')
        self.estado_combo.set('pendiente')
        self.estado_combo.grid(row=5, column=1, pady=5, padx=5, sticky='w')

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpiar", command=self.limpiar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar).pack(side='left', padx=5)

        # Tabla
        table_frame = ttk.LabelFrame(main_frame, text="Listado de Pedidos", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')

        self.tabla = ttk.Treeview(table_frame,
                                  columns=('id', 'cliente', 'producto', 'cantidad', 'fecha_pedido', 'fecha_entrega',
                                           'estado'),
                                  show='headings',
                                  yscrollcommand=scroll_y.set)
        self.tabla.pack(fill='both', expand=True)
        scroll_y.config(command=self.tabla.yview)

        # Configurar columnas
        self.tabla.heading('id', text='ID')
        self.tabla.heading('cliente', text='Cliente')
        self.tabla.heading('producto', text='Producto')
        self.tabla.heading('cantidad', text='Cantidad')
        self.tabla.heading('fecha_pedido', text='Fecha Pedido')
        self.tabla.heading('fecha_entrega', text='Fecha Entrega')
        self.tabla.heading('estado', text='Estado')

        self.tabla.column('id', width=50)
        self.tabla.column('cliente', width=150)
        self.tabla.column('producto', width=150)
        self.tabla.column('cantidad', width=70)
        self.tabla.column('fecha_pedido', width=100)
        self.tabla.column('fecha_entrega', width=100)
        self.tabla.column('estado', width=100)

        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

    def cargar_combo_clientes(self, clientes):
        self.clientes_dict = {c['nombre']: c['id'] for c in clientes}
        self.cliente_combo['values'] = list(self.clientes_dict.keys())

    def cargar_combo_productos(self, productos):
        self.productos_dict = {p['nombre']: p['id'] for p in productos}
        self.producto_combo['values'] = list(self.productos_dict.keys())

    def actualizar_tabla(self, pedidos):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for pedido in pedidos:
            self.tabla.insert('', 'end', values=(
                pedido['id'],
                pedido.get('cliente_nombre', ''),
                pedido.get('producto_nombre', ''),
                pedido['cantidad'],
                pedido['fecha_pedido'],
                pedido.get('fecha_entrega', ''),
                pedido.get('estado', 'pendiente')
            ))

    def on_select(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            pedido_id = item['values'][0]
            self.pedido_actual = self.controller.obtener_por_id(pedido_id)
            if self.pedido_actual:
                self.cargar_datos_formulario(self.pedido_actual)

    def cargar_datos_formulario(self, pedido):
        # Seleccionar cliente
        for nombre, id_cliente in self.clientes_dict.items():
            if id_cliente == pedido['cliente_id']:
                self.cliente_combo.set(nombre)
                break
        # Seleccionar producto
        for nombre, id_producto in self.productos_dict.items():
            if id_producto == pedido['producto_id']:
                self.producto_combo.set(nombre)
                break

        self.cantidad_var.set(str(pedido['cantidad']))
        self.fecha_pedido.set_date(pedido['fecha_pedido'])
        if pedido.get('fecha_entrega'):
            self.fecha_entrega.set_date(pedido['fecha_entrega'])
        self.estado_combo.set(pedido.get('estado', 'pendiente'))

    def guardar(self):
        datos = {
            'cliente_id': self.clientes_dict.get(self.cliente_combo.get()),
            'producto_id': self.productos_dict.get(self.producto_combo.get()),
            'cantidad': self.cantidad_var.get(),
            'fecha_pedido': self.fecha_pedido.get(),
            'fecha_entrega': self.fecha_entrega.get(),
            'estado': self.estado_combo.get()
        }
        self.controller.guardar(datos, self.pedido_actual)
        self.limpiar()

    def eliminar(self):
        if self.pedido_actual:
            self.controller.eliminar(self.pedido_actual['id'])
            self.limpiar()

    def limpiar(self):
        self.pedido_actual = None
        self.cliente_combo.set('')
        self.producto_combo.set('')
        self.cantidad_var.set('')
        self.estado_combo.set('pendiente')
        self.tabla.selection_remove(self.tabla.selection())

    def apply_theme(self, theme):
        self.parent.configure(bg=theme['bg'])