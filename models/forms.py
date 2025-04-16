from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField,SubmitField
from wtforms.validators import DataRequired, Email ,EqualTo , Length
from wtforms import ValidationError
from models import Usuario

class Registro(FlaskForm):
    nombre = StringField('Nombre de usuario', validators=[DataRequired(), Length(min = 5, max= 24)])
    correo_electronico = StringField('Correo electronico ', validators=[DataRequired(),Email(),Length(max= 45)])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min = 6 ,max= 24)])
    confirmar_contraseña = PasswordField('Confirmar contraseña,', validators=[DataRequired(),EqualTo('contraseña')])
    biografia = TextAreaField('Biografia', validators=[Length(max=200)])
    submit = SubmitField('Registrarse')

    def validacion_nombre(self,nombre):
        usuario = Usuario.query.filter_by(nombre=nombre.data).first()
        if usuario:
            raise ValidationError('Este nombre de usuario ya existe, porfavor elige uno nuevo')
        
    def validacion_correo(self,correo_electronico):
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico.data).first()
        if usuario:
            raise ValidationError('Este correo electrónico ya está registrado. ¿Olvidaste tu contraseña?')