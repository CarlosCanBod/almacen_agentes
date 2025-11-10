import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

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

            if len(tiempos_ciclo) < 5000:
                radio_gaus: int = 3
            else:
                radio_gaus:int = 50


            tiempos_ciclo_suavizado = ndimage.gaussian_filter1d(tiempos_ciclo*1000,radio_gaus)
            #tiempos_ciclo_suavizado = np.convolve(tiempos_ciclo,nucleo,mode="same")
            if grafica_uso_memoria:
                plt.subplot(2,1,1)
                plt.plot(tiempos_ciclo_suavizado)
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
                plt.plot(tiempos_ciclo_suavizado)
                plt.title("Tiempos de cálculo por ciclo" + " Mundo " +str(n_mundo))
                plt.xlabel("Ciclo")
                plt.ylabel("Tiempo (ms)")
                plt.grid()
                plt.show()

        except Exception as e:
            pass


if __name__ == "__main__":
    main()