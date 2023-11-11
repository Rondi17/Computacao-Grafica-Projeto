from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
import numpy as np

#obs: colocar tipo
class GraphicsItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ponto(QGraphicsEllipseItem):
    def __init__(self, x, y):
        print(f'try instantiate point {x}, {y}')
        super().__init__(x, y, 1, 1)
        self.setBrush(Qt.black)
        self.name : str
        self.clipped : False
        

class Reta(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.name:str
        self.centerX = 0.0
        self.centerY = 0.0
        self.x1N  = x1
        self.y1N = y1
        self.x2N : x2
        self.y2N : y2
        
        self.RC : list
        self.coeficienteLinear : float

        self.clipped = False
        self.showing = False

        #intersection points
        self.x1I = x1
        self.y1I = y1
        self.x2I = x2
        self.y2I = y2

    def calculateCenter(self):
        self.centerX = (self.line().x1() + self.line().x2()) / 2
        self.centerY = (self.line().y1() + self.line().y2()) / 2

    def getCenter(self):
        return [self.centerX, self.centerY]

    def getCenterX(self):
        return self.centerX

    def getCenterY(self):
        return self.centerY
    
    def resetIntersection(self):
        self.x1I = self.line().x1()
        self.y1I = self.line().y1()
        self.x2I = self.line().x2()
        self.y2I = self.line().y2()


class Wireframe():
    def __init__(self, lista, vertices):
        self.lines :list[Reta] = []
        self.vertices = vertices  #vai ter a lista de listas com os vertices
        self.points = lista
        self.normalized_vertices = [] #vai ter [(x1, y1,x2, y2)] retas que formam
        self.criar(lista, vertices)
        self.color = None
        self.brush = None
        self.fillPolygon = None

        self.clippingLocation = []
        self.clippingOrder = []

        self.name :str
        self.centerX = 0.0
        self.centerY = 0.0

    def criar(self, lista, vertices):
        for i in range(len(lista)):
            x1, y1, x2, y2 = lista[i-1].x(), lista[i-1].y(), lista[i].x(), lista[i].y()
            #print(f' 1- {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
            self.lines.append(Reta(x1, y1, x2, y2))

        for i in range(len(vertices)):
            x1, y1, x2, y2 = vertices[i-1][0], vertices[i-1][1], vertices[i][0], vertices[i][1]
            #print(f' 2- {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
            self.normalized_vertices.append([x1, y1, x2, y2])

    def calculateCenter(self):
        for point in self.points:
            self.centerX += point.x()
            self.centerY += point.y()
        self.centerX = self.centerX / len(self.points)
        self.centerY = self.centerY / len(self.points)

    def getCenter(self):
        return [self.centerX, self.centerY]

    def getCenterX(self):
        return self.centerX

    def getCenterY(self):
        return self.centerY
    
    def recriateLines(self):
        self.lines = []
        for i in range(len(self.vertices)):
            x1, y1, x2, y2 = self.vertices[i-1][0], self.vertices[i-1][1], self.vertices[i][0], self.vertices[i][1]
            #print(f' 1- {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
            self.lines.append(Reta(x1, y1, x2, y2))

class HermiteCurve():
    def __init__(self, curves:list):
        self.curves = curves
        self.curve_points = []      #pontos de todas as curvas
        self.curve_clipping = []    #pontos clipados
        self.color = None
        self.evaluate()

    #funcao para calcular a posicao da curva de Hermite em t [0, 1]
    def point_on_curve(self,p1:tuple, p4:tuple, r1:tuple, r4:tuple, t:float):
        t2 = t * t
        t3 = t2 * t
        h1 = 2 * t3 - 3 * t2 + 1
        h2 = -2 * t3 + 3 * t2
        h3 = t3 - 2 * t2 + t
        h4 = t3 - t2
        TMH = np.array([h1,h2,h3,h4]) #Matriz 1x4
        GHx = np.array([[p1[0]], [p4[0]], [r1[0]], [r4[0]]]) #Matriz 4x1
        GHy = np.array([[p1[1]], [p4[1]], [r1[1]], [r4[1]]]) #Matriz 4x1

        #x = h1 * p1[0] + h2 * p4[0] + h3 * r1[0] + h4 * r4[0]
        #y = h1 * p1[1] + h2 * p4[1] + h3 * r1[1] + h4 * r4[1]

        x = np.matmul(TMH, GHx) #matriz 1x1
        y = np.matmul(TMH, GHy) #matriz 1x1
        return x[0],y[0]

    #avalie a curva em varios valores de t
    def evaluate(self):
        for curve in self.curves:
            points = [] #armazena os pontos que formam a curva
            for t in range(0,100):
                x, y = self.point_on_curve(curve[0], curve[1], curve[2], curve[3], t/100.0)
                points.append([x,y])
            self.curve_points.append(points)

    def clipping(self, xmin, ymin, xmax, ymax):
        self.curve_clipping = []
        for list in self.curve_points:
            for sub in list:    #sub = [x, y]
                if (xmin <= sub[0] <= xmax and ymin <= sub[1] <= ymax):
                    self.curve_clipping.append(sub) 

class BSplineCurve():
    def __init__(self, control_points):
        self.control_points = control_points
        self.delta = 0.01
        self.color = None
        self.curve_clipping = []    #pontos clipados
        self.vertices = []
        self.forward_differences()

    def forward_differences(self):
        spline_vertices = []
        iterations = int(1 / self.delta)

        for i in range(0, len(self.control_points)):
            iterator = i + 4 #4 em 4

            if iterator > len(self.control_points):
                break
            points = self.control_points[i:iterator]

            #calcular parametros para cada 4 pontos de controle
            delta_x, delta_y = self.calculate_bspline_parameters(points)
            x = delta_x[0]
            y = delta_y[0]
            spline_vertices.append((x, y, 0))
            for _ in range(0, iterations):
                x += delta_x[1]
                delta_x[1] += delta_x[2]
                delta_x[2] += delta_x[3]

                y += delta_y[1]
                delta_y[1] += delta_y[2]
                delta_y[2] += delta_y[3]

                spline_vertices.append((x, y, 0))
        self.vertices = spline_vertices
    
    def calculate_bspline_parameters(self, points):
        #MBS == Matriz b-spline base
        #GBS == Matriz de geometria de b-spline
        MBS = self.matrix_bspline_base()

        GBS_x = []
        GBS_y = []
        for (x, y) in points:
            GBS_x.append(x)
            GBS_y.append(y)
        
        GBS_x = np.array([GBS_x]).T
        coefficients_x = np.matmul(MBS, GBS_x.T[0])
        initial_conditions_x = self.calculate_initial_conditions(coefficients_x)

        GBS_y = np.array([GBS_y]).T
        coefficients_y = np.matmul(MBS, GBS_y.T[0])
        initial_conditions_y = self.calculate_initial_conditions(coefficients_y)

        return initial_conditions_x, initial_conditions_y

    def matrix_bspline_base(self):
        return np.array(
        [
            [-1 / 6, 1 / 2, -1 / 2, 1 / 6],
            [1 / 2, -1, 1 / 2, 0],
            [-1 / 2, 0, 1 / 2, 0],
            [1 / 6, 2 / 3, 1 / 6, 0],
        ]
    )

    def calculate_initial_conditions(self, coefficients):
        a = coefficients[0]
        b = coefficients[1]
        c = coefficients[2]
        d = coefficients[3]
        delta_2 = self.delta ** 2
        delta_3 = self.delta ** 3
        return [
        d,
        a * delta_3 + b * delta_2 + c * self.delta,
        6 * a * delta_3 + 2 * b * delta_2,
        6 * a * delta_3,
    ]

    def clipping(self, xmin, ymin, xmax, ymax):
        self.curve_clipping = []
        for tuple_ in self.vertices:    #tuple_ = [x, y]
                if (xmin <= tuple_[0] <= xmax and ymin <= tuple_[1] <= ymax):
                     self.curve_clipping.append(tuple_)


class Point3D(GraphicsItem):
    def __init__(self, name: str, vertices: list):
        super().__init__(name, vertices)
        self.clipped_point = [] #lista de pontos que aparecem depois da projecao
        self.normalized_point = []

    def transform_toQPointF(self) -> QPointF:
        return None
        #return QPointF(self.x, self.y)

    def clipping(self, xmin, ymin, xmax, ymax):
        if (xmin <= self.vertices[0] <= xmax and ymin <= self.vertices[1] <= ymax):
            self.clipped_point = self.vertices
        print("pontos clipados ")

    def calculateCenter(self):
        #o centro de um ponto é o propio ponto
        x = self.vertices[0]
        y = self.vertices[1]
        z = self.vertices[2]
        return [x, y, z]
    
    def translate(self, translate_matrix):
        old_vertice = np.array([self.vertices[0], self.vertices[1], self.vertices[2]])
        new_vertice = np.matmul(old_vertice, translate_matrix)
        self.vertices[0] = new_vertice[0]
        self.vertices[1] = new_vertice[1]
        self.vertices[2] = new_vertice[2]
