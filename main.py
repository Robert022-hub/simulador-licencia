import tkinter as tk
import os
from tkinter import messagebox
import mysql.connector
from simulador import obtener_historial_texto, obtener_preguntas_practica, obtener_opciones, obtener_intentos_final, guardar_intento, guardar_respuesta, registrar_usuario, obtener_preguntas_final, obtener_datos_dashboard_usuario
from dashboard import menu_dashboard, abrir_dashboard_personal
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk

# Función de verificación de login
def verificar_login(usuario, contraseña):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
    cursor.execute(query, (usuario, contraseña))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado["id_usuario"] if resultado else None

# Función al hacer clic en Iniciar Sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    id_usuario = verificar_login(usuario, contrasena)

    if id_usuario:
        messagebox.showinfo("Acceso permitido", f"¡Bienvenido, {usuario}!")
        root.destroy()
        abrir_menu_principal(id_usuario, usuario)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Menú principal
def abrir_menu_principal(id_usuario, nombre):
    ventana = tk.Tk()
    ventana.title("Menú Principal")
    ventana.geometry("350x350")

    label = tk.Label(ventana, text=f"Bienvenido, {nombre}", font=("Arial", 14))
    label.pack(pady=15)

    from simulador import obtener_preguntas_practica, obtener_opciones

    def cerrar_sesion():
        ventana.destroy()

    def abrir_simulador_practica():
        from PIL import Image, ImageTk

        contador_var = tk.StringVar()
        tiempo_var = tk.StringVar()
        tiempo_restante = [60]
        tiempo_var.set("⏱️ Tiempo: 60s")
        respuestas_guardadas = []

        sim = tk.Toplevel()
        sim.title("Simulador de Práctica")
        sim.geometry("600x600")
        sim.config(bg="#ecf0f1")

        preguntas = obtener_preguntas_practica()
        indice = {"actual": 0}
        puntuacion = {"total": 0}

        pregunta_var = tk.StringVar()
        resultado_var = tk.StringVar()
        botones_opciones = []

        label_imagen = tk.Label(sim)
        label_imagen.pack(pady=10)
        # UI
        tk.Label(sim, textvariable=tiempo_var, font=("Arial", 10, "bold"), bg="#ecf0f1", fg="#e74c3c").pack()
        tk.Label(sim, textvariable=contador_var, font=("Arial", 11, "italic"), bg="#ecf0f1", fg="#7f8c8d").pack(pady=(10, 0))
        tk.Label(sim, textvariable=pregunta_var, wraplength=450, font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

        frame_opciones = tk.LabelFrame(sim, text="Opciones", bg="#ecf0f1", fg="#34495e", font=("Arial", 12, "bold"))
        frame_opciones.pack(pady=10, fill="both", expand=True)

        tk.Button(sim, text="↩️ Volver al menú", command=sim.destroy, bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        for _ in range(4):
            btn = tk.Button(frame_opciones, text="", width=50, bg="#3498db", fg="white", font=("Arial", 10, "bold"), relief="raised")
            btn.pack(pady=5)
            botones_opciones.append(btn)

        tk.Label(sim, textvariable=resultado_var, font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#27ae60").pack(pady=15)

        def actualizar_imagen(nombre_archivo):
            try:
                ruta = os.path.join("imagenes", nombre_archivo)
                img = Image.open(ruta)
                img = img.resize((300, 180))
                img_tk = ImageTk.PhotoImage(img)
                label_imagen.configure(image=img_tk)
                label_imagen.image = img_tk
            except:
                label_imagen.config(image='')
                label_imagen.image = None

        def cargar_pregunta():
            resultado_var.set("")
            if hasattr(sim, "after_id"):
                sim.after_cancel(sim.after_id)

            tiempo_restante[0] = 60
            tiempo_var.set("⏱️ Tiempo: 60s")
            sim.after_id = sim.after(1000, actualizar_tiempo)

            if indice["actual"] < len(preguntas):
                pregunta = preguntas[indice["actual"]]
                opciones = obtener_opciones(pregunta["id_pregunta"])
                contador_var.set(f"📍 Pregunta {indice['actual'] + 1} de {len(preguntas)}")
                pregunta_var.set(f" {pregunta['pregunta']}")

                if pregunta.get("imagen") and os.path.exists(os.path.join("imagenes", pregunta["imagen"])):
                    actualizar_imagen(pregunta["imagen"])
                else:
                    label_imagen.config(image='')
                    label_imagen.image = None


                for i, boton in enumerate(botones_opciones):
                    if i < len(opciones):
                        texto = opciones[i]["texto_opcion"]
                        correcta = opciones[i]["es_correcta"]
                        boton.config(text=texto)
                        boton.correcta = correcta
                        boton.id_opcion = opciones[i]["id_opcion"]
                        boton.id_pregunta = pregunta["id_pregunta"]
                        boton.config(state="normal")
                    else:
                        boton.config(text="", state="disabled")
            else:
                simular_terminado()

        def responder(boton):
            if hasattr(sim, "after_id"):
                sim.after_cancel(sim.after_id)

            correcta = boton.correcta
            if correcta:
                resultado_var.set("✅ ¡Correcto!")
                puntuacion["total"] += 5
            else:
                resultado_var.set("❌ Incorrecto.")
            respuestas_guardadas.append((boton.id_pregunta, boton.id_opcion, int(correcta)))

            for b in botones_opciones:
                b.config(state="disabled")
            indice["actual"] += 1
            sim.after(1500, cargar_pregunta)

        def tiempo_agotado():
            resultado_var.set("⏰ Tiempo agotado. Respuesta incorrecta.")
            pregunta = preguntas[indice["actual"]]
            respuestas_guardadas.append((pregunta["id_pregunta"], 0, 0))
            indice["actual"] += 1
            for b in botones_opciones:
                b.config(state="disabled")
            sim.after(2000, cargar_pregunta)

        def actualizar_tiempo():
            tiempo_restante[0] -= 1
            tiempo_var.set(f"⏱️ Tiempo: {tiempo_restante[0]}s")
            if tiempo_restante[0] <= 0:
                tiempo_agotado()
            else:
                sim.after_id = sim.after(1000, actualizar_tiempo)

        def simular_terminado():
            pregunta_var.set("✅ Simulador completado.")
            resultado_var.set(f"Tu puntuación: {puntuacion['total']}/100")
            for b in botones_opciones:
                b.config(state="disabled")

            id_examen = guardar_intento(id_usuario, "práctica", puntuacion["total"])
            for id_preg, id_opc, correct in respuestas_guardadas:
                guardar_respuesta(id_examen, id_preg, id_opc, correct)

        for boton in botones_opciones:
            boton.config(command=lambda b=boton: responder(b))

        cargar_pregunta()

        
    def abrir_simulador_final():

        intentos = obtener_intentos_final(id_usuario)
        if intentos >= 3:
            messagebox.showwarning("Intentos agotados", "⚠️ Ya has realizado los 3 intentos del examen final.")
            return

        sim = tk.Toplevel()
        sim.title("Simulador Final")
        sim.geometry("600x600")
        sim.config(bg="#ecf0f1")

        contador_var = tk.StringVar()
        tiempo_var = tk.StringVar()
        tiempo_var.set("⏱️ Tiempo: 60s")
        tiempo_restante = [60]

        preguntas = obtener_preguntas_final()
        indice = {"actual": 0}
        puntuacion = {"total": 0}
        respuestas_guardadas = []

        pregunta_var = tk.StringVar()
        resultado_var = tk.StringVar()
        botones_opciones = []

        def actualizar_imagen(nombre_archivo):
            try:
                ruta = os.path.join("imagenes", nombre_archivo)
                img = Image.open(ruta)
                img = img.resize((300, 180))
                img_tk = ImageTk.PhotoImage(img)
                label_imagen.configure(image=img_tk)
                label_imagen.image = img_tk
            except:
                label_imagen.config(image='')
                label_imagen.image = None

        def actualizar_tiempo():
            tiempo_restante[0] -= 1
            tiempo_var.set(f"⏱️ Tiempo: {tiempo_restante[0]}s")
            if tiempo_restante[0] <= 0:
                tiempo_agotado()
            else:
                sim.after_id = sim.after(1000, actualizar_tiempo)

        def tiempo_agotado():
            resultado_var.set("⏰ Tiempo agotado. Respuesta incorrecta.")
            pregunta = preguntas[indice["actual"]]
            respuestas_guardadas.append((pregunta["id_pregunta"], 0, 0))
            indice["actual"] += 1
            for b in botones_opciones:
                b.config(state="disabled")
            sim.after(2000, cargar_pregunta)

        def cargar_pregunta():
            resultado_var.set("")
            if hasattr(sim, "after_id"):
                sim.after_cancel(sim.after_id)

            tiempo_restante[0] = 60
            tiempo_var.set("⏱️ Tiempo: 60s")
            sim.after_id = sim.after(1000, actualizar_tiempo)

            if indice["actual"] < len(preguntas):
                pregunta = preguntas[indice["actual"]]
                opciones = obtener_opciones(pregunta["id_pregunta"])

                contador_var.set(f"📍 Pregunta {indice['actual'] + 1} de {len(preguntas)}")
                pregunta_var.set(f" {pregunta['pregunta']}")

                if pregunta.get("imagen") and os.path.exists(os.path.join("imagenes", pregunta["imagen"])):
                    actualizar_imagen(pregunta["imagen"])
                else:
                    label_imagen.config(image='')
                    label_imagen.image = None


                for i, boton in enumerate(botones_opciones):
                    if i < len(opciones):
                        texto = opciones[i]["texto_opcion"]
                        correcta = opciones[i]["es_correcta"]
                        boton.config(text=texto, state="normal")
                        boton.correcta = correcta
                        boton.id_opcion = opciones[i]["id_opcion"]
                        boton.id_pregunta = pregunta["id_pregunta"]
                    else:
                        boton.config(text="", state="disabled")
            else:
                simular_terminado()

        def responder(boton):
            if hasattr(sim, "after_id"):
                sim.after_cancel(sim.after_id)

            correcta = boton.correcta
            if correcta:
                resultado_var.set("✅ ¡Correcto!")
                puntuacion["total"] += 2.5
            else:
                resultado_var.set("❌ Incorrecto.")

            respuestas_guardadas.append((boton.id_pregunta, boton.id_opcion, int(correcta)))

            for b in botones_opciones:
                b.config(state="disabled")
            indice["actual"] += 1
            sim.after(1500, cargar_pregunta)

        def simular_terminado():
            pregunta_var.set("📘 Examen final terminado.")
            resultado_var.set(f"Tu puntuación: {puntuacion['total']}/100")
            for b in botones_opciones:
                b.config(state="disabled")

            id_examen = guardar_intento(id_usuario, "final", puntuacion["total"])
            for id_preg, id_opc, correct in respuestas_guardadas:
                guardar_respuesta(id_examen, id_preg, id_opc, correct)

            aprobado = "🎉 ¡Aprobado!" if puntuacion["total"] >= 75 else "📕 No aprobado."
            messagebox.showinfo("Resultado Final", f"{aprobado}\nPuntuación: {puntuacion['total']}/100")

        # UI
        tk.Label(sim, textvariable=tiempo_var, font=("Arial", 10, "bold"), bg="#ecf0f1", fg="#e74c3c").pack()
        tk.Label(sim, textvariable=contador_var, font=("Arial", 10, "italic")).pack(pady=(10, 0))

        label_imagen = tk.Label(sim)
        label_imagen.pack(pady=10)

        tk.Label(sim, textvariable=pregunta_var, wraplength=450, font=("Arial", 12)).pack(pady=10)

        frame_opciones = tk.LabelFrame(sim, text="Opciones", bg="#ecf0f1", fg="#34495e", font=("Arial", 12, "bold"))
        frame_opciones.pack(pady=10, fill="both", expand=True)

        for _ in range(4):
            btn = tk.Button(frame_opciones, text="", width=50, bg="#3498db", fg="white", font=("Arial", 10, "bold"), relief="raised")
            btn.pack(pady=5)
            botones_opciones.append(btn)

        def crear_callback(b):
            return lambda: responder(b)

        for boton in botones_opciones:
            boton.config(command=crear_callback(boton))

        tk.Label(sim, textvariable=resultado_var, font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#27ae60").pack(pady=15)
        tk.Button(sim, text="↩️ Volver al menú", command=sim.destroy, bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        cargar_pregunta()


    def ver_historial():
        historial = obtener_historial_texto(id_usuario)
        messagebox.showinfo("📚 Historial", historial)

    def ver_dashboard():
        selector = tk.Toplevel()
        selector.title("📊 Selección de estadísticas")
        selector.geometry("300x200")

        tk.Label(selector, text="¿Qué estadísticas quieres ver?", font=("Arial", 12, "bold")).pack(pady=20)

        tk.Button(selector, text="🧪 Estadísticas de Práctica", width=30,
                  command=lambda: [selector.destroy(), mostrar_dashboard("práctica")]).pack(pady=10)

        tk.Button(selector, text="📘 Estadísticas del Examen Final", width=30,
                command=lambda: [selector.destroy(), mostrar_dashboard("final")]).pack(pady=5)



    # Botones del menú
    tk.Button(ventana, text="🧪 Simulador de Práctica", width=25, command=abrir_simulador_practica).pack(pady=5)
    tk.Button(ventana, text="📘 Simulador Final", width=25, command=abrir_simulador_final).pack(pady=5)
    tk.Button(ventana, text="📚 Ver Historial", width=25, command=ver_historial).pack(pady=5)
    tk.Button(ventana, text="📊 Dashboard Personal", width=25, command=lambda: abrir_dashboard_personal(id_usuario)).pack(pady=5)
    tk.Button(ventana, text="🌀 Cerrar sesión", width=25, command=cerrar_sesion).pack(pady=5)
    tk.Button(ventana, text="🚪 Salir", width=25, command=ventana.destroy).pack(pady=20)

    ventana.mainloop()

def abrir_ventana_registro():
    reg = tk.Toplevel()
    reg.title("Registro de Usuario")
    reg.geometry("300x250")

    tk.Label(reg, text="Nuevo usuario:").pack(pady=5)
    entry_nuevo = tk.Entry(reg)
    entry_nuevo.pack()

    tk.Label(reg, text="Contraseña:").pack(pady=5)
    entry_pass1 = tk.Entry(reg, show="*")
    entry_pass1.pack()

    tk.Label(reg, text="Confirmar contraseña:").pack(pady=5)
    entry_pass2 = tk.Entry(reg, show="*")
    entry_pass2.pack()

    def registrar():
        user = entry_nuevo.get()
        p1 = entry_pass1.get()
        p2 = entry_pass2.get()

        if not user or not p1 or not p2:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
            return
        if p1 != p2:
            messagebox.showerror("Contraseña", "Las contraseñas no coinciden.")
            return

        exito, mensaje = registrar_usuario(user, p1)
        if exito:
            messagebox.showinfo("Registro", mensaje)
            reg.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(reg, text="Registrarse", command=registrar).pack(pady=15)

def mostrar_dashboard(tipo):
    datos = obtener_datos_dashboard_usuario(tipo)
    if not datos:
        messagebox.showinfo("Sin datos", "No hay datos disponibles para este tipo de examen.")
        return

    titulo = "🧪 Resultados de Práctica" if tipo == "práctica" else "📘 Resultados del Final"
    color_titulo = "#007bff" if tipo == "final" else "#28a745"

    ventana = tk.Toplevel()
    ventana.title(f"Dashboard: {titulo}")
    ventana.geometry("850x600")

    tk.Label(ventana, text=titulo, font=("Arial", 14, "bold"), fg=color_titulo).pack(pady=10)

    columnas = ("Usuario", "Exámenes", "Promedio")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings", height=8)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=200)

    aprobados = 0
    reprobados = 0
    for usuario, cantidad, promedio in datos:
        tag = "verde" if promedio >= 75 else "rojo"
        tree.insert("", "end", values=(usuario, cantidad, round(promedio, 2)), tags=(tag,))
        if promedio >= 75:
            aprobados += 1
        else:
            reprobados += 1

    tree.tag_configure("verde", background="#d4edda")
    tree.tag_configure("rojo", background="#f8d7da")
    tree.pack(pady=5)

    # Agrega barra
    usuarios = [fila[0] for fila in datos]
    promedios = [fila[2] for fila in datos]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(usuarios, promedios, color=["green" if p >= 75 else "red" for p in promedios])
    ax.set_title(f"Promedios por Usuario ({tipo})")
    ax.set_ylabel("Promedio")
    ax.set_ylim(0, 100)
    ax.set_xticks(range(len(usuarios)))
    ax.set_xticklabels(usuarios, rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    # Mostrar total de aprobados/reprobados
    resumen = f"✅ Aprobados: {aprobados}   ❌ Reprobados: {reprobados}"
    tk.Label(ventana, text=resumen, font=("Arial", 11)).pack(pady=5)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

# Interfaz de Login
root = tk.Tk()
root.title("Simulador de Examen - Login")
root.geometry("300x200")

tk.Label(root, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Contraseña:").pack(pady=5)
entry_contrasena = tk.Entry(root, show="*")
entry_contrasena.pack()

tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=20)

tk.Button(root, text="Registrarse", command=abrir_ventana_registro).pack(pady=5)

root.mainloop()
