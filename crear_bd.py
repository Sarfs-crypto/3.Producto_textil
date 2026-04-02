"""
Script para crear la base de datos SQLite de TextilPro
"""
import sqlite3
import os


def crear_base_datos():
    # Ruta de la base de datos
    db_path = os.path.join('base_datos', 'textilpro.db')

    # Crear carpeta si no existe
    os.makedirs('base_datos', exist_ok=True)

    # Eliminar si existe
    if os.path.exists(db_path):
        os.remove(db_path)

    # Conectar a la base de datos (la crea automáticamente)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo VARCHAR(50) UNIQUE NOT NULL,
        nombre VARCHAR(200) NOT NULL,
        descripcion TEXT,
        categoria VARCHAR(100),
        talla VARCHAR(10),
        color VARCHAR(50),
        precio_compra DECIMAL(10,2) NOT NULL,
        precio_venta DECIMAL(10,2) NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        stock_minimo INTEGER DEFAULT 5,
        imagen_path VARCHAR(500),
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        estado BOOLEAN DEFAULT 1
    )
    ''')

    # Crear tabla de proveedores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ruc VARCHAR(20) UNIQUE NOT NULL,
        nombre VARCHAR(200) NOT NULL,
        contacto VARCHAR(100),
        telefono VARCHAR(20),
        email VARCHAR(100),
        direccion TEXT,
        imagen_path VARCHAR(500),
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        estado BOOLEAN DEFAULT 1
    )
    ''')

    # Crear tabla de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_venta VARCHAR(20) UNIQUE NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        cliente VARCHAR(200),
        total DECIMAL(10,2) NOT NULL,
        estado VARCHAR(20) DEFAULT 'completada'
    )
    ''')

    # Crear tabla de detalles de venta
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS venta_detalles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario DECIMAL(10,2) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    # Insertar datos de ejemplo
    productos_ejemplo = [
        ('TEL001', 'Algodón Premium', 'Algodón 100% orgánico', 'Telas', 'Rollo', 'Blanco', 25.00, 45.00, 100),
        ('TEL002', 'Seda Natural', 'Seda pura de alta calidad', 'Telas', 'Rollo', 'Crudo', 80.00, 150.00, 50),
        ('CAM001', 'Camisa Casual', 'Camisa de algodón para caballero', 'Prendas', 'M', 'Azul', 15.00, 35.00, 80),
        ('CAM002', 'Camisa Formal', 'Camisa de vestir manga larga', 'Prendas', 'L', 'Blanco', 20.00, 45.00, 60),
        ('PAN001', 'Pantalón Jean', 'Jean clásico azul', 'Prendas', '32', 'Azul', 25.00, 55.00, 40),
        ('HIL001', 'Hilo Poliéster', 'Hilo de alta resistencia', 'Insumos', '500m', 'Negro', 5.00, 12.00, 200),
    ]

    cursor.executemany('''
        INSERT INTO productos (codigo, nombre, descripcion, categoria, talla, color, precio_compra, precio_venta, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', productos_ejemplo)

    # Proveedores de ejemplo
    proveedores_ejemplo = [
        ('20123456789', 'Textiles del Perú SAC', 'Juan Pérez', '987654321', 'ventas@textilesperu.com',
         'Av. Industrial 123, Lima'),
        ('20987654321', 'Insumos Textiles EIRL', 'María López', '987654322', 'maria@insumostextiles.com',
         'Calle Comercio 456, Arequipa'),
        ('20456789012', 'Moda Express SAC', 'Carlos Ruiz', '987654323', 'carlos@modaexpress.com',
         'Jr. La Moda 789, Trujillo'),
    ]

    cursor.executemany('''
        INSERT INTO proveedores (ruc, nombre, contacto, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', proveedores_ejemplo)

    # Ventas de ejemplo
    cursor.execute('''
        INSERT INTO ventas (codigo_venta, cliente, total)
        VALUES ('VENTA001', 'Cliente Mayorista', 1250.00)
    ''')

    cursor.execute('''
        INSERT INTO ventas (codigo_venta, cliente, total)
        VALUES ('VENTA002', 'Tienda de Ropa La Elegante', 850.00)
    ''')

    # Confirmar cambios
    conn.commit()

    # Verificar que se creó correctamente
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    print(f"✓ Base de datos creada correctamente")
    print(f"  - Productos: {count}")

    cursor.execute("SELECT COUNT(*) FROM proveedores")
    count = cursor.fetchone()[0]
    print(f"  - Proveedores: {count}")

    cursor.execute("SELECT COUNT(*) FROM ventas")
    count = cursor.fetchone()[0]
    print(f"  - Ventas: {count}")

    # Cerrar conexión
    cursor.close()
    conn.close()

    print(f"\nBase de datos guardada en: {db_path}")


if __name__ == "__main__":
    crear_base_datos()