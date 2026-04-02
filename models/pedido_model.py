"""
Modelo para gestión de pedidos
Operaciones CRUD completas con joins
"""
from models.database import Database

class PedidoModel:
    def __init__(self):
        self.db = Database()

    def insertar(self, cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega):
        query = """
            INSERT INTO pedidos (cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega, estado) 
            VALUES (?, ?, ?, ?, ?, 'pendiente')
        """
        return self.db.execute_query(query, (cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega))

    def actualizar(self, id, cliente_id, producto_id, cantidad, fecha_entrega, estado):
        query = """
            UPDATE pedidos 
            SET cliente_id=?, producto_id=?, cantidad=?, fecha_entrega=?, estado=? 
            WHERE id=?
        """
        return self.db.execute_query(query, (cliente_id, producto_id, cantidad, fecha_entrega, estado, id))

    def eliminar(self, id):
        query = "DELETE FROM pedidos WHERE id=?"
        return self.db.execute_query(query, (id,))

    def listar_todos(self):
        query = """
            SELECT p.*, 
                   c.nombre as cliente_nombre, 
                   pr.nombre as producto_nombre 
            FROM pedidos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN productos pr ON p.producto_id = pr.id
            ORDER BY p.fecha_pedido DESC
        """
        result = self.db.execute_query(query)
        return result if result else []

    def buscar(self, busqueda):
        query = """
            SELECT p.*, 
                   c.nombre as cliente_nombre, 
                   pr.nombre as producto_nombre 
            FROM pedidos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN productos pr ON p.producto_id = pr.id
            WHERE c.nombre LIKE ? OR pr.nombre LIKE ?
            ORDER BY p.fecha_pedido DESC
        """
        result = self.db.execute_query(query, (f'%{busqueda}%', f'%{busqueda}%'))
        return result if result else []

    def obtener_por_id(self, id):
        query = """
            SELECT p.*, 
                   c.nombre as cliente_nombre, 
                   pr.nombre as producto_nombre 
            FROM pedidos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN productos pr ON p.producto_id = pr.id
            WHERE p.id=?
        """
        result = self.db.execute_query(query, (id,))
        return result[0] if result and len(result) > 0 else None

    def listar_por_cliente(self, cliente_id):
        query = """
            SELECT p.*, pr.nombre as producto_nombre 
            FROM pedidos p
            LEFT JOIN productos pr ON p.producto_id = pr.id
            WHERE p.cliente_id = ?
            ORDER BY p.fecha_pedido DESC
        """
        result = self.db.execute_query(query, (cliente_id,))
        return result if result else []