from typing import Any
import numpy as np  # Se usa para copiar el entorno para el mapa.


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


    def comprobar_lugar_deseado(self) -> bool:
        
        if self.pos_x != self.x_objetivo:
            return False
        elif self.pos_y != self.y_objetivo:
            return False
        elif self.ang_actual != self.ang_objetivo:
            return False

        return True
    

    def __str__(self) -> str:
        return f"Lugar(x={self.pos_x}, y={self.pos_y}, ori='{self.ang_actual}')"



class Estado():
    def __init__(self,R_x:int ,R_y:int ,R_ang:str ,R_levantado: bool, Lista_palets: "list[Palet]" ) -> None:    
        self.Robot_x:int = R_x
        self.Robot_y:int = R_y
        self.Robot_orientacion: str = R_ang
        self.Robot_activado:bool = R_levantado
        self.Lista_estanterias: "list[Palet]" = Lista_palets


    def __eq__(self: "Estado", otro_estado: "Estado"):  # type: ignore

        return  hash(self) == hash(otro_estado)
                

    def __hash__(self) -> int:
        
        hash_palets = 0
        if self.Lista_estanterias != None:
            for palet in self.Lista_estanterias:
                hash_palets = hash(palet)


        return hash((self.Robot_x,self.Robot_y,self.Robot_orientacion,self.Robot_activado,hash_palets))


