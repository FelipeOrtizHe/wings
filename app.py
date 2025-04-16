from flask import Flask, render_template, redirect, url_for
from models.extensions import db
from utils import config
from models import Usuario, Post
from models.forms import Registro
from werkzeug.security import generate_password_hash
from utils.secret import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object(config)
app.config.from_pyfile('utils/config.py')
app.config.from_pyfile('utils/secret.py')

db.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/testdb")
def test_db_connection():
    try:
        usuarios = Usuario.query.all()
        posts = Post.query.all()
        return render_template('test_db.html', usuarios=usuarios,posts=posts ,error=None)
    except Exception as e:
        db.session.rollback()
        return render_template('test_db.html', usuarios=[], error=str(e))
    
@app.route("/registro", methods=['GET','POST'])
def registro():
    form = Registro()
    if form.validate_on_submit():
        hashed_contraseña = generate_password_hash(form.contraseña.data)
        nuevo_usuario = Usuario(nombre = form.nombre.data,
                                correo_electronico = form.correo_electronico.data,
                                contraseña = hashed_contraseña,
                                biografi = form.biografia.data)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("/"))
    return render_template('registro.html', title= 'Registro', form = form)

if __name__ == '__main__':
    with app.app_context():  # Corrección de la tipografía aquí
        db.create_all()
    app.run(debug=app.config['DEBUG'])