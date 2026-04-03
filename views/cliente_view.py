import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import Validators
from utils.image_handler import ImageHandler
from utils.themes import Themes

class ClienteView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.image_handler = ImageHandler()
        self.cliente_actual = None
        self.imagen_preview = None
        self.current_theme = Themes.current
        self.crear_interfaz()

    def crear_interfaz(self):
        # Contenedor principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Formulario ---
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)

        # Nombre
        ttk.Label(form_frame, text="Nombre (*):", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(form_frame, textvariable=self.nombre_var, width=40)
        self.nombre_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')

        # Teléfono (solo números)
        ttk.Label(form_frame, text="Teléfono:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        vcmd_telefono = (form_frame.register(self._validar_solo_numeros), '%P')
        self.telefono_var = tk.StringVar()
        self.telefono_entry = ttk.Entry(form_frame, textvariable=self.telefono_var, validate='key', validatecommand=vcmd_telefono, width=40)
        self.telefono_entry.grid(row=1, column=1, pady=5, padx=10, sticky='ew')

        # Email
        ttk.Label(form_frame, text="Email:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=40)
        self.email_entry.grid(row=2, column=1, pady=5, padx=10, sticky='ew')

        # Dirección
        ttk.Label(form_frame, text="Dirección:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        self.direccion_text = tk.Text(form_frame, height=3, width=35)
        self.direccion_text.grid(row=3, column=1, pady=5, padx=10, sticky='ew')

        # Imagen
        ttk.Label(form_frame, text="Imagen:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', pady=5)
        img_frame = ttk.Frame(form_frame)
        img_frame.grid(row=4, column=1, pady=5, padx=10, sticky='w')
        ttk.Button(img_frame, text="📷 Seleccionar Imagen", command=self.seleccionar_imagen).pack(side='left', padx=5)
        self.imagen_label = ttk.Label(img_frame, text="Sin imagen", relief='solid', width=25, anchor='center')
        self.imagen_label.pack(side='left', padx=10)

        # --- Botones de acción ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpiar", command=self.limpiar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar).pack(side='left', padx=5)

        # --- Tabla de clientes ---
        table_frame = ttk.LabelFrame(main_frame, text="Listado de Clientes", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        self.tabla = ttk.Treeview(table_frame, columns=('id', 'nombre', 'telefono', 'email'), show='headings',
                                  yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla.pack(fill='both', expand=True)
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.heading('id', text='ID')
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.heading('telefono', text='Teléfono')
        self.tabla.heading('email', text='Email')
        self.tabla.column('id', width=50, anchor='center')
        self.tabla.column('nombre', width=250)
        self.tabla.column('telefono', width=120)
        self.tabla.column('email', width=200)

        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

        form_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def _validar_solo_numeros(self, texto):
        return texto == "" or texto.isdigit()

    def actualizar_tabla(self, clientes):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for cliente in clientes:
            self.tabla.insert('', 'end', values=(cliente['id'], cliente['nombre'],
                                                 cliente.get('telefono', ''), cliente.get('email', '')))
        if not clientes:
            self.tabla.insert('', 'end', values=('', 'No hay clientes registrados', '', ''))

    def on_select(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            cliente_id = self.tabla.item(seleccion[0])['values'][0]
            if cliente_id:
                self.cliente_actual = self.controller.obtener_por_id(cliente_id)
                if self.cliente_actual:
                    self.cargar_datos_formulario(self.cliente_actual)

    def cargar_datos_formulario(self, cliente):
        self.nombre_var.set(cliente.get('nombre', ''))
        self.telefono_var.set(cliente.get('telefono', ''))
        self.email_var.set(cliente.get('email', ''))
        self.direccion_text.delete('1.0', 'end')
        self.direccion_text.insert('1.0', cliente.get('direccion', ''))
        # Vista previa de imagen (opcional)

    def guardar(self):
        datos = {
            'nombre': self.nombre_var.get().strip(),
            'telefono': self.telefono_var.get().strip(),
            'email': self.email_var.get().strip(),
            'direccion': self.direccion_text.get('1.0', 'end-1c').strip()
        }
        self.controller.guardar(datos, self.cliente_actual)

    def eliminar(self):
        if self.cliente_actual:
            self.controller.eliminar(self.cliente_actual['id'])
        else:
            messagebox.showwarning("Seleccionar", "Selecciona un cliente de la tabla.")

    def seleccionar_imagen(self):
        ruta = self.image_handler.seleccionar_imagen()
        if ruta:
            self.controller.imagen_actual = ruta
            preview = self.image_handler.cargar_thumbnail(ruta)
            if preview:
                self.imagen_label.config(image=preview, text='')
                self.imagen_label.image = preview

    def limpiar(self):
        self.cliente_actual = None
        self.nombre_var.set('')
        self.telefono_var.set('')
        self.email_var.set('')
        self.direccion_text.delete('1.0', 'end')
        self.imagen_label.config(image='', text='Sin imagen')
        self.imagen_label.image = None
        self.controller.imagen_actual = None
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.parent.configure(bg=theme['bg'])