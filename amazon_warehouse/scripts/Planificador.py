from typing import Any
import numpy as np  # Se usa para copiar el entorno para el mapa.

from Class_colas_prioridad import cola_prio,nodo_cola_prioridad


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
                hash_palets = hash(palet) + hash_palets


        return hash((self.Robot_x,self.Robot_y,self.Robot_orientacion,self.Robot_activado,hash_palets))


class Busqueda():

    def __init__(self,estado_inicial: "Estado", entorno: "list[list]") -> None:
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
        self.estado_actual = estado_inicial


        self.filas = len(entorno)
        self.columnas = len(entorno[0])

        self.entorno = entorno



        #self.lis_abierta: "list[Estado]" = [estado_inicial]
        self.lis_cerrada: "list[nodo_cola_prioridad]" = []

        self.lis_abierta = cola_prio()    

        self.lis_abierta.insertar(estado_inicial,prioridad=self.heuristica_total(estado_inicial))


        return None
    
    def heuristica_robot_origen(self,robot_x,robot_y,robot_orientacion,rob_activado)-> int:
        coste = abs(self.estado_ini.Robot_x- robot_x) + abs(self.estado_ini.Robot_y - robot_y)

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


                if palet.x_objetivo==palet.pos_x and palet.y_objetivo==palet.pos_y:
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
            x2 = palet.pos_x
            y2 = palet.pos_y
            x3= palet.x_objetivo
            y3 = palet.y_objetivo
            
            if x2 != x3 or y2 != y3:
                dist = abs(x2-x1) + abs(y2-y1)
                coste = coste + dist
            
        return coste



    

    def heuristica_total(self,estado_comprobar: Estado) -> int:
        
        
        coste_robot_origen = 0
        coste_palets_robot = 0

        #coste_robot_origen = self.heuristica_robot_origen(estado_comprobar.Robot_x,estado_comprobar.Robot_y, estado_comprobar.Robot_orientacion,estado_comprobar.Robot_activado)
        coste_palets_objetivo = 0

        if len(estado_comprobar.Lista_estanterias):
            coste_palets_objetivo: int = (self.heuristica_palets1(estado_comprobar))

            coste_palets_robot = self.heur_robot_palet(estado_comprobar) 
    
        coste_total = coste_palets_objetivo + coste_robot_origen + coste_palets_robot

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

    def girar_izq(self, estado: Estado) -> Any:
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

            # Que no pueda girar en los bordes con palet
            if cord_robot_x == 0 or cord_robot_x == self.columnas-1:
                return None
            if cord_robot_y == 0 or cord_robot_y == self.filas-1:
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


    def girar_der(self, estado: Estado) -> Any:
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

