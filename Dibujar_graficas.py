import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

def main():


    for n in range(0,50):
        grafica_uso_memoria: bool = False
        n_mundo = n
        try:
            memoria_ciclo = np.loadtxt("uso_memoria_mundo_" + str(n_mundo) +  ".csv", delimiter=",")
            grafica_uso_memoria = True
        except:
            pass

        try:
            tiempos_ciclo = np.loadtxt("tiempos_mundo_"+ str(n_mundo) + ".csv", delimiter=",")
            tiempos_ciclo_suavizado = np.convolve(tiempos_ciclo,[0.05,0.15,0.6,0.15,0.05],mode="same")
            if grafica_uso_memoria:
                plt.subplot(2,1,1)
                plt.plot(tiempos_ciclo_suavizado*1000)
                plt.title("Tiempos de cálculo por ciclo" + " Mundo " +str(n_mundo))
                plt.xlabel("Ciclo")
                plt.ylabel("Tiempo (ms)")
                plt.grid()


                memoria_ciclo = np.loadtxt("uso_memoria_mundo_" + str(n_mundo) +  ".csv", delimiter=",")
                plt.subplot(2,1,2)
                plt.plot(memoria_ciclo)
                plt.title("Uso de memoria por ciclo" + " Mundo " +str(n_mundo))
                plt.xlabel("Ciclo")
                plt.ylabel("Memoria (bytes)")

                plt.show()
        
            else:
                plt.subplot(1,1,1)
                plt.plot(tiempos_ciclo*1000)
                plt.title("Tiempos de cálculo por ciclo" + " Mundo " +str(n_mundo))
                plt.xlabel("Ciclo")
                plt.ylabel("Tiempo (ms)")
                plt.grid()
                plt.show()

        except:
            pass


if __name__ == "__main__":
    main()