import os
import mysql.connector
from icrawler.builtin import GoogleImageCrawler
from PIL import Image

# ========== CONFIGURACIÓN ==========
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",  # <-- Cambia esto por la real
    "database": "simulador_examen"
}

carpeta_temp = "imagenes_temporales"
carpeta_final = "imagenes_preguntas"

os.makedirs(carpeta_temp, exist_ok=True)
os.makedirs(carpeta_final, exist_ok=True)

# ========== CONEXIÓN A LA BASE ==========
conexion = mysql.connector.connect(**db_config)
cursor = conexion.cursor()
cursor.execute("SELECT id_pregunta, pregunta FROM preguntas WHERE imagen IS NULL")
preguntas = cursor.fetchall()

# ========== CONTADORES ==========
descargadas = 0
no_encontradas = 0
errores = 0

# ========== CONFIGURAR CRAWLER ==========
crawler = GoogleImageCrawler(storage={"root_dir": carpeta_temp})

# ========== PROCESAR PREGUNTAS ==========
for id_pregunta, texto_pregunta in preguntas:
    print(f"\n🔍 Pregunta {id_pregunta}: {texto_pregunta[:60]}...")

    try:
        # Buscar imagen
        crawler.crawl(keyword=texto_pregunta, max_num=1, file_idx_offset=0)
        archivos = os.listdir(carpeta_temp)

        if not archivos:
            print(f"⚠️  No se encontró imagen para la pregunta {id_pregunta}")
            no_encontradas += 1
            continue

        # Abrir imagen descargada
        ruta_origen = os.path.join(carpeta_temp, archivos[0])
        imagen = Image.open(ruta_origen)

        # Convertir a PNG, 400x400 px y en escala de grises
        imagen = imagen.resize((400, 400))
        imagen = imagen.convert("L")

        nombre_final = f"pregunta{id_pregunta}.png"
        ruta_final = os.path.join(carpeta_final, nombre_final)
        imagen.save(ruta_final)

        # Guardar referencia en base de datos
        cursor.execute("UPDATE preguntas SET imagen = %s WHERE id_pregunta = %s", (nombre_final, id_pregunta))
        conexion.commit()

        descargadas += 1
        print(f"✅ Guardada como {nombre_final}")

    except Exception as e:
        print(f"❌ Error con la pregunta {id_pregunta}: {e}")
        errores += 1

    # Limpiar temporal
    for archivo in os.listdir(carpeta_temp):
        os.remove(os.path.join(carpeta_temp, archivo))

# ========== FINAL ==========
cursor.close()
conexion.close()

print("\n📊 RESUMEN FINAL:")
print(f"✅ Imágenes descargadas: {descargadas}")
print(f"⚠️ Sin resultados encontrados: {no_encontradas}")
print(f"❌ Errores al procesar: {errores}")
print("\n🟢 Proceso completo.")
