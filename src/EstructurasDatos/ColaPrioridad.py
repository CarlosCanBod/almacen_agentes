from typing import Any


# Cada elemento/nodo de la lista enlazada
# tiene un dato, el nodo siguiente y una prioridad
# Cuando se introduzca en una cola de prioridad
# se va a introducir el que mas prioridad tenga adelante
class NodoColaPrioridad:
    def __init__(self, dato=0, prioridad=1):
        self.dato: Any = dato
        self.siguiente = None
        self.prioridad = prioridad  # Se considera que cuanto mas alto mas importante :)

    # Se crea este metodo para poder imprimir un nodo indivudual
    def __str__(self):
        cadena = "(" + str(self.dato) + "," + str(self.prioridad) + ")" + " "
        return cadena

    def __eq__(self, otro: object) -> bool:
        return hash(self) == hash(otro)

    def __hash__(self) -> int:
        return hash((self.dato, self.prioridad))

    def __lt__(self, otro: "NodoColaPrioridad") -> bool:
        return self.prioridad < otro.prioridad


# Aqui se crea la cola de prioridad ordenada
# Los nodos/elementos se van a ordenar de menor a mayor prioridad
class ColaPrio:

    def __init__(self):
        self.cabeza = None

    def __str__(self):
        try:
            cadena = "Lista tiene: "
            nodo_aux = self.cabeza
            while nodo_aux is not None:
                cadena = cadena + "(" + str(nodo_aux.dato) + "," + str(nodo_aux.prioridad) + ")" + " "
                nodo_aux = nodo_aux.siguiente

            return cadena
        except Exception as e:
            print("error al convertir lista en string")
            print(e)
            return "Error imprimir cola prioridad"

    def __len__(self):
        if self.cabeza is not None:
            nodo_actual = self.cabeza
            tamano = 0
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
                tamano += 1

            tamano += 1
            return tamano
        else:
            return 0

    def valor_cabeza(self) -> Any:
        if self.cabeza is not None:
            return self.cabeza.prioridad
        else:
            return None

    # Introduce el elemento en la lista y su posicion depende de su prioridad
    # Cuanta mas prioridad mas a la derecha se va a colocar.
    def insertar(self, dato: Any, prioridad: int):
        try:
            # Si la cola esta vacia se introduce el nodo/elemento
            # al principio.
            if self.cabeza is None:
                self.cabeza = NodoColaPrioridad(dato, prioridad)

            # Si el elemento que se va a meter tiene menos prioridad
            # que el primero, el nuevo va a ser la nueva cabeza(el primero de la cola)
            elif self.cabeza.prioridad <= prioridad:
                nodo_nuevo = NodoColaPrioridad(dato, prioridad)

                nodo_nuevo.siguiente = self.cabeza  # type: ignore
                self.cabeza = nodo_nuevo

                # En este caso el elemento nuevo
            else:

                # el nodo auxiliar se crea como el primero,
                # para ir buscando uno a uno donde meter el nuevo
                # dependiendo de su prioridad, va a buscar el siguiente elemento
                # hasta que su prioridad sea igual o mayor
                nodo_actual = self.cabeza
                nodo_previo = None
                fin = False
                while (nodo_actual is not None) and not fin:
                    # Si el nodo actual tiene mas prioridad
                    # que el que se va a meter sale del bucle
                    if nodo_actual.prioridad <= prioridad:
                        fin = True
                    else:
                        nodo_previo = nodo_actual
                        nodo_actual = nodo_actual.siguiente

                # Cuando se encuentra donde meter el nuevo elemento
                # Se crea con los parametros que sean, y se asigna como a continuacion
                # el que esta despues del auxiliar, y se pone delante del auxiliar
                # el nuevo elemento, por lo que si hay empate el nuevo se queda atras
                nodo_nuevo = NodoColaPrioridad(dato, prioridad)
                nodo_nuevo.siguiente = nodo_actual  # type: ignore
                nodo_previo.siguiente = nodo_nuevo  # type: ignore

        except Exception as e:
            print("Error al introducir elemento en la lista")
            print("Error: ", e)

    def eliminar(self, dato: Any, prioridad: int, valor_cabeza: int, trozo: int) -> None:

        if self.cabeza is not None:
            nodo_actual = self.cabeza  # Se busca aqui el nodo a eliminar
            nodo_previo = None
            fin = False

            while (nodo_actual is not None) and not fin:
                if nodo_actual.dato == dato and nodo_actual.prioridad == prioridad:
                    fin = True
                else:  # Se va al siguiente nodo
                    nodo_previo = nodo_actual
                    nodo_actual = nodo_actual.siguiente

            if fin:
                if nodo_previo is not None:
                    nodo_previo.siguiente = nodo_actual.siguiente  # type: ignore
                    return None
                else:
                    # Si es el primero el que se borra
                    if nodo_actual is not None:
                        self.cabeza = nodo_actual.siguiente
                        return None

            print("ERROR NO ENCONTRADO DATO PARA ELIMINAR: ", hash(dato), prioridad, "TROZO: ", trozo,
                  "  Valor cabeza: ", valor_cabeza)
            return None
        return None

    # Si la cola esta vacia devuelve true
    def vacio(self):
        return self.cabeza is None

    # Borra el elemento mas a la derecha
    def pop(self):
        try:
            if self.cabeza is not None:
                nodo_actual = self.cabeza
                nodo_previo = None

                # Va hacia el elemento mas a la derecha para borrarlo
                while nodo_actual.siguiente is not None:
                    nodo_previo = nodo_actual
                    nodo_actual = nodo_actual.siguiente

                if nodo_previo is not None:
                    nodo_previo.siguiente = None

        except Exception as e:
            print("Error en pop lista prioridad")
            print(e)

    # Devuelve cual es el elemento con mas prioridad(mas a la derecha)
    # Pero no lo borra
    def primero(self):
        if self.cabeza is not None:
            nodo_actual = self.cabeza
            if nodo_actual.siguiente is not None:
                while nodo_actual.siguiente is not None:
                    nodo_actual = nodo_actual.siguiente

                return nodo_actual
            return None
        else:
            return None

    # Devuelve cual es el elemento mas a la izquierda
    # pero no lo borra
    def ultimo(self):
        return self.cabeza

    # Devuelve el tamano de la cola
    # Recorriendo la cola y contando
    def tamano(self):

        if self.cabeza is not None:
            nodo_actual = self.cabeza
            tamano = 0
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
                tamano += 1

            tamano += 1
            return tamano
        else:
            return 0

    # Devuelve el elemento con mas prioridad y lo borra de la cola
    def extraer(self):
        if self.cabeza is not None:
            nodo_actual = self.cabeza
            nodo_previo = None
            if nodo_actual.siguiente is not None:
                while nodo_actual.siguiente is not None:
                    nodo_previo = nodo_actual
                    nodo_actual = nodo_actual.siguiente

                if nodo_previo is not None:
                    nodo_previo.siguiente = None  # Asi el nodo que se devuelve ya no tiene quien lo referencie
            else:
                # Si es el unico, no hay siguiente, se borra la cabeza.
                self.cabeza = None

            return nodo_actual
        else:
            return None


"""
Fin clases de cola prioridad

"""
