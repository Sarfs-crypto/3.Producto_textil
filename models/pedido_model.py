"""
Modelo para gestión de pedidos
Operaciones CRUD completas
"""
from models.database import Database


class PedidoModel:
    def __init__(self):
        self.db = Database()

    def insertar(self, cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega):
        """Insertar nuevo pedido"""
        query = """
            INSERT INTO pedidos (cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega, estado) 
            VALUES (?, ?, ?, ?, ?, 'pendiente')
        """
        return self.db.execute_query(query, (cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega))

    def actualizar(self, id, cliente_id, producto_id, cantidad, fecha_entrega, estado):
        """Actualizar pedido existente"""
        query = """
            UPDATE pedidos 
            SET cliente_id=?, producto_id=?, cantidad=?, fecha_entrega=?, estado=? 
            WHERE id=?
        """
        return self.db.execute_query(query, (cliente_id, producto_id, cantidad, fecha_entrega, estado, id))

    def eliminar(self, id):
        """Eliminar pedido"""
        query = "DELETE FROM pedidos WHERE id=?"
        return self.db.execute_query(query, (id,))

    def listar_todos(self):
        """Listar todos los pedidos con nombres de cliente y producto"""
        query = """
            SELECT p.*, 
                   c.nombre as cliente_nombre, 
                   pr.nombre as producto_nombre 
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            JOIN productos pr ON p.producto_id = pr.id
            ORDER BY p.fecha_pedido DESC
        """
        return self.db.execute_query(query)

    def buscar(self, busqueda):
        """Buscar pedidos por cliente o producto"""
        query = """
            SELECT p.*, 
                   c.nombre as cliente_nombre, 
                   pr.nombre as producto_nombre 
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            JOIN productos pr ON p.producto_id = pr.id
            WHERE c.nombre LIKE ? OR pr.nombre LIKE ?
            ORDER BY p.fecha_pedido DESC
        """
        return self.db.execute_query(query, (f'%{busqueda}%', f'%{busqueda}%'))

    def obtener_por_id(self, id):
        """Obtener un pedido por su ID"""
        query = """
            SELECT p.*, 
                   c.nombre as cliente_nombre, 
                   pr.nombre as producto_nombre 
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            JOIN productos pr ON p.producto_id = pr.id
            WHERE p.id=?
        """
        result = self.db.execute_query(query, (id,))
        return result[0] if result else None

    def listar_por_cliente(self, cliente_id):
        """Listar pedidos de un cliente específico"""
        query = """
            SELECT p.*, pr.nombre as producto_nombre 
            FROM pedidos p
            JOIN productos pr ON p.producto_id = pr.id
            WHERE p.cliente_id = ?
            ORDER BY p.fecha_pedido DESC
        """
        return self.db.execute_query(query, (cliente_id,))