#!/usr/bin/env python
import rospy
from utils import navigation

class Practica1:

    def __init__(self):
        self.nav = navigation.Navigation()
	# NOTA: Implementar la funcion execSearch con el algoritmo de busqueda seleccionado. Una vez implementado, descomentar la llamada a la funcion en este init, generar el plan a partir de las
	# peticiones (requests) que reciba, y ejecutarlo en Gazebo
	# self.execSearch(requests)

	# NOTA: Estas dos lineas sirven para comprobar que el paquete funciona correctamente. Ejecutan un plan definido a mano. Deben ser comentadas/eliminadas una vez se implemente
	# execSearch
        self.execTest0()
        #self.execTest1()

    def execSearch(self,requests):
	print("SEARCH ")
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
