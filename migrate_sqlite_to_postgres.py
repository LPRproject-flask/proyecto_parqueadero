# migrate_sqlite_to_postgres.py
import sqlite3
from app import app
from models import db, User, Plate

# Conectarse a la base de datos SQLite
sqlite_conn = sqlite3.connect("db/data.db")
sqlite_cursor = sqlite_conn.cursor()

with app.app_context():
    print("🔄 Migrando usuarios...")

    # Migrar usuarios
    sqlite_cursor.execute("SELECT id, username, email, password FROM users")
    users = sqlite_cursor.fetchall()
    for id, username, email, password in users:
        # Verificar si ya existe en PostgreSQL
        existing = User.query.filter_by(username=username).first()
        if not existing:
            new_user = User(
                id=id,
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)

    print("🔄 Migrando placas...")

    # Migrar placas
    sqlite_cursor.execute("SELECT id, nombre, placa, cedula, foto, email FROM plates")
    plates = sqlite_cursor.fetchall()
    for id, nombre, placa, cedula, foto, email in plates:
        # Verificar si ya existe en PostgreSQL
        existing = Plate.query.filter_by(placa=placa).first()
        if not existing:
            new_plate = Plate(
                id=id,
                nombre=nombre,
                placa=placa,
                cedula=cedula,
                foto=foto,
                email=email
            )
            db.session.add(new_plate)

    # Guardar todos los cambios
    db.session.commit()
    print("✅ Migración completada con éxito.")

# Cerrar conexión SQLite
sqlite_conn.close()
