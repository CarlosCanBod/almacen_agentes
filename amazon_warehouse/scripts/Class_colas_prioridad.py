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


            return nodo_actual
        else:
            pass