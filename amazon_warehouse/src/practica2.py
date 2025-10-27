#!/usr/bin/env python
import rospy    #type: ignore

from utils import navigation
from utils import Planificador 



print("ADIOSSS")


class Practica1:

    def __init__(self):

        self.nav = navigation.Navigation()
        self.execSearch()

        # NOTA: Implementar la funcion execSearch con el algoritmo de busqueda seleccionado. Una vez implementado, descomentar la llamada a la funcion en este init, generar el plan a partir de las
        # peticiones (requests) que reciba, y ejecutarlo en Gazebo

	

     

    def execSearch(self):
        entorno = [
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0,0,0]
        ]

        paletillos = [Planificador.Palet(2,2,False,2,3,True)] #[Palet(1,1,True,1,4,True),Palet(3,1,True,3,4,True)]

        situacion1 = Planificador.Estado(0,0,"S",False,paletillos)

        buscador = Planificador.Busqueda(situacion1,entorno)

        buscador.expandir(profundidad=5000)

	    # NOTA: Implementa aqui tu algoritmo de busqueda. Para ello, se pueden generar las clases, funciones, y ficheros adicionales que se consideren necesarios

        # DEBUG

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
