"""
Módulo de temas claro/oscuro profesional
Cumple con: Implementar al menos 2 temas visuales intercambiables
"""
from tkinter import ttk

class Themes:
    # Tema Claro (Light) - Profesional y limpio
    light = {
        'name': 'Claro',
        'bg': '#F5F5F5',  # ← CLAVE PRINCIPAL
        'bg_primary': '#F5F5F5',
        'bg_secondary': '#FFFFFF',
        'bg_tertiary': '#E8E8E8',
        'fg': '#2C3E50',  # ← CLAVE PRINCIPAL
        'fg_primary': '#2C3E50',
        'fg_secondary': '#34495E',
        'fg_tertiary': '#7F8C8D',
        'button_bg': '#3498DB',
        'button_fg': '#FFFFFF',
        'button_hover': '#2980B9',
        'entry_bg': '#FFFFFF',
        'entry_fg': '#2C3E50',
        'entry_border': '#BDC3C7',
        'tree_bg': '#FFFFFF',
        'tree_fg': '#2C3E50',
        'tree_selected': '#3498DB',
        'tree_selected_fg': '#FFFFFF',
        'tree_alternate': '#F8F9FA',
        'title_bg': '#2C3E50',
        'title_fg': '#FFFFFF',
        'success_bg': '#D4EDDA',
        'success_fg': '#155724',
        'error_bg': '#F8D7DA',
        'error_fg': '#721C24',
        'warning_bg': '#FFF3CD',
        'warning_fg': '#856404'
    }

    # Tema Oscuro (Dark) - Profesional y moderno
    dark = {
        'name': 'Oscuro',
        'bg': '#1E1E1E',  # ← CLAVE PRINCIPAL
        'bg_primary': '#1E1E1E',
        'bg_secondary': '#2D2D2D',
        'bg_tertiary': '#3D3D3D',
        'fg': '#ECF0F1',  # ← CLAVE PRINCIPAL
        'fg_primary': '#ECF0F1',
        'fg_secondary': '#BDC3C7',
        'fg_tertiary': '#95A5A6',
        'button_bg': '#2980B9',
        'button_fg': '#FFFFFF',
        'button_hover': '#3498DB',
        'entry_bg': '#3D3D3D',
        'entry_fg': '#ECF0F1',
        'entry_border': '#5D5D5D',
        'tree_bg': '#2D2D2D',
        'tree_fg': '#ECF0F1',
        'tree_selected': '#2980B9',
        'tree_selected_fg': '#FFFFFF',
        'tree_alternate': '#383838',
        'title_bg': '#1a1a2e',
        'title_fg': '#FFFFFF',
        'success_bg': '#1E3A2A',
        'success_fg': '#81C784',
        'error_bg': '#3E1E1E',
        'error_fg': '#E57373',
        'warning_bg': '#3E3A1E',
        'warning_fg': '#FFD54F'
    }

    current = light

    @classmethod
    def toggle(cls):
        """Cambiar entre tema claro y oscuro"""
        if cls.current == cls.light:
            cls.current = cls.dark
        else:
            cls.current = cls.light
        return cls.current

    @classmethod
    def get_current(cls):
        """Obtener el tema actual"""
        return cls.current

    @classmethod
    def aplicar_estilos_ttk(cls, estilo):
        """Aplicar estilos a los widgets de ttk"""
        tema = cls.current

        # Configurar estilos para diferentes widgets
        estilo.configure('TFrame', background=tema['bg'])
        estilo.configure('TLabel', background=tema['bg'], foreground=tema['fg'])
        estilo.configure('TLabelframe', background=tema['bg'], foreground=tema['fg'])
        estilo.configure('TLabelframe.Label', background=tema['bg'], foreground=tema['fg'])

        # Estilo para botones primarios
        estilo.configure('Primary.TButton',
                        background=tema['button_bg'],
                        foreground=tema['button_fg'],
                        font=('Segoe UI', 9, 'bold'))

        # Estilo para botones secundarios
        estilo.configure('Secondary.TButton',
                        background=tema['bg_tertiary'],
                        foreground=tema['fg'])

        # Estilo para entradas
        estilo.configure('TEntry',
                        fieldbackground=tema['entry_bg'],
                        foreground=tema['entry_fg'])

        # Estilo para Treeview
        estilo.configure('Treeview',
                        background=tema['tree_bg'],
                        foreground=tema['tree_fg'],
                        fieldbackground=tema['tree_bg'])

        estilo.map('Treeview',
                  background=[('selected', tema['tree_selected'])],
                  foreground=[('selected', tema['tree_selected_fg'])])