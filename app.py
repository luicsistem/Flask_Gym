from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#libreria que se conecta con mysql
from flask_mysqldb import MySQL
#controles para los formularios
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
#libreria que me permite encriptar el password
from passlib.hash import sha256_crypt
#saltos de linea en los formularios
from functools import wraps
#importar la clase de formularios
#from formularios import*
from formularios import RegistrarUsuario

app = Flask(__name__, static_url_path='/static')
app.debug = True
# cadena de conexion a mi base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gym'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# inicializando MYSQL
mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/blogs')
def blogs():
    return render_template('blogs.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        pass_cand = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM clientes where nick=%s", [usuario])
        if result > 0:
            data = cur.fetchone()
            password = data['pass']
            # comparacion de passwords
            if sha256_crypt.verify(pass_cand, password):
                session['logged_in'] = True
                session['username'] = usuario
                flash("usuario correcto", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'usuario errado'
                return render_template("login.html", error=error)
            cur.close()
        else:
            error = 'clave incorrecta'
            return render_template("login.html")
    return render_template("login.html")



@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrarUsuario(request.form)  # Herencia POO
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        usuario = form.usuario.data
        correo = form.correo.data
        password = sha256_crypt.encrypt(str(form.password.data))
        obs = form.comentarios.data
        # Grabarlo en la BD
        # crear un cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nombre,correo,usuario,pass,observacion)values(%s,%s,%s,%s,%s)",
                    (nombre, correo, usuario, password, obs))
        mysql.connection.commit()
        cur.close()
        flash("Registro Grabado con exito")
        redirect(url_for("login"))
    return render_template("registrar.html", form=form)



@app.route('/dashboard')
def dashbaord():
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, port=8000)
