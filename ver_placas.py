import sqlite3

def ver_placas():
    # Conectar a la base de datos
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    
    # Consulta para obtener las placas registradas
    cursor.execute("SELECT id, nombre, placa, cedula, foto, email FROM plates")
    placas = cursor.fetchall()  # Obtener todos los resultados
    
    # Cerrar la conexión
    conn.close()

    # Verificar si hay placas registradas
    if placas:
        print("\n\U0001F4CB Lista de placas registradas:")
        print("-" * 80)
        for placa in placas:
            print(f"\U0001F7E2 ID: {placa[0]} | \U0001F464 Propietario: {placa[1]} | 🚗 Placa: {placa[2]} | 🆔 Cédula: {placa[3]} | email: {placa[4]}")
            print("-" * 80)
    else:
        print("\u26A0\ufe0f No hay placas registradas.")

# Ejecutar la función
if __name__ == "__main__":
    ver_placas()