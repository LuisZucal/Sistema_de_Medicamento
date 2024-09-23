from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from config import Config
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

mail = Mail(app)

# Definir el modelo de Farmaceutico
class Farmaceutico(db.Model):
    __tablename__ = 'Farmaceuticos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15))
    correo_electronico = db.Column(db.String(100))
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)

class Doctor(db.Model):
    __bind_key__ = 'db2'  # Usar la segunda base de datos
    __tablename__ = 'Doctor'
    DoctorID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Especialidad = db.Column(db.String(100))
    Rut = db.Column(db.String(20), unique=True)

    recetas = db.relationship('Receta', backref='doctor_rel', lazy=True)

class Paciente(db.Model):
    __bind_key__ = 'db2'  # Usar la segunda base de datos
    __tablename__ = 'Paciente'
    PacienteID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Rut = db.Column(db.String(20), unique=True)
    Edad = db.Column(db.Integer)
    Direccion = db.Column(db.String(150))

    recetas = db.relationship('Receta', backref='paciente_rel', lazy=True)

class Medicamento(db.Model):
    __bind_key__ = 'db2'  # Usar la segunda base de datos
    __tablename__ = 'Medicamento'
    MedicamentoID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.String(255))
    Cantidad = db.Column(db.Integer)

    recetas = db.relationship('Receta', backref='medicamento_rel', lazy=True)

class Receta(db.Model):
    __bind_key__ = 'db2'  # Usar la segunda base de datos
    __tablename__ = 'Receta'
    RecetaID = db.Column(db.Integer, primary_key=True)
    PacienteID = db.Column(db.Integer, db.ForeignKey('Paciente.PacienteID'), nullable=False)
    DoctorID = db.Column(db.Integer, db.ForeignKey('Doctor.DoctorID'), nullable=False)
    MedicamentoID = db.Column(db.Integer, db.ForeignKey('Medicamento.MedicamentoID'), nullable=False)
    FechaEntrega = db.Column(db.Date, nullable=False)
    CantidadMedicamento = db.Column(db.Integer, nullable=False)

    paciente = db.relationship('Paciente', backref='recetas_asociadas')
    doctor = db.relationship('Doctor', backref='recetas_asociadas')  # Este es el cambio
    medicamento = db.relationship('Medicamento', backref='recetas_asociadas')


# Función para validar entradas de usuario
def validate_user_input(data):
    return bool(re.match("^[A-Za-z0-9_]*$", data))

def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

# Crear usuario (farmacéutico o administrador)
@app.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        tipo_usuario = request.form['tipo_usuario']
        telefono = request.form.get('telefono')
        correo_electronico = request.form.get('correo_electronico')

        if not validate_user_input(usuario):
            flash('El nombre de usuario contiene caracteres no válidos.')
            return redirect(url_for('create_user'))

        if not validate_email(correo_electronico):
            flash('El correo electrónico no es válido.')
            return redirect(url_for('create_user'))

        if len(contrasena) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.')
            return redirect(url_for('create_user'))

        hashed_password = generate_password_hash(contrasena)

        try:
            if tipo_usuario == 'farmaceutico':
                nuevo_usuario = Farmaceutico(
                    nombre=nombre,
                    apellido=apellido,
                    usuario=usuario,
                    contrasena=hashed_password,
                    telefono=telefono,
                    correo_electronico=correo_electronico
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                flash('Usuario creado exitosamente.')
                return redirect(url_for('create_user'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el usuario: {str(e)}')
            return redirect(url_for('create_user'))

    return render_template('create_user.html')

@app.route('/buscar_paciente', methods=['POST'])
def buscar_paciente():
    rut = request.form['rut_paciente']
    
    # Consulta a la base de datos
    paciente = Paciente.query.filter_by(Rut=rut).first()
    
    if paciente:
        # Redirigir a la página de receta médica
        return redirect(url_for('receta_medica', rut=rut))
    else:
        flash('Paciente no encontrado.', 'error')
        return redirect(url_for('dashboard_farmaceutico'))  # Redirigir de vuelta al formulario

@app.route('/receta_medica/<rut>')
def receta_medica(rut):
    paciente = Paciente.query.filter_by(Rut=rut).first()
    
    if paciente:
        recetas = Receta.query.filter_by(PacienteID=paciente.PacienteID).all()
        return render_template('recetaMedica.html', paciente=paciente, recetas=recetas)
    else:
        flash('No se encontró el paciente.', 'error')
        return redirect(url_for('dashboard_farmaceutico'))

@app.route('/entrega', methods=['POST'])
def entrega():
    accion = request.form['accion']
    medicamentos_ids = request.form.getlist('medicamento')
    
    if accion == 'entrega':
        # Lógica para la entrega de medicamentos
        pass
    elif accion == 'entrega_tercero':
        # Lógica para la entrega a terceros
        pass

    # Redirigir después de la acción
    return redirect(url_for('dashboard_farmaceutico'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        if usuario == 'admin' and contrasena == 'admin123':
            return redirect(url_for('create_user'))  # Redirigir a la página de crear usuario

        # Verificar si el usuario es un farmacéutico
        usuario_en_db = Farmaceutico.query.filter_by(usuario=usuario).first()

        if usuario_en_db and check_password_hash(usuario_en_db.contrasena, contrasena):
            session['tipo_usuario'] = 'farmaceutico'
            return redirect(url_for('dashboard_farmaceutico'))

        flash('Credenciales incorrectas.')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))

# Recuperar contraseña
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('El campo de correo electrónico está vacío.')
            return redirect(url_for('forgot_password'))

        msg = Message("Recuperación de contraseña", recipients=[email])
        msg.body = "Instrucciones para restablecer tu contraseña."
        mail.send(msg)

        flash('Las instrucciones para restablecer tu contraseña han sido enviadas a tu correo electrónico.')
        return redirect(url_for('forgot_password'))

    return render_template('forgot-password.html')

# Dashboard farmacéutico
@app.route('/dashboard_farmaceutico')
def dashboard_farmaceutico():
    if session.get('tipo_usuario') == 'farmaceutico':
        return render_template('dashboard_farmaceutico.html')
    flash('Acceso denegado.')
    return redirect(url_for('login'))

# Página de inicio
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = Config.SECRET_KEY
    app.run(debug=True)
