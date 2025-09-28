from repository.conexion import CConexion

def ingresarVehiculo(placa, tipo, ingreso, salida, cobro):
    try:
        con = CConexion.get_conexion()
        if con is None:
            return
        cursor = con.cursor()
        sql = "INSERT INTO registros (placa, tipo_vehiculo, ingreso, salida, cobro) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (placa, tipo, ingreso, salida, cobro))
        con.commit()
        con.close()
        print("✅ Vehículo ingresado")
    except Exception as e:
        print("❌ Error al ingresar:", e)


def modificarVehiculo(placa, salida, cobro):
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


def mostrarVehiculos():
    try:
        con = CConexion.get_conexion()
        if con is None:
            return []
        cursor = con.cursor()
        cursor.execute("SELECT placa, tipo_vehiculo, ingreso, salida, cobro FROM registros ORDER BY ingreso DESC")
        datos = cursor.fetchall()
        con.close()
        return datos
    except Exception as e:
        print("❌ Error al mostrar:", e)
        return []


def obtenerIngreso(placa):
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
