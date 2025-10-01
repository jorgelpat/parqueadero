from repository.conexion import CConexion

def ingresar_vehiculo(placa, tipo, ingreso, salida, cobro):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return None
        
        cursor = con.cursor()

        # Verificar si hay un ingreso activo para esa placa
        sql_check = "SELECT 1 FROM registros WHERE placa = %s AND salida IS NULL LIMIT 1"
        cursor.execute(sql_check, (placa,))
        if cursor.fetchone():
            con.close()
            return False
        
        # Insertar nuevo registro (No hay ingreso activo)
        sql = "INSERT INTO registros (placa, tipo_vehiculo, ingreso, salida, cobro) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (placa, tipo, ingreso, salida, cobro))
        con.commit()
        con.close()
        print("✅ Vehículo ingresado")
        return True
    except ValueError as error:
        print("❌ Error al ingresar:", error)
        return None


def modificar_vehiculo(placa, salida, cobro):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return
        cursor = con.cursor()
        sql = "UPDATE registros SET salida = %s, cobro = %s WHERE placa = %s AND salida IS NULL"
        cursor.execute(sql, (salida, cobro, placa))
        con.commit()
        con.close()
        print("✅ Vehículo actualizado")
    except Exception as e:
        print("❌ Error al actualizar:", e)


def mostrar_vehiculos():
    try:
        con = CConexion.get_conexion()
        if con is None:
            return []
        cursor = con.cursor()
        cursor.execute("SELECT id_registro, placa, tipo_vehiculo, ingreso, salida, cobro FROM registros ORDER BY ingreso DESC")
        datos = cursor.fetchall()
        con.close()
        return datos
    except Exception as e:
        print("Error al mostrar:", e)
        return []


def obtener_ingreso(placa):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return None
        cursor = con.cursor()
        sql = "SELECT ingreso FROM registros WHERE placa = %s AND salida IS NULL"
        cursor.execute(sql, (placa,))
        result = cursor.fetchone()
        con.close()
        return result[0] if result else None
    except Exception as e:
        print("❌ Error al obtener ingreso:", e)
        return None
    
def eliminar_vehiculo(id_registro, usuario_admin, observacion):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return None
        cursor = con.cursor()

        # Marcar como eliminado en registros
        sql1 = "UPDATE registros SET eliminado = 1 WHERE id_registro = %s"
        cursor.execute(sql1, (id_registro,))

        # Guardar log de eliminación
        sql2 = "INSERT INTO eliminaciones (id_Registro, usuario_admin, observacion) VALUES (%s, %s, %s)"
        cursor.execute(sql2, (id_registro, usuario_admin, observacion))

        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error al eliminar vehículo: ", e)
        return False