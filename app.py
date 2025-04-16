from flask import Flask, render_template
from models.extensions import db
from utils import config
from models import Usuario, Post

app = Flask(__name__)
app.config.from_object(config)
app.config.from_pyfile('utils/config.py')

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

if __name__ == '__main__':
    with app.app_context():  # Corrección de la tipografía aquí
        db.create_all()
    app.run(debug=app.config['DEBUG'])