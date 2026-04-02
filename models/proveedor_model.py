from models.database import Database

class ProveedorModel:
    def __init__(self):
        self.db = Database()

    def listar_todos(self):
        return self.db.execute_query("SELECT * FROM proveedores WHERE estado=1 ORDER BY nombre", fetch_all=True)

    def insertar(self, datos):
        query = """
            INSERT INTO proveedores (ruc, nombre, contacto, telefono, email, direccion, imagen_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (datos['ruc'], datos['nombre'], datos['contacto'], datos['telefono'],
                  datos['email'], datos['direccion'], datos.get('imagen_path'))
        return self.db.execute_query(query, params)

    def actualizar(self, id, datos):
        query = """
            UPDATE proveedores SET ruc=?, nombre=?, contacto=?, telefono=?, email=?, direccion=?, imagen_path=?
            WHERE id=?
        """
        params = (datos['ruc'], datos['nombre'], datos['contacto'], datos['telefono'],
                  datos['email'], datos['direccion'], datos.get('imagen_path'), id)
        return self.db.execute_query(query, params)

    def eliminar(self, id):
        return self.db.execute_query("UPDATE proveedores SET estado=0 WHERE id=?", (id,))

    def obtener_por_id(self, id):
        return self.db.execute_query("SELECT * FROM proveedores WHERE id=?", (id,), fetch_one=True)