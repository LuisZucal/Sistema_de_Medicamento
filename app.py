from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from config import Config
from flask_mail import Mail, Message
from flask import jsonify
from datetime import date


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

class TipoMedicamento(db.Model):
    __bind_key__ = 'db2'  # Usar la segunda base de datos
    __tablename__ = 'Tipo_Medicamento'  # Nombre correcto de la tabla
    id_tipo = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(50), name='nombre_tipo', nullable=False)  # Coma corregida

    # Relación con la tabla Medicamento, renombramos el backref
    medicamentos_rel = db.relationship('Medicamento', backref='tipo_medicamento', lazy=True)



class Medicamento(db.Model):
    __bind_key__ = 'db2'  # Usar la segunda base de datos
    __tablename__ = 'Medicamento'  # Nombre correcto de la tabla
    MedicamentoID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.String(255))
    Cantidad = db.Column(db.Integer)
    
    # Clave foránea que apunta a TipoMedicamento
    id_tipo = db.Column(db.Integer, db.ForeignKey('Tipo_Medicamento.id_tipo'), nullable=False)
    
    # Relación con TipoMedicamento
    tipo_medicamento_rel = db.relationship('TipoMedicamento', backref='medicamentos', lazy=True)
    
    recetas = db.relationship('Receta', backref='medicamento_rel', lazy=True)

    

def obtener_medicamentos_por_tipo(tipo_id):
    # Filtrar medicamentos por tipo y retornar solo el nombre y el id
    return Medicamento.query.filter_by(id_tipo=tipo_id).all()



class MedicamentoEntregado(db.Model):
    __tablename__ = 'medicamentos_entregados'
    
    id_m_entregados = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    rut = db.Column(db.String(12), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    medicamento_nombre = db.Column(db.String(100), nullable=False)  # Verifica este nombre
    cantidad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<MedicamentoEntregado {self.nombre} - Medicamento: {self.medicamento_nombre}, Cantidad: {self.cantidad}>"

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





# Definir la ruta para /entrega_tercero

@app.route('/entrega_tercero', methods=['GET', 'POST'])
def entregar_tercero():
    if request.method == 'POST':
        # Maneja la lógica de entrega de tercero aquí
        # Por ejemplo, obtener paciente, recetas, etc.
        return render_template('entrega_tercero.html')
    return render_template('entrega_tercero.html')






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
        # Aquí redirigimos a la plantilla entrega_tercero.html
        # Puedes pasar datos necesarios si los tienes
        return render_template('entrega_tercero.html', medicamentos_ids=medicamentos_ids)

    # Redirigir después de la acción si es necesario
    return redirect(url_for('dashboard_farmaceutico'))

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


# AUI ESTOY IMPLEMENTANDO LAS RUTAS PARA MOSTRAR LOS MEDICAMENTOS EN EL FRONENDT
from flask import render_template

@app.route('/tipo_medicamento', methods=['GET'])
def mostrar_tipo_medicamento():
    # Consulta a la base de datos solo para tipos de medicamentos
    tipos_medicamentos = TipoMedicamento.query.all()

    # Preparar los datos en formato JSON para verificar
    tipos_data = [{'id_tipo': tipo.id_tipo, 'nombre_tipo': tipo.nombre_tipo} for tipo in tipos_medicamentos]

    # Retornar los datos en formato JSON para verificar en Postman o el navegador
    return jsonify({
        'tipos_medicamentos': tipos_data
    })

@app.route('/medicamentos/<int:tipo_id>')
def get_medicamentos(tipo_id):
    # Obtener medicamentos utilizando la función definida
    medicamentos = obtener_medicamentos_por_tipo(tipo_id)
    
    # Preparar los datos en formato JSON
    medicamentos_data = [{'id': med.MedicamentoID, 'nombre': med.Nombre} for med in medicamentos]
    
    # Retornar los datos en formato JSON
    return jsonify(medicamentos_data)

@app.route('/cargar_medicamento', methods=['POST'])
def cargar_medicamento():
    try:
        data = request.get_json()
        
        fecha = data.get('fecha')
        rut = data.get('rut')
        nombre = data.get('nombre')
        medicamentos = data.get('medicamentos')
        
        for medicamento in medicamentos:
            nuevo_registro = MedicamentoEntregado(
                fecha=fecha,
                rut=rut,
                nombre=nombre,
                medicamento_nombre=medicamento['nombre'],
                cantidad=medicamento['cantidad']
            )
            db.session.add(nuevo_registro)

        db.session.commit()
        
        return jsonify({"mensaje": "Medicamentos entregados correctamente."})
    
    except Exception as e:
        print(f"Error al procesar la solicitud: {str(e)}")
        return jsonify({"error": "Hubo un error al procesar la solicitud."}), 500

if __name__ == '__main__':
    app.secret_key = Config.SECRET_KEY
    app.run(debug=True)
