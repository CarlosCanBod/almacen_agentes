#!/usr/bin/env python
import rospy    #type: ignore

from utils import navigation
from utils import Planificador as pl


print("ADIOSSS")


class Practica1:

    def __init__(self):

        self.nav = navigation.Navigation()
        self.execSearch()
        #self.execTest0()
        # NOTA: Implementar la funcion execSearch con el algoritmo de busqueda seleccionado. Una vez implementado, descomentar la llamada a la funcion en este init, generar el plan a partir de las
        # peticiones (requests) que reciba, y ejecutarlo en Gazebo

	

     

    def execSearch(self):
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

    
        paletillos = [pl.Palet(5,2,False,1,5,True)] #[Palet(1,1,True,1,4,True),Palet(3,1,True,3,4,True)] 1,4

        situacion1 = pl.Estado(8,4,"N",False,paletillos)

        buscador = pl.Busqueda(situacion1,entorno)

        camino_junto = buscador.expandir(profundidad=15000)

        if camino_junto != None:
            camino_pasos = camino_junto.split(".")

            for orden in camino_pasos:

                if orden == "A":
                    self.nav.move(1)
                elif orden == "GD":
                    self.nav.rotateRight()
                elif orden == "GI":
                    self.nav.rotateLeft()
                elif orden == "S":
                    self.nav.upLift()
                elif orden == "B":
                    self.nav.downLift()
                else:
                    print("Instruccion: ",orden, " ignorada")


        else:
            print("No encontrado camino")




    def execTest0(self):
        print("TEST WAREHOUSE0")
        
        self.nav.move(1)
        self.nav.rotateLeft()
        self.nav.move(1)
        self.nav.rotateRight()
        self.nav.move(2)
        self.nav.rotateLeft()
        self.nav.move(1)
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.rotateLeft()
        self.nav.move(3)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.move(4)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.rotateLeft()
        self.nav.move(3)
        self.nav.rotateRight()
        self.nav.move(2)
        self.nav.rotateLeft()
        self.nav.move(4)
        self.nav.rotateLeft()
        self.nav.move(1)
        self.nav.rotateLeft() 









    def execTest1(self):
        print("TEST WAREHOUSE1")
        
        # First pallet
        self.nav.move(3)
        self.nav.rotateLeft()
        self.nav.move(2)
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.upLift()
        self.nav.move(2)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.move(7)
        self.nav.downLift()
        self.nav.rotateLeft()
        self.nav.upLift()
        self.nav.move(2)
        self.nav.downLift()
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.move(2)
        self.nav.rotateRight()

        # Second pallet       
        self.nav.move(5)
        self.nav.rotateLeft()
        self.nav.move(3)
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.upLift()
        self.nav.move(3)
        self.nav.rotateRight()
        self.nav.move(6)
        self.nav.downLift()
        self.nav.rotateRight()
        self.nav.rotateRight()
        self.nav.move(11)

        # Init position
        self.nav.rotateLeft()
        self.nav.rotateLeft()

if __name__ == '__main__':
    try:
        p = Practica1()
    except (RuntimeError, TypeError, NameError) as err:
        rospy.loginfo("Practica2 terminated: ", err)
