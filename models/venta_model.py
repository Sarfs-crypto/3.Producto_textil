from models.database import Database
from datetime import datetime

class VentaModel:
    def __init__(self):
        self.db = Database()

    def registrar_venta(self, datos):
        codigo = f"VENTA{datetime.now().strftime('%Y%m%d%H%M%S')}"
        venta_id = self.db.execute_query(
            "INSERT INTO ventas (codigo_venta, cliente, total) VALUES (?, ?, ?)",
            (codigo, datos['cliente'], datos['total'])
        )
        if not venta_id:
            return None
        for detalle in datos['detalles']:
            self.db.execute_query(
                "INSERT INTO venta_detalles (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
                (venta_id, detalle['producto_id'], detalle['cantidad'], detalle['precio_unitario'], detalle['subtotal'])
            )
            self.db.execute_query("UPDATE productos SET stock = stock - ? WHERE id=?", (detalle['cantidad'], detalle['producto_id']))
        return venta_id

    def listar_ventas(self):
        return self.db.execute_query("SELECT * FROM ventas ORDER BY fecha DESC", fetch_all=True)

    def obtener_detalles_venta(self, venta_id):
        query = """
            SELECT vd.*, p.nombre as producto_nombre, p.codigo as producto_codigo
            FROM venta_detalles vd
            JOIN productos p ON vd.producto_id = p.id
            WHERE vd.venta_id = ?
        """
        return self.db.execute_query(query, (venta_id,), fetch_all=True)