"""
Vista para gestión de productos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import Validators
from utils.image_handler import ImageHandler

class ProductoView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.image_handler = ImageHandler()
        self.producto_actual = None
        self.imagen_preview = None
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)

        # Nombre
        ttk.Label(form_frame, text="Nombre (*):").grid(row=0, column=0, sticky='w', pady=5)
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(form_frame, textvariable=self.nombre_var, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5, padx=5)

        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky='w', pady=5)
        self.descripcion_text = tk.Text(form_frame, height=3, width=30)
        self.descripcion_text.grid(row=1, column=1, pady=5, padx=5)

        # Precio (solo números decimales)
        ttk.Label(form_frame, text="Precio (*):").grid(row=2, column=0, sticky='w', pady=5)
        vcmd_decimal = (form_frame.register(Validators.solo_numeros_decimales), '%P')
        self.precio_var = tk.StringVar()
        self.precio_entry = ttk.Entry(form_frame, textvariable=self.precio_var,
                                      validate='key', validatecommand=vcmd_decimal, width=20)
        self.precio_entry.grid(row=2, column=1, pady=5, padx=5, sticky='w')

        # Stock (solo números) - CORREGIDO: usar solo_numeros
        ttk.Label(form_frame, text="Stock:").grid(row=3, column=0, sticky='w', pady=5)
        vcmd_num = (form_frame.register(Validators.solo_numeros), '%P')  # ← CORREGIDO
        self.stock_var = tk.StringVar()
        self.stock_entry = ttk.Entry(form_frame, textvariable=self.stock_var,
                                     validate='key', validatecommand=vcmd_num, width=20)
        self.stock_entry.grid(row=3, column=1, pady=5, padx=5, sticky='w')

        # Imagen
        ttk.Label(form_frame, text="Imagen:").grid(row=4, column=0, sticky='w', pady=5)
        ttk.Button(form_frame, text="📷 Seleccionar Imagen", command=self.seleccionar_imagen).grid(row=4, column=1, sticky='w', pady=5, padx=5)

        self.imagen_label = ttk.Label(form_frame, text="Sin imagen", relief='solid', width=20)
        self.imagen_label.grid(row=5, column=1, sticky='w', pady=5, padx=5)

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpiar", command=self.limpiar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar).pack(side='left', padx=5)

        # Tabla
        table_frame = ttk.LabelFrame(main_frame, text="Listado de Productos", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')

        self.tabla = ttk.Treeview(table_frame, columns=('id', 'nombre', 'precio', 'stock'),
                                  show='headings', yscrollcommand=scroll_y.set)
        self.tabla.pack(fill='both', expand=True)
        scroll_y.config(command=self.tabla.yview)

        self.tabla.heading('id', text='ID')
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.heading('precio', text='Precio')
        self.tabla.heading('stock', text='Stock')

        self.tabla.column('id', width=50)
        self.tabla.column('nombre', width=200)
        self.tabla.column('precio', width=100)
        self.tabla.column('stock', width=80)

        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

    def actualizar_tabla(self, datos):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for row in datos:
            self.tabla.insert('', 'end', values=(row['id'], row['nombre'], f"${row['precio']:,.2f}", row['stock']))

    def on_select(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            producto_id = item['values'][0]
            self.producto_actual = self.controller.obtener_por_id(producto_id)
            if self.producto_actual:
                self.cargar_datos_formulario(self.producto_actual)

    def cargar_datos_formulario(self, producto):
        self.nombre_var.set(producto.get('nombre', ''))
        self.descripcion_text.delete('1.0', 'end')
        self.descripcion_text.insert('1.0', producto.get('descripcion', ''))
        self.precio_var.set(str(producto.get('precio', '')))
        self.stock_var.set(str(producto.get('stock', '')))

    def guardar(self):
        datos = {
            'nombre': self.nombre_var.get(),
            'descripcion': self.descripcion_text.get('1.0', 'end-1c'),
            'precio': self.precio_var.get(),
            'stock': self.stock_var.get() or '0'
        }
        self.controller.guardar(datos, self.producto_actual)
        self.limpiar()

    def eliminar(self):
        if self.producto_actual:
            self.controller.eliminar(self.producto_actual['id'])
            self.limpiar()

    def seleccionar_imagen(self):
        ruta = self.image_handler.seleccionar_imagen()
        if ruta:
            self.controller.imagen_actual = ruta
            preview = self.image_handler.cargar_para_tk(ruta)
            if preview:
                self.imagen_label.config(image=preview, text='')
                self.imagen_label.image = preview

    def limpiar(self):
        self.producto_actual = None
        self.nombre_var.set('')
        self.descripcion_text.delete('1.0', 'end')
        self.precio_var.set('')
        self.stock_var.set('')
        self.imagen_label.config(image='', text='Sin imagen')
        self.tabla.selection_remove(self.tabla.selection())

    def apply_theme(self, theme):
        self.parent.configure(bg=theme['bg'])