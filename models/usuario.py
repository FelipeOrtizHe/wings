from models.extensions import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, name='id_usuarios')
    nombre = db.Column(db.String(24), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(45), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    biografia = db.Column(db.Text, nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    imagen_perfil = db.Column(db.String(200))
    posts = db.relationship('Post', lazy=True) # Eliminar backref='autor'

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

    def get_id(self):
        return str(self.id)