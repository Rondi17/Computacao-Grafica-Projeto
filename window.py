from graphicsitem import *
import numpy as np
import math

class Mundo():
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


class Window():
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.padrao_x_min = x_min
        self.padrao_x_max = x_max
        self.padrao_y_min = y_min
        self.padrao_y_max = y_max
        
        self.centerX = self.x_max - self.x_min
        self.centerY = self.y_max - self.y_min
        self.Vup : Reta
        self.degrees = 0
        self.pan_factor = 1

    def calculate_sen_cos(self, view_up):

        #vetor que representa eixo y = (0,1)
        produto_interno = view_up[0] * 0 + view_up[1] * 1 + view_up[2] * 1

        #produto escalar
        a = view_up[0]
        b = view_up[1]
        c = view_up[2]
        a *= a
        b *= b
        c *= c
        norma_view_up = np.sqrt(a + b + c)
        norma_eixo_y = 1.4142135623730951

        cos_theta = produto_interno / (norma_view_up * norma_eixo_y)
        sen_theta = np.sqrt(1 - np.power(cos_theta, 2))

        rotate_matrix = np.array([[cos_theta, -sen_theta, 0],
                                  [sen_theta, cos_theta, 0],
                                  [0, 0, 1]])

        return cos_theta, sen_theta

    def scn(self, degrees, width, height):
        #matriz composta = matriz translacao * matriz rotacao *
        dx = self.x_min + 0.5
        dy = self.y_min + 0.5

        translate_matrix = np.array([[1, 0, 0],
                        [0, 1, 0],
                        [dx, dy, 1]])

        rotate_matrix = np.array([[math.cos(math.radians(degrees)), -(math.sin(math.radians(degrees))), 0],
                         [math.sin(math.radians(degrees)), math.cos(math.radians(degrees)), 0],
                         [0, 0, 1]])

        normalization_matrix = np.array([[2 / width, 0, 0],
                                         [0, 2 / height, 0],
                                         [0, 0, 1]])
        combined_matrix = np.dot(translate_matrix, np.dot(rotate_matrix, normalization_matrix))
        return combined_matrix

    def pan_right(self):
        self.x_min -= self.pan_factor
        self.x_max -= self.pan_factor

    def pan_left(self):
        self.x_min += self.pan_factor
        self.x_max += self.pan_factor

    def pan_up(self):
        self.y_min -= self.pan_factor
        self.y_max -= self.pan_factor

    def pan_down(self):
        self.y_min += self.pan_factor
        self.y_max += self.pan_factor
    
    def draw(self):
        lista = []
        obj1 = Reta(self.x_min, self.y_min, self.x_max, self.y_min)
        obj2 = Reta(self.x_min, self.y_min, self.x_min, self.y_max)
        obj3 = Reta(self.x_min, self.y_max, self.x_max, self.y_max)
        obj4 = Reta(self.x_max, self.y_min, self.x_max, self.y_max)
        lista.append(obj1)
        lista.append(obj2)
        lista.append(obj3)
        lista.append(obj4)
        return lista

    