import unittest
from simulador import (
    obtener_preguntas_practica,
    obtener_preguntas_final,
    obtener_intentos_final,
    obtener_opciones,
    guardar_intento,
    guardar_respuesta,
)
import mysql.connector


class TestSimulador(unittest.TestCase):
    def setUp(self):
        # ID ficticio para pruebas, asegúrate que existe un usuario con este ID
        self.id_usuario = 1

    def test_intentos_final_limit(self):
        """El usuario no debe poder hacer más de 3 intentos del simulador final"""
        intentos = obtener_intentos_final(self.id_usuario)
        self.assertLessEqual(intentos, 3, "El usuario excedió los 3 intentos permitidos")

    def test_preguntas_practica_cantidad(self):
        """El simulador de práctica debe tener exactamente 20 preguntas"""
        preguntas = obtener_preguntas_practica()
        self.assertEqual(len(preguntas), 20, "El simulador de práctica no tiene 20 preguntas")

    def test_preguntas_sin_repetir(self):
        """No deben repetirse preguntas en una misma simulación"""
        preguntas = obtener_preguntas_practica()
        ids = [p['id_pregunta'] for p in preguntas]
        self.assertEqual(len(ids), len(set(ids)), "Hay preguntas repetidas en la simulación")

    def test_aprobacion_porcentaje(self):
        """Si el usuario saca 75 o más, debe marcarse como aprobado"""
        puntuacion = 75
        id_examen = guardar_intento(self.id_usuario, "práctica", puntuacion)

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="simulador_examen"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT aprobado FROM examenes WHERE id_examen = %s", (id_examen,))
        resultado = cursor.fetchone()[0]
        conexion.close()

        self.assertTrue(resultado, "El examen debería marcarse como aprobado con 75 puntos")

    def test_tiempo_agotado_simulado(self):
        """Si se acaba el tiempo sin responder, debe marcarse como incorrecta"""

        preguntas = obtener_preguntas_practica()
        id_pregunta_valida = preguntas[0]['id_pregunta']

        opciones = obtener_opciones(id_pregunta_valida)
        id_opcion_valida = opciones[0]["id_opcion"]

        id_examen = guardar_intento(self.id_usuario, "práctica", 0)

        # Simulamos que no se contestó correctamente
        guardar_respuesta(id_examen, id_pregunta=id_pregunta_valida, id_opcion=id_opcion_valida, correcta=0)

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="simulador_examen"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT correcta FROM respuestas WHERE id_examen = %s AND id_pregunta = %s", (id_examen, id_pregunta_valida))
        resultado = cursor.fetchone()[0]
        conexion.close()

        self.assertEqual(resultado, 0, "La respuesta sin contestar debería registrarse como incorrecta")

if __name__ == '__main__':
    unittest.main()
