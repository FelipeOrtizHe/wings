from .extensions import db

class Post(db.Model):
    __tablename__ = 'post'
    id_post = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuarios'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255))
    fecha_creacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    autor = db.relationship('Usuario', lazy=True)

    def __repr__(self):
        return f'<Post {self.contenido[:20]}>'