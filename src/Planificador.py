#!/usr/bin/env python
from time import time
from typing import Any

from EstructurasDatos.ColaPrioridad import ColaPrio
from EstructurasDatos.Objetos import Palet, Estado


class Busqueda:

    def __init__(self, estado_inicial: "Estado", entorno: "list[list]", pesos: "tuple[int,int,int]" = (5, 1, 2),
                 modo_djistra: bool = False) -> None:
        # Mapeo de orientaciones
        self.estado_final = None
        self.movimientos = {
            'N': (-1, 0),
            'S': (1, 0),
            'E': (0, 1),
            'O': (0, -1)
        }
        self.rotar_izquierda = {'N': 'O', 'O': 'S', 'S': 'E', 'E': 'N'}
        self.rotar_derecha = {'N': 'E', 'E': 'S', 'S': 'O', 'O': 'N'}

        self.estado_ini = estado_inicial
        self.estado_actual = estado_inicial

        self.peso1 = pesos[0]
        self.peso2 = pesos[1]
        self.peso3 = pesos[2]
        self.modo_djistra = modo_djistra

        self.filas = len(entorno)
        self.columnas = len(entorno[0])
        self.entorno = entorno

        self.coste_final: int = 0
        self.longitud_camino: int = 0
        self.tiempo_total: float = 0.0
        self.nodos_expandidos: int = 0
        self.lis_tiempo_ciclo: "list[float]" = []
        self.lis_memoria_ciclo: "list[float]" = []

        self.lis_cerrada: "dict[int,int]" = {}

        # Se va a usar para a la hora de insertar en lista abierta
        # mirar si esta en abierta, y si lo esta pues se hace la cosa lenta
        # de cambiarlo por el nuevo si es mas barato
        self.diccionario_estados_abierta: "dict[int,int]" = {}

        self.lis_abierta = ColaPrio()
        # Aqui se van a meter los nodos si su coste es mayor al de la cabeza de lista abierta,
        # a ver si hace que vaya mas rapido el codigo, ya que lo que hace que se vaya mas lento 
        # es meter nuevos estados en lista abierta cuando ya hay muchos.
        self.lis_abierta_lenta: ColaPrio = ColaPrio()
        self.lis_abierta_mas_lenta: ColaPrio = ColaPrio()

        self.lis_abierta.insertar(estado_inicial, prioridad=self.heuristica_total(estado_inicial))
        self.diccionario_estados_abierta.update({hash(estado_inicial): self.heuristica_total(estado_inicial)})

    def heuristica_robot_origen(self, robot_x, robot_y, robot_orientacion, rob_activado) -> int:
        coste = abs(self.estado_ini.Robot_x - robot_x) + abs(self.estado_ini.Robot_y - robot_y)

        if coste == 0:
            if robot_orientacion != self.estado_ini.Robot_orientacion:
                coste = coste + 1

            if rob_activado:
                coste = + 1

        return coste

    def heuristica_palets1(self, estado_comprobar: Estado) -> int:

        lista_palets: "list[Palet]" = estado_comprobar.Lista_estanterias

        coste = 0

        if lista_palets is not None:
            for palet in lista_palets:

                c1 = abs(palet.x_objetivo - palet.pos_x) + abs(palet.y_objetivo - palet.pos_y)

                if palet.ang_actual != palet.ang_objetivo:
                    c1 = c1 + 1

                coste = coste + self.peso1 * c1

        return coste

    @staticmethod
    def heur_robot_palet(estado_comprobar: Estado):

        coste = 0
        x1 = estado_comprobar.Robot_x
        y1 = estado_comprobar.Robot_y

        lista_palets: "list[Palet]" = estado_comprobar.Lista_estanterias

        for palet in lista_palets:

            if palet.necesita_moverse():
                x_palet = palet.pos_x
                y_palet = palet.pos_y
                dist = abs(x_palet - x1) + abs(y_palet - y1)

                coste = coste + dist

        return coste

    def heuristica_total(self, estado_comprobar: Estado) -> int:

        coste_palets_robot = 0

        coste_robot_origen = self.heuristica_robot_origen(estado_comprobar.Robot_x, estado_comprobar.Robot_y,
                                                          estado_comprobar.Robot_orientacion,
                                                          estado_comprobar.Robot_activado)
        coste_palets_objetivo = 0

        if len(estado_comprobar.Lista_estanterias):
            coste_palets_objetivo: int = (self.heuristica_palets1(estado_comprobar))

            # Que el robot quiera ir a por los palets que tienen que moverse
            if not self.modo_djistra:
                coste_palets_robot = self.heur_robot_palet(estado_comprobar)

        coste_total = coste_palets_objetivo + self.peso2 * coste_robot_origen + self.peso3 * coste_palets_robot

        if self.modo_djistra:
            if coste_total != 0:
                coste_total = 1

        return coste_total

    @staticmethod
    def levantar_bajar(estado: Estado) -> Any:
        """
        Tiene que estar debajo de un palet para poder usar esto,
        si no, no sube o baja.

        Va a invertir el estado que tenga.
        """

        cord_robot_x: int = estado.Robot_x
        cord_robot_y: int = estado.Robot_y
        robot_angulo: str = estado.Robot_orientacion
        rob_activado: bool = estado.Robot_activado
        lis_estanterias: "list[Palet]" = estado.Lista_estanterias.copy()

        for palet in lis_estanterias:
            if cord_robot_x == palet.pos_x and cord_robot_y == palet.pos_y:
                rob_activado = not rob_activado
                estado_nuevo: Estado = Estado(cord_robot_x, cord_robot_y, robot_angulo, rob_activado, lis_estanterias)
                return estado_nuevo

        # Si no ha encontrado un palet encima del robot, no se devuelve estado
        return None

    def girar(self, estado: Estado, izquierda: bool = True) -> Any:
        """
            Gira el robot a la izquierda
            Si no tiene palet no hay requisitos para girar

            Si lo hay, no puede haber obstaculos o palets alrededor del robot.
        
        """

        cord_robot_x: int = estado.Robot_x
        cord_robot_y: int = estado.Robot_y
        robot_angulo: str = estado.Robot_orientacion
        rob_activado: bool = estado.Robot_activado
        lis_estanterias_copia: "list[Palet]" = estado.Lista_estanterias.copy()

        if izquierda:
            robot_angulo = self.rotar_izquierda[robot_angulo]
        else:
            robot_angulo = self.rotar_derecha[robot_angulo]

        if not rob_activado:

            estado_nuevo: Estado = Estado(cord_robot_x, cord_robot_y, robot_angulo, rob_activado, lis_estanterias_copia)
            return estado_nuevo

        else:

            # Si lleva palet hay que hacer mas comprobaciones
            # Que no este cerca de algun obstaculo 
            # Los obstaculos tienen valor 9 en entorno, y paredes 1 por ejemplo
            # No pueden girar si tienen bloque, pero si pared cerca
            for ancho in range(-1, 2):
                for alto in range(-1, 2):
                    try:
                        if self.entorno[cord_robot_x + ancho][cord_robot_y + alto] == 9:
                            return None
                    except Exception as e:
                        print("ERROR GIRAR: ", e)
                        pass

            # Que no pueda girar en los bordes con palet
            if cord_robot_x == 0 or cord_robot_x == self.filas - 1:
                return None
            if cord_robot_y == 0 or cord_robot_y == self.columnas - 1:
                return None

            lista_palets_quietos: "list[Palet] " = []
            palet_girado = None

            for palet in lis_estanterias_copia:

                # Gira el palet si es el que esta en la posicion del robot
                if palet.pos_x == cord_robot_x and palet.pos_y == cord_robot_y:

                    pal_pos_x = palet.pos_x
                    pal_obj_x = palet.x_objetivo
                    pal_pos_y = palet.pos_y
                    pal_obj_y = palet.y_objetivo
                    pal_ang_act = not palet.ang_actual
                    pal_obj_ang = palet.ang_objetivo

                    palet_girado: Palet = Palet(pal_pos_x, pal_pos_y, pal_ang_act,
                                                pal_obj_x, pal_obj_y, pal_obj_ang)

                else:

                    # Si no es el palet que lleva
                    # Mira alrededor del otro palet, no se puede girar ahi.
                    for ancho in range(-1, 1):
                        for alto in range(-1, 1):
                            if cord_robot_x == palet.pos_x + ancho and cord_robot_y == palet.pos_y + alto:
                                return None
                    lista_palets_quietos.append(palet)

            if palet_girado is not None:
                lista_palets_quietos.append(palet_girado)

            estado_nuevo: Estado = Estado(cord_robot_x, cord_robot_y, robot_angulo, rob_activado, lista_palets_quietos)
            return estado_nuevo

    def avanzar(self, estado: Estado) -> Any:

        Rob_pos_x = estado.Robot_x
        Rob_pos_y = estado.Robot_y
        Rang = estado.Robot_orientacion
        R_levan = estado.Robot_activado

        # Mira a que posicion cambia el robot si avanza, mirando la orientacion
        dx, dy = self.movimientos[Rang]

        # nueva posicion del robot
        Rx_n = Rob_pos_x + dx
        Ry_n = Rob_pos_y + dy

        lista_palets_copia = estado.Lista_estanterias.copy()

        # Comprobar que robot puede moverse, si no devuelve None
        # Primero si sale fuera del entorno, y luego si en el entorno estatico la nueva posicion
        # esta ocupada por pared o obstaculo
        if 0 > Rx_n or Rx_n >= self.filas:
            return None
        if 0 > Ry_n or Ry_n >= self.columnas:
            return None
        if self.entorno[Rx_n][Ry_n]:  # En principio detecta obstaculo = 9 y paredes = 1
            return None

        # El robot no baja o sube el palet aqui, queda igual

        if not R_levan:
            # Comprobar que el robot no choca con patas de alguna estanteria
            for palet in lista_palets_copia:
                if palet.ang_actual == 1:  # Si el palet esta en vertical
                    # Al estar en vertical el robot no se puede mover 1 encima o debajo
                    # de la posicion del palet
                    if palet.pos_x == Rx_n and (palet.pos_y + 1 == Ry_n or palet.pos_y - 1 == Ry_n):
                        return None
                else:
                    # Si esta horizontal, el robot no se puede poner 1 casilla por los lados
                    # en eje X,
                    if palet.pos_y == Ry_n and (palet.pos_x + 1 == Rx_n or palet.pos_x - 1 == Rx_n):
                        return None

            lista_palets_nueva = lista_palets_copia

        # Si el robot está levantado tiene estanteria, por lo que  hay que hacer más comprobaciones.
        else:  # Si no lleva palet
            lleva_vertical: bool = False

            # Aqui se meten los palets que no se mueven, 
            # para despues no comparar el que se mueve consigo mismo
            lista_palets_quietos: "list[Palet] " = []
            Palet_movido = None

            # Buscar que palet es el que lleva el robot y mover su posicion a que este
            # encima del robot
            for palet in lista_palets_copia:
                if palet.pos_x == estado.Robot_x and palet.pos_y == estado.Robot_y:

                    Pal_pos_x = palet.pos_x
                    Pal_obj_x = palet.x_objetivo
                    Pal_pos_y = palet.pos_y
                    Pal_obj_y = palet.y_objetivo
                    Pal_ang_act = palet.ang_actual
                    Pal_obj_ang = palet.ang_objetivo

                    Palet_movido: Palet = Palet(Pal_pos_x, Pal_pos_y, Pal_ang_act,
                                                Pal_obj_x, Pal_obj_y, Pal_obj_ang)

                    Palet_movido.pos_x = Palet_movido.pos_x + dx
                    Palet_movido.pos_y = Palet_movido.pos_y + dy

                    if Palet_movido.ang_actual:  # Si es vertical el palet que lleva
                        lleva_vertical: bool = True
                    else:

                        lleva_vertical: bool = False

                else:
                    lista_palets_quietos.append(palet)

            # Con la nueva posicion del palet miramos si no choca con otro palet o obstaculo
            # Utilizo la posicion del robot, si el palet que lleva esta en vertical, hay que mirar arriba y abajo,
            # si es horizontal a la izquierda y derecha de el.
            if lleva_vertical:

                if Ry_n == 0 or Ry_n == self.filas - 1:
                    return None

                try:
                    if 0 > Rx_n >= self.filas or 0 > Ry_n + 1 >= self.columnas or self.entorno[Rx_n][Ry_n + 1] == 9:
                        return None
                    elif 0 > Rx_n >= self.filas or 0 > Ry_n - 1 >= self.columnas or self.entorno[Rx_n][Ry_n - 1] == 9:
                        return None
                except Exception as e:
                    print("Error avanzar ", e)
                    return None

                for palet in lista_palets_quietos:

                    # Que no se meta en otro palet
                    if Rx_n == palet.pos_x and Ry_n == palet.pos_y:
                        return None

                    if palet.ang_actual == 1:  # Si el otro palet esta en vertical

                        # Al estar en vertical el robot no se puede mover 1 encima o debajo
                        # de la posicion del palet
                        if palet.pos_x == Rx_n and (
                                palet.pos_y - 1 == Ry_n or palet.pos_y == Ry_n or palet.pos_y + 1 == Ry_n):
                            return None

                    else:
                        # Mira alrededor del otro palet, no se puede mover ahi.
                        for ancho in range(-1, 1):
                            for alto in range(-1, 1):
                                if Rx_n == palet.pos_x + ancho and Ry_n == palet.pos_y + alto:
                                    return None
            else:
                # Si lo lleva en horizontal

                if Rx_n == 0 or Rx_n == self.columnas - 1:
                    return None

                try:
                    if 0 > Rx_n + 1 > self.filas or 0 > Ry_n > self.columnas or self.entorno[Rx_n + 1][Ry_n] == 9:
                        return None
                    elif 0 > Rx_n - 1 > self.filas or 0 > Ry_n > self.columnas or self.entorno[Rx_n - 1][Ry_n] == 9:
                        return None
                except Exception as e:
                    print("Error avanzar 2: ", e)
                    return None

                for palet in lista_palets_quietos:

                    # Que no se meta en otro palet
                    if Rx_n == palet.pos_x and Ry_n == palet.pos_y:
                        return None

                    if palet.ang_actual == 0:  # Si el otro palet esta en horizontal

                        # Al estar en horizontal el robot no se puede mover 1 der o izquierda
                        # de la posicion del palet
                        if palet.pos_y == Ry_n and (
                                palet.pos_x - 1 == Rx_n or palet.pos_x == Rx_n or palet.pos_x + 1 == Rx_n):
                            return None

                    else:
                        # Mira alrededor del otro palet, no se puede mover ahi.
                        for ancho in range(-1, 1):
                            for alto in range(-1, 1):
                                if Rx_n == palet.pos_x + ancho and Ry_n == palet.pos_y + alto:
                                    return None

            lista_palets_nueva = lista_palets_quietos
            if Palet_movido is not None:
                lista_palets_nueva.append(Palet_movido)

        return Estado(Rx_n, Ry_n, Rang, R_levan, lista_palets=lista_palets_nueva)

    def insertar_en_abierta(self, estado_nuevo: Estado, coste_f_nuevo: int, valor_cabeza: int) -> None:

        # Buscar en lista cerrada
        hash_estado = hash(estado_nuevo)
        prioridad_vieja = self.lis_cerrada.get(hash_estado)

        # Si no esta en cerrada deberia devolver None
        if prioridad_vieja is not None:
            if coste_f_nuevo > prioridad_vieja:
                # Si ya existe el estado en cerrada, pero el nuevo
                # es peor o igual, no se añade en abierta porque hay un camino mejor
                # para llegar a ese estado.
                return None
            else:
                self.lis_cerrada.pop(hash_estado)  # Borrar de lista cerrada el estado viejo
                # para hacer dic mas pequeño, alomejor no se deberia hacer
                # porque hasta que no se meta el otro se podrian repetir estados

        coste_estado_en_abierta = self.diccionario_estados_abierta.get(hash_estado, None)
        # Supongo que da None si no esta en abierta

        if coste_estado_en_abierta is not None:
            # Si ya existe en abierta, mirar si el nuevo es mejor
            if coste_f_nuevo < coste_estado_en_abierta:
                # Si es mejor el nuevo estado, hay que buscar y sacar el viejo de abierta
                # y meter el nuevo
                self.diccionario_estados_abierta.pop(hash_estado)
                if valor_cabeza is not None and valor_cabeza >= coste_estado_en_abierta:
                    # Se busca en la lista donde deberia estar ese estado,prio
                    self.lis_abierta.eliminar(estado_nuevo, coste_estado_en_abierta, valor_cabeza, 0)
                else:
                    valor_cabeza_lenta = self.lis_abierta_lenta.valor_cabeza()
                    if valor_cabeza is not None and valor_cabeza_lenta >= coste_estado_en_abierta:
                        self.lis_abierta_lenta.eliminar(estado_nuevo, coste_estado_en_abierta, valor_cabeza_lenta, 1)
                    else:
                        self.lis_abierta_mas_lenta.eliminar(estado_nuevo, coste_estado_en_abierta, valor_cabeza_lenta,
                                                            2)
            else:
                return None

        self.diccionario_estados_abierta[hash_estado] = coste_f_nuevo

        if valor_cabeza is None or valor_cabeza >= coste_f_nuevo:
            self.lis_abierta.insertar(dato=estado_nuevo, prioridad=coste_f_nuevo)
        else:
            valor_cabeza_lenta = self.lis_abierta_lenta.valor_cabeza()
            if valor_cabeza_lenta is None or valor_cabeza_lenta >= coste_f_nuevo:
                self.lis_abierta_lenta.insertar(dato=estado_nuevo, prioridad=coste_f_nuevo)
            else:
                self.lis_abierta_mas_lenta.insertar(dato=estado_nuevo, prioridad=coste_f_nuevo)

        return None

    def actualizar_listas_abiertas(self):
        self.lis_abierta = self.lis_abierta_lenta
        self.lis_abierta_lenta = self.lis_abierta_mas_lenta
        self.lis_abierta_mas_lenta = ColaPrio()

    def expandir(self, estado_sacado, coste_g, valor_cabeza=9999) -> None:

        estado_avance: Estado = self.avanzar(estado_sacado)
        if estado_avance is not None:
            coste_h = self.heuristica_total(estado_avance)
            if estado_avance.Robot_activado:
                coste_g1 = coste_g + 2
            else:
                coste_g1 = coste_g + 1

            coste_f_nuevo = coste_h + coste_g1

            estado_avance.asignar_padre(estado_sacado, coste_g1, "A")

            self.insertar_en_abierta(estado_avance, coste_f_nuevo, valor_cabeza)

            self.nodos_expandidos += 1

        estado_gir_der: Estado = self.girar(estado_sacado, False)
        if estado_gir_der is not None:
            coste_h = self.heuristica_total(estado_gir_der)

            if estado_gir_der.Robot_activado:
                coste_g1 = coste_g + 3
            else:
                coste_g1 = coste_g + 2

            coste_f_nuevo = coste_h + coste_g1

            estado_gir_der.asignar_padre(estado_sacado, coste_g1, "GD")

            self.insertar_en_abierta(estado_gir_der, coste_f_nuevo, valor_cabeza)

            self.nodos_expandidos += 1

        estado_gir_izq: Estado = self.girar(estado_sacado, True)
        if estado_gir_izq is not None:
            coste_h = self.heuristica_total(estado_gir_izq)

            if estado_gir_izq.Robot_activado:
                coste_g1 = coste_g + 3
            else:
                coste_g1 = coste_g + 2

            coste_f_nuevo = coste_h + coste_g1
            estado_gir_izq.asignar_padre(estado_sacado, coste_g1, "GI")

            self.insertar_en_abierta(estado_gir_izq, coste_f_nuevo, valor_cabeza)

            self.nodos_expandidos += 1

        estado_levantar: Estado = self.levantar_bajar(estado_sacado)
        if estado_levantar is not None:
            coste_h = self.heuristica_total(estado_levantar)

            coste_g1 = coste_g + 3
            coste_f_nuevo = coste_h + coste_g1

            if estado_sacado.Robot_activado:  # Si estaba activado ahora se baja
                estado_levantar.asignar_padre(estado_sacado, coste_g1, "B")
            else:  # Se sube el palet
                estado_levantar.asignar_padre(estado_sacado, coste_g1, "S")

            self.insertar_en_abierta(estado_levantar, coste_f_nuevo, valor_cabeza)
            self.nodos_expandidos += 1

    def resolver(self, profundidad=100, limite_tiempo=800):
        ciclos = 0
        Exito = False
        camino_hecho = None
        self.nodos_expandidos: int = 0
        self.tiempo_total: float = 0.0
        self.coste_final: int = 0

        tiempo_inicio = time()

        try:
            while (profundidad > ciclos) and not Exito:
                tiempo_inicio_bucle = time()

                repetido: bool = False

                valor_cabeza = self.lis_abierta.valor_cabeza()

                if not self.lis_abierta.vacio():
                    estado_coste = self.lis_abierta.extraer()
                else:
                    # Si lista abierta esta vacia, se meten todos los datos de la lista lenta
                    print("Metiendo nodos lista lenta a abierta en ciclo ", ciclos)
                    self.actualizar_listas_abiertas()

                    valor_cabeza = self.lis_abierta.valor_cabeza()

                    estado_coste = self.lis_abierta.extraer()

                if estado_coste is None:
                    print("Lista abierta vacia, no hay mas estados que expandir")
                    break

                estado_sacado: Estado = estado_coste.dato
                coste_sacado: int = estado_coste.prioridad
                hash_estado: int = hash(estado_sacado)

                if ciclos % 100 == 0:
                    print("Ciclos: ", ciclos, "Coste F minimo: ", coste_sacado, "Coste H: ",
                          self.heuristica_total(estado_sacado))
                    if limite_tiempo < time() - tiempo_inicio:
                        print("Se pasa tiempo maximo, se sale")
                        break

                ciclos = ciclos + 1

                if True:

                    try:
                        self.diccionario_estados_abierta.pop(hash_estado)
                    except Exception as e:
                        print("Posible error diccionario lista abierta ciclo ", ciclos)
                        print("Se intento sacar: ", hash_estado, coste_sacado)
                        print(e)
                        exit()

                    self.lis_cerrada.update({hash_estado: coste_sacado})
                    c_h = self.heuristica_total(estado_sacado)
                    coste_g: int = estado_sacado.costo_g

                    if c_h == 0:
                        Exito = True
                        repetido = True  # Para que no expanda una vez tenga exito

                        self.coste_final = coste_g
                        self.estado_final = estado_sacado

                        camino_hecho = estado_sacado.volver_inicio()

                if not repetido:
                    self.expandir(estado_sacado, coste_g, valor_cabeza)

                    self.lis_tiempo_ciclo.append(time() - tiempo_inicio_bucle)

        except KeyboardInterrupt:
            print("Saliendo de busqueda de forma manual")

        except Exception as e:
            print("Error buscando solucion", e)

        if len(self.lis_abierta) == 0 and Exito is False:
            print("Error, no se encontro solucion")

        print("Encontrado solucion: ", Exito)

        self.tiempo_total = time() - tiempo_inicio

        # Longitud camino
        if camino_hecho is not None:
            camino_pasos = camino_hecho.split(".")  # type: ignore
            self.longitud_camino: int = len(camino_pasos) - 1  # resta el paso inicio que no es real

        return camino_hecho


def main():
  pass


if __name__ == "__main__":
    main()
