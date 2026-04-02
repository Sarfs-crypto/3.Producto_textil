"""
Módulo de validaciones
Cumple con: Validación de email (regex), campos numéricos, longitud de texto
"""
import re
from datetime import datetime


class Validators:

    @staticmethod
    def solo_numeros(texto):
        """Validar que solo contenga números"""
        if texto == "":
            return True
        return texto.isdigit()

    @staticmethod
    def solo_numeros_decimales(texto):
        """Validar números decimales (para precios)"""
        if texto == "":
            return True
        try:
            float(texto)
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_email(email):
        """Validar formato de email usando expresiones regulares"""
        if not email:
            return True
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    @staticmethod
    def validar_longitud(texto, min_len=3, max_len=100):
        """Validar longitud mínima y máxima de texto"""
        if not texto:
            return False
        return min_len <= len(texto) <= max_len

    @staticmethod
    def validar_precio(precio):
        """Validar que el precio sea positivo"""
        try:
            return float(precio) > 0
        except:
            return False