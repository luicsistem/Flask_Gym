#Controles para el uso de Formularios
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
class RegistrarUsuario(Form):
    nombre = StringField('Nombre', [validators.length(min=1, max=50)])
    apellido = StringField('apellido', [validators.length(min=4, max=50)])
    usuario = StringField('Usuario o Nickname', [validators.length(min=4, max=25)])
    correo = StringField('Email', [validators.length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message="Password Vacio")])
    confirm = PasswordField("Confirmar Password")
    descripcion = TextAreaField('descripcion', [validators.length(min=1, max=500)])