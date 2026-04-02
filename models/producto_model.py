from models.database import Database


class ProductoModel:
    def __init__(self):
        self.db = Database()

    def insertar(self, nombre, descripcion, precio, stock, imagen_path):
        query = "INSERT INTO productos (nombre, descripcion, precio, stock, imagen_path) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_query(query, (nombre, descripcion, precio, stock, imagen_path))

    def actualizar(self, id, nombre, descripcion, precio, stock, imagen_path):
        query = "UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=?, imagen_path=? WHERE id=?"
        return self.db.execute_query(query, (nombre, descripcion, precio, stock, imagen_path, id))

    def eliminar(self, id):
        query = "DELETE FROM productos WHERE id=?"
        return self.db.execute_query(query, (id,))

    def listar_todos(self):
        query = "SELECT * FROM productos ORDER BY nombre"
        return self.db.execute_query(query)

    def buscar(self, busqueda):
        query = "SELECT * FROM productos WHERE nombre LIKE ? OR descripcion LIKE ?"
        return self.db.execute_query(query, (f'%{busqueda}%', f'%{busqueda}%'))

    def obtener_por_id(self, id):
        query = "SELECT * FROM productos WHERE id=?"
        result = self.db.execute_query(query, (id,))
        return result[0] if result else None