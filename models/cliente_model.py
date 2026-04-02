"""
Modelo para gestión de clientes
Operaciones CRUD completas
"""
from models.database import Database

class ClienteModel:
    def __init__(self):
        self.db = Database()

    def insertar(self, nombre, telefono, email, direccion, imagen_path):
        query = """
            INSERT INTO clientes (nombre, telefono, email, direccion, imagen_path, fecha_registro)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """
        return self.db.execute_query(query, (nombre, telefono, email, direccion, imagen_path))

    def actualizar(self, id, nombre, telefono, email, direccion, imagen_path):
        query = """
            UPDATE clientes 
            SET nombre=?, telefono=?, email=?, direccion=?, imagen_path=?
            WHERE id=?
        """
        return self.db.execute_query(query, (nombre, telefono, email, direccion, imagen_path, id))

    def eliminar(self, id):
        query = "DELETE FROM clientes WHERE id=?"
        return self.db.execute_query(query, (id,))

    def listar_todos(self):
        query = "SELECT * FROM clientes ORDER BY nombre"
        result = self.db.execute_query(query)
        return result if result else []

    def buscar(self, busqueda):
        query = """
            SELECT * FROM clientes 
            WHERE nombre LIKE ? OR email LIKE ? OR telefono LIKE ?
            ORDER BY nombre
        """
        result = self.db.execute_query(query, (f'%{busqueda}%', f'%{busqueda}%', f'%{busqueda}%'))
        return result if result else []

    def obtener_por_id(self, id):
        query = "SELECT * FROM clientes WHERE id=?"
        result = self.db.execute_query(query, (id,))
        return result[0] if result and len(result) > 0 else None