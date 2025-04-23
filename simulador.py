import mysql.connector
import random

def obtener_preguntas_practica():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM preguntas"
    cursor.execute(query)
    todas = cursor.fetchall()
    seleccionadas = random.sample(todas, 20)

    cursor.close()
    conexion.close()
    return seleccionadas

from datetime import datetime

def guardar_intento(id_usuario, tipo_examen, puntuacion):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )

    cursor = conexion.cursor()

    aprobado = puntuacion >= 75
    query = """
    INSERT INTO examenes (id_usuario, tipo_examen, fecha_realizacion, puntuacion, aprobado)
    VALUES (%s, %s, %s, %s, %s)
    """
    datos = (id_usuario, tipo_examen, datetime.now(), puntuacion, aprobado)
    cursor.execute(query, datos)
    conexion.commit()

    cursor.close()
    conexion.close()
    print("📝 Intento guardado en la base de datos.")

def obtener_intentos_final(id_usuario):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )

    cursor = conexion.cursor()
    query = "SELECT COUNT(*) FROM examenes WHERE id_usuario = %s AND tipo_examen = 'final'"
    cursor.execute(query, (id_usuario,))
    cantidad = cursor.fetchone()[0]

    cursor.close()
    conexion.close()
    return cantidad

def guardar_intento(id_usuario, tipo_examen, puntuacion):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()

    aprobado = puntuacion >= 75
    query = """
    INSERT INTO examenes (id_usuario, tipo_examen, fecha_realizacion, puntuacion, aprobado)
    VALUES (%s, %s, NOW(), %s, %s)
    """
    cursor.execute(query, (id_usuario, tipo_examen, puntuacion, aprobado))
    conexion.commit()
    id_examen = cursor.lastrowid

    cursor.close()
    conexion.close()
    print("📝 Intento guardado.")
    return id_examen

def guardar_respuesta(id_examen, id_pregunta, id_opcion_seleccionada, correcta):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()

    query = """
    INSERT INTO respuestas (id_examen, id_pregunta, id_opcion_seleccionada, correcta)
    VALUES (%s, %s, %s, %s)
    """
    datos = (id_examen, id_pregunta, id_opcion_seleccionada, correcta)
    cursor.execute(query, datos)
    conexion.commit()

    cursor.close()
    conexion.close()

def mostrar_respuestas_por_examen(id_examen):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT 
        r.id_respuesta,
        p.pregunta,
        o.texto_opcion AS opcion_seleccionada,
        r.correcta
    FROM respuestas r
    JOIN preguntas p ON r.id_pregunta = p.id_pregunta
    LEFT JOIN opciones o ON r.id_opcion_seleccionada = o.id_opcion
    WHERE r.id_examen = %s
    """
    cursor.execute(query, (id_examen,))
    resultados = cursor.fetchall()

    print(f"\n📋 Respuestas del examen #{id_examen}:\n")
    for r in resultados:
        estado = "✅ Correcta" if r['correcta'] else "❌ Incorrecta"
        print(f"• {r['pregunta']}\n  → Seleccionó: {r['opcion_seleccionada']} | {estado}\n")

    cursor.close()
    conexion.close()

def mostrar_historial_usuario(id_usuario):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT id_examen, tipo_examen, fecha_realizacion, puntuacion, aprobado
    FROM examenes
    WHERE id_usuario = %s
    ORDER BY fecha_realizacion DESC
    """
    cursor.execute(query, (id_usuario,))
    examenes = cursor.fetchall()

    print(f"\n Historial de exámenes del usuario #{id_usuario}:\n")
    if not examenes:
        print("⚠️ No hay intentos registrados todavía.")
    else:
        for e in examenes:
            estado = "✅ Aprobado" if e['aprobado'] else "❌ No aprobado"
            print(f"📄 Examen #{e['id_examen']} - {e['tipo_examen'].capitalize()}")
            print(f"   Fecha: {e['fecha_realizacion']} | Puntos: {e['puntuacion']}/100 | {estado}\n")

    cursor.close()
    conexion.close()

def obtener_historial_texto(id_usuario):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT id_examen, tipo_examen, fecha_realizacion, puntuacion, aprobado
    FROM examenes
    WHERE id_usuario = %s
    ORDER BY fecha_realizacion DESC
    """
    cursor.execute(query, (id_usuario,))
    examenes = cursor.fetchall()

    if not examenes:
        return "⚠️ No hay intentos registrados todavía."

    historial = "📚 Historial de exámenes:\n\n"
    for e in examenes:
        estado = "✅ Aprobado" if e["aprobado"] else "❌ No aprobado"
        historial += f"📄 #{e['id_examen']} - {e['tipo_examen'].capitalize()} | {e['fecha_realizacion']} | {e['puntuacion']}/100 | {estado}\n"

    cursor.close()
    conexion.close()
    return historial

def obtener_preguntas_practica():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM preguntas WHERE tipo = 'práctica' ORDER BY RAND() LIMIT 20")
    preguntas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return preguntas

def obtener_opciones(id_pregunta):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM opciones WHERE id_pregunta = %s", (id_pregunta,))
    opciones = cursor.fetchall()
    cursor.close()
    conexion.close()
    return opciones

# Verifica cuántos intentos lleva el usuario
def obtener_intentos_final(id_usuario):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM examenes WHERE id_usuario = %s AND tipo_examen = 'final'", (id_usuario,))
    intentos = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    return intentos

# Guarda el examen en la tabla examenes
def guardar_intento(id_usuario, tipo_examen, puntuacion):
    aprobado = 1 if puntuacion >= 75 else 0
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO examenes (id_usuario, tipo_examen, fecha_realizacion, puntuacion, aprobado)
        VALUES (%s, %s, NOW(), %s, %s)
    """, (id_usuario, tipo_examen, puntuacion, aprobado))
    conexion.commit()
    id_examen = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_examen

# Guarda respuestas
def guardar_respuesta(id_examen, id_pregunta, id_opcion, correcta):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO respuestas (id_examen, id_pregunta, id_opcion_seleccionada, correcta)
        VALUES (%s, %s, %s, %s)
    """, (id_examen, id_pregunta, id_opcion, correcta))
    conexion.commit()
    cursor.close()
    conexion.close()

def registrar_usuario(nombre_usuario, contraseña):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return False, "⚠️ El usuario ya existe."

    cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (%s, %s)", (nombre_usuario, contraseña))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True, "✅ Usuario registrado con éxito."

import random
import mysql.connector

def obtener_preguntas_final():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM preguntas WHERE tipo = 'final'"
    cursor.execute(query)
    todas = cursor.fetchall()

    if len(todas) < 40:
        seleccionadas = todas  # por si tienes menos de 40
    else:
        seleccionadas = random.sample(todas, 40)

    cursor.close()
    conexion.close()
    return seleccionadas

def obtener_datos_dashboard(tipo):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor()

    cursor.execute(f"""
        SELECT u.nombre_usuario, COUNT(e.id_examen), AVG(e.puntuacion)
        FROM Usuarios u
        JOIN Examenes e ON u.id_usuario = e.id_usuario
        WHERE e.tipo_examen = %s
        GROUP BY u.id_usuario
    """, (tipo,))
    
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos
