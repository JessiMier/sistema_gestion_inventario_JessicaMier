import sqlite3

NOMBRE_BD = "inventario.db"

def inicializar_db():
    """Crea la base de datos y la tabla productos"""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    
    query = '''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    '''
    cursor.execute(query)
    conexion.commit()
    conexion.close()
    print("Base de datos 'inventario.db' inicializada correctamente.")

def crear_producto(nombre, descripcion, cantidad, precio, categoria):
    """Inserta un nuevo producto en la tabla."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    query = '''
       INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
       VALUES (?, ?, ?, ?, ?)
    '''
    parametros = (nombre, descripcion, cantidad, precio, categoria)
    cursor.execute(query, parametros)
    conexion.commit()
    conexion.close()

def obtener_productos():
    """Recupera todos los productos de la base de datos."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    consulta_sql= '''
        SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos
    '''
    cursor.execute(consulta_sql)
    filas = cursor.fetchall()
    conexion.close()
    return filas

def buscar_producto_por_id(id_producto):
    """Busca un producto específico mediante su ID (Requerimiento Obligatorio)."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    consulta_sql= '''
        SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?
    '''
    parametros = (id_producto)
    cursor.execute(consulta_sql, parametros)
    producto = cursor.fetchone()
    conexion.close()
    return producto

def actualizar_producto_precio_stock(id_producto, nueva_cantidad, nuevo_precio):
    """Actualiza la cantidad y el precio de un producto mediante su ID."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    query = "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?"
    cursor.execute(query, (nueva_cantidad, nuevo_precio, id_producto))
    conexion.commit()
    # rowcount nos dice cuantas filas se modificaron (si es 0, el ID no existía)
    filas_afectadas = cursor.rowcount 
    conexion.close()
    return filas_afectadas > 0

def eliminar_producto_por_id(id_producto):
    """Elimina un producto de la base de datos mediante su ID."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0

def reporte_bajo_stock(limite):
    """Trae los productos cuya cantidad sea igual o inferior al límite dado."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad <= ?", (limite,))
    filas = cursor.fetchall()
    conexion.close()
    return filas