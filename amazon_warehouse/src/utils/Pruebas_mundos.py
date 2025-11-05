from Planificador import Palet,Estado, Busqueda
import matplotlib.pyplot as plt

def main():
    mundo_simulado = 2
    buscador = None
    camino = 0

    if mundo_simulado == 0:
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