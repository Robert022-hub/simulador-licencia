import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )

    if conexion.is_connected():
        print("✅ ¡Conexión exitosa a MySQL!")

except Error as e:
    print(f"❌ Error al conectar a MySQL: {e}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("🔒 Conexión cerrada.")
