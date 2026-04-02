# bd.py
import sqlite3
import os

print("="*50)
print("CREANDO BASE DE DATOS TEXTILPRO")
print("="*50)

# Crear carpeta
os.makedirs('base_datos', exist_ok=True)

# Ruta
db_path = os.path.join('base_datos', 'textilpro.db')
print(f"📁 Creando en: {db_path}")

# Eliminar si existe corrupto
if os.path.exists(db_path):
    os.remove(db_path)
    print("✓ Archivo anterior eliminado")

# Conectar
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabla productos
cursor.execute('''
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    talla TEXT,
    color TEXT,
    precio_compra REAL DEFAULT 0,
    precio_venta REAL DEFAULT 0,
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    imagen_path TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER DEFAULT 1
)
''')

# Tabla proveedores
cursor.execute('''
CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruc TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    contacto TEXT,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    imagen_path TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER DEFAULT 1
)
''')

# Tabla ventas
cursor.execute('''
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_venta TEXT NOT NULL UNIQUE,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente TEXT,
    total REAL DEFAULT 0,
    estado TEXT DEFAULT 'completada'
)
''')

# Tabla detalles venta
cursor.execute('''
CREATE TABLE venta_detalles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
''')

# Datos de ejemplo
print("📦 Insertando datos...")

productos = [
    ('TEL001', 'Algodón Premium', 'Algodón 100% orgánico', 'Telas', 'Rollo', 'Blanco', 25, 45, 100),
    ('CAM001', 'Camisa Casual', 'Camisa de algodón', 'Prendas', 'M', 'Azul', 15, 35, 80),
]

for p in productos:
    cursor.execute('''
        INSERT INTO productos (codigo, nombre, descripcion, categoria, talla, color, precio_compra, precio_venta, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', p)

proveedores = [
    ('20123456789', 'Textiles del Perú SAC', 'Juan Pérez', '987654321', 'ventas@textilesperu.com', 'Av. Industrial 123'),
]

for prov in proveedores:
    cursor.execute('''
        INSERT INTO proveedores (ruc, nombre, contacto, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', prov)

cursor.execute("INSERT INTO ventas (codigo_venta, cliente, total) VALUES (?, ?, ?)",
               ('VENTA001', 'Cliente Mayorista', 1250.00))

conn.commit()

# Verificar
cursor.execute("SELECT COUNT(*) FROM productos")
print(f"✅ Productos: {cursor.fetchone()[0]}")

cursor.close()
conn.close()

print(f"✅ Base de datos creada en: {db_path}")
print("🚀 Ahora ejecuta: python main.py")