class Busqueda():

    def __init__(self,estado_inicial: "Estado",estado_objetivo: "Estado", entorno: "list[list]") -> None:
        # Mapeo de orientaciones
        self.movimientos = {
            'N': (1, 0),
            'S': (-1, 0),
            'E': (0, 1),
            'O': (0, -1)
        }
        self.rotar_izquierda = {'N': 'O', 'O': 'S', 'S': 'E', 'E': 'N'}
        self.rotar_derecha = {'N': 'E', 'E': 'S', 'S': 'O', 'O': 'N'}

        self.estado_ini = estado_inicial
        self.estado_final = estado_objetivo
        self.estado_actual = estado_inicial


        self.filas = len(entorno)
        self.columnas = len(entorno[0])

        self.entorno = entorno



        self.lis_abierta: "list[Estado]" = [estado_inicial]
        self.lis_cerrada: "list[Estado]" = []

        return None
    
    def heuristica_robot_origen(self,robot_x,robot_y,robot_orientacion)-> int:
        coste = abs(robot_x+robot_y)

        if robot_orientacion != self.estado_ini.Robot_orientacion:
            coste = coste + 1

        return coste


    def heuristica_palets1(self,lista_palets: "list[Palet]") -> int:

        coste = 0

        if lista_palets != None:
            for palet in lista_palets:

                c1 = (palet.x_objetivo-palet.pos_x)**2 + (palet.y_objetivo-palet.pos_y)**2

                if palet.ang_actual != palet.ang_objetivo:
                    c1 = c1 +1


                coste = coste + c1


        return coste


    def heuristica_total(self,estado_comprobar: Estado,coste_previo:int = 0) -> int:
        coste_total = coste_previo
        
        lista_palets = estado_comprobar.Lista_estanterias
        
        coste_total = self.heuristica_robot_origen(estado_comprobar.Robot_x,estado_comprobar.Robot_y,
                                              estado_comprobar.Robot_orientacion)

        coste_total: int = self.heuristica_palets1(lista_palets)  + coste_total

        return coste_total




    def levantar_bajar(self, estado: Estado):
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

    def girar_izq(self, estado: Estado):
        """
            Gira el robot a la izquierda
            Si no tiene palet no hay requisitos para girar

            Si lo hay, no puede haber nada alrededor de la posicion del robot
        
        """

        cord_robot_x: int  = estado.Robot_x
        cord_robot_y: int = estado.Robot_y
        robot_angulo: str = estado.Robot_orientacion
        rob_activado: bool = estado.Robot_activado
        lis_estanterias: "list[Palet]" = estado.Lista_estanterias.copy()


        if rob_activado == 0:
            robot_angulo = self.rotar_izquierda[robot_angulo]

            estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lis_estanterias)
            return estado_nuevo

        else: 
            robot_angulo = self.rotar_izquierda[robot_angulo]

            # Si lleva palet hay que hacer mas comprobaciones
            # Que no este cerca de algun obstaculo o pared
            for ancho in range(-1,1):
                for alto in range(-1,1):
                    if self.entorno[cord_robot_x +ancho][cord_robot_y + alto]:
                        return None


            for palet in lis_estanterias:

                # Gira el palet si es el que esta en la posicion del robot
                if palet.pos_x == cord_robot_x and palet.pos_y == cord_robot_y:
                    palet.ang_actual = not(palet.ang_actual)

                else:

                    # Si no es el palet que lleva
                    # Mira alrededor del otro palet, no se puede girar ahi.
                    for ancho in range(-1,1):
                        for alto in range(-1,1):
                            if cord_robot_x == palet.pos_x +ancho and cord_robot_y == palet.pos_y + alto:
                                return None
            estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lis_estanterias)
            return estado_nuevo


    def girar_der(self, estado: Estado):
        """
            Gira el robot a la izquierda
            Si no tiene palet no hay requisitos para girar

            Si lo hay, no puede haber nada alrededor de la posicion del robot
        
        """
        cord_robot_x: int  = estado.Robot_x
        cord_robot_y: int = estado.Robot_y
        robot_angulo: str = estado.Robot_orientacion
        rob_activado: bool = estado.Robot_activado
        lis_estanterias: "list[Palet]" = estado.Lista_estanterias.copy()

        robot_angulo = self.rotar_derecha[robot_angulo]


        if rob_activado == 0:

            estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lis_estanterias)

            return estado_nuevo

        else: 
            # Si lleva palet hay que hacer mas comprobaciones

            # Que no este cerca de algun obstaculo o pared
            for ancho in range(-1,1):
                for alto in range(-1,1):
                    if self.entorno[cord_robot_x +ancho][cord_robot_y + alto]:
                        return None


            for palet in lis_estanterias:

                # Gira el palet si es el que esta en la posicion del robot
                if palet.pos_x == cord_robot_x and palet.pos_y == cord_robot_y:
                    palet.ang_actual = not(palet.ang_actual)

                else:

                    # Si no es el palet que lleva
                    # Mira alrededor del otro palet, no se puede girar ahi.
                    for ancho in range(-1,1):
                        for alto in range(-1,1):
                            if cord_robot_x == palet.pos_x +ancho and cord_robot_y == palet.pos_y + alto:
                                return None
                            

            estado_nuevo: Estado = Estado(cord_robot_x,cord_robot_y,robot_angulo,rob_activado,lis_estanterias)
            return estado_nuevo


    def avanzar(self, estado: Estado) -> Any:

        # Mira a que posicion cambia el robot si avanza, mirando la orientacion
        Rang = estado.Robot_orientacion
        dx, dy = self.movimientos[estado.Robot_orientacion]

        # nueva posicion del robot
        Rx_n = estado.Robot_x + dx
        Ry_n = estado.Robot_y + dy

        lista_palets_nueva = []

        # Comprobar que robot puede moverse, si no devuelve None
        # Primero si sale fuera del entorno, y luego si en el entorno estatico la nueva posicion
        # esta ocupada por pared o obstaculo
        if 0 > Rx_n or Rx_n >= self.filas: 
            return None
        if 0 > Ry_n or Ry_n >= self.columnas: 
            return None
        if self.entorno[Rx_n][Ry_n]:
            return None


        # El robot no baja o sube el palet aqui, queda igual
        R_levan = estado.Robot_activado

        if R_levan == False:
            # Comprobar que el robot no choca con patas de alguna estanteria
            for palet in estado.Lista_estanterias:
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

            lista_palets_nueva = estado.Lista_estanterias.copy()


        # Si el robot está levantado tiene estanteria, por lo que  hay que hacer más comprobaciones.
        else:    # Si no lleva palet


            if estado.Lista_estanterias == None:
                print("Error, palet desaparecio")

                self.imprimir(estado,self.entorno)
                return None




            lleva_vertical: bool = False
            
            # Aqui se meten los palets que no se mueven, 
            # para despues no comparar el que se mueve consigo mismo
            lista_palets_quietos: "list[Palet] " = []   
            Palet_movido = None     #type:ignore

            # Buscar que palet es el que lleva el robot y mover su posicion a que este
            # encima del robot
            for palet in estado.Lista_estanterias:
                if palet.pos_x == estado.Robot_x and palet.pos_y == estado.Robot_y:

                    Palet_movido: Palet = palet

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

                # Que no choque con entorno el palet MIRAR SI ES REAL
                if 0 > Rx_n >= self.filas  or 0 > Ry_n + 1 >= self.columnas or self.entorno[Rx_n][Ry_n+1]:
                    return None
                elif 0 > Rx_n >= self.filas  or 0 > Ry_n - 1 >= self.columnas or self.entorno[Rx_n][Ry_n-1]:
                    return None


                for palet in lista_palets_quietos:

                    # Que no se meta en otro palet
                    if Rx_n == palet.pos_x and Ry_n == palet.pos_y:
                        return None


                    if palet.ang_actual == 1: # Si el otro palet esta en vertical

                        # Al estar en vertical el robot no se puede mover 1 encima o debajo
                        # de la posicion del palet
                        # PENDIENTE
                        if palet.pos_x == Rx_n and (palet.pos_y-1 == (Ry_n) or palet.pos_y == (Ry_n) or palet.pos_y+1 == (Ry_n)):
                            return None
                        
                    else:
                       # Mira alrededor del otro palet, no se puede mover ahi.
                        for ancho in range(-1,1):
                            for alto in range(-1,1):
                                if Rx_n == palet.pos_x +ancho and Ry_n == palet.pos_y + alto:
                                    return None
            else:
                # Si lo lleva en horizontal


                
                # Que no choque con entorno el palet MIRAR SI ES REAL
                if 0 > Rx_n+1 > self.filas  or 0 > Ry_n  > self.columnas or self.entorno[Rx_n+1][Ry_n]:
                    return None
                elif 0 > Rx_n-1 > self.filas  or 0 > Ry_n  > self.columnas or self.entorno[Rx_n-1][Ry_n]:
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
                


            #PENDIENTE DE SI LLEVA EL PALET EN HORIZONTAL
            if Palet_movido != None:
                lista_palets_nueva = lista_palets_quietos.append(Palet_movido)  # type: ignore


    
        return Estado(Rx_n,Ry_n,Rang,R_levan,Lista_palets=lista_palets_nueva) #type:ignore
    


    def expandir(self,profundidad= 100):
        """
        Expande a partir del primer elemento de la lista abierta de estados.

        
        
        """

        ciclos = 0
        Exito = False

        while len(self.lis_abierta) > 0 and (profundidad >= ciclos) and Exito == False:

            repetido:bool = False
            sucesores: "list[Estado]" =[]

            estado_sacado: Estado = self.lis_abierta.pop(0)


            # Hacer aqui comprobaciones de que el que se saca existe.





            print("Profundidad: ",ciclos)
            ciclos = ciclos+1
            if estado_sacado not in self.lis_cerrada:
                print("Nuevo")
                self.lis_cerrada.append(estado_sacado)

                if estado_sacado == self.estado_final or self.heuristica_total(estado_sacado) == 0:
                    Exito = True
                    print("Llegado al final")
                    self.imprimir(estado_sacado,self.entorno)


            else:
                print("Repetido")
                repetido:bool = True

            if repetido == False:
                # Añadir cuando puede avanzar
                """
                Pendiente hacer que haga bastantes distancias,
                hacer bucle  o algo asi.
                
                """
                estado_nuevo = self.avanzar(estado_sacado)
                if estado_nuevo != None:
                    sucesores.append(estado_nuevo)

                # Cuando puede girar izq
                estado_nuevo = self.girar_izq(estado=estado_sacado)
                if estado_nuevo != None:
                    sucesores.append(estado_nuevo)

                # Cuando puede girar der
                estado_nuevo = self.girar_der(estado=estado_sacado)
                if estado_nuevo != None:
                    sucesores.append(estado_nuevo)


                # levantar o bajar palet
                estado_nuevo = self.levantar_bajar(estado=estado_sacado)
                if estado_nuevo != None:
                    sucesores.append(estado_nuevo)


            
            # Imprimir los sucesores generados
            #print("Num estados: ", len(sucesores)); print(sucesores)
            if Exito == False:
                for s in sucesores:
                    if s != None :
                        print("Estado coste:", self.heuristica_total(s,0))
                        self.imprimir(s,self.entorno)
                        self.lis_abierta.append(s)

            
            repetido:bool = False


        if len(self.lis_abierta)== 0 and Exito == False:
            print("Error, no se encontro solucion")

        print("Exito: ", Exito)
        return None

          

    def imprimir(self,estado: Estado ,entorno) -> None:
        
        #mapa = [[0 for i in range(self.filas)] for j in range(self.columnas)]
        mapa = np.copy(entorno)

        if estado != None:
            mapa[estado.Robot_x][estado.Robot_y] =  2#ord(estado.Robot_orientacion)//10

            if estado.Lista_estanterias != None:
                for palet in estado.Lista_estanterias:
                    if palet.ang_actual == 1:
                        mapa[palet.pos_x][palet.pos_y] = 6
                        mapa[palet.pos_x][palet.pos_y+1] = 8
                        mapa[palet.pos_x][palet.pos_y-1] = 8


                    else:
                        mapa[palet.pos_x][palet.pos_y] = 9
                        mapa[palet.pos_x+1][palet.pos_y] = 8        
                        mapa[palet.pos_x-1][palet.pos_y] = 8



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

    entorno = [
        [0, 0, 0, 0,1],
        [0, 0, 0, 0,0],
        [0, 0, 0, 0,0],
        [0, 0, 0, 0,0]
    ]

    paletillos = [Palet(1,1,True,1,1,False)]
    paletillos_obj = [Palet(1,1,True,1,1,False)]  # Borrar cuando se haga a*, utilizar distancia actual a deseada como valor h(n)

    situacion1 = Estado(0,0,"E",False,paletillos)
    situacion2 = Estado(0,0,"E",False,paletillos)

    situacion_final = Estado(0,0,"E",False,paletillos_obj)

    print(situacion1==situacion_final)


    buscador = Busqueda(situacion1,situacion_final,entorno)


    buscador.expandir(profundidad=10000)
    #print(situacion1==situacion2)



    return None


if __name__ == "__main__":
    main()