import os
from PIL import Image

# Ruta de la carpeta donde están las imágenes
ruta_carpeta = 'imagenes'

# IDs para cada tipo
ids_practica = [
    1, 5, 7, 9, 13, 14, 15, 18, 24, 25, 28, 31, 36, 38, 39, 43, 45, 46, 47, 50,
    51, 52, 53, 60, 61, 62, 63, 66, 67, 68, 69, 72, 74, 75, 77
]

ids_final = [
    161, 165, 167, 169, 173, 174, 175, 178, 184, 185, 188, 191, 196, 198, 199,
    203, 205, 206, 207, 210, 211, 212, 213, 220, 221, 222, 223, 226, 227, 228,
    229, 232, 234, 235, 237
]

# Separar imágenes
imagenes = sorted([
    f for f in os.listdir(ruta_carpeta)
    if f.lower().endswith((".jpg", ".jpeg"))
])

imagenes_practica = [f for f in imagenes if "copia" not in f.lower()]
imagenes_final = [f for f in imagenes if "copia" in f.lower()]

# Validación
if len(imagenes_practica) < len(ids_practica):
    print(f"⚠️ Faltan imágenes de práctica: tienes {len(imagenes_practica)} y se necesitan {len(ids_practica)}")

if len(imagenes_final) < len(ids_final):
    print(f"⚠️ Faltan imágenes de final: tienes {len(imagenes_final)} y se necesitan {len(ids_final)}")

# Función para convertir y renombrar
def convertir_y_renombrar(lista_imagenes, ids):
    for archivo, id_pregunta in zip(lista_imagenes, ids):
        ruta_original = os.path.join(ruta_carpeta, archivo)
        nuevo_nombre = f'imagen{id_pregunta}.png'
        ruta_nueva = os.path.join(ruta_carpeta, nuevo_nombre)

        # Borrar si ya existe una imagen PNG con ese nombre
        if os.path.exists(ruta_nueva):
            os.remove(ruta_nueva)
            print(f"🗑️ Eliminada imagen existente: {nuevo_nombre}")

        try:
            # Abrir, convertir a PNG y guardar
            img = Image.open(ruta_original).convert("RGB")
            img.save(ruta_nueva, "PNG")
            print(f"✅ {archivo} → {nuevo_nombre}")
        except Exception as e:
            print(f"❌ Error con {archivo}: {e}")

        # Eliminar el archivo original JPG
        os.remove(ruta_original)

# Ejecutar
print("🔄 Renombrando imágenes de práctica...")
convertir_y_renombrar(imagenes_practica, ids_practica)

print("🔄 Renombrando imágenes del examen final...")
convertir_y_renombrar(imagenes_final, ids_final)

print("\n✅ Proceso completado.")
