import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="simulador_examen"
)

cursor = conexion.cursor()
cursor.execute("SHOW TABLES")
tablas = cursor.fetchall()
print("Tablas en la base de datos:")
for tabla in tablas:
    print(tabla[0])

cursor.close()
conexion.close()
