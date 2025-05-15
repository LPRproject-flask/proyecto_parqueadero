from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Plate(db.Model):
    __tablename__ = 'plates'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    placa = db.Column(db.String, nullable=False, unique=True)
    cedula = db.Column(db.String, nullable=False)
    foto = db.Column(db.String)  # Es opcional, así que no va con nullable=False
    email = db.Column(db.String)  # También es opcional según SQLite

    def __repr__(self):
        return f'<Plate {self.placa} - {self.nombre}>'
