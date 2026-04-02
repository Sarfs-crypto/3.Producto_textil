"""
Vista principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.producto_view import ProductoView
from views.proveedor_view import ProveedorView
from views.venta_view import VentaView
from utils.themes import Themes


class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.root = controller.root
        self.current_theme = Themes.current_theme

        self.root.configure(bg=self.current_theme['bg_primary'])

        self.crear_menu()
        self.crear_toolbar()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.crear_pestanas()

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar todo a Excel", command=self.exportar_todo_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Tema Claro", command=lambda: self.cambiar_tema('light'))
        view_menu.add_command(label="Tema Oscuro", command=lambda: self.cambiar_tema('dark'))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)

    def crear_toolbar(self):
        toolbar = tk.Frame(self.root, bg=self.current_theme['bg_secondary'], height=50)
        toolbar.pack(fill='x', padx=5, pady=5)

        ttk.Button(toolbar, text="Exportar Excel", command=self.exportar_actual).pack(side='left', padx=2)
        ttk.Button(toolbar, text="Exportar PDF", command=self.exportar_pdf_actual).pack(side='left', padx=2)

        ttk.Separator(toolbar, orient='vertical').pack(side='left', padx=10, fill='y')

        ttk.Label(toolbar, text="Buscar:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        ttk.Entry(toolbar, textvariable=self.search_var, width=30).pack(side='left', padx=5)

    def crear_pestanas(self):
        # Pestaña de Productos
        self.producto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.producto_frame, text="Productos")
        self.producto_view = ProductoView(self.producto_frame, self.controller.producto_controller)
        self.controller.producto_controller.set_view(self.producto_view)

        # Pestaña de Proveedores
        self.proveedor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.proveedor_frame, text="Proveedores")
        self.proveedor_view = ProveedorView(self.proveedor_frame, self.controller.proveedor_controller)
        self.controller.proveedor_controller.set_view(self.proveedor_view)

        # Pestaña de Ventas
        self.venta_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.venta_frame, text="Ventas")
        self.venta_view = VentaView(self.venta_frame, self.controller.venta_controller)
        self.controller.venta_controller.set_view(self.venta_view)

    def on_tab_change(self, event):
        tab = self.notebook.select()
        tab_text = self.notebook.tab(tab, "text")

        if tab_text == "Productos":
            self.controller.producto_controller.cargar_datos()
        elif tab_text == "Proveedores":
            self.controller.proveedor_controller.cargar_datos()
        elif tab_text == "Ventas":
            self.controller.venta_controller.cargar_datos()
            self.controller.venta_controller.cargar_productos_para_venta()

    def on_search(self, *args):
        busqueda = self.search_var.get()
        tab = self.notebook.select()
        tab_text = self.notebook.tab(tab, "text")

        if busqueda:
            if tab_text == "Productos":
                self.controller.producto_controller.buscar(busqueda)
            elif tab_text == "Proveedores":
                self.controller.proveedor_controller.buscar(busqueda)
        else:
            if tab_text == "Productos":
                self.controller.producto_controller.cargar_datos()
            elif tab_text == "Proveedores":
                self.controller.proveedor_controller.cargar_datos()

    def exportar_actual(self):
        tab = self.notebook.select()
        tab_text = self.notebook.tab(tab, "text")

        if tab_text == "Productos":
            self.controller.producto_controller.exportar_excel()
        elif tab_text == "Proveedores":
            self.controller.proveedor_controller.exportar_excel()
        elif tab_text == "Ventas":
            self.controller.venta_controller.exportar_excel()

    def exportar_pdf_actual(self):
        tab = self.notebook.select()
        tab_text = self.notebook.tab(tab, "text")

        if tab_text == "Productos":
            self.controller.producto_controller.exportar_pdf()
        elif tab_text == "Proveedores":
            self.controller.proveedor_controller.exportar_pdf()
        elif tab_text == "Ventas":
            self.controller.venta_controller.exportar_pdf()

    def exportar_todo_excel(self):
        """Exportar todos los datos"""
        from utils.exporters import Exporters

        # Productos
        productos = self.controller.producto_controller.model.listar_todos()
        if productos:
            columnas = ['ID', 'Código', 'Nombre', 'Categoría', 'Talla', 'Color', 'Precio Venta', 'Stock']
            Exporters.exportar_a_excel(productos, columnas, "TextilPro_Productos")

        # Proveedores
        proveedores = self.controller.proveedor_controller.model.listar_todos()
        if proveedores:
            columnas = ['ID', 'RUC', 'Nombre', 'Contacto', 'Teléfono', 'Email']
            Exporters.exportar_a_excel(proveedores, columnas, "TextilPro_Proveedores")

    def cambiar_tema(self, tema):
        self.controller.toggle_theme()

    def mostrar_acerca_de(self):
        acerca = tk.Toplevel(self.root)
        acerca.title("Acerca de TextilPro")
        acerca.geometry("500x350")
        acerca.transient(self.root)
        acerca.grab_set()

        x = (acerca.winfo_screenwidth() // 2) - (500 // 2)
        y = (acerca.winfo_screenheight() // 2) - (350 // 2)
        acerca.geometry(f'+{x}+{y}')

        ttk.Label(acerca, text="TextilPro", font=('Arial', 20, 'bold')).pack(pady=20)
        ttk.Label(acerca, text="Sistema de Gestión para Industria Textil", font=('Arial', 12)).pack()
        ttk.Label(acerca, text="Versión 1.0").pack(pady=5)
        ttk.Label(acerca, text="Basado en taller_PO-industria-textil").pack()
        ttk.Label(acerca, text="© 2024 - Todos los derechos reservados").pack(pady=10)

        ttk.Separator(acerca, orient='horizontal').pack(fill='x', padx=20, pady=15)

        ttk.Label(acerca, text="Tecnologías: Python, Tkinter, SQLite\n"
                               "Patrón MVC, Validaciones, Exportación Excel/PDF",
                  justify='center').pack(pady=10)

        ttk.Button(acerca, text="Cerrar", command=acerca.destroy).pack(pady=15)

    def mostrar_frame(self, frame_name):
        if frame_name == 'productos':
            self.notebook.select(self.producto_frame)
        elif frame_name == 'proveedores':
            self.notebook.select(self.proveedor_frame)
        elif frame_name == 'ventas':
            self.notebook.select(self.venta_frame)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.root.configure(bg=theme['bg_primary'])