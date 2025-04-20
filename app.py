from flask import Flask, render_template, redirect, url_for,flash
from models.extensions import db
from utils import config
from models import Usuario, Post
from models.forms import Registro, Crear_registro , login
from werkzeug.security import generate_password_hash, check_password_hash
from utils.secret import SECRET_KEY
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_login import login_user, logout_user,current_user,login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object(config)
app.config.from_pyfile('utils/config.py')
app.config.from_pyfile('utils/secret.py')

db.init_app(app)


@app.route("/")
def index():
    return redirect(url_for("posts"))

@app.route("/home")
def posts():
    form_crear_post = Crear_registro()
    posts = Post.query.all()
    return render_template('index.html', posts=posts, form_crear_post =form_crear_post)   

@app.route("/crear_post", methods=['POST'])
def crear_post():
    form_crear_post = Crear_registro()
    if form_crear_post.validate_on_submit():
        contenido = form_crear_post.contenido.data
        nueva_publicacion =Post(cotenido= contenido, fecha_publicacion= datetime.timezone.UTC-5())
        db.session.add(nueva_publicacion)
        db.session.commit()
        flash('¡Publicación creada!', 'success')

        return redirect(url_for('home'))
    return redirect(url_for('home'))



@app.route("/testdb")
def test_db_connection():
    try:
        usuarios = Usuario.query.all()
        posts = Post.query.all()
        return render_template('test_db.html', usuarios=usuarios,posts=posts ,error=None)
    except Exception as e:
        db.session.rollback()
        return render_template('test_db.html', usuarios=[], error=str(e))

@app.route("/login", method=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = login()
    return render_template('login.html', form=form)

@app.route("/login", method=['POST'])
def login_post():
    form = login()
    if form.validate_on_submit():
        identificacion = form.identificar.data
        contraseña = form.contraseña.data
        recordar = form.recordar.data

        usuario = Usuario.query.filter((Usuario.nombre == identificacion) |(Usuario.correo_electronico == identificacion )).first()

        if usuario and usuario.check_password(contraseña):
            login_user(usuario, recordar= recordar)
            flash('Inicio de sesion exitoso')
        else:
            flash('nombre de usuario o correo electronico contraseña incorrectos. Por favor, inténtalo de nuevo.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('¡Sesión cerrada!', 'info')
    return redirect(url_for('home'))




@app.route("/registro", methods=['GET','POST'])
def registro():
    form = Registro()
    if form.validate_on_submit():
        if form.submit_registro.data:
            hashed_contraseña = generate_password_hash(form.contraseña.data)
            nuevo_usuario = Usuario(nombre = form.nombre.data,
                                    correo_electronico = form.correo_electronico.data,
                                    contraseña = hashed_contraseña,
                                    biografia = form.biografia.data)
            db.session.add(nuevo_usuario)
            try:
                db.session.commit()
                return redirect(url_for("posts"))
            except IntegrityError as e:
                db.session.rollback()
                if "Duplicate entry" in str(e) and "nombre_UNIQUE" in str(e):
                    form.nombre.errors.append('Este nombre de usuario ya está en uso.')
                elif "Duplicate entry" in str(e) and "correo_electronico_UNIQUE" in str(e):
                    form.correo_electronico.errors.append('Este correo electrónico ya está registrado.')
                else:
                    form.errors.append('Ocurrió un error al registrar el usuario.')
    return render_template('registro.html', title= 'Registro', form = form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=app.config['DEBUG'])