from models.database import Database

class ProductoModel:
    def __init__(self):
        self.db = Database()

    def listar_todos(self):
        query = "SELECT * FROM productos WHERE estado=1 ORDER BY nombre"
        return self.db.execute_query(query, fetch_all=True)

    def insertar(self, datos):
        query = """
            INSERT INTO productos (codigo, nombre, descripcion, categoria, talla, color,
                                   precio_compra, precio_venta, stock, stock_minimo, imagen_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (datos['codigo'], datos['nombre'], datos['descripcion'], datos['categoria'],
                  datos['talla'], datos['color'], float(datos['precio_compra']),
                  float(datos['precio_venta']), int(datos['stock']), int(datos['stock_minimo']),
                  datos.get('imagen_path'))
        return self.db.execute_query(query, params)

    def actualizar(self, id, datos):
        query = """
            UPDATE productos SET codigo=?, nombre=?, descripcion=?, categoria=?, talla=?,
                   color=?, precio_compra=?, precio_venta=?, stock=?, stock_minimo=?, imagen_path=?
            WHERE id=?
        """
        params = (datos['codigo'], datos['nombre'], datos['descripcion'], datos['categoria'],
                  datos['talla'], datos['color'], float(datos['precio_compra']),
                  float(datos['precio_venta']), int(datos['stock']), int(datos['stock_minimo']),
                  datos.get('imagen_path'), id)
        return self.db.execute_query(query, params)

    def eliminar(self, id):
        return self.db.execute_query("UPDATE productos SET estado=0 WHERE id=?", (id,))

    def obtener_por_id(self, id):
        return self.db.execute_query("SELECT * FROM productos WHERE id=?", (id,), fetch_one=True)