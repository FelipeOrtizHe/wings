import os

# General Flask Settings
DEBUG = True  # Cambiar a False en producción
# Es muy importante tener una SECRET_KEY segura para las sesiones y la seguridad en general.
# En producción, es mejor configurarla como una variable de entorno.

# ... otras configuraciones ...

# Database Settings (MySQL)
SQLALCHEMY_DATABASE_URI = 'mysql://root:root1234@localhost/red_social'
#                                     ^^^^^^^^^^^^^^^
#                                     Nombre de la variable de entorno

# ... otras configuraciones ...
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Esto evita un warning de Flask-SQLAlchemy sobre futuros cambios en la biblioteca. Puedes dejarlo en False.