"""
Módulo de validaciones profesionales
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
        """Validar formato de email usando expresiones regulares (RFC 5322)"""
        if not email:
            return True  # Campo opcional
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

    @staticmethod
    def validar_cantidad(cantidad):
        """Validar que la cantidad sea entero positivo"""
        try:
            return int(cantidad) > 0
        except:
            return False

    @staticmethod
    def validar_fecha(fecha_str):
        """Validar formato de fecha YYYY-MM-DD"""
        if not fecha_str:
            return True
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except:
            return False

    @staticmethod
    def limpiar_texto(texto):
        """Limpiar texto de caracteres especiales no deseados"""
        if not texto:
            return ""
        # Eliminar caracteres que no sean letras, números, espacios y puntos
        return re.sub(r'[^\w\s\.\-áéíóúñÑ]', '', texto)