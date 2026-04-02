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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, 'base_datos', 'textilpro.db')
        print(f"🔍 Buscando BD en: {self.db_path}")
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            if not os.path.exists(self.db_path):
                messagebox.showerror("Error", f"No se encuentra:\n{self.db_path}\n\nEjecuta: python bd.py")
                return False
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print("✅ Conectado a SQLite")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        if not self.connection:
            return None if not fetch_one and not fetch_all else ([] if fetch_all else None)
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            if fetch_one:
                row = cursor.fetchone()
                return dict(row) if row else None
            if fetch_all:
                rows = cursor.fetchall()
                return [dict(row) for row in rows] if rows else []
            self.connection.commit()
            return cursor.lastrowid or cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"{e}\n\nQuery: {query}")
            return None if not fetch_one and not fetch_all else ([] if fetch_all else None)
        finally:
            if cursor:
                cursor.close()