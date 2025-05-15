from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inicializa app y base de datos
app = Flask(__name__)

# Configura PostgreSQL (usa tu URL real de Render)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adminudec:YDySMJyI64fWllahlhvwCnNpNbDivKlM@dpg-d0aeui2dbo4c73cdsgn0-a.oregon-postgres.render.com/parqueadero_udec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def sincronizar_secuencia():
    with app.app_context():
        # Obtiene el nombre real de la secuencia
        seq_name_result = db.session.execute(
            text("SELECT pg_get_serial_sequence('users', 'id')")
        ).fetchone()

        if seq_name_result:
            seq_name = seq_name_result[0]
            print(f"🟢 Secuencia detectada: {seq_name}")

            # Sincroniza la secuencia con el último ID actual
            db.session.execute(
                text(f"SELECT setval('{seq_name}', (SELECT COALESCE(MAX(id), 1) FROM plates))")
            )
            db.session.commit()
            print("✅ Secuencia sincronizada correctamente.")
        else:
            print("❌ No se pudo obtener el nombre de la secuencia.")

if __name__ == "__main__":
    sincronizar_secuencia()
