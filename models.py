from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plate(db.Model):
    __tablename__ = 'plates'

    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String, nullable=False)     # <- nombre del dueño
    plate_number = db.Column(db.String, unique=True, nullable=False)  # <- número de placa
    owner_id = db.Column(db.String, nullable=False)        # <- cédula o ID del dueño

    def __repr__(self):
        return f'<Plate {self.plate_number} - {self.owner_name}>'
