
import sqlite3
import os
import tkinter.messagebox as messagebox


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Establecer conexión con la base de datos SQLite"""
        try:
            # Crear carpeta si no existe
            os.makedirs('base_datos', exist_ok=True)

            self.connection = sqlite3.connect('base_datos/textil.db')
            self.connection.row_factory = sqlite3.Row
            print("✓ Conectado a SQLite - base_datos/textil.db")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos",
                                 f"No se pudo conectar a la base de datos:\n{e}")
            self.connection = None

    def execute_query(self, query, params=None):
        """Ejecutar una consulta SQL y retornar resultados"""
        if not self.connection:
            self.connect()
            if not self.connection:
                return None if query.strip().upper().startswith('SELECT') else False

        cursor = None
        try:
            cursor = self.connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Si es SELECT, retornar lista de diccionarios
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                return [dict(row) for row in rows] if rows else []
            else:
                # Para INSERT, UPDATE, DELETE
                self.connection.commit()
                return cursor.lastrowid if query.strip().upper().startswith('INSERT') else True

        except Exception as e:
            self.connection.rollback()
            print(f"Error en query: {e}")
            print(f"Query: {query}")
            return None if query.strip().upper().startswith('SELECT') else False
        finally:
            if cursor:
                cursor.close()

    def close(self):
        """Cerrar la conexión"""
        if self.connection:
            self.connection.close()
            self.connection = None