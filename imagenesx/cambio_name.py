import os
from PIL import Image

# Ruta de la carpeta con las imágenes
ruta_carpeta = 'imagenes'

# IDs de preguntas que deben tener imagen
ids_con_imagen = [
    1, 5, 7, 9, 13, 14, 15, 18, 24, 25, 28, 31, 36, 38, 39, 43, 45, 46, 47, 50, 51, 52, 53,
    60, 61, 62, 63, 66, 67, 68, 69, 72, 74, 75, 77,
    161, 165, 167, 169, 173, 174, 175, 178, 184, 185, 188, 191, 196, 198, 199, 203, 205, 206, 207,
    210, 211, 212, 213, 220, 221, 222, 223, 226, 227, 228, 229, 232, 234, 235, 237
]

# Buscar archivos .jpg o .jpeg
archivos_jpg = sorted([
    f for f in os.listdir(ruta_carpeta)
    if f.lower().endswith(('.jpg', '.jpeg')) and 'copia' in f.lower()
])

# Validación
if len(archivos_jpg) != len(ids_con_imagen):
    print(f"⚠️ Hay {len(archivos_jpg)} imágenes JPG pero {len(ids_con_imagen)} IDs a renombrar.")
    if len(archivos_jpg) < len(ids_con_imagen):
        print("🔴 Faltan imágenes para cubrir todos los IDs. No se puede continuar.")
        exit()

# Conversión y renombrado
for archivo, id_pregunta in zip(archivos_jpg, ids_con_imagen):
    ruta_jpg = os.path.join(ruta_carpeta, archivo)
    nuevo_nombre = f'imagen{id_pregunta}.png'
    ruta_png = os.path.join(ruta_carpeta, nuevo_nombre)

    try:
        # Borrar si ya existe una imagen con el mismo nombre
        if os.path.exists(ruta_png):
            os.remove(ruta_png)

        with Image.open(ruta_jpg) as img:
            img = img.convert("RGB")
            img.save(ruta_png, "PNG")
        os.remove(ruta_jpg)  # Eliminar el original .jpg
        print(f"✅ Convertido y renombrado: {archivo} → {nuevo_nombre}")
    except Exception as e:
        print(f"❌ Error con {archivo}: {e}")
