from simulador import obtener_preguntas_practica, obtener_opciones

import threading

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

puntuacion = 0

preguntas = obtener_preguntas_practica()

for i, pregunta in enumerate(preguntas, start=1):
    print(f"\n🧠 Pregunta {i}: {pregunta['pregunta']}")
    opciones = obtener_opciones(pregunta['id_pregunta'])
    
    for idx, opcion in enumerate(opciones, start=1):
        print(f"{idx}. {opcion['texto_opcion']}")

    try:
        seleccion = input_con_tiempo("Tu respuesta (1-3): ", timeout=60)

        if seleccion is None:
            raise TimeoutError

        seleccion = int(seleccion)
        if opciones[seleccion - 1]['es_correcta']:
            print("✅ ¡Correcto!")
            puntuacion += 5
        else:
            print("❌ Incorrecto.")
    except:
        print("⏰ Sin respuesta válida. Se marca como incorrecta.")


print(f"\n🧾 Resultado final: {puntuacion}/100")
if puntuacion >= 75:
    print("🎉 ¡Aprobado!")
else:
    print("📕 No aprobado.")

from login import verificar_login
from simulador import guardar_intento

# Obtener login primero
usuario = input("Usuario: ")
contrasena = input("Contraseña: ")
login_exitoso, id_usuario = verificar_login(usuario, contrasena)

if not login_exitoso:
    print("❌ Usuario inválido.")
    exit()

# Resto del simulador (preguntas, respuestas, puntuación)...

# Al final
guardar_intento(id_usuario, "practica", puntuacion)
