"""
Vista para gestión de clientes
Formulario completo con validaciones y gestión de imágenes
"""
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
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # ========== FORMULARIO ==========
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)

        # Campo: Nombre
        ttk.Label(form_frame, text="Nombre (*):", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=8)
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(form_frame, textvariable=self.nombre_var, width=40, font=('Arial', 10))
        self.nombre_entry.grid(row=0, column=1, pady=8, padx=10, sticky='ew')

        # Campo: Teléfono (solo números)
        ttk.Label(form_frame, text="Teléfono:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=8)
        vcmd_telefono = (form_frame.register(self._validar_solo_numeros), '%P')
        self.telefono_var = tk.StringVar()
        self.telefono_entry = ttk.Entry(form_frame, textvariable=self.telefono_var,
                                        validate='key', validatecommand=vcmd_telefono,
                                        width=40, font=('Arial', 10))
        self.telefono_entry.grid(row=1, column=1, pady=8, padx=10, sticky='ew')

        # Campo: Email
        ttk.Label(form_frame, text="Email:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=8)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=40, font=('Arial', 10))
        self.email_entry.grid(row=2, column=1, pady=8, padx=10, sticky='ew')

        # Campo: Dirección
        ttk.Label(form_frame, text="Dirección:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=8)
        self.direccion_text = tk.Text(form_frame, height=4, width=35, font=('Arial', 10))
        self.direccion_text.grid(row=3, column=1, pady=8, padx=10, sticky='ew')

        # Campo: Imagen
        ttk.Label(form_frame, text="Imagen:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', pady=8)

        imagen_frame = ttk.Frame(form_frame)
        imagen_frame.grid(row=4, column=1, pady=8, padx=10, sticky='w')

        self.btn_imagen = ttk.Button(imagen_frame, text="📷 Seleccionar Imagen", command=self.seleccionar_imagen)
        self.btn_imagen.pack(side='left', padx=5)

        self.imagen_label = ttk.Label(imagen_frame, text="Sin imagen", relief='solid', width=25, anchor='center')
        self.imagen_label.pack(side='left', padx=10)

        # ========== BOTONES ==========
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)

        self.btn_guardar = ttk.Button(btn_frame, text="💾 Guardar", command=self.guardar, width=12)
        self.btn_guardar.pack(side='left', padx=5)

        self.btn_limpiar = ttk.Button(btn_frame, text="🧹 Limpiar", command=self.limpiar, width=12)
        self.btn_limpiar.pack(side='left', padx=5)

        self.btn_eliminar = ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar, width=12)
        self.btn_eliminar.pack(side='left', padx=5)

        # ========== TABLA ==========
        table_frame = ttk.LabelFrame(main_frame, text="Listado de Clientes", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        # Treeview
        self.tabla = ttk.Treeview(table_frame,
                                  columns=('id', 'nombre', 'telefono', 'email'),
                                  show='headings',
                                  yscrollcommand=scroll_y.set,
                                  xscrollcommand=scroll_x.set)
        self.tabla.pack(fill='both', expand=True)

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        # Configurar columnas
        self.tabla.heading('id', text='ID')
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.heading('telefono', text='Teléfono')
        self.tabla.heading('email', text='Email')

        self.tabla.column('id', width=50, anchor='center')
        self.tabla.column('nombre', width=250)
        self.tabla.column('telefono', width=120, anchor='center')
        self.tabla.column('email', width=200)

        # Vincular evento de selección
        self.tabla.bind('<<TreeviewSelect>>', self.on_select)

        # Configurar grid weights
        form_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def _validar_solo_numeros(self, texto):
        """Validar que solo contenga números"""
        if texto == "":
            return True
        return texto.isdigit() and len(texto) <= 15

    def actualizar_tabla(self, clientes):
        """Actualizar la tabla con los clientes"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar clientes
        for cliente in clientes:
            self.tabla.insert('', 'end', values=(
                cliente['id'],
                cliente['nombre'],
                cliente.get('telefono', ''),
                cliente.get('email', '')
            ), iid=cliente['id'])

        # Mostrar mensaje si no hay datos
        if not clientes:
            self.tabla.insert('', 'end', values=('', 'No hay clientes registrados', '', ''))

    def on_select(self, event):
        """Evento al seleccionar un cliente en la tabla"""
        seleccion = self.tabla.selection()
        if seleccion:
            try:
                cliente_id = int(seleccion[0])
                cliente = self.controller.obtener_por_id(cliente_id)
                if cliente:
                    self.cargar_datos_formulario(cliente)
            except ValueError:
                pass  # Es el mensaje "No hay clientes"

    def cargar_datos_formulario(self, cliente):
        """Cargar datos del cliente en el formulario"""
        self.cliente_actual = cliente
        self.nombre_var.set(cliente.get('nombre', ''))
        self.telefono_var.set(cliente.get('telefono', ''))
        self.email_var.set(cliente.get('email', ''))
        self.direccion_text.delete('1.0', 'end')
        self.direccion_text.insert('1.0', cliente.get('direccion', ''))

        # Cargar imagen si existe
        if cliente.get('imagen_path') and cliente['imagen_path']:
            img = self.image_handler.cargar_thumbnail(cliente['imagen_path'])
            if img:
                self.imagen_label.config(image=img, text='')
                self.imagen_label.image = img
            else:
                self.imagen_label.config(image='', text='Sin imagen')
        else:
            self.imagen_label.config(image='', text='Sin imagen')

    def guardar(self):
        """Guardar cliente"""
        # Validar nombre
        nombre = self.nombre_var.get().strip()
        if not Validators.validar_longitud(nombre, 3, 100):
            messagebox.showerror("Error", "El nombre debe tener entre 3 y 100 caracteres")
            return

        # Validar email
        email = self.email_var.get().strip()
        if email and not Validators.validar_email(email):
            messagebox.showerror("Error", "Formato de email inválido.\nEjemplo: usuario@dominio.com")
            return

        # Preparar datos
        datos = {
            'nombre': nombre,
            'telefono': self.telefono_var.get().strip(),
            'email': email,
            'direccion': self.direccion_text.get('1.0', 'end-1c').strip()
        }

        # Guardar
        self.controller.guardar(datos, self.cliente_actual)
        self.limpiar()

    def eliminar(self):
        """Eliminar cliente"""
        if self.cliente_actual:
            self.controller.eliminar(self.cliente_actual['id'])
            self.limpiar()
        else:
            messagebox.showwarning("Seleccionar", "Por favor seleccione un cliente de la tabla")

    def seleccionar_imagen(self):
        """Seleccionar imagen para el cliente"""
        ruta = self.image_handler.seleccionar_imagen()
        if ruta:
            self.controller.imagen_actual = ruta
            preview = self.image_handler.cargar_thumbnail(ruta)
            if preview:
                self.imagen_label.config(image=preview, text='')
                self.imagen_label.image = preview

    def limpiar(self):
        """Limpiar formulario"""
        self.cliente_actual = None
        self.nombre_var.set('')
        self.telefono_var.set('')
        self.email_var.set('')
        self.direccion_text.delete('1.0', 'end')
        self.imagen_label.config(image='', text='Sin imagen')
        self.imagen_label.image = None
        self.controller.imagen_actual = None

        # Limpiar selección de la tabla
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

    def apply_theme(self, theme):
        """Aplicar tema a la vista"""
        self.current_theme = theme
        self.parent.configure(bg=theme['bg'])