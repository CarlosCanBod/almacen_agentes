#!/usr/bin/env python
from typing import Any
from time import time
import numpy as np  # Se usa para copiar el entorno para el mapa.
import matplotlib.pyplot as plt
import tracemalloc


from typing import Any

#Cada elemento/nodo de la lista enlazada 
#tiene un dato, el nodo siguiente y una prioridad
#Cuando se introduzca en una cola de prioridad 
#se va a introducir el que mas prioridad tenga adelante
class nodo_cola_prioridad():
    def __init__(self,dato = 0,prioridad = 1):
        self.dato: Any = dato
        self.siguiente = None
        self.prioridad = prioridad #Se considera que cuanto mas alto mas importante :)

    #Se crea este metodo para poder imprimir un nodo indivudual
    def __str__(self):
        cadena = "(" + str(self.dato) + "," + str(self.prioridad) + ")" + " "
        return cadena


    def __eq__(self, otro: object) -> bool:
        
        return hash(self) == hash(otro)


    def __hash__(self) -> int:

        return hash((self.dato,self.prioridad))

    def __lt__(self,otro: "nodo_cola_prioridad")-> bool:
        return self.prioridad < otro.prioridad

#Aqui se crea la cola de prioridad ordenada
#Los nodos/elementos se van a ordenar de menor a mayor prioridad
class cola_prio():

    def __init__(self):
        self.cabeza = None

    def __str__(self):
        try:
            cadena = "Lista tiene: "
            nodo_aux = self.cabeza
            while nodo_aux != None:
                cadena = cadena + "(" + str(nodo_aux.dato) + "," + str(nodo_aux.prioridad) + ")" + " "
                nodo_aux = nodo_aux.siguiente

            return cadena
        except:
            print("error al convertir lista en string")

            return "Error imprimir cola prioridad"


    def __len__(self):
        if self.cabeza != None:
            nodo_actual = self.cabeza
            tamano = 0;
            while nodo_actual.siguiente != None:
                nodo_actual = nodo_actual.siguiente
                tamano += 1

            tamano += 1
            return tamano
        else:
            return 0

    def valor_cabeza(self) -> Any:
        if self.cabeza != None:
            return self.cabeza.prioridad
        else:
            return None


    #Introduce el elemento en la lista y su posicion depende de su prioridad
    #Cuanta mas prioridad mas a la derecha se va a colocar. 
    def insertar(self,dato: Any,prioridad: int):
        try:
            #Si la cola esta vacia se introduce el nodo/elemento
            #al principio. 
            if self.cabeza == None:
                self.cabeza = nodo_cola_prioridad(dato,prioridad)
                

            #Si el elemento que se va a meter tiene menos prioridad
            #que el primero, el nuevo va a ser la nueva cabeza(el primero de la cola)
            elif self.cabeza.prioridad <= prioridad: 
                    nodo_nuevo = nodo_cola_prioridad(dato, prioridad) 
                    
                    nodo_nuevo.siguiente = self.cabeza      #type: ignore
                    self.cabeza = nodo_nuevo 


            #En este caso el elemento nuevo 
            else: 

                #el nodo auxiliar se crea como el primero,
                #para ir buscando uno a uno donde meter el nuevo
                #dependiendo de su prioridad, va a buscar el siguiente elemento 
                #hasta que su prioridad sea igual o mayor
                nodo_actual = self.cabeza
                nodo_previo = None
                fin = False
                while (nodo_actual != None) and (fin == False): 
                    #Si el nodo actual tiene mas prioridad
                    #que el que se va a meter sale del bucle 
                    if nodo_actual.prioridad <= prioridad:
                        fin = True
                    else: 
                        nodo_previo = nodo_actual
                        nodo_actual = nodo_actual.siguiente

                #Cuando se encuentra donde meter el nuevo elemento
                #Se crea con los parametros que sean, y se asigna como a continuacion 
                #el que esta despues del auxiliar, y se pone delante del auxiliar 
                #el nuevo elemento, por lo que si hay empate el nuevo se queda atras
                nodo_nuevo = nodo_cola_prioridad(dato,prioridad)
                nodo_nuevo.siguiente = nodo_actual  #type: ignore
                nodo_previo.siguiente = nodo_nuevo  # type: ignore

        except:
            print("Error al introducir elemento en la lista")

    def eliminar(self,dato: Any,prioridad: int, VALOR_CABEZA:int, trozo: int) -> None:
    
        if self.cabeza != None:
            nodo_actual = self.cabeza   # Se busca aqui el nodo a eliminar
            nodo_previo = None
            fin = False

            while (nodo_actual != None) and (fin == False):
                if nodo_actual.dato == dato and nodo_actual.prioridad == prioridad:
                    fin = True
                else: # Se va al siguiente nodo
                    nodo_previo = nodo_actual
                    nodo_actual = nodo_actual.siguiente

            if fin == True:
                if nodo_previo != None:
                    nodo_previo.siguiente = nodo_actual.siguiente  # type: ignore
                    return None
                else:
                    # Si es el primero el que se borra
                    if nodo_actual != None:
                        self.cabeza = nodo_actual.siguiente
                        return None
            print("ERROR NO ENCONTRADO DATO PARA ELIMINAR: ",hash(dato),prioridad, "TROZO: ",trozo,"  Valor cabeza: ", VALOR_CABEZA)
            return None



    #Si la cola esta vacia devuelve true
    def vacio(self):
        return self.cabeza == None

    #Borra el elemento mas a la derecha
    def pop(self):
        try:
            if self.cabeza != None:
                nodo_actual = self.cabeza
                nodo_previo = None

                #Va hacia el elemento mas a la derecha para borrarlo
                while nodo_actual.siguiente != None:
                    nodo_previo = nodo_actual
                    nodo_actual = nodo_actual.siguiente

                if nodo_previo != None:
                    nodo_previo.siguiente = None
            

        except:
            print("Error en pop lista prioridad")    

    #Devuelve cual es el elemento con mas prioridad(mas a la derecha)
    #Pero no lo borra    
    def primero(self):
        if self.cabeza != None:
            nodo_actual = self.cabeza
            if nodo_actual.siguiente != None:
                while nodo_actual.siguiente != None:
                    nodo_actual = nodo_actual.siguiente

                return nodo_actual
        else:
            pass

    #Devuelve cual es el elemento mas a la izquierda
    # pero no lo borra
    def ultimo(self):
        return self.cabeza
    
    #Devuelve el tamano de la cola
    #Recorriendo la cola y contando
    def tamano(self):
        
        if self.cabeza != None:
            nodo_actual = self.cabeza
            tamano = 0;
            while nodo_actual.siguiente != None:
                nodo_actual = nodo_actual.siguiente
                tamano += 1

            tamano += 1
            return tamano
        else:
            return 0
        
    #Devuelve el elemento con mas prioridad y lo borra de la cola
    def extraer(self):
        if self.cabeza != None:
            nodo_actual = self.cabeza
            nodo_previo = None
            if nodo_actual.siguiente != None:
                while nodo_actual.siguiente != None:
                    nodo_previo = nodo_actual
                    nodo_actual = nodo_actual.siguiente

                if nodo_previo != None:
                    nodo_previo.siguiente = None #Asi el nodo que se devuelve ya no tiene quien lo referencie
            else:
                # Si es el unico, no hay siguiente, se borra la cabeza.
                self.cabeza = None


            return nodo_actual
        else:
            pass

