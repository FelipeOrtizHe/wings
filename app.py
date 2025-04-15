from flask import Flask, render_template

app = Flask(__name__)

app.config.from_pyfile('config.py') 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])