from repository.conexion import CConexion

def verificar_usuario(usuario, password):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return False
        cursor = con.cursor()
        sql = "SELECT 1 FROM usuarios WHERE usuario = %s AND password = %s LIMIT 1"
        cursor.execute(sql, (usuario,password))
        result = cursor.fetchone()
        con.close()
        return result is not None
    except Exception as e:
        print("Error al verificar Usuario", e)
        return False
    

def crear_usuario(usuario, password):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return False
        cursor = con.cursor()
        sql = "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)"
        cursor.execute(sql, (usuario, password))
        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error al verificar Usuario", e)
        return False