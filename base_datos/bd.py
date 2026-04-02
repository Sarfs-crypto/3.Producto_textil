import sqlite3
import os

os.makedirs('base_datos', exist_ok=True)
db_path = os.path.join('base_datos', 'textilpro.db')
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Tablas
cur.execute('''CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE, nombre TEXT, descripcion TEXT,
    categoria TEXT, talla TEXT, color TEXT,
    precio_compra REAL, precio_venta REAL,
    stock INTEGER, stock_minimo INTEGER,
    imagen_path TEXT, fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER DEFAULT 1)''')

cur.execute('''CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruc TEXT UNIQUE, nombre TEXT, contacto TEXT,
    telefono TEXT, email TEXT, direccion TEXT,
    imagen_path TEXT, fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER DEFAULT 1)''')

cur.execute('''CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_venta TEXT UNIQUE, fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente TEXT, total REAL, estado TEXT DEFAULT 'completada')''')

cur.execute('''CREATE TABLE venta_detalles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER, producto_id INTEGER,
    cantidad INTEGER, precio_unitario REAL, subtotal REAL,
    FOREIGN KEY(venta_id) REFERENCES ventas(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id))''')

# Datos de ejemplo
productos = [
    ('TEL001', 'Algodón Premium', 'Algodón 100% orgánico', 'Telas', 'Rollo', 'Blanco', 25, 45, 100),
    ('CAM001', 'Camisa Casual', 'Camisa de algodón', 'Prendas', 'M', 'Azul', 15, 35, 80),
]
for p in productos:
    cur.execute('INSERT INTO productos (codigo, nombre, descripcion, categoria, talla, color, precio_compra, precio_venta, stock) VALUES (?,?,?,?,?,?,?,?,?)', p)

proveedores = [
    ('20123456789', 'Textiles del Perú SAC', 'Juan Pérez', '987654321', 'ventas@textilesperu.com', 'Av. Industrial 123'),
]
for prov in proveedores:
    cur.execute('INSERT INTO proveedores (ruc, nombre, contacto, telefono, email, direccion) VALUES (?,?,?,?,?,?)', prov)

cur.execute("INSERT INTO ventas (codigo_venta, cliente, total) VALUES (?, ?, ?)", ('VENTA001', 'Cliente Mayorista', 1250))

conn.commit()
conn.close()
print("✅ Base de datos creada correctamente")