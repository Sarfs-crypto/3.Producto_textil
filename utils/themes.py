"""
Módulo de temas claro/oscuro
Cumple con: Implementar al menos 2 temas visuales intercambiables
"""
class Themes:
    # Tema claro
    light = {
        'name': 'light',
        'bg': '#f0f0f0',
        'bg_secondary': '#ffffff',
        'fg': '#000000',
        'fg_secondary': '#333333',
        'button_bg': '#e1e1e1',
        'button_fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'tree_bg': '#ffffff',
        'tree_fg': '#000000',
        'tree_selected': '#0078d7'
    }

    # Tema oscuro
    dark = {
        'name': 'dark',
        'bg': '#2d2d2d',
        'bg_secondary': '#3d3d3d',
        'fg': '#ffffff',
        'fg_secondary': '#cccccc',
        'button_bg': '#4d4d4d',
        'button_fg': '#ffffff',
        'entry_bg': '#4d4d4d',
        'entry_fg': '#ffffff',
        'tree_bg': '#3d3d3d',
        'tree_fg': '#ffffff',
        'tree_selected': '#0078d7'
    }

    current = light

    @classmethod
    def toggle(cls):
        if cls.current == cls.light:
            cls.current = cls.dark
        else:
            cls.current = cls.light
        return cls.current