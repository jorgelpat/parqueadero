import bcrypt
from repository.conexion import CConexion

def verificar_usuario(usuario, password):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return False
        cursor = con.cursor()
        sql = "SELECT password FROM usuarios WHERE usuario = %s LIMIT 1"
        cursor.execute(sql, (usuario,))
        result = cursor.fetchone()
        con.close()

        if not result:
            return False

        hashed = result[0]  # Hash guardado en la BD
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception as e:
        print("Error al verificar usuario:", e)
        return False
    

def crear_usuario(usuario, password):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return False
        cursor = con.cursor()

        # Generar hash de la contraseña
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        sql = "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)"
        cursor.execute(sql, (usuario, hashed.decode("utf-8")))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error al verificar Usuario", e)
        return False