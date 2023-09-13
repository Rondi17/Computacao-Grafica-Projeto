from graphicsitem import *
import numpy as np
import math


class Window():
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.padrao_x_min = x_min
        self.x_max = x_max
        self.padrao_x_max = x_max

        self.y_min = y_min
        self.padrao_y_min = y_min
        self.y_max = y_max
        self.padrao_y_max = y_max
        
        self.centerX = self.x_max - self.x_min
        self.centerY = self.y_max - self.y_min
        self.Vup : Reta

    def move(self, degrees, dx, dy):
        #matriz composta = matriz translacao * matriz rotacao *

        #1matriz detranslacao
        translate_matrix = np.array([[1, 0, 0],
                        [0, 1, 0],
                        [dx, dy, 1]])
        
        #2 matriz de rotacao
        rotate_matrix = np.array([[math.cos(math.radians(degrees)), -(math.sin(math.radians(degrees))), 0],
                         [math.sin(math.radians(degrees)), math.cos(math.radians(degrees)), 0],
                         [0, 0, 1]])

        #3 - Normalize o conteúdo da window, realizando um escalonamento do mundo
        #3 matriz de normalizacao para 1x1
        normalization_matriz = np.array([[1, 0, 0],
                                         [0, 1, 0],
                                         [0, 0, 1]])

        #aplique isso na widow, e passa a matriz coposta como parametro
        combined_matrix = np.dot(translate_matrix, np.dot(rotate_matrix, normalization_matriz))
        print("resultado = ", combined_matrix)
        return combined_matrix

    def pan_right(self):
        dx = 10
        return dx

    def pan_left(self):
        self.x_min += self.pan_factor
        self.x_max += self.pan_factor

    def pan_up(self):
        self.y_min -= self.pan_factor
        self.y_max -= self.pan_factor

    def pan_down(self):
        self.y_min += self.pan_factor
        self.y_max += self.pan_factor

    