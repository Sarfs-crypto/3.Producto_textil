"""
SCRIPT DEFINITIVO PARA CREAR BASE DE DATOS
"""
import sqlite3
import os

print("="*60)
print("CREANDO BASE DE DATOS TEXTILPRO")
print("="*60)

# Obtener la ruta exacta del proyecto
proyecto_dir = os.path.dirname(os.path.abspath(__file__))
base_datos_dir = os.path.join(proyecto_dir, 'base_datos')
db_path = os.path.join(base_datos_dir, 'textilpro.db')

print(f"\n📁 Directorio del proyecto: {proyecto_dir}")
print(f"📄 Archivo de BD: {db_path}")

# Crear carpeta si no existe
if not os.path.exists(base_datos_dir):
    os.makedirs(base_datos_dir)
    print("✓ Carpeta base_datos creada")

# Eliminar base de datos existente si está corrupta
if os.path.exists(db_path):
    os.remove(db_path)
    print("✓ Base de datos anterior eliminada")

# Crear nueva base de datos
print("\n🔧 Creando nueva base de datos...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla productos
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
print("✓ Tabla 'productos' creada")

# Crear tabla proveedores
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
print("✓ Tabla 'proveedores' creada")

# Crear tabla ventas
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
print("✓ Tabla 'ventas' creada")

# Crear tabla detalles venta
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
print("✓ Tabla 'venta_detalles' creada")

# Insertar datos de ejemplo
print("\n📦 Insertando datos de ejemplo...")

productos = [
    ('TEL001', 'Algodón Premium', 'Algodón 100% orgánico', 'Telas', 'Rollo', 'Blanco', 25.00, 45.00, 100),
    ('TEL002', 'Seda Natural', 'Seda pura de alta calidad', 'Telas', 'Rollo', 'Crudo', 80.00, 150.00, 50),
    ('CAM001', 'Camisa Casual', 'Camisa de algodón para caballero', 'Prendas', 'M', 'Azul', 15.00, 35.00, 80),
    ('CAM002', 'Camisa Formal', 'Camisa de vestir manga larga', 'Prendas', 'L', 'Blanco', 20.00, 45.00, 60),
    ('PAN001', 'Pantalón Jean', 'Jean clásico azul', 'Prendas', '32', 'Azul', 25.00, 55.00, 40),
    ('HIL001', 'Hilo Poliéster', 'Hilo de alta resistencia', 'Insumos', '500m', 'Negro', 5.00, 12.00, 200),
]

for p in productos:
    cursor.execute('''
        INSERT INTO productos (codigo, nombre, descripcion, categoria, talla, color, 
                               precio_compra, precio_venta, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', p)
print(f"✓ Insertados {len(productos)} productos")

proveedores = [
    ('20123456789', 'Textiles del Perú SAC', 'Juan Pérez', '987654321', 'ventas@textilesperu.com', 'Av. Industrial 123, Lima'),
    ('20987654321', 'Insumos Textiles EIRL', 'María López', '987654322', 'maria@insumostextiles.com', 'Calle Comercio 456, Arequipa'),
    ('20456789012', 'Moda Express SAC', 'Carlos Ruiz', '987654323', 'carlos@modaexpress.com', 'Jr. La Moda 789, Trujillo'),
]

for prov in proveedores:
    cursor.execute('''
        INSERT INTO proveedores (ruc, nombre, contacto, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', prov)
print(f"✓ Insertados {len(proveedores)} proveedores")

cursor.execute('INSERT INTO ventas (codigo_venta, cliente, total) VALUES (?, ?, ?)',
               ('VENTA001', 'Cliente Mayorista', 1250.00))
cursor.execute('INSERT INTO ventas (codigo_venta, cliente, total) VALUES (?, ?, ?)',
               ('VENTA002', 'Tienda de Ropa La Elegante', 850.00))
print("✓ Insertadas 2 ventas")

# Confirmar cambios
conn.commit()

print("\n✅ VERIFICANDO...")
cursor.execute("SELECT COUNT(*) FROM productos")
print(f"   Productos: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM proveedores")
print(f"   Proveedores: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ventas")
print(f"   Ventas: {cursor.fetchone()[0]}")

# Mostrar productos
print("\n📋 LISTA DE PRODUCTOS:")
cursor.execute("SELECT id, codigo, nombre, precio_venta, stock FROM productos")
for row in cursor.fetchall():
    print(f"   {row[0]}. {row[1]} - {row[2]} - ${row[3]} - Stock: {row[4]}")

# Cerrar
cursor.close()
conn.close()

tamaño = os.path.getsize(db_path)
print(f"\n💾 Archivo creado: {db_path}")
print(f"   Tamaño: {tamaño} bytes")

print("\n" + "="*60)
print("✅ BASE DE DATOS CREADA EXITOSAMENTE!")
print("="*60)
print("\n🚀 Ahora ejecuta: python main.py")

input("\nPresiona Enter para salir...")