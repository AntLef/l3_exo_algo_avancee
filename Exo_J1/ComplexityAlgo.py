import numpy as np
import matplotlib.pyplot as plt
import math


class ComplexityAlgo:

    def __init__(self, i):
        self.i = i

    def Logarithmic(self):
        return np.log10(self.i)

    def Linear(self):
        return self.i

    def Quasilinear(self):
        return self.i * math.log10(self.i)

    def Quadratic(self):
        return pow(self.i, 2)

    def Exponential(self):
        return pow(2, self.i)

    """
    ╔══════════════════╦═════════════════╗
    ║       Name       ║ Time Complexity ║
    ╠══════════════════╬═════════════════╣
    ║ Constant Time    ║       O(1)      ║
    ╠══════════════════╬═════════════════╣
    ║ Logarithmic Time ║     O(log n)    ║
    ╠══════════════════╬═════════════════╣
    ║ Linear Time      ║       O(n)      ║
    ╠══════════════════╬═════════════════╣
    ║ Quasilinear Time ║    O(n log n)   ║
    ╠══════════════════╬═════════════════╣
    ║ Quadratic Time   ║      O(n^2)     ║
    ╠══════════════════╬═════════════════╣
    ║ Exponential Time ║      O(2^n)     ║
    ╠══════════════════╬═════════════════╣
    ║ Factorial Time   ║       O(n!)     ║
    ╚══════════════════╩═════════════════╝
    """