#            Que no pueda girar en los bordes con palet
            if cord_robot_x == 0 or cord_robot_x == self.columnas -1:
                return None
            if cord_robot_y == 0 or cord_robot_y == self.filas -1:
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
        if self.entorno[Rx_n][Ry_n]:
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
                    if 0 > Rx_n >= self.filas  or 0 > Ry_n + 1 >= self.columnas or self.entorno[Rx_n][Ry_n+1]:
                        return None
                    elif 0 > Rx_n >= self.filas  or 0 > Ry_n - 1 >= self.columnas or self.entorno[Rx_n][Ry_n-1]:
                        return None
                except:
                    return None

                for palet in lista_palets_quietos:

                    # Que no se meta en otro palet
                    if Rx_n == palet.pos_x and Ry_n == palet.pos_y:
                        print("Choque 1")
                        return None


                    if palet.ang_actual == 1: # Si el otro palet esta en vertical

                        # Al estar en vertical el robot no se puede mover 1 encima o debajo
                        # de la posicion del palet
                        # PENDIENTE
                        if palet.pos_x == Rx_n and (palet.pos_y-1 == (Ry_n) or palet.pos_y == (Ry_n) or palet.pos_y+1 == (Ry_n)):
                            print("Choque 2")

                            return None
                        
                    else:
                       # Mira alrededor del otro palet, no se puede mover ahi.
                        for ancho in range(-1,1):
                            for alto in range(-1,1):
                                if Rx_n == palet.pos_x +ancho and Ry_n == palet.pos_y + alto:
                                    print("Choque 3")
                                    return None
            else:
                # Si lo lleva en horizontal

                if Rx_n == 0 or Rx_n == self.columnas -1 :
                    return None


                try:
                    if 0 > Rx_n+1 > self.filas  or 0 > Ry_n  > self.columnas or self.entorno[Rx_n+1][Ry_n]:
                        return None
                    elif 0 > Rx_n-1 > self.filas  or 0 > Ry_n  > self.columnas or self.entorno[Rx_n-1][Ry_n]:
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
    


    def expandir(self,profundidad= 100):
        """
        Expande a partir del primer elemento de la lista abierta de estados.

        
        
        """

        

        ciclos = 0
        Exito = False
        estado_sacado = None    #type: ignore
        coste_sacado = 0

        while  (profundidad >= ciclos) and Exito == False:

            repetido:bool = False
            sucesores: "list[Estado]" =[]

            estado_coste = self.lis_abierta.extraer()

            if estado_coste == None:
                break

            estado_sacado: Estado = estado_coste.dato
            coste_sacado: int = estado_coste.prioridad


            if ciclos%10 == 0:
                print("Profundidad: ",ciclos)
                c_h = self.heuristica_total(estado_sacado)
                print("Coste H: ",c_h)

            ciclos = ciclos+1
            coste_g = 0

            if estado_coste not in self.lis_cerrada:
                #print("Nuevo")
                self.lis_cerrada.append(estado_coste)
                c_h = self.heuristica_total(estado_sacado)

                #print("Coste H: ",c_h)
                coste_g = coste_sacado-c_h                         
                
                #print("Coste G: ",coste_g)
                #print("Coste F: ",coste_sacado)


                #self.imprimir(estado_sacado,self.entorno)

                #print("Se saca el estado de arriba")
                if self.heuristica_total(estado_sacado) == 0:
                    Exito = True
                    print("Llegado al final")

                    print("Coste H: ",c_h)
                    print("Coste G: ",coste_g)

                    self.imprimir(estado_sacado,self.entorno)

            else:

                #print("Repetido")
                repetido:bool = True


            if repetido == False:

                # Añadir cuando puede avanzar
                """
                Pendiente hacer que haga bastantes distancias,
                hacer bucle  o algo asi.
                
                """
                estado_avance: Estado = self.avanzar(estado_sacado)
                if estado_avance != None:
                    coste_h = self.heuristica_total(estado_avance)
                    if estado_avance.Robot_activado:
                        coste_g1 = coste_g + 2
                    else:
                        coste_g1 = coste_g + 1 

                    coste_f_nuevo = coste_h + coste_g1

                    sucesores.append(estado_avance)
                    self.lis_abierta.insertar(dato=estado_avance,prioridad=coste_f_nuevo)


                estado_gir_der: Estado = self.girar_der(estado_sacado)
                if estado_gir_der != None:
                    coste_h = self.heuristica_total(estado_gir_der)

                    if estado_gir_der.Robot_activado:
                        coste_g1 = coste_g + 4
                    else:
                        coste_g1 = coste_g +3

                    coste_f_nuevo = coste_h + coste_g1

                    sucesores.append(estado_gir_der)
                    self.lis_abierta.insertar(dato=estado_gir_der,prioridad=coste_f_nuevo)


                estado_gir_izq: Estado = self.girar_izq(estado_sacado)
                if estado_gir_izq != None:
                    coste_h = self.heuristica_total(estado_gir_izq)

                    if estado_gir_der.Robot_activado:
                        coste_g1 = coste_g + 4
                    else:
                        coste_g1 = coste_g + 3
                   
                    coste_f_nuevo = coste_h + coste_g1

                    sucesores.append(estado_gir_izq)
                    self.lis_abierta.insertar(dato=estado_gir_izq,prioridad=coste_f_nuevo)
               


                estado_levantar: Estado = self.levantar_bajar(estado_sacado)
                if estado_levantar != None:
                    coste_h = self.heuristica_total(estado_levantar)

                    coste_g1 = coste_g + 3

                    coste_f_nuevo = coste_h + coste_g1

                    sucesores.append(estado_levantar)
                    self.lis_abierta.insertar(dato=estado_levantar,prioridad=coste_f_nuevo)


     
            # Imprimir los sucesores generados
            if Exito == False:
                #print(self.lis_abierta)

                print("Cantidad sucesores creados: ", len(sucesores))
                for s in sucesores:
                    if s != None :
                        print("Coste H abajo:", self.heuristica_total(s))
                        print("Coste G abajo:",coste_sacado - self.heuristica_total(s))

                        self.imprimir(s,self.entorno)

            repetido:bool = False

            if self.lis_abierta.vacio():
                break


        if len(self.lis_abierta) == 0 and Exito == False:
            print("Error, no se encontro solucion")

        if estado_sacado != None:

            c_h = self.heuristica_total(estado_sacado)

            print("Coste H: ",c_h)
            coste_g = coste_sacado-c_h 
            print("Coste G: ",coste_g)

            self.imprimir(estado_sacado,self.entorno)

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

                        try:
                            mapa[palet.pos_x][palet.pos_y+1] = 8
                        except:
                            pass

                        try:
                            mapa[palet.pos_x][palet.pos_y-1] = 8
                        except:
                            pass

                    else:
                        mapa[palet.pos_x][palet.pos_y] = 9
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

    entorno = [
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0]
        #[0, 0, 0, 0,0,0]
    ]

   
    paletillos = [Palet(3,3,True,2,2,False)] #[Palet(1,1,True,1,4,True),Palet(3,1,True,3,4,True)]

    situacion1 = Estado(0,0,"E",False,paletillos)

    buscador = Busqueda(situacion1,entorno)

    buscador.expandir(profundidad=2000)

 

    return None


if __name__ == "__main__":
    main()
