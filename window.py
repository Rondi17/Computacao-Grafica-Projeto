from graphicsitem import *
import numpy as np
import math

class Mundo():
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.padrao_x_min = x_min
        self.padrao_x_max = x_max
        self.padrao_y_min = y_min
        self.padrao_y_max = y_max

    def getCenterX(self):
        return self.x_max - self.x_min

    def getCenterY(self):
        return self.y_max - self.y_min
    
    def getCenterX_padrao(self):
        return self.padrao_x_max - self.padrao_x_min

    def getCenterY_padrao(self):
        return self.padrao_y_max - self.padrao_y_min

    def getCenter(self):
        return [self.getCenterX(), self.getCenterY()]
    
    def getXmin(self):
        return self.x_min
    
    def setXmin(self, value):
        self.x_min = value
    
    def getYmin(self):
        return self.y_min
    
    def setYmin(self, value):
        self.y_min = value

    def getXmax(self):
        return self.x_max
    
    def setXmax(self, value):
        self.x_max = value

    def getYmax(self):
        return self.y_max
    
    def setYmax(self, value):
        self.y_max = value
    


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
        self.pan_factor = 0.1
    
    def print(self):
        print("centrox:", self.centerX)
        print("centroy: ", self.centerY)

    def scn(self, width, height):
        dx = self.x_min
        dy = self.y_min

        translate_matrix = np.array([[1, 0, 0],
                        [0, 1, 0],
                        [-self.centerX, -self.centerY, 1]])

        rotate_matrix = np.array([[math.cos(math.radians(self.degrees)), -(math.sin(math.radians(self.degrees))), 0],
                         [math.sin(math.radians(self.degrees)), math.cos(math.radians(self.degrees)), 0],
                         [0, 0, 1]])

        normalization_matrix = np.array([[1 / (width/2), 0, 0],
                                         [0, 1 / (height/2), 0],
                                         [0, 0, 1]])

        combined_matrix = np.matmul(np.matmul(translate_matrix, rotate_matrix), normalization_matrix)
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

    def getCenterX(self):
        return self.padrao_x_max - self.padrao_x_min

    def getCenterY(self):
        return self.padrao_y_max - self.padrao_y_min

    def getCenter(self):
        return [self.getCenterX(), self.getCenterY()]
