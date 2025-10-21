from typing import Any

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
            'N': (-1, 0),
            'S': (1, 0),
            'E': (0, 1),
            'O': (0, -1)
        }
        self.filas = len(entorno)
        self.columnas = len(entorno[0])

        self.entorno = entorno

        return None
    

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
        if 0 > Rx_n > self.filas  or 0 > Ry_n > self.columnas or self.entorno[Rx_n][Ry_n]:
            return None


        # El robot no baja o sube el palet aqui, queda igual
        R_levan = estado.Robot_activado

        if R_levan == False:
            # Comprobar que el robot no choca con patas de alguna estanteria
            for palet in estado.Lista_estanterias:
                if palet.ang_actual == 1: # Si el palet esta en vertical
                    # Al estar en vertical el robot no se puede mover 1 encima o debajo
                    # de la posicion del palet
                    if palet.pos_x == Rx_n and (palet.pos_y == (Ry_n-1) or palet.pos_y == (Ry_n+1) ):
                        return None
                else:
                    # Si esta horizontal, el robot no se puede poner 1 casilla por los lados
                    # en eje X,
                    if palet.pos_y == Ry_n and (palet.pos_x == (Rx_n-1) or palet.pos_x == (Rx_n+1) ):
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
                if 0 > Rx_n > self.filas  or 0 > Ry_n + 1 > self.columnas or self.entorno[Rx_n][Ry_n]:
                    return None
                elif 0 > Rx_n > self.filas  or 0 > Ry_n - 1 > self.columnas or self.entorno[Rx_n][Ry_n]:
                    return None


                for palet in lista_palets_quietos:
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



            #PENDIENTE DE SI LLEVA EL PALET EN HORIZONTAL

            lista_palets_nueva = lista_palets_quietos.append(Palet_movido)  # type: ignore


        return Estado(Rx_n,Ry_n,Rang,R_levan,Lista_palets=lista_palets_nueva) #type:ignore


    def expandir(self, estado_original: Estado):

        sucesores =[]

        # Añadir cuando puede avanzar
        # Cuando puede girar izq
        # Cuando puede girar der
        # Cuando levanta o baja palet


        return sucesores

def main():

    palet1 = Palet(0,0,True,3,3,True)

    print(palet1)

    return None


if __name__ == "__main__":
    main()