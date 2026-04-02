"""
Script para crear la base de datos SQLite desde cero
Ejecutar: python crear_bd_limpio.py
"""
import sqlite3
import os


def crear_base_datos():
    # Crear carpeta si no existe
    os.makedirs('base_datos', exist_ok=True)

    # Eliminar archivo antiguo si existe
    db_path = 'base_datos/textil.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Archivo antiguo eliminado: {db_path}")

    # Conectar a la base de datos (la crea automáticamente)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("📁 Creando base de datos...")

    # ========== TABLA: CLIENTES ==========
    cursor.execute('''
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            direccion TEXT,
            imagen_path TEXT,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Tabla 'clientes' creada")

    # ========== TABLA: PRODUCTOS ==========
    cursor.execute('''
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            imagen_path TEXT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Tabla 'productos' creada")

    # ========== TABLA: PEDIDOS ==========
    cursor.execute('''
        CREATE TABLE pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER NOT NULL,
            fecha_pedido DATE NOT NULL,
            fecha_entrega DATE,
            estado TEXT DEFAULT 'pendiente',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
        )
    ''')
    print("✓ Tabla 'pedidos' creada")

    # ========== DATOS DE EJEMPLO ==========

    # Insertar clientes de ejemplo
    clientes = [
        ('Ana Martínez', '3001234567', 'ana@textil.com', 'Calle 1 #2-3', None),
        ('Carlos López', '3109876543', 'carlos@textil.com', 'Carrera 4 #5-6', None),
        ('María García', '3209876543', 'maria@textil.com', 'Avenida 7 #8-9', None),
        ('Juan Pérez', '3112223344', 'juan@textil.com', 'Calle 10 #11-12', None),
    ]

    cursor.executemany('''
        INSERT INTO clientes (nombre, telefono, email, direccion, imagen_path)
        VALUES (?, ?, ?, ?, ?)
    ''', clientes)
    print(f"✓ {len(clientes)} clientes insertados")

    # Insertar productos de ejemplo
    productos = [
        ('Camiseta Algodón', 'Camiseta 100% algodón, varios colores', 25000.00, 100, None),
        ('Pantalón Jeans', 'Pantalón denim azul, tela resistente', 89000.00, 50, None),
        ('Chaqueta Poliéster', 'Chaqueta impermeable para exteriores', 120000.00, 30, None),
        ('Bufanda Lana', 'Bufanda de lana de oveja, color gris', 35000.00, 75, None),
        ('Gorra Deportiva', 'Gorra con visera curva, ajustable', 28000.00, 120, None),
    ]

    cursor.executemany('''
        INSERT INTO productos (nombre, descripcion, precio, stock, imagen_path)
        VALUES (?, ?, ?, ?, ?)
    ''', productos)
    print(f"✓ {len(productos)} productos insertados")

    # Insertar pedidos de ejemplo
    pedidos = [
        (1, 1, 2, '2024-01-15', '2024-01-20', 'completado'),
        (2, 2, 1, '2024-01-20', '2024-01-25', 'en proceso'),
        (1, 3, 1, '2024-01-25', None, 'pendiente'),
        (3, 1, 3, '2024-02-01', '2024-02-05', 'completado'),
        (4, 4, 2, '2024-02-10', None, 'pendiente'),
    ]

    cursor.executemany('''
        INSERT INTO pedidos (cliente_id, producto_id, cantidad, fecha_pedido, fecha_entrega, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', pedidos)
    print(f"✓ {len(pedidos)} pedidos insertados")

    # Confirmar cambios
    conn.commit()

    # Verificar resultados
    cursor.execute("SELECT COUNT(*) FROM clientes")
    count_clientes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM productos")
    count_productos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    count_pedidos = cursor.fetchone()[0]

    conn.close()

    print("\n" + "=" * 50)
    print("✅ BASE DE DATOS CREADA EXITOSAMENTE")
    print("=" * 50)
    print(f"Ubicación: {db_path}")
    print(f"Clientes: {count_clientes}")
    print(f"Productos: {count_productos}")
    print(f"Pedidos: {count_pedidos}")
    print("=" * 50)


if __name__ == "__main__":
    crear_base_datos()