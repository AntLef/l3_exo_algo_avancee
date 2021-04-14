import numpy as np
import matplotlib.pyplot as plt
import math

from Exo_J1.ComplexityAlgo import ComplexityAlgo


class BigSleep:

    def __init__(self):
        self

    def exo_1_1(self, n: int):
        print("\nExo 1_1")
        plt.plot(np.array([ComplexityAlgo(i).Logarithmic() for i in range(1, n)]))
        plt.plot(np.array([ComplexityAlgo(i).Linear() for i in range(1, n)]))
        plt.plot(np.array([ComplexityAlgo(i).Quasilinear() for i in range(1, n)]))
        plt.plot(np.array([ComplexityAlgo(i).Quadratic() for i in range(1, n)]))
        plt.plot(np.array([ComplexityAlgo(i).Exponential() for i in range(1, n)]))
        # Function add a legend
        plt.legend(['log(n)', 'n', 'n log(n)', 'n²', '2^n'])
        plt.show()
        print("voir graphique")

    def exo_1_2(self):
        print("\nExo 1_2")
        sec = 1
        print("Pour", sec, "secondes : ")

        i = (float(sec)) / 10 ** -7

        print("Nombre d'i possible :", i)
        print("log(n) :",   ComplexityAlgo(i).Logarithmic())
        print("n :",        ComplexityAlgo(i).Linear())
        print("n log(n) :", ComplexityAlgo(i).Quasilinear())
        print("n² :",       ComplexityAlgo(i).Quadratic())
        print("2^n :", "Result too large, see right comment") # ComplexityAlgo(i).Exponential()

    def exo_1_3(self, list):
        print("\nExo 1_3")

        def ifPermQ(table):
            return "true" if max(table) <= len(table) and len(set(table)) == len(table) else "false"

        def ifPermL(table):
            return "true" if len([i for i in table if i <= len(table)]) == len(table) else "false"

        print("list :", list)
        print(ifPermQ(list))
        print(ifPermL(list))

    def exo_1_4(self, n):
        print("\nExo 1_4")
        """
                            (n2 – 3n -1 ) / (n+1)
        ordre de grandeur = O(n²)
                            (n log(n) +n² + log(n)²)/ (n+1)
        ordre de grandeur = O(log(n)²)
        """
        print("result :")
        print("(n2 – 3n -1 ) / (n+1)           =", ( (n**2) - (3**n) -1 ) / (n+1))
        print("(n log(n) +n² + log(n)²)/ (n+1) =", ( (n * ComplexityAlgo(n).Logarithmic()) + n**2 + (ComplexityAlgo(n).Logarithmic()**2) ) / (n+1))

    def exo_2_1(self):
        print("\nExo 2_1")

        def sortBySelection(tab):
            for i in range(len(tab)):
                min = i
                for j in range(i + 1, len(tab)):
                    if tab[min] > tab[j]:
                        min = j

                tmp = tab[i]
                tab[i] = tab[min]
                tab[min] = tmp
            return tab

        tab = [98, 22, 15, 32, 2, 74, 63, 70]

        print("le tableau avant le tri est :", tab)
        sortBySelection(tab)
        print("Le tableau après le tri est :", tab)

    def exo_2_2(self):
        print("\nExo 2_2")
        print("Terminaison      : Basculant à chaques iteration la plus petite valeur dans une autres liste, "
              "la terminaison est assuré")
        print("Complétude       : Tant que la liste contient des nombres comparables la complétude est assurée")

    def exo_2_3(self):
        print("\nExo 2_3")
        print("Coût             : Son cout équivaut à n (algo linéaire)")

    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================

    def print(self):
        BigSleep().exo_1_1(4)
        BigSleep().exo_1_2()
        BigSleep().exo_1_3([1, 2, 5, 3, 7, 4])
        BigSleep().exo_1_4(2)

        BigSleep().exo_2_1()
        BigSleep().exo_2_2()
        BigSleep().exo_2_3()


if __name__ == '__main__':
    BigSleep().print()
