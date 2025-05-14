import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Crear tabla de usuarios con la columna email
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Crear tabla de placas (vehículos)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS plates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        placa TEXT NOT NULL UNIQUE,
        cedula TEXT NOT NULL
    )
''')

# Verificar si la columna 'email' existe en la tabla users y agregarla si no existe
cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]
if "email" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN email TEXT NOT NULL UNIQUE")

# Guardar y cerrar conexión
conn.commit()
conn.close()