"""
Fin clases de cola prioridad

"""

buscar_errores: bool = False

# Esto va a hacer que el coste heuristica sea como maximo uno,
# para que sepa si llega al final. De esta forma solo se usa el costo G.
modo_djistra:bool = False




class Palet():
    def __init__(self,x_inicial: int,y_inicial:int ,ang_inicial:bool ,x_objetivo:int ,y_objetivo:int ,ang_objetivo:bool) -> None:
        self.pos_x:int = x_inicial
        self.pos_y:int = y_inicial
        # Las estanterias el valor ang actual 1 es vertical y 0 horizontal
        self.ang_actual:bool = ang_inicial

        self.x_objetivo:int = x_objetivo
        self.y_objetivo:int = y_objetivo
        self.ang_objetivo:bool =  ang_objetivo

        return None

    def __hash__(self) -> int:

        return hash((self.pos_x,self.pos_y,self.ang_actual,self.x_objetivo,self.y_objetivo,self.ang_objetivo))

    def __str__(self) -> str:
        return f"Lugar(x={self.pos_x}, y={self.pos_y}, ori='{self.ang_actual}')"

    def necesita_moverse(self) -> bool:

        if self.ang_actual != self.ang_objetivo:
            return True
        elif self.pos_x != self.x_objetivo:
            return True
        elif self.pos_y != self.y_objetivo:
            return True
        
        return False


class Estado():
    def __init__(self,R_x:int ,R_y:int ,R_ang:str ,R_levantado: bool, Lista_palets: "list[Palet]" ) -> None:    
        self.Robot_x:int = R_x
        self.Robot_y:int = R_y
        self.Robot_orientacion: str = R_ang
        self.Robot_activado:bool = R_levantado
        self.Lista_estanterias: "list[Palet]" = Lista_palets

        self.estado_padre: Any = None
        self.costo_g: int = 0
        self.accion: str = "Inicio"


    def asignar_padre(self,padre: "Estado",coste_accion:int, nombre_accion: str) -> None:

        self.estado_padre = padre
        self.costo_g = coste_accion
        self.accion = nombre_accion


    def volver_inicio(self) -> str:

        if self.estado_padre == None:
            return self.accion
        else:
            return  self.estado_padre.volver_inicio() + "." + self.accion 

    def __eq__(self: "Estado", otro_estado: "Estado"):  # type: ignore

        return  hash(self) == hash(otro_estado)
                

    def __hash__(self) -> int:
        
        hash_palets = 0
        if self.Lista_estanterias != None:
            for palet in self.Lista_estanterias:
                hash_palets = hash(palet) + hash_palets


        return hash((self.Robot_x,self.Robot_y,self.Robot_orientacion,self.Robot_activado,hash_palets))




