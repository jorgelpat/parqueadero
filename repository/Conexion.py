import mysql.connector

class CConexion:
    @staticmethod
    def get_conexion():
        try:
            conexion = mysql.connector.connect(
                user='root',
                password='123456',
                host='127.0.0.1',
                database='parqueadero',
                port='3306'
            )
            return conexion
        except mysql.connector.Error as error:
            print("❌ Error al conectar a la BD:", error)
            return None
