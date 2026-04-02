"""
Módulo para gestión de temas claro/oscuro
"""
from tkinter import ttk


class Themes:
    light_theme = {
        'bg_primary': '#F5F5F5',
        'bg_secondary': '#FFFFFF',
        'fg_primary': '#212121',
        'fg_secondary': '#757575',
        'button_bg': '#E0E0E0',
        'button_fg': '#212121',
        'entry_bg': '#FFFFFF',
        'entry_fg': '#212121',
        'treeview_bg': '#FFFFFF',
        'treeview_fg': '#212121',
        'treeview_selected': '#BBDEFB',
        'highlight': '#2196F3',
        'error_bg': '#FFEBEE',
        'error_fg': '#C62828',
        'success_bg': '#E8F5E9',
        'success_fg': '#2E7D32',
        'warning_bg': '#FFF3E0',
        'warning_fg': '#EF6C00'
    }

    dark_theme = {
        'bg_primary': '#121212',
        'bg_secondary': '#1E1E1E',
        'fg_primary': '#FFFFFF',
        'fg_secondary': '#B0B0B0',
        'button_bg': '#2C2C2C',
        'button_fg': '#FFFFFF',
        'entry_bg': '#2C2C2C',
        'entry_fg': '#FFFFFF',
        'treeview_bg': '#1E1E1E',
        'treeview_fg': '#FFFFFF',
        'treeview_selected': '#2196F3',
        'highlight': '#2196F3',
        'error_bg': '#4A2A2A',
        'error_fg': '#FF8A80',
        'success_bg': '#1E3A2A',
        'success_fg': '#81C784',
        'warning_bg': '#4A3A1E',
        'warning_fg': '#FFB74D'
    }

    current_theme = light_theme

    @classmethod
    def toggle_theme(cls):
        """Cambiar entre tema claro y oscuro"""
        if cls.current_theme == cls.light_theme:
            cls.current_theme = cls.dark_theme
        else:
            cls.current_theme = cls.light_theme
        return cls.current_theme

    @classmethod
    def get_color(cls, key):
        """Obtener color del tema actual"""
        return cls.current_theme.get(key, '#FFFFFF')