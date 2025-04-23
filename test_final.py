from simulador import (
    obtener_preguntas_final,
    obtener_opciones,
    guardar_intento,
    obtener_intentos_final,
    guardar_respuesta,
    mostrar_respuestas_por_examen,
    mostrar_historial_usuario
)

from login import verificar_login
from threading import Thread
import threading

# Función con temporizador
def input_con_tiempo(prompt, timeout=60):
    respuesta = [None]

    def preguntar():
        respuesta[0] = input(prompt)

    hilo = threading.Thread(target=preguntar)
    hilo.daemon = True
    hilo.start()
    hilo.join(timeout)

    if hilo.is_alive():
        print("\n⏰ ¡Tiempo agotado!")
        return None
    return respuesta[0]

# Login
usuario = input("Usuario: ")
contrasena = input("Contraseña: ")
login_exitoso, id_usuario = verificar_login(usuario, contrasena)

if not login_exitoso:
    print("❌ Usuario inválido.")
    exit()

# Verificar intentos
intentos = obtener_intentos_final(id_usuario)
if intentos >= 3:
    print("⚠️ Ya has alcanzado los 3 intentos del simulador final.")
    exit()

# Simulador Final
puntuacion = 0
preguntas = obtener_preguntas_final()
respuestas_guardadas = []

for i, pregunta in enumerate(preguntas, start=1):
    print(f"\n🧠 Pregunta {i}: {pregunta['pregunta']}")
    opciones = obtener_opciones(pregunta['id_pregunta'])

    for idx, opcion in enumerate(opciones, start=1):
        print(f"{idx}. {opcion['texto_opcion']}")

    seleccion = input_con_tiempo("Tu respuesta (1-3): ", timeout=60)

    try:
        if seleccion is None:
            raise TimeoutError

        seleccion = int(seleccion)
        correcta = opciones[seleccion - 1]['es_correcta']
        if correcta:
            print("✅ ¡Correcto!")
            puntuacion += 2.5
        else:
            print("❌ Incorrecto.")

        respuestas_guardadas.append((pregunta['id_pregunta'], opciones[seleccion - 1]['id_opcion'], correcta))

    except:
        print("⏰ Sin respuesta válida. Se marca como incorrecta.")
        respuestas_guardadas.append((pregunta['id_pregunta'], 0, 0))  # 0 = sin seleccionar


print(f"\n🧾 Resultado final: {puntuacion}/100")
if puntuacion >= 75:
    print("🎉 ¡Aprobado!")
else:
    print("📕 No aprobado.")

id_examen = guardar_intento(id_usuario, "final", puntuacion)

for id_pregunta, id_opcion, correcta in respuestas_guardadas:
    guardar_respuesta(id_examen, id_pregunta, id_opcion, correcta)

mostrar_respuestas_por_examen(id_examen)
mostrar_historial_usuario(id_usuario)
op = input("¿Deseas ver las respuestas de alguno de tus exámenes? (s/n): ")
if op.lower() == "s":
    examen_id = int(input("Introduce el ID del examen: "))
    mostrar_respuestas_por_examen(examen_id)
