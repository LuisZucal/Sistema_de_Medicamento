from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Farmaceutico, Doctor, Paciente, Receta, TipoMedicamento, Medicamento, MedicamentoEntregado
from datetime import datetime

def init_routes(app):

    # Ruta de inicio
    @app.route('/')
    def index():
        return redirect(url_for('login'))
    
    @app.route('/forgot-password')
    def forgot_password():
        return render_template('forgot-password.html')

    # Ruta de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']

            # Verificación de credenciales
            usuario_en_db = Farmaceutico.query.filter_by(usuario=usuario).first()
            if usuario_en_db and check_password_hash(usuario_en_db.contrasena, contrasena):
                session['tipo_usuario'] = 'farmaceutico'
                return redirect(url_for('dashboard_farmaceutico'))

            flash('Credenciales incorrectas.')
        return render_template('login.html')

    # Ruta para cerrar sesión
    @app.route('/logout')
    def logout():
        session.clear()
        flash('Has cerrado sesión correctamente.')
        return redirect(url_for('login'))

    # Ruta para crear usuario
    @app.route('/admin/create_user', methods=['GET', 'POST'])
    def create_user():
        if request.method == 'POST':
            # Lógica para crear usuario
            # ...
            pass
        return render_template('create_user.html')

    # Ruta para el dashboard farmacéutico
    @app.route('/dashboard_farmaceutico')
    def dashboard_farmaceutico():
        if session.get('tipo_usuario') == 'farmaceutico':
            return render_template('dashboard_farmaceutico.html')
        flash('Acceso denegado.')
        return redirect(url_for('login'))

    # Ruta para mostrar tipos de medicamentos
    @app.route('/tipo_medicamento', methods=['GET'])
    def mostrar_tipo_medicamento():
        tipos_medicamentos = TipoMedicamento.query.all()
        tipos_data = [{'id_tipo': tipo.id_tipo, 'nombre_tipo': tipo.nombre_tipo} for tipo in tipos_medicamentos]
        return jsonify({'tipos_medicamentos': tipos_data})

    # Ruta para buscar paciente
    @app.route('/buscar_paciente', methods=['POST'])
    def buscar_paciente():
        rut = request.form['rut_paciente']
        paciente = Paciente.query.filter_by(Rut=rut).first()
        if paciente:
            return redirect(url_for('receta_medica', rut=rut))
        else:
            flash('Paciente no encontrado.', 'error')
            return redirect(url_for('dashboard_farmaceutico'))

    # Ruta para mostrar receta médica
    @app.route('/receta_medica/<rut>')
    def receta_medica(rut):
        paciente = Paciente.query.filter_by(Rut=rut).first()
        if paciente:
            recetas = Receta.query.filter_by(PacienteID=paciente.PacienteID).all()
            today = datetime.now().date()
            today_formatted = today.strftime('%Y-%m-%d')
            return render_template('recetaMedica.html', paciente=paciente, recetas=recetas, today=today_formatted)
        else:
            flash('No se encontró el paciente.', 'error')
            return redirect(url_for('dashboard_farmaceutico'))

    # Ruta para entrega de medicamentos
    @app.route('/entrega', methods=['POST'])
    def entrega():
        accion = request.form['accion']
        if accion == 'entregar_medicamento':
            # Lógica para entregar medicamento
            # ...
            pass
        return redirect(url_for('dashboard_farmaceutico'))

  
