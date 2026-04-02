"""
Vista para gestión de productos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import Validators


class ProductoView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.imagen_preview = None

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # PanedWindow para dividir
        paned = ttk.PanedWindow(main_frame, orient='horizontal')
        paned.pack(fill='both', expand=True)

        # Frame izquierdo - Formulario
        form_frame = ttk.Frame(paned, width=450)
        paned.add(form_frame, weight=1)

        # Frame derecho - Tabla
        table_frame = ttk.Frame(paned)
        paned.add(table_frame, weight=2)

        # ========== FORMULARIO ==========
        ttk.Label(form_frame, text="Gestión de Productos", font=('Arial', 14, 'bold')).pack(pady=10)

        campos_frame = ttk.LabelFrame(form_frame, text="Datos del Producto", padding=10)
        campos_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Campos
        ttk.Label(campos_frame, text="Código:").grid(row=0, column=0, sticky='w', pady=3)
        self.codigo_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.codigo_var, width=30).grid(row=0, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Nombre:").grid(row=1, column=0, sticky='w', pady=3)
        self.nombre_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.nombre_var, width=30).grid(row=1, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Descripción:").grid(row=2, column=0, sticky='w', pady=3)
        self.descripcion_text = tk.Text(campos_frame, height=3, width=30)
        self.descripcion_text.grid(row=2, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Categoría:").grid(row=3, column=0, sticky='w', pady=3)
        self.categoria_var = tk.StringVar()
        ttk.Combobox(campos_frame, textvariable=self.categoria_var,
                     values=['Telas', 'Prendas', 'Insumos', 'Accesorios'],
                     width=28).grid(row=3, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Talla:").grid(row=4, column=0, sticky='w', pady=3)
        self.talla_var = tk.StringVar()
        ttk.Combobox(campos_frame, textvariable=self.talla_var,
                     values=['XS', 'S', 'M', 'L', 'XL', 'Rollo', 'Metro'],
                     width=28).grid(row=4, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Color:").grid(row=5, column=0, sticky='w', pady=3)
        self.color_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.color_var, width=30).grid(row=5, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Precio Compra:").grid(row=6, column=0, sticky='w', pady=3)
        self.pcompra_var = tk.StringVar()
        vcmd = (campos_frame.register(Validators.validar_solo_numeros), '%P')
        ttk.Entry(campos_frame, textvariable=self.pcompra_var, validate='key',
                  validatecommand=vcmd, width=30).grid(row=6, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Precio Venta:").grid(row=7, column=0, sticky='w', pady=3)
        self.pventa_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.pventa_var, validate='key',
                  validatecommand=vcmd, width=30).grid(row=7, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Stock:").grid(row=8, column=0, sticky='w', pady=3)
        self.stock_var = tk.StringVar()
        vcmd_int = (campos_frame.register(Validators.validar_entero), '%P')
        ttk.Entry(campos_frame, textvariable=self.stock_var, validate='key',
                  validatecommand=vcmd_int, width=30).grid(row=8, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Stock Mínimo:").grid(row=9, column=0, sticky='w', pady=3)
        self.stock_min_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.stock_min_var, validate='key',
                  validatecommand=vcmd_int, width=30).grid(row=9, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Imagen:").grid(row=10, column=0, sticky='w', pady=3)
        img_frame = ttk.Frame(campos_frame)
        img_frame.grid(row=10, column=1, pady=3, padx=5)
        ttk.Button(img_frame, text="Seleccionar", command=self.controller.seleccionar_imagen).pack(side='left')
        self.imagen_label = ttk.Label(img_frame, text="Sin imagen", relief='solid', width=15)
        self.imagen_label.pack(side='left', padx=5)

        # Botones
        botones_frame = ttk.Frame(form_frame)
        botones_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(botones_frame, text="Guardar", command=self.guardar).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_formulario).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="Eliminar", command=self.eliminar).pack(side='left', padx=5)

        # ========== TABLA ==========
        ttk.Label(table_frame, text="Listado de Productos", font=('Arial', 14, 'bold')).pack(pady=10)

        tabla_container = ttk.Frame(table_frame)
        tabla_container.pack(fill='both', expand=True, padx=10, pady=5)

        scroll_y = ttk.Scrollbar(tabla_container)
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(tabla_container, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        self.tabla = ttk.Treeview(tabla_container,
                                  columns=('id', 'codigo', 'nombre', 'categoria', 'precio_venta', 'stock'),
                                  show='tree headings',
                                  yscrollcommand=scroll_y.set,
                                  xscrollcommand=scroll_x.set)
        self.tabla.pack(fill='both', expand=True)

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.heading('#0', text='')
        self.tabla.column('#0', width=0)
        self.tabla.heading('id', text='ID')
        self.tabla.column('id', width=50)
        self.tabla.heading('codigo', text='Código')
        self.tabla.column('codigo', width=80)
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.column('nombre', width=200)
        self.tabla.heading('categoria', text='Categoría')
        self.tabla.column('categoria', width=100)
        self.tabla.heading('precio_venta', text='Precio')
        self.tabla.column('precio_venta', width=80)
        self.tabla.heading('stock', text='Stock')
        self.tabla.column('stock', width=60)

        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

        campos_frame.columnconfigure(1, weight=1)

    def actualizar_tabla(self, productos):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for p in productos:
            self.tabla.insert('', 'end', values=(
                p['id'], p['codigo'], p['nombre'], p['categoria'],
                f"${p['precio_venta']:.2f}", p['stock']
            ), iid=p['id'])

    def on_select(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            producto_id = seleccion[0]
            from models.producto_model import ProductoModel
            producto = ProductoModel().obtener_por_id(producto_id)
            if producto:
                self.controller.cargar_producto_para_editar(producto)
                self.cargar_datos_formulario(producto)

    def cargar_datos_formulario(self, producto):
        self.codigo_var.set(producto.get('codigo', ''))
        self.nombre_var.set(producto.get('nombre', ''))
        self.descripcion_text.delete('1.0', 'end')
        self.descripcion_text.insert('1.0', producto.get('descripcion', ''))
        self.categoria_var.set(producto.get('categoria', ''))
        self.talla_var.set(producto.get('talla', ''))
        self.color_var.set(producto.get('color', ''))
        self.pcompra_var.set(str(producto.get('precio_compra', '')))
        self.pventa_var.set(str(producto.get('precio_venta', '')))
        self.stock_var.set(str(producto.get('stock', '')))
        self.stock_min_var.set(str(producto.get('stock_minimo', '')))

        if producto.get('imagen_path'):
            from utils.image_handler import ImageHandler
            img = ImageHandler().cargar_imagen_para_tk(producto['imagen_path'])
            if img:
                self.mostrar_imagen_preview(img)

    def guardar(self):
        datos = {
            'codigo': self.codigo_var.get(),
            'nombre': self.nombre_var.get(),
            'descripcion': self.descripcion_text.get('1.0', 'end-1c'),
            'categoria': self.categoria_var.get(),
            'talla': self.talla_var.get(),
            'color': self.color_var.get(),
            'precio_compra': self.pcompra_var.get(),
            'precio_venta': self.pventa_var.get(),
            'stock': self.stock_var.get(),
            'stock_minimo': self.stock_min_var.get()
        }
        self.controller.guardar_producto(datos)

    def eliminar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            self.controller.eliminar_producto(seleccion[0])
        else:
            messagebox.showwarning("Seleccionar", "Seleccione un producto")

    def mostrar_imagen_preview(self, imagen_tk):
        self.imagen_preview = imagen_tk
        self.imagen_label.config(image=imagen_tk, text='')

    def limpiar_formulario(self):
        self.codigo_var.set('')
        self.nombre_var.set('')
        self.descripcion_text.delete('1.0', 'end')
        self.categoria_var.set('')
        self.talla_var.set('')
        self.color_var.set('')
        self.pcompra_var.set('')
        self.pventa_var.set('')
        self.stock_var.set('')
        self.stock_min_var.set('')
        self.imagen_label.config(image='', text='Sin imagen')
        self.imagen_preview = None

    def apply_theme(self, theme):
        pass