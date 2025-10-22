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

        return False
                

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


        return None
    



    def heuristica_1(self,estado_comprobar: Estado) -> int:

        return 4




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



        if rob_activado == 0:
            robot_angulo = self.rotar_derecha[robot_angulo]


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
            lleva_vertical: bool = False
            
            # Aqui se meten los palets que no se mueven, 
            # para despues no comparar el que se mueve consigo mismo
            lista_palets_quietos: "list[Palet] " = []   


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

            lista_palets_nueva = lista_palets_quietos.append(Palet_movido)  # type: ignore


        return Estado(Rx_n,Ry_n,Rang,R_levan,Lista_palets=lista_palets_nueva) #type:ignore


    def expandir(self, estado_dado: Estado):

        sucesores: "list[Estado]" =[]




        # Añadir cuando puede avanzar
        """
        Pendiente hacer que haga bastantes distancias,
        hacer bucle  o algo asi.
        
        """
        estado_nuevo = self.avanzar(estado_dado)
        if estado_nuevo != None:
            sucesores.append(estado_nuevo)



        # Cuando puede girar izq
        estado_nuevo = self.girar_izq(estado=estado_dado)
        if estado_nuevo != None:
            sucesores.append(estado_nuevo)

        # Cuando puede girar der
        estado_nuevo = self.girar_der(estado=estado_dado)
        if estado_nuevo != None:
            sucesores.append(estado_nuevo)


        # levantar o bajar palet
        estado_nuevo = self.levantar_bajar(estado=estado_dado)
        if estado_nuevo != None:
            sucesores.append(estado_nuevo)


        # Imprimir los sucesores generados
        print("Num estados: ", len(sucesores)); print(sucesores)
        for s in sucesores:
            if s != None:
                print("Estado:")
                self.imprimir(s,self.entorno)




        return sucesores


    def imprimir(self,estado: Estado ,entorno) -> None:
        
        #mapa = [[0 for i in range(self.filas)] for j in range(self.columnas)]
        mapa = np.copy(entorno)

        if estado != None:
            mapa[estado.Robot_x][estado.Robot_y] =  2#ord(estado.Robot_orientacion)//10

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

    paletillos = [Palet(1,1,True,1,1,False),Palet(2,3,False,3,3,False)]
    situacion1 = Estado(0,0,"E",False,paletillos)

    situacion_final = Estado(2,3,"E",False,paletillos)

    buscador = Busqueda(situacion1,situacion_final,entorno)


    buscador.expandir(situacion1)

    return None


if __name__ == "__main__":
    main()