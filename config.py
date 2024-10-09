import os
from urllib.parse import quote_plus

class Config:
# Configuración de la primera base de datos
    DB_DRIVER = "ODBC Driver 17 for SQL Server"
    DB_SERVER = os.getenv('DB_SERVER', 'DESKTOP-E7TMHHH')  # Valor por defecto
    DB_NAME = os.getenv('DB_NAME', 'HospitalLogin')
    DB_USER = os.getenv('DB_USER', 'sa')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', 'admin123'))  # Escapando caracteres especiales
    SECRET_KEY = os.getenv('SECRET_KEY', '01f2a2e466e4fefb442d0b997845b0a9e79d3f2028a5e6df')


    # Configuración de la segunda base de datos
    DB_DRIVER2 = "ODBC Driver 17 for SQL Server"
    DB_SERVER2 = os.getenv('DB_SERVER2', 'DESKTOP-E7TMHHH')
    DB_NAME2 = os.getenv('DB_NAME2', 'HospitalMedicamento')
    DB_USER2 = os.getenv('DB_USER2', 'sa')
    DB_PASSWORD2 = os.getenv('DB_PASSWORD2', 'admin123')  # No codificar aquí

    # URI de conexión para la primera base de datos
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc:///?odbc_connect="
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    # URI de conexión para la segunda base de datos
    SQLALCHEMY_BINDS = {
        'db2': (
            f"mssql+pyodbc:///?odbc_connect="
            f"DRIVER={{{DB_DRIVER2}}};"
            f"SERVER={DB_SERVER2};"
            f"DATABASE={DB_NAME2};"
            f"UID={DB_USER2};"
            f"PWD={DB_PASSWORD2};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
