"""
Vista para gestión de proveedores
"""
import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import Validators


class ProveedorView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.imagen_preview = None

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        paned = ttk.PanedWindow(main_frame, orient='horizontal')
        paned.pack(fill='both', expand=True)

        form_frame = ttk.Frame(paned, width=450)
        paned.add(form_frame, weight=1)

        table_frame = ttk.Frame(paned)
        paned.add(table_frame, weight=2)

        # FORMULARIO
        ttk.Label(form_frame, text="Gestión de Proveedores", font=('Arial', 14, 'bold')).pack(pady=10)

        campos_frame = ttk.LabelFrame(form_frame, text="Datos del Proveedor", padding=10)
        campos_frame.pack(fill='both', expand=True, padx=10, pady=10)

        vcmd_int = (campos_frame.register(Validators.validar_entero), '%P')

        ttk.Label(campos_frame, text="RUC:").grid(row=0, column=0, sticky='w', pady=3)
        self.ruc_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.ruc_var, validate='key',
                  validatecommand=vcmd_int, width=30).grid(row=0, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Nombre:").grid(row=1, column=0, sticky='w', pady=3)
        self.nombre_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.nombre_var, width=30).grid(row=1, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Contacto:").grid(row=2, column=0, sticky='w', pady=3)
        self.contacto_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.contacto_var, width=30).grid(row=2, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Teléfono:").grid(row=3, column=0, sticky='w', pady=3)
        self.telefono_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.telefono_var, validate='key',
                  validatecommand=vcmd_int, width=30).grid(row=3, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Email:").grid(row=4, column=0, sticky='w', pady=3)
        self.email_var = tk.StringVar()
        ttk.Entry(campos_frame, textvariable=self.email_var, width=30).grid(row=4, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Dirección:").grid(row=5, column=0, sticky='w', pady=3)
        self.direccion_text = tk.Text(campos_frame, height=3, width=30)
        self.direccion_text.grid(row=5, column=1, pady=3, padx=5)

        ttk.Label(campos_frame, text="Logo:").grid(row=6, column=0, sticky='w', pady=3)
        img_frame = ttk.Frame(campos_frame)
        img_frame.grid(row=6, column=1, pady=3, padx=5)
        ttk.Button(img_frame, text="Seleccionar", command=self.controller.seleccionar_imagen).pack(side='left')
        self.imagen_label = ttk.Label(img_frame, text="Sin imagen", relief='solid', width=15)
        self.imagen_label.pack(side='left', padx=5)

        # Botones
        botones_frame = ttk.Frame(form_frame)
        botones_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(botones_frame, text="Guardar", command=self.guardar).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_formulario).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="Eliminar", command=self.eliminar).pack(side='left', padx=5)

        # TABLA
        ttk.Label(table_frame, text="Listado de Proveedores", font=('Arial', 14, 'bold')).pack(pady=10)

        tabla_container = ttk.Frame(table_frame)
        tabla_container.pack(fill='both', expand=True, padx=10, pady=5)

        scroll_y = ttk.Scrollbar(tabla_container)
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(tabla_container, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        self.tabla = ttk.Treeview(tabla_container,
                                  columns=('id', 'ruc', 'nombre', 'contacto', 'telefono'),
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
        self.tabla.heading('ruc', text='RUC')
        self.tabla.column('ruc', width=100)
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.column('nombre', width=200)
        self.tabla.heading('contacto', text='Contacto')
        self.tabla.column('contacto', width=120)
        self.tabla.heading('telefono', text='Teléfono')
        self.tabla.column('telefono', width=100)

        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

        campos_frame.columnconfigure(1, weight=1)

    def actualizar_tabla(self, proveedores):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for p in proveedores:
            self.tabla.insert('', 'end', values=(
                p['id'], p['ruc'], p['nombre'], p['contacto'], p['telefono']
            ), iid=p['id'])

    def on_select(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            proveedor_id = seleccion[0]
            from models.proveedor_model import ProveedorModel
            proveedor = ProveedorModel().obtener_por_id(proveedor_id)
            if proveedor:
                self.controller.cargar_proveedor_para_editar(proveedor)
                self.cargar_datos_formulario(proveedor)

    def cargar_datos_formulario(self, proveedor):
        self.ruc_var.set(proveedor.get('ruc', ''))
        self.nombre_var.set(proveedor.get('nombre', ''))
        self.contacto_var.set(proveedor.get('contacto', ''))
        self.telefono_var.set(proveedor.get('telefono', ''))
        self.email_var.set(proveedor.get('email', ''))
        self.direccion_text.delete('1.0', 'end')
        self.direccion_text.insert('1.0', proveedor.get('direccion', ''))

        if proveedor.get('imagen_path'):
            from utils.image_handler import ImageHandler
            img = ImageHandler().cargar_imagen_para_tk(proveedor['imagen_path'])
            if img:
                self.mostrar_imagen_preview(img)

    def guardar(self):
        datos = {
            'ruc': self.ruc_var.get(),
            'nombre': self.nombre_var.get(),
            'contacto': self.contacto_var.get(),
            'telefono': self.telefono_var.get(),
            'email': self.email_var.get(),
            'direccion': self.direccion_text.get('1.0', 'end-1c')
        }
        self.controller.guardar_proveedor(datos)

    def eliminar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            self.controller.eliminar_proveedor(seleccion[0])
        else:
            messagebox.showwarning("Seleccionar", "Seleccione un proveedor")

    def mostrar_imagen_preview(self, imagen_tk):
        self.imagen_preview = imagen_tk
        self.imagen_label.config(image=imagen_tk, text='')

    def limpiar_formulario(self):
        self.ruc_var.set('')
        self.nombre_var.set('')
        self.contacto_var.set('')
        self.telefono_var.set('')
        self.email_var.set('')
        self.direccion_text.delete('1.0', 'end')
        self.imagen_label.config(image='', text='Sin imagen')
        self.imagen_preview = None

    def apply_theme(self, theme):
        pass