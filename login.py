import mysql.connector
from mysql.connector import Error

def verificar_login(usuario, contraseña):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="simulador_examen"
        )

        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
            cursor.execute(query, (usuario, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                return True, resultado['id_usuario']
            else:
                return False, None

    except Error as e:
        print(f"❌ Error en login: {e}")
        return False, None

    finally:
        if conexion.is_connected():
            conexion.close()
