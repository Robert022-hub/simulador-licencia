import mysql.connector

# Palabras clave indicadoras de contenido visual
palabras_clave = [
    "señal", "línea", "zona escolar", "peatón", "cruce", "camión", 
    "flecha", "alto", "continua", "discontinua", "visual", "luz", "luminosa",
    "rebasar", "intersección", "curva", "pista", "tránsito"
]

# Función para obtener preguntas por tipo
def obtener_preguntas(tipo):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_pregunta, pregunta FROM preguntas WHERE tipo = %s", (tipo,))
    preguntas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return preguntas

# Revisión por tipo
for tipo in ["práctica", "final"]:
    print(f"\n🔎 Preguntas del examen {tipo.upper()} que probablemente requieren imagen:\n")

    preguntas = obtener_preguntas(tipo)
    for p in preguntas:
        texto = p["pregunta"].lower()
        if any(palabra in texto for palabra in palabras_clave):
            print(f"✅ ({p['id_pregunta']}) {p['pregunta']}")

print("\n🎯 Revisión completa. Estas preguntas son candidatas ideales para tener imágenes asociadas.")
