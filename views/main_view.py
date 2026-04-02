"""
Vista principal con pestañas y barra de herramientas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.cliente_view import ClienteView
from views.producto_view import ProductoView
from views.pedido_view import PedidoView
from utils.themes import Themes
from utils.exporters import Exporters


class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.root = controller.root
        self.current_theme = Themes.current

        # Configurar ventana
        self.root.title("TextilPro - Sistema de Gestión Textil")
        self.root.geometry("1400x800")
        self.root.configure(bg=self.current_theme['bg'])

        # Crear menú
        self.crear_menu()

        # Crear barra de herramientas
        self.crear_toolbar()

        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear pestañas
        self.crear_pestanas()

        # Vincular evento de cambio de pestaña
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar Clientes a Excel",
                              command=lambda: self.controller.cliente_controller.exportar_excel())
        file_menu.add_command(label="Exportar Productos a Excel",
                              command=lambda: self.controller.producto_controller.exportar_excel())
        file_menu.add_command(label="Exportar Pedidos a Excel",
                              command=lambda: self.controller.pedido_controller.exportar_excel())
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Tema Claro",
                              command=lambda: self.controller.toggle_theme())
        view_menu.add_command(label="Tema Oscuro",
                              command=lambda: self.controller.toggle_theme())

        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)

    def crear_toolbar(self):
        toolbar = tk.Frame(self.root, bg=self.current_theme['bg_secondary'], height=40)
        toolbar.pack(fill='x', padx=5, pady=5)

        ttk.Button(toolbar, text="📊 Clientes",
                   command=self.controller.mostrar_clientes).pack(side='left', padx=2)
        ttk.Button(toolbar, text="📦 Productos",
                   command=self.controller.mostrar_productos).pack(side='left', padx=2)
        ttk.Button(toolbar, text="📋 Pedidos",
                   command=self.controller.mostrar_pedidos).pack(side='left', padx=2)

        ttk.Separator(toolbar, orient='vertical').pack(side='left', padx=10, fill='y')

        # Buscador
        ttk.Label(toolbar, text="🔍 Buscar:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        ttk.Entry(toolbar, textvariable=self.search_var, width=30).pack(side='left', padx=5)

        # Botón tema
        ttk.Button(toolbar, text="🌓 Cambiar Tema",
                   command=self.controller.toggle_theme).pack(side='right', padx=5)

    def crear_pestanas(self):
        # Pestaña Clientes
        self.cliente_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cliente_frame, text="👥 Clientes")
        self.cliente_view = ClienteView(self.cliente_frame, self.controller.cliente_controller)
        self.controller.cliente_controller.set_view(self.cliente_view)

        # Pestaña Productos
        self.producto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.producto_frame, text="📦 Productos")
        self.producto_view = ProductoView(self.producto_frame, self.controller.producto_controller)
        self.controller.producto_controller.set_view(self.producto_view)

        # Pestaña Pedidos
        self.pedido_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pedido_frame, text="📋 Pedidos")
        self.pedido_view = PedidoView(self.pedido_frame, self.controller.pedido_controller)
        self.controller.pedido_controller.set_view(self.pedido_view)

    def on_tab_change(self, event):
        tab = self.notebook.select()
        tab_text = self.notebook.tab(tab, "text")

        if "Clientes" in tab_text:
            self.controller.cliente_controller.cargar_datos()
        elif "Productos" in tab_text:
            self.controller.producto_controller.cargar_datos()
        elif "Pedidos" in tab_text:
            self.controller.pedido_controller.cargar_datos()

    def on_search(self, *args):
        busqueda = self.search_var.get()
        tab = self.notebook.select()
        tab_text = self.notebook.tab(tab, "text")

        if "Clientes" in tab_text:
            if busqueda:
                self.controller.cliente_controller.buscar(busqueda)
            else:
                self.controller.cliente_controller.cargar_datos()
        elif "Productos" in tab_text:
            if busqueda:
                self.controller.producto_controller.buscar(busqueda)
            else:
                self.controller.producto_controller.cargar_datos()

    def mostrar_frame(self, frame_name):
        if frame_name == 'clientes':
            self.notebook.select(self.cliente_frame)
        elif frame_name == 'productos':
            self.notebook.select(self.producto_frame)
        elif frame_name == 'pedidos':
            self.notebook.select(self.pedido_frame)

    def mostrar_acerca_de(self):
        acerca = tk.Toplevel(self.root)
        acerca.title("Acerca de TextilPro")
        acerca.geometry("400x300")
        acerca.transient(self.root)
        acerca.grab_set()

        ttk.Label(acerca, text="TextilPro - Sistema de Gestión Textil",
                  font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(acerca, text="Versión 1.0").pack()
        ttk.Label(acerca, text="Desarrollado por: James Mosquera Rentería").pack(pady=5)
        ttk.Label(acerca, text="Jornada Noche").pack()
        ttk.Button(acerca, text="Cerrar", command=acerca.destroy).pack(pady=20)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.root.configure(bg=theme['bg'])