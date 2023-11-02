import numpy as np
import math
from graphicsitem import *

class Transformation():
    #--------------------------------- Translate ---------------------------------

    def get_translate_matrix(vector):
        return np.array([[1, 0, 0],
                        [0, 1, 0],
                        [vector[0], vector[1], 1]])
    
    def get_translate_toOrigin_matrix(vector):
        return np.array(([[1, 0, 0],
                        [0, 1, 0],
                        [-vector[0], -vector[1], 1]]))
    
    #----------------------------------- Scale ---------------------------------

    def get_scale_matrix(vector):
        return np.array([[vector[0], 0, 0],
                                     [0, vector[1], 0],
                                     [0, 0, 1]])
    
    def get_final_scale_matrix(self, object, vector):
        translate_toOrigin_matrix = self.get_translate_toOrigin_matrix(object.getCenter())
        scale_matrix = self.get_scale_matrix(vector)
        translate_back = self.get_translate_matrix(object.getCenter())
        final_matrix = np.matmul(translate_toOrigin_matrix, scale_matrix)
        final_matrix = np.matmul(final_matrix, translate_back)
        return final_matrix

    #----------------------------------- Rotate ---------------------------------
    
    def get_rotate_matrix(degrees):
        return np.array([[math.cos(math.radians(degrees)), -(math.sin(math.radians(degrees))), 0],
                         [math.sin(math.radians(degrees)), math.cos(math.radians(degrees)), 0],
                         [0, 0, 1]])
    
    def get_final_rotate_matrix(self, degrees, centerX, centerY):
        translate_toOrigin_matrix = self.get_translate_toOrigin_matrix([centerX, centerY])
        rotate_matrix = self.get_rotate_matrix(degrees)
        translate_back = self.get_translate_matrix([centerX, centerY])
        final_matrix = np.matmul(translate_toOrigin_matrix, rotate_matrix)
        final_matrix = np.matmul(final_matrix, translate_back)
        return final_matrix
    

class Transformation_3D():
    #--------------------------------- Translate ---------------------------------

    def get_translate_matrix(vector):
        return np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0]
                        [vector[0], vector[1], vector[2], 1]])
    
    def get_translate_toOrigin_matrix(vector):
        return np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0]
                        [-vector[0], -vector[1], -vector[2], 1]])
    
    #----------------------------------- Scale ---------------------------------

    def get_scale_matrix(vector):
        return np.array([[vector[0], 0,         0,          0],
                        [0,         vector[1],  0,          0],
                        [0,         0,          vector[2],  0]
                        [0,         0,          0,          1]])
    
    def get_final_scale_matrix(self, object, vector):
        translate_toOrigin_matrix = self.get_translate_toOrigin_matrix(object.getCenter())
        scale_matrix = self.get_scale_matrix(vector)
        translate_back = self.get_translate_matrix(object.getCenter())
        final_matrix = np.matmul(translate_toOrigin_matrix, scale_matrix)
        final_matrix = np.matmul(final_matrix, translate_back)
        return final_matrix
    
    #----------------------------------- Rotate ---------------------------------

    def get_rotate_matrix_X(degrees):
        return np.array([[1, 0,                                     0 ,                              0]
                         [0, math.cos(math.radians(degrees)),       math.sin(math.radians(degrees)), 0],
                         [0, -(math.sin(math.radians(degrees))),    math.cos(math.radians(degrees)), 0],
                         [0,                                        0, 0,                           1]])
    
    def get_rotate_matrix_Y(degrees):
        return np.array([[math.cos(math.radians(degrees)), 0, -(math.sin(math.radians(degrees))),   0]
                         [0,                               1, 0,                                    0],
                         [math.sin(math.radians(degrees)), 0, math.cos(math.radians(degrees)),      0],
                         [0,                               0, 0,                                    1]])
    
    def get_rotate_matrix_Z(degrees):
        return np.array([[math.cos(math.radians(degrees)),      math.sin(math.radians(degrees)), 0, 0],
                         [-(math.sin(math.radians(degrees))),   math.cos(math.radians(degrees)), 0, 0],
                         [0,                                    0,                               1, 0],
                         [0,                                    0,                               0, 1]])
    
    def get_final_rotate_matrix(self, centerX, centerY, centerZ, arbitrary: bool = False, degreesX = 0, degreesY = 0, degreesZ = 0):
        translate_toOrigin_matrix = self.get_translate_toOrigin_matrix([centerX, centerY, centerZ])
        if arbitrary:
            pass
        else:
            Rx = self.get_rotate_matrix_X(degreesX)
            Ry = self.get_rotate_matrix_Y(degreesY)
            Rz = self.get_rotate_matrix_Z(degreesZ)
        translate_back = self.get_translate_matrix([centerX, centerY])
        final_matrix = self.concatMatrix([translate_toOrigin_matrix, Rx, Ry, Rz, translate_back])
        return final_matrix
    
    
    def concatMatrix(matrices: list[np.array]):
        for i in range(len(matrices)):
            if i == 0:
                final_matrix = np.matmul(matrices[i], matrices[i+1])
            else:
                final_matrix = np.matmul(final_matrix, matrices[i])
        
        return final_matrix
    
    #def parallel_projection(window_center, )
