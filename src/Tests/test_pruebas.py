import unittest
from typing import Any
from random import randint

from EstructurasDatos.ColaPrioridad import NodoColaPrioridad, ColaPrio
from EstructurasDatos.Objetos import Palet, Estado
from Planificador import Busqueda, girar, levantar_bajar


class TestColaPrio(unittest.TestCase):

    def test_hola(self):
        cola = ColaPrio()
        cola.insertar(20, 2)

        nodo: NodoColaPrioridad = cola.extraer()
        self.assertIsNotNone(nodo)
        self.assertEqual(nodo.dato, 20)
        self.assertIsNone(cola.extraer())

    def test_insertar_mucho(self):
        cola = ColaPrio()
        tamano: int = 100

        for i in range(tamano):
            cola.insertar(randint(0, 50), randint(0, 50))

        self.assertEqual(cola.tamano(), tamano)
        self.assertIsNotNone(cola.extraer())

    def test_insertar_extraer(self):
        cola = ColaPrio()
        cola.insertar(10, 2)
        cola.insertar(15, 2)
        cola.insertar(5, 1)
        cola.insertar(20, 4)

        tamano = cola.tamano()
        for i in range(1, tamano + 1):
            nodo: Any = cola.extraer()
            self.assertEqual(nodo.dato, 5 * i)


# noinspection bad-assignment
class TestBusqueda(unittest.TestCase):

    def test_expansion(self):
        lista_palets = [Palet(2, 2, False, 1, 1, False)]

        estado_inicial = Estado(0, 0, "S", False, lista_palets)

        entorno = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        buscador = Busqueda(estado_inicial, entorno)

        estado_nuevo: Any = buscador.avanzar(estado_inicial)

        self.assertIsNotNone(estado_nuevo)
        # Avanzar hacia abajo
        self.assertEqual(1, estado_nuevo.Robot_x)
        self.assertEqual(0, estado_nuevo.Robot_y)

    def test_girar(self):
        lista_palets = [Palet(2, 2, False, 1, 1, False)]

        estado_inicial = Estado(0, 0, "S", False, lista_palets)

        entorno = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        estado_girado: Estado = girar(estado_inicial, entorno, izquierda=True)

        # Comprobacion girar 360 de forma legal, sin palet.
        self.assertEqual(estado_girado.Robot_orientacion, "E")
        estado_girado: Estado = girar(estado_girado, entorno, izquierda=True)
        self.assertEqual(estado_girado.Robot_orientacion, "N")
        estado_girado: Estado = girar(estado_girado, entorno, izquierda=True)
        self.assertEqual(estado_girado.Robot_orientacion, "O")
        estado_girado: Estado = girar(estado_girado, entorno, izquierda=True)
        self.assertEqual(estado_girado.Robot_orientacion, "S")

    def test_levantar(self):
        lista_palets = [Palet(2, 2, False, 1, 1, False)]

        estado_inicial = Estado(0, 0, "S", False, lista_palets)

        entorno = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        estado_nuevo = levantar_bajar(estado_inicial)


if __name__ == "__main__":
    unittest.main()
