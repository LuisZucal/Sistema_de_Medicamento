from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

db = SQLAlchemy()

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
    __bind_key__ = 'db2'
    __tablename__ = 'Doctor'
    DoctorID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Especialidad = db.Column(db.String(100))
    Rut = db.Column(db.String(20), unique=True)
    recetas = db.relationship('Receta', backref='doctor_rel', lazy=True)

class Paciente(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'Paciente'
    PacienteID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Rut = db.Column(db.String(20), unique=True)
    Edad = db.Column(db.Integer)
    Direccion = db.Column(db.String(150))
    recetas = db.relationship('Receta', backref='paciente_rel', lazy=True)

class TipoMedicamento(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'Tipo_Medicamento'
    id_tipo = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(50), name='nombre_tipo', nullable=False)
    medicamentos_rel = db.relationship('Medicamento', backref='tipo_medicamento', lazy=True)

class Medicamento(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'Medicamento'
    MedicamentoID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.String(255))
    Cantidad = db.Column(db.Integer)
    id_tipo = db.Column(db.Integer, db.ForeignKey('Tipo_Medicamento.id_tipo'), nullable=False)
    tipo_medicamento_rel = db.relationship('TipoMedicamento', backref='medicamentos', lazy=True)
    recetas = db.relationship('Receta', backref='medicamento_rel', lazy=True)

class MedicamentoEntregado(db.Model):
    __tablename__ = 'medicamentos_entregados'
    id_m_entregados = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut = db.Column(db.String(12), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    medicamento_nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<MedicamentoEntregado {self.nombre} - Medicamento: {self.medicamento_nombre}, Cantidad: {self.cantidad}>"

class Receta(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'Receta'
    RecetaID = db.Column(db.Integer, primary_key=True)
    PacienteID = db.Column(db.Integer, db.ForeignKey('Paciente.PacienteID'), nullable=False)
    DoctorID = db.Column(db.Integer, db.ForeignKey('Doctor.DoctorID'), nullable=False)
    MedicamentoID = db.Column(db.Integer, db.ForeignKey('Medicamento.MedicamentoID'), nullable=False)
    FechaEntrega = db.Column(db.Date, default=datetime.today().date, nullable=True)
    CantidadMedicamento = db.Column(db.Integer, nullable=False)

    paciente = db.relationship('Paciente', backref='recetas_asociadas')
    doctor = db.relationship('Doctor', backref='recetas_asociadas')
    medicamento = db.relationship('Medicamento', backref='recetas_asociadas')

# Funciones de validación
def validate_user_input(data):
    return bool(re.match("^[A-Za-z0-9_]*$", data))

def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
