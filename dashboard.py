import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from io import BytesIO
from simulador import obtener_datos_dashboard_usuario

# Conexión y carga de datos
def obtener_dataframe():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simulador_examen"
    )
    query = """
    SELECT e.id_usuario, u.nombre_usuario, e.tipo_examen, e.fecha_realizacion, e.puntuacion, e.aprobado
    FROM examenes e
    JOIN usuarios u ON e.id_usuario = u.id_usuario
    """
    df = pd.read_sql(query, conexion)
    conexion.close()
    return df

# Promedio por tipo
def grafica_promedio_por_tipo(df):
    promedio = df.groupby("tipo_examen")["puntuacion"].mean()
    promedio.plot(kind="bar", color=["skyblue", "orange"], title="Promedio por tipo de examen")
    plt.ylabel("Puntuación promedio")
    plt.xlabel("Tipo de examen")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

# Aprobados vs No Aprobados
def grafica_aprobados_vs_no(df):
    conteo = df['aprobado'].value_counts()
    etiquetas = ['Aprobado', 'No aprobado']
    colores = ['lightgreen', 'salmon']
    conteo_lista = [conteo.get(1, 0), conteo.get(0, 0)]

    plt.pie(conteo_lista, labels=etiquetas, autopct='%1.1f%%', colors=colores, startangle=90)
    plt.title("Porcentaje de exámenes aprobados vs no aprobados")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Evolución de un usuario
def grafica_evolucion_usuario(df, nombre_usuario):
    df_usuario = df[df['nombre_usuario'] == nombre_usuario]

    if df_usuario.empty:
        print(f"⚠️ No hay registros para el usuario '{nombre_usuario}'")
        return

    df_usuario = df_usuario.sort_values(by='fecha_realizacion')
    plt.plot(df_usuario['fecha_realizacion'], df_usuario['puntuacion'], marker='o', linestyle='-')
    plt.title(f"Evolución de {nombre_usuario}")
    plt.xlabel("Fecha")
    plt.ylabel("Puntuación")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Menú principal
def menu_dashboard():
    df = obtener_dataframe()

    while True:
        print("\n===== DASHBOARD =====")
        print("1. Ver promedios por tipo de examen")
        print("2. Ver porcentaje de aprobados vs no aprobados")
        print("3. Ver evolución de un usuario")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            grafica_promedio_por_tipo(df)
        elif opcion == "2":
            grafica_aprobados_vs_no(df)
        elif opcion == "3":
            nombre = input("🔍 Escribe el nombre del usuario exactamente como está registrado: ")
            grafica_evolucion_usuario(df, nombre)
        elif opcion == "4":
            print("👋 Cerrando dashboard...")
            break
        else:
            print("❌ Opción inválida.")

def menu_dashboard():
    import matplotlib.pyplot as plt
    import pandas as pd
    import mysql.connector

    # Tu función obtener_dataframe y las gráficas ya están aquí...

    df = obtener_dataframe()
    while True:
        print("\n===== DASHBOARD =====")
        print("1. Ver promedios por tipo de examen")
        print("2. Ver porcentaje de aprobados vs no aprobados")
        print("3. Ver evolución de un usuario")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            grafica_promedio_por_tipo(df)
        elif opcion == "2":
            grafica_aprobados_vs_no(df)
        elif opcion == "3":
            nombre = input("🔍 Nombre del usuario: ")
            grafica_evolucion_usuario(df, nombre)
        elif opcion == "4":
            print("👋 Cerrando dashboard...")
            break
        else:
            print("❌ Opción inválida.")

def abrir_dashboard_personal(id_usuario):
    datos = obtener_datos_dashboard_usuario(id_usuario)  # Debe devolver tipo, total, total_puntos

    # Preparar datos
    tipos = [d["tipo"].capitalize() for d in datos]
    promedios = [d["total_puntos"] / d["total"] for d in datos]

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(tipos, promedios, color=["#3498db", "#e67e22"])
    ax.set_title("Promedio de Puntuación por Tipo de Examen")
    ax.set_ylabel("Puntuación Promedio / 100")
    for bar, avg in zip(bars, promedios):
        ax.annotate(f'{avg:.1f}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    ventana = tk.Toplevel()
    ventana.title("📊 Dashboard Personal")
    ventana.config(bg="#ecf0f1")
    ventana.geometry("600x500")

    img = Image.open(buf)
    img_tk = ImageTk.PhotoImage(img)

    tk.Label(ventana, image=img_tk, bg="#ecf0f1").pack(pady=10)
    ventana.mainloop()

# Arranque
if __name__ == "__main__":
    menu_dashboard()