class Busqueda():

    def __init__(self,estado_inicial: "Estado", entorno: "list[list]",pesos: list[int] = [5,1,2]) -> None:
        # Mapeo de orientaciones
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

        self.filas = len(entorno)
        self.columnas = len(entorno[0])
        self.entorno = entorno

        self.coste_final:int = 0
        self.longitud_camino: int = 0
        self.tiempo_total: float = 0.0
        self.nodos_expandidos: int = 0
        self.lis_tiempo_ciclo: "list[float]" = []
        self.lis_memoria_ciclo: "list[float]" = []


        #self.lis_cerrada: "list[nodo_cola_prioridad]" = []
        self.lis_cerrada: "dict[int,int]" = {}


        # Se va a usar para a la hora de insertar en lista abierta
        # mirar si esta en abierta, y si lo esta pues se hace la cosa lenta
        # de cambiarlo por el nuevo si es mas barato
        self.diccionario_estados_abierta: "dict[int,int]" = {}


        self.lis_abierta = cola_prio()    
        # Aqui se van a meter los nodos si su coste es mayor al de la cabeza de lista abierta,
        # a ver si hace que vaya mas rapido el codigo, ya que lo que hace que se vaya mas lento 
        # es meter nuevos estados en lista abierta cuando ya hay muchos.
        self.lis_abierta_lenta: cola_prio = cola_prio()
        self.lis_abierta_mas_lenta: cola_prio = cola_prio()

        self.lis_abierta.insertar(estado_inicial,prioridad=self.heuristica_total(estado_inicial))
        self.diccionario_estados_abierta.update({hash(estado_inicial):self.heuristica_total(estado_inicial)})

        return None
    
    def heuristica_robot_origen(self,robot_x,robot_y,robot_orientacion,rob_activado)-> int:
        coste = abs(self.estado_ini.Robot_x- robot_x) + abs(self.estado_ini.Robot_y - robot_y)

        if coste == 0:
            if robot_orientacion != self.estado_ini.Robot_orientacion:
                coste = coste + 1

            if rob_activado:
                coste =+ 1

        return coste


    def heuristica_palets1(self,estado_comprobar: Estado) -> int:

        lista_palets: "list[Palet]" = estado_comprobar.Lista_estanterias

        coste = 0

        if lista_palets != None:
            for palet in lista_palets:

                c1 = abs(palet.x_objetivo-palet.pos_x) + abs(palet.y_objetivo-palet.pos_y)

                if palet.ang_actual != palet.ang_objetivo:
                    c1 = c1 + 1

                coste = coste + c1


        return coste

    def heur_robot_palet(self,estado_comprobar: Estado):

        coste = 0
        x1 = estado_comprobar.Robot_x
        y1 = estado_comprobar.Robot_y

        lista_palets: "list[Palet]" = estado_comprobar.Lista_estanterias
        
        for palet in lista_palets:

            if palet.necesita_moverse():
                x_palet = palet.pos_x
                y_palet = palet.pos_y
                dist = abs(x_palet-x1) + abs(y_palet-y1)
                
                coste = coste + dist
                
        return coste

    def heuristica_total(self,estado_comprobar: Estado) -> int:
        
        
        coste_robot_origen = 0
        coste_palets_robot = 0

        coste_robot_origen = self.heuristica_robot_origen(estado_comprobar.Robot_x,estado_comprobar.Robot_y, estado_comprobar.Robot_orientacion,estado_comprobar.Robot_activado)
        coste_palets_objetivo = 0

        if len(estado_comprobar.Lista_estanterias):
            coste_palets_objetivo: int = (self.heuristica_palets1(estado_comprobar))

            # Que el robot quiera ir a por los palets que tienen que moverse
            if modo_djistra == False:
                #coste_palets_robot = self.heur_robot_palet(estado_comprobar) 
                pass

        coste_total = self.peso1*coste_palets_objetivo + self.peso2*coste_robot_origen + self.peso3*coste_palets_robot

        if modo_djistra:
            if coste_total != 0:
                coste_total = 1

        return coste_total
    
    def levantar_bajar(self, estado: Estado) -> Any:
        """
        Tiene que estar debajo de un palet para poder usar esto,
        si no, no sube o baja.

        Va a invertir el estado que tenga.
        """
        
        
        cord_robot_x: int  = estado.Robot_x
        cord_robot_y: int = estado.Robot_y
        robot_angulo: str = estado.Robot_orientacion
        rob_activado: bool = estado.Robot_activado
        lis_estanterias: "list[Palet]" = estado.Lista_estanterias.copy()

        
        for palet in lis_estanterias:
            if cord_robot_x == palet.pos_x and cord_robot_y == palet.pos_y:
                rob_activado = not(rob_activado)
                estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lis_estanterias)
                return estado_nuevo

        # Si no ha encontrado un palet encima del robot, no se devuelve estado
        return None

    def girar(self, estado: Estado, izquierda: bool = True) -> Any:
        """
            Gira el robot a la izquierda
            Si no tiene palet no hay requisitos para girar

            Si lo hay, no puede haber nada alrededor de la posicion del robot
        
        """

        cord_robot_x: int  = estado.Robot_x
        cord_robot_y: int = estado.Robot_y
        robot_angulo: str = estado.Robot_orientacion
        rob_activado: bool = estado.Robot_activado
        lis_estanterias_copia: "list[Palet]" = estado.Lista_estanterias.copy()

        if izquierda:
            robot_angulo = self.rotar_izquierda[robot_angulo]
        else:
            robot_angulo = self.rotar_derecha[robot_angulo]

        if rob_activado == 0:

            estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lis_estanterias_copia)
            return estado_nuevo

        else: 

            # Si lleva palet hay que hacer mas comprobaciones
            # Que no este cerca de algun obstaculo 
            # Los obstaculos tienen valor 9 en entorno, y paredes 1 por ejemplo
            # No pueden girar si tienen bloque, pero si pared cerca
            for ancho in range(-1,2):
                for alto in range(-1,2):
                    #if ancho == 1 and alto == 0:
                    #    print("ENTORNO AL SUR: ", self.entorno[cord_robot_x +ancho][cord_robot_y+alto])
                    #print(ancho)
                    try:
                        if self.entorno[cord_robot_x +ancho][cord_robot_y + alto] == 9:
                            return None
                    except:
                        pass

            # Que no pueda girar en los bordes con palet
            # REVISAR QUE NO ELIMINE CAMINOS CORRECTOS
            if cord_robot_x == 0 or cord_robot_x == self.filas-1:
                #print("GIRO ILEGAL")
                return None
            if cord_robot_y == 0 or cord_robot_y == self.columnas-1:
                #print("GIRO ILEGAL")
                return None

            lista_palets_quietos: "list[Palet] " = []   
            Palet_girado = None     #type:ignore

            for palet in lis_estanterias_copia:

                # Gira el palet si es el que esta en la posicion del robot
                if palet.pos_x == cord_robot_x and palet.pos_y == cord_robot_y:

                    Pal_pos_x = palet.pos_x; Pal_obj_x = palet.x_objetivo
                    Pal_pos_y = palet.pos_y; Pal_obj_y = palet.y_objetivo
                    Pal_ang_act = not(palet.ang_actual); Pal_obj_ang = palet.ang_objetivo
                    

                    Palet_girado: Palet = Palet(Pal_pos_x,Pal_pos_y,Pal_ang_act,
                                                Pal_obj_x,Pal_obj_y,Pal_obj_ang)
                    if buscar_errores:
                        print("GIRADO",cord_robot_x, " y ",cord_robot_y)
                        print("PALET EN X ",palet.pos_x, " y ",palet.pos_y, "PASA DE ", palet.ang_actual, "A ", not(palet.ang_actual))

                    


                else:

                    # Si no es el palet que lleva
                    # Mira alrededor del otro palet, no se puede girar ahi.
                    for ancho in range(-1,1):
                        for alto in range(-1,1):
                            if cord_robot_x == palet.pos_x +ancho and cord_robot_y == palet.pos_y + alto:
                                return None
                    lista_palets_quietos.append(palet)        
                    
            if Palet_girado != None:
                lista_palets_quietos.append(Palet_girado)

                if buscar_errores:
                    print("Estado nuevo giro palet")

            estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lista_palets_quietos)
            return estado_nuevo

    def avanzar(self, estado: Estado) -> Any:

        Rob_pos_x = estado.Robot_x
        Rob_pos_y= estado.Robot_y
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
        if self.entorno[Rx_n][Ry_n]: # En principio detecta obstaculo = 9 y paredes = 1
            return None


        # El robot no baja o sube el palet aqui, queda igual

        if R_levan == False:
            # Comprobar que el robot no choca con patas de alguna estanteria
            for palet in lista_palets_copia:
                if palet.ang_actual == 1: # Si el palet esta en vertical
                    # Al estar en vertical el robot no se puede mover 1 encima o debajo
                    # de la posicion del palet
                    if palet.pos_x == Rx_n and (palet.pos_y + 1 == Ry_n or palet.pos_y -1 == Ry_n ):
                        return None
                else:
                    # Si esta horizontal, el robot no se puede poner 1 casilla por los lados
                    # en eje X,
                    if palet.pos_y == Ry_n and (palet.pos_x +1 == (Rx_n) or palet.pos_x -1  == Rx_n):
                        return None

            lista_palets_nueva = lista_palets_copia

        # Si el robot está levantado tiene estanteria, por lo que  hay que hacer más comprobaciones.
        else:    # Si no lleva palet


            if lista_palets_copia == None:
                print("Error, palet desaparecio")

                self.imprimir(estado,self.entorno)
                exit()




            lleva_vertical: bool = False
            
            # Aqui se meten los palets que no se mueven, 
            # para despues no comparar el que se mueve consigo mismo
            lista_palets_quietos: "list[Palet] " = []   
            Palet_movido = None     #type:ignore

            # Buscar que palet es el que lleva el robot y mover su posicion a que este
            # encima del robot
            for palet in lista_palets_copia:
                if palet.pos_x == estado.Robot_x and palet.pos_y == estado.Robot_y:

                    Pal_pos_x = palet.pos_x; Pal_obj_x = palet.x_objetivo
                    Pal_pos_y = palet.pos_y; Pal_obj_y = palet.y_objetivo
                    Pal_ang_act = palet.ang_actual; Pal_obj_ang = palet.ang_objetivo
                    

                    Palet_movido: Palet = Palet(Pal_pos_x,Pal_pos_y,Pal_ang_act,
                                                Pal_obj_x,Pal_obj_y,Pal_obj_ang)

                    Palet_movido.pos_x = Palet_movido.pos_x + dx
                    Palet_movido.pos_y = Palet_movido.pos_y + dy

                    if Palet_movido.ang_actual == True:    # Si es vertical el palet que lleva
                        lleva_vertical: bool = True
                    else:

                        lleva_vertical: bool = False

                else:
                    lista_palets_quietos.append(palet)
            


            # Con la nueva posicion del palet miramos si no choca con otro palet o obstaculo
            # Utilizo la posicion del robot, si el palet que lleva esta en vertical, hay que mirar arriba y abajo,
            # si es horizontal a la izquierda y derecha de el.
            
            if lleva_vertical == True:

                if Ry_n == 0 or Ry_n == self.filas -1 :
                    return None
                 

                # QUITAR ESTE TRY POR ALGO BUENO 
                try:
                    if 0 > Rx_n >= self.filas  or 0 > Ry_n + 1 >= self.columnas or self.entorno[Rx_n][Ry_n+1] == 9:
                        return None
                    elif 0 > Rx_n >= self.filas  or 0 > Ry_n - 1 >= self.columnas or self.entorno[Rx_n][Ry_n-1] == 9:
                        return None
                except:
                    return None

                for palet in lista_palets_quietos:

                    # Que no se meta en otro palet
                    if Rx_n == palet.pos_x and Ry_n == palet.pos_y:
                        #print("Choque 1")
                        return None


                    if palet.ang_actual == 1: # Si el otro palet esta en vertical

                        # Al estar en vertical el robot no se puede mover 1 encima o debajo
                        # de la posicion del palet
                        if palet.pos_x == Rx_n and (palet.pos_y-1 == (Ry_n) or palet.pos_y == (Ry_n) or palet.pos_y+1 == (Ry_n)):
                            #print("Choque 2")

                            return None
                        
                    else:
                       # Mira alrededor del otro palet, no se puede mover ahi.
                        for ancho in range(-1,1):
                            for alto in range(-1,1):
                                if Rx_n == palet.pos_x +ancho and Ry_n == palet.pos_y + alto:
                                    #print("Choque 3")
                                    return None
            else:
                # Si lo lleva en horizontal

                if Rx_n == 0 or Rx_n == self.columnas -1 :
                    return None


                try:
                    if 0 > Rx_n+1 > self.filas  or 0 > Ry_n  > self.columnas or self.entorno[Rx_n+1][Ry_n]== 9:
                        return None
                    elif 0 > Rx_n-1 > self.filas  or 0 > Ry_n  > self.columnas or self.entorno[Rx_n-1][Ry_n]== 9:
                        return None
                except:
                    return None

                for palet in lista_palets_quietos:


                     # Que no se meta en otro palet
                    if Rx_n == palet.pos_x and Ry_n == palet.pos_y:
                        return None
                    

                    if palet.ang_actual == 0: # Si el otro palet esta en horizontal

                        # Al estar en horizontal el robot no se puede mover 1 der o izquierda
                        # de la posicion del palet
                        if palet.pos_y == Ry_n and (palet.pos_x-1 == (Rx_n) or palet.pos_x == (Rx_n) or palet.pos_x+1 == (Rx_n)):
                            return None
                        
                    else:
                       # Mira alrededor del otro palet, no se puede mover ahi.
                        for ancho in range(-1,1):
                            for alto in range(-1,1):
                                if Rx_n == palet.pos_x +ancho and Ry_n == palet.pos_y + alto:
                                    return None
                


            lista_palets_nueva = lista_palets_quietos
            if Palet_movido != None:
                
                lista_palets_nueva.append(Palet_movido)


                #print("Se devuelve: ", type(lista_palets_nueva)) 
                #self.imprimir(Estado(Rx_n,Ry_n,Rang,R_levan,Lista_palets=lista_palets_nueva) ,self.entorno)
                #print("Fin devolver")


        return Estado(Rx_n,Ry_n,Rang,R_levan,Lista_palets=lista_palets_nueva) 


    def insertar_en_abierta(self,estado_nuevo: Estado,coste_f_nuevo:int,valor_cabeza:int) -> None:

        # Buscar en lista cerrada
        hash_estado = hash(estado_nuevo)
        prioridad_vieja = self.lis_cerrada.get(hash_estado)

        # Si no esta en cerrada deberia devolver None
        if prioridad_vieja != None:
            if coste_f_nuevo > prioridad_vieja:
                # Si ya existe el estado en cerrada, pero el nuevo
                # es peor o igual, no se añade en abierta porque hay un camino mejor
                # para llegar a ese estado.
                return None
            else:
                self.lis_cerrada.pop(hash_estado)  # Borrar de lista cerrada el estado viejo
                                                    # para hacer dic mas pequeño, alomejor no se deberia hacer
                                                    # porque hasta que no se meta el otro se podrian repetir estados

        coste_estado_en_abierta = self.diccionario_estados_abierta.get(hash_estado,None) # Supongo que da None si no esta en abierta

        if coste_estado_en_abierta != None:
            # Si ya existe en abierta, mirar si el nuevo es mejor
            if coste_f_nuevo < coste_estado_en_abierta:
                # Si es mejor el nuevo estado, hay que buscar y sacar el viejo de abierta
                # y meter el nuevo
                self.diccionario_estados_abierta.pop(hash_estado)
                if  valor_cabeza != None and valor_cabeza >= coste_estado_en_abierta: # Se busca en la lista donde deberia estar ese estado,prio
                    #print("Metido en lista abierta ")
                    self.lis_abierta.eliminar(estado_nuevo,coste_estado_en_abierta,valor_cabeza,0)
                else:
                    valor_cabeza_lenta = self.lis_abierta_lenta.valor_cabeza()
                    if  valor_cabeza != None and valor_cabeza_lenta >= coste_estado_en_abierta:
                        self.lis_abierta_lenta.eliminar(estado_nuevo,coste_estado_en_abierta,valor_cabeza_lenta,1)
                    else:
                        self.lis_abierta_mas_lenta.eliminar(estado_nuevo,coste_estado_en_abierta,valor_cabeza_lenta,2)
            else:
                return None


        self.diccionario_estados_abierta[hash_estado] = coste_f_nuevo


        if  valor_cabeza == None or valor_cabeza >= coste_f_nuevo:
            #print("Metido en lista abierta ")
            self.lis_abierta.insertar(dato=estado_nuevo,prioridad=coste_f_nuevo)
        else:
            valor_cabeza_lenta = self.lis_abierta_lenta.valor_cabeza()
            if  valor_cabeza_lenta == None or valor_cabeza_lenta >= coste_f_nuevo:
                self.lis_abierta_lenta.insertar(dato=estado_nuevo,prioridad=coste_f_nuevo)
            else:
                self.lis_abierta_mas_lenta.insertar(dato=estado_nuevo,prioridad=coste_f_nuevo)
        
        
        return None

    def actualizar_listas_abiertas(self):   
        self.lis_abierta = self.lis_abierta_lenta
        #tam_lenta2 = len(self.lis_abierta_mas_lenta)
        #if tam_lenta2 > 0:
        #    self.lis_abierta_lenta = cola_prio()
        #    for i in range(0,tam_lenta2,1):
        #        sacado: nodo_cola_prioridad  = self.lis_abierta_mas_lenta.extraer() #type: ignore
        #        self.lis_abierta_lenta.insertar(sacado.dato,sacado.prioridad)
        #else:

        self.lis_abierta_lenta = self.lis_abierta_mas_lenta
        self.lis_abierta_mas_lenta = cola_prio()
        
    def expandir(self,estado_sacado,coste_g,valor_cabeza = 9999) -> None:
        """
        Pendiente hacer que haga bastantes distancias,
        hacer bucle  o algo asi.
        
        """                
        factor_g: int =1



        #tiempo_in_expandir = time()
        estado_avance: Estado = self.avanzar(estado_sacado)
        if estado_avance != None:
            coste_h = self.heuristica_total(estado_avance)
            if estado_avance.Robot_activado:
                coste_g1 = coste_g + 2
            else:
                coste_g1 = coste_g + 1 
                
            coste_f_nuevo = coste_h + coste_g1*factor_g

            estado_avance.asignar_padre(estado_sacado,coste_g1,"A")

            self.insertar_en_abierta(estado_avance,coste_f_nuevo,valor_cabeza)
            

            self.nodos_expandidos += 1

        
        estado_gir_der: Estado = self.girar(estado_sacado,False)
        if estado_gir_der != None:
            coste_h = self.heuristica_total(estado_gir_der)

            if estado_gir_der.Robot_activado:
                coste_g1 = coste_g + 3
            else:
                coste_g1 = coste_g + 2

            coste_f_nuevo = coste_h + coste_g1*factor_g

            estado_gir_der.asignar_padre(estado_sacado,coste_g1,"GD")


            self.insertar_en_abierta(estado_gir_der,coste_f_nuevo,valor_cabeza)
            
            self.nodos_expandidos += 1


        estado_gir_izq: Estado = self.girar(estado_sacado,True)
        if estado_gir_izq != None:
            coste_h = self.heuristica_total(estado_gir_izq)

            if estado_gir_izq.Robot_activado:
                #print("robot activado")
                coste_g1 = coste_g + 3
            else:
                coste_g1 = coste_g + 2
            
            coste_f_nuevo = coste_h + coste_g1*factor_g
            estado_gir_izq.asignar_padre(estado_sacado,coste_g1,"GI")


            self.insertar_en_abierta(estado_gir_izq,coste_f_nuevo,valor_cabeza)

            self.nodos_expandidos += 1


        estado_levantar: Estado = self.levantar_bajar(estado_sacado)
        if estado_levantar != None:
            #print("robot activado en ciclo: ", ciclos)
            coste_h = self.heuristica_total(estado_levantar)

            coste_g1 = coste_g + 3
            coste_f_nuevo = coste_h + coste_g1*factor_g

            if estado_sacado.Robot_activado: # Si estaba activado ahora se baja
                estado_levantar.asignar_padre(estado_sacado,coste_g1,"B")
            else: # Se sube el palet 
                estado_levantar.asignar_padre(estado_sacado,coste_g1,"S")

            self.insertar_en_abierta(estado_levantar,coste_f_nuevo,valor_cabeza)
            self.nodos_expandidos += 1

    def resolver(self,profundidad= 100,medir_memoria: bool = False):

        if medir_memoria:
            tracemalloc.start()    

        ciclos = 0
        Exito = False
        estado_sacado = None    #type: ignore
        estado_coste = None  #type: ignore
        camino_hecho = None
        self.nodos_expandidos: int = 0
        self.tiempo_total: float = 0.0
        self.coste_final: int = 0
        

        tiempo_inicio = time()


        #print("INICIAL DIBUJO", self.estado_ini.Lista_estanterias[0].ang_actual)
        #self.imprimir(self.estado_ini,self.entorno)

        while  (profundidad > ciclos) and Exito == False:
            tiempo_inicio_bucle = time()
        

            repetido:bool = False

            valor_cabeza = self.lis_abierta.valor_cabeza()

            if self.lis_abierta.vacio() == False:
                estado_coste = self.lis_abierta.extraer()
            else:
                # Si lista abierta esta vacia, se meten todos los datos de la lista lenta
                print("Metiendo nodos lista lenta a abierta en ciclo ", ciclos)
                self.actualizar_listas_abiertas()

                valor_cabeza = self.lis_abierta.valor_cabeza()

                estado_coste = self.lis_abierta.extraer()


            if estado_coste == None:
                print("Lista abierta vacia, no hay mas estados que expandir")
                break

            estado_sacado: Estado = estado_coste.dato
            coste_sacado: int = estado_coste.prioridad
            hash_estado: int = hash(estado_sacado)

            if ciclos%100 == 0:
                print("Ciclos: ", ciclos, "Coste F minimo: ",coste_sacado, "Coste H: ", self.heuristica_total(estado_sacado))

            ciclos = ciclos+1
            coste_g = 0

            if True:

                try:
                    self.diccionario_estados_abierta.pop(hash_estado)
                except:
                    #print(self.diccionario_estados_abierta)
                    print("Posible error diccionario lista abierta ciclo ", ciclos)
                    print("Se intento sacar: ",hash_estado,coste_sacado)
                    exit()


                self.lis_cerrada.update({hash_estado:coste_sacado})
                c_h = self.heuristica_total(estado_sacado)
                coste_g: int = estado_sacado.costo_g                         
    
                if c_h == 0:
                    Exito = True
                    repetido = True # Para que no expanda una vez tenga exito

                    self.coste_final = coste_g
                    self.estado_final = estado_sacado

                    if buscar_errores:
                        papi: Estado = estado_sacado.estado_padre
                        while papi.estado_padre != None:
                            papi = papi.estado_padre
                            print("PADRE",papi.Lista_estanterias[0].ang_actual)
                            self.imprimir(papi,self.entorno)
                    
                    camino_hecho = estado_sacado.volver_inicio()
                    print(camino_hecho)

            else:  repetido:bool = True

            if repetido == False:
                self.expandir(estado_sacado,coste_g,valor_cabeza)
          

       
            repetido:bool = False
            if medir_memoria:
                mem = tracemalloc.get_traced_memory()[0]
                self.lis_memoria_ciclo.append(mem)
            else:
                self.lis_tiempo_ciclo.append(time() - tiempo_inicio_bucle)
       

        if len(self.lis_abierta) == 0 and Exito == False:
            print("Error, no se encontro solucion")

        print("Encontrado solucion: ", Exito)

        self.tiempo_total = time() - tiempo_inicio

        # Longitud camino
        if camino_hecho != None:
            camino_pasos = camino_hecho.split(".")            #type: ignore
            self.longitud_camino: int = len(camino_pasos) -1   #resta el paso inicio que no es real

        if medir_memoria:
            tracemalloc.stop()
        return camino_hecho



    def imprimir(self,estado: Estado ,entorno) -> None:
        
        #mapa = [[0 for i in range(self.filas)] for j in range(self.columnas)]
        mapa = np.copy(entorno)

        if estado != None:
            if estado.Robot_activado:
                mapa[estado.Robot_x][estado.Robot_y] =  22
            else:
                mapa[estado.Robot_x][estado.Robot_y] =  2#ord(estado.Robot_orientacion)//10

            if estado.Lista_estanterias != None:
                for palet in estado.Lista_estanterias:
                    if palet.ang_actual == 1:
                        mapa[palet.pos_x][palet.pos_y] = 6

                        try:
                            mapa[palet.pos_x][palet.pos_y+1] = 8
                        except:
                            pass

                        try:
                            mapa[palet.pos_x][palet.pos_y-1] = 8
                        except:
                            pass

                    else:
                        mapa[palet.pos_x][palet.pos_y] = 7
                        try:
                            mapa[palet.pos_x+1][palet.pos_y] = 8        
                        except:
                            pass
                        
                        try:
                            mapa[palet.pos_x-1][palet.pos_y] = 8
                        except:
                            pass


                    if palet.pos_x == estado.Robot_x and estado.Robot_y == palet.pos_y:
                        if estado.Robot_activado:
                            mapa[palet.pos_x][palet.pos_y] = 4
                        else:
                            mapa[palet.pos_x][palet.pos_y] = 3


        #print("robot x: ",estado.Robot_x)
        #print("robot y: ",estado.Robot_y)
        #print("Orientacion: ",estado.Robot_orientacion)

        for fila in mapa:
            print(fila)

        return None

