from app import app
from models import db

with app.app_context():
    print("⚠️  Eliminando tablas...")
    db.drop_all()
    
    print("✅ Tablas eliminadas. Ahora creando nuevas...")
    db.create_all()
    
    print("🎉 Base de datos reiniciada con éxito.")