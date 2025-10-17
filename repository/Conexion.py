import mysql.connector
from repository.config_db import DB_CONFIG

class CConexion:
    @staticmethod
    def get_conexion():
        try:
            conexion = mysql.connector.connect(**DB_CONFIG) # Con ** desempaquetamos el diccionario
            return conexion
        except mysql.connector.Error as error:
            print("Error al conectar a la BD:", error)
            return None