def main():
    mundo_simulado = 2
    buscador = None
    camino = 0

    if mundo_simulado == 0 and buscar_errores == False:
        print("Mundo 0")
        # Coste minimo encontrado 66

        entorno = [
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 1, 9, 9, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 9, 9, 9, 1],
            [1, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0]
        ]

    
        paletillos = [Palet(5,2,False,1,5,True)] #[Palet(1,1,True,1,4,True),Palet(3,1,True,3,4,True)] 1,4

        situacion1 = Estado(8,4,"N",False,paletillos)

        buscador = Busqueda(situacion1,entorno)

        buscador.resolver(profundidad=50000)

        

    elif mundo_simulado == 1:
        print("Mundo 1")
        # coste minimo 131 h 5* 1* 3* ciclo 13100

        entorno = [
        #Y0                                           #Y14
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  #X 0
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  #X 9
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],  
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],  
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]   #X 14
            ]

        
        paletillos = [Palet(9,3,False,9,3,False),Palet(7,3,False,7,3,False), # Palets izquierda
                     Palet(9,5,False,2,5,False),Palet(7,5,False,7,5,False),
                          
                        Palet(9,10,False,9,10,False),Palet(7,10,False,1,7,True), # Palets derecha
                        Palet(9,12,False,9,12,False),Palet(7,12,False,7,12,False)
                          ]                             # Palets mas arriba

        situacion1 = Estado(12,7,"N",False,paletillos)

        buscador = Busqueda(situacion1,entorno)

        buscador.resolver(profundidad=25000)
    elif mundo_simulado == 2:
        print("Mundo 2")
        # Minimo camino 58
        # coste minimo 58 h 5* 1* 2*
        entorno = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        paletillos = [Palet(4,1,True,1,1,True),Palet(4,5,True,1,5,True)] 
        situacion1 = Estado(0,3,"E",False,paletillos)

        buscador = Busqueda(situacion1,entorno)

        buscador.resolver(profundidad=20000)



    elif mundo_simulado == 10:
        entorno = [
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 9, 9, 9, 1],
        ]

        paletillos = [Palet(1,3,True,1,5,True)] #[Palet(1,1,True,1,4,True),Palet(3,1,True,3,4,True)] 1,4
        situacion1 = Estado(1,3,"E",True,paletillos)

        buscador = Busqueda(situacion1,entorno)

        sit2 = buscador.girar(situacion1,False)

        buscador.imprimir(sit2,entorno)


    if buscador != None:
        print("Tiempo total calculo: ", buscador.tiempo_total)
        print("Coste total camino: ", buscador.coste_final)
        
        print("Longitud plan: ", buscador.longitud_camino)
        print("Nodos expandidos: ",buscador.nodos_expandidos)

        lista_tiempos = buscador.lis_tiempo_ciclo
        
        print("Tiempo medio ciclo: ", sum(lista_tiempos)/len(lista_tiempos))

        plt.plot(lista_tiempos)
        plt.show()

    return None


if __name__ == "__main__":
    main()
