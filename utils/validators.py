"""
Módulo de validaciones
"""
import re
from datetime import datetime


class Validators:

    @staticmethod
    def validar_solo_numeros(texto):
        """Validar que solo contenga números"""
        if texto == "" or texto is None:
            return True
        try:
            float(texto)
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_entero(texto):
        """Validar que sea un número entero"""
        if texto == "" or texto is None:
            return True
        try:
            int(texto)
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_email(email):
        """Validar formato de email"""
        if not email:
            return True
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    @staticmethod
    def validar_ruc(ruc):
        """Validar RUC (11 dígitos)"""
        if not ruc:
            return False
        return len(ruc) == 11 and ruc.isdigit()

    @staticmethod
    def validar_telefono(telefono):
        """Validar teléfono (9 dígitos)"""
        if not telefono:
            return True
        return len(telefono) >= 7 and len(telefono) <= 15 and telefono.isdigit()

    @staticmethod
    def validar_longitud_texto(texto, min_len=2, max_len=200):
        """Validar longitud de texto"""
        if not texto:
            return False
        return min_len <= len(texto) <= max_len

    @staticmethod
    def validar_precio(precio):
        """Validar precio positivo"""
        try:
            precio_float = float(precio)
            return precio_float >= 0
        except:
            return False

    @staticmethod
    def validar_codigo(codigo):
        """Validar código de producto (al menos 3 caracteres)"""
        if not codigo:
            return False
        return len(codigo) >= 3

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