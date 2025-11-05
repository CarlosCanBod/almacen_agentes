from Planificador import Palet,Estado, Busqueda
import matplotlib.pyplot as plt

def cargar_entornos() -> list[list[list[int]]]:
    entorno0 = [
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
    entorno1 = [
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

    entorno2 = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

    entorno3 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [9, 9, 9, 9, 0, 9, 9, 9, 9 ,9 ,9 ,9 ,9 ,9 ,9 ,9 ,9 ,9 ,9 ,9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,9 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,9 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 9, 9, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0 ,9 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]    
        ]




    return [entorno0,entorno1,entorno2,entorno3]

def cargar_estados() -> list[Estado]:
    # Mundo 0
    paletillos = [Palet(5,2,False,1,5,True)] 
    situacion0 = Estado(8,4,"N",False,paletillos)

    # Mundo 1
    paletillos = [Palet(9,3,False,9,3,False),Palet(7,3,False,7,3,False), # Palets izquierda
                     Palet(9,5,False,2,5,False),Palet(7,5,False,7,5,False),
                          
                        Palet(9,10,False,9,10,False),Palet(7,10,False,1,7,True), # Palets derecha
                        Palet(9,12,False,9,12,False),Palet(7,12,False,7,12,False)
                          ]                             # Palets mas arriba
    situacion1 = Estado(12,7,"N",False,paletillos)

    # Mundo 2
    paletillos = [Palet(4,1,True,1,1,True),Palet(4,5,True,1,5,True)] 
    situacion2 = Estado(0,3,"E",False,paletillos)


    # Mundo 3
    paletillos = [Palet(20,10,False,7,17,False)]
    situacion3 = Estado(0,0,"S",False,paletillos)

    return [situacion0,situacion1,situacion2,situacion3]

def main():
    buscador = None
    camino = 0

    lista_entornos = cargar_entornos()
    situaciones = cargar_estados()
    try:
        with open("PRUEBA_BORRAR.txt","x") as f:
            pass
        f.close()
    except: pass
   
    
    for i in range(0,len(situaciones)):
        if lista_entornos[i] == None:
            print("Falta entono")
            break
        pesos_h = [5,1,2]
        buscador = Busqueda(situaciones[i],lista_entornos[i],pesos=pesos_h)

        buscador.resolver(profundidad=25000)

        if buscador != None:
            lista_tiempos = buscador.lis_tiempo_ciclo
            tiempo_medio = sum(lista_tiempos)/len(lista_tiempos)
            with open("PRUEBA_BORRAR.txt","a") as w:
                w.writelines("Mundo: " + str(i) + "\n")
                w.writelines("Pesos: " + str(pesos_h) + "\n")
                w.writelines("Tiempo total calculo: " + str(buscador.tiempo_total)+ "\n")
                w.writelines("Coste total camino: " + str(buscador.coste_final)+ "\n")
                w.writelines("Longitud plan: " + str(buscador.longitud_camino)+ "\n")
                w.writelines("Nodos expandidos: " + str(buscador.nodos_expandidos)+ "\n")
                w.writelines("Tiempo medio ciclo: " + str(tiempo_medio)+ "\n")
                w.writelines("\n")

            w.close()
            
            print("Tiempo total calculo: ", buscador.tiempo_total)
            print("Coste total camino: ", buscador.coste_final)
            
            print("Longitud plan: ", buscador.longitud_camino)
            print("Nodos expandidos: ",buscador.nodos_expandidos)

            lista_tiempos = buscador.lis_tiempo_ciclo
            
            print("Tiempo medio ciclo: ", tiempo_medio)

            #plt.plot(lista_tiempos)
            #plt.show()


    return None


if __name__ == "__main__":
    main()