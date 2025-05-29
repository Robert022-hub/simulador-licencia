with open("actualizar_imagenes.sql", "w") as f:
    for i in range(161, 241):
        ruta = f"C:/Users/Roberto Yeshua/OneDrive/Escritorio/PROYECTO-TINOCO-SIMULACION/imagenes/imagen{i}.png"
        f.write(f"UPDATE preguntas SET imagen = '{ruta}' WHERE id_pregunta = {i};\n")
