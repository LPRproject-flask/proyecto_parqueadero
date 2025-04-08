import sqlite3

def ver_usuarios():
    # Conectar a la base de datos (data.db en la carpeta db)
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    
    # Consulta para obtener los usuarios registrados con su email y contraseña
    cursor.execute("SELECT id, username, password FROM users")
    usuarios = cursor.fetchall()  # Obtener todos los resultados
    
    # Cerrar la conexión
    conn.close()

    # Verificar si hay usuarios registrados
    if usuarios:
        print("\n\U0001F4CB Lista de usuarios registrados:")
        print("-" * 80)
        for usuario in usuarios:
            print(f"\U0001F7E2 ID: {usuario[0]} | \U0001F464 Usuario: {usuario[1]} | \U0001F4E7 Email: {usuario[2]}")
            print("-" * 80)
    else:
        print("\u26A0\ufe0f No hay usuarios registrados.")

# Ejecutar la función
if __name__ == "__main__":
    ver_usuarios()