# crear_todo.py
import sqlite3
import os

# Eliminar base de datos antigua si existe
db_path = 'base_datos/textil.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️ Base de datos antigua eliminada")

# Crear carpeta si no existe
os.makedirs('base_datos', exist_ok=True)

# Conectar a nueva base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("📁 Creando tablas...")

# Crear tabla CLIENTES
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

# Crear tabla PRODUCTOS
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

# Crear tabla PEDIDOS
cursor.execute('''
    CREATE TABLE pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER NOT NULL,
        fecha_pedido DATE NOT NULL,
        fecha_entrega DATE,
        estado TEXT DEFAULT 'pendiente'
    )
''')
print("✓ Tabla 'pedidos' creada")

# Insertar datos de ejemplo
print("\n📝 Insertando datos de ejemplo...")

clientes = [
    ('Ana Martínez', '3001234567', 'ana@textil.com', 'Calle 1 #2-3', None),
    ('Carlos López', '3109876543', 'carlos@textil.com', 'Carrera 4 #5-6', None),
    ('Santiago Morales', '309293881', 'santiago@test.com', 'nose', None),
]
cursor.executemany('''
    INSERT INTO clientes (nombre, telefono, email, direccion, imagen_path)
    VALUES (?, ?, ?, ?, ?)
''', clientes)
print(f"✓ {len(clientes)} clientes insertados")

productos = [
    ('Camiseta Algodón', 'Camiseta 100% algodón', 25000, 100, None),
    ('Pantalón Jeans', 'Pantalón denim azul', 89000, 50, None),
    ('Chaqueta Poliéster', 'Chaqueta impermeable', 120000, 30, None),
]
cursor.executemany('''
    INSERT INTO productos (nombre, descripcion, precio, stock, imagen_path)
    VALUES (?, ?, ?, ?, ?)
''', productos)
print(f"✓ {len(productos)} productos insertados")

conn.commit()

# Verificar
cursor.execute("SELECT COUNT(*) FROM clientes")
count = cursor.fetchone()[0]
print(f"\n✅ Total clientes en la base de datos: {count}")

# Mostrar clientes
cursor.execute("SELECT * FROM clientes")
print("\n📋 Lista de clientes:")
for cliente in cursor.fetchall():
    print(f"   ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[3]}")

conn.close()

print("\n" + "="*50)
print("✅ BASE DE DATOS CREADA CON ÉXITO")
print("="*50)
print(f"📌 Ubicación: {db_path}")
print("📌 Tablas: clientes, productos, pedidos")
print("📌 Clientes disponibles para usar en pedidos")
print("="*50)