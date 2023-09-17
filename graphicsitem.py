from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPoint


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
        


class Reta(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.name:str
        self.centerX = 0.0
        self.centerY = 0.0
        self.x1N : float
        self.y1N : float
        self.x2N : float
        self.y2N : float

    def calculateCenter(self):
        self.centerX = (self.line().x1() + self.line().x2()) / 2
        self.centerY = (self.line().y1() + self.line().y2()) / 2

    def getCenter(self):
        return [self.centerX, self.centerY]

    def getCenterX(self):
        return self.centerX

    def getCenterY(self):
        return self.centerY


class Wireframe():
    def __init__(self, lista, vertices):
        self.lines = []
        self.vertices = vertices
        self.normalized_vertices = []
        self.criar(lista, vertices)
        self.points = lista
        self.color = None

        self.name :str
        self.centerX = 0.0
        self.centerY = 0.0

    def criar(self, lista, vertices):
        for i in range(len(lista)):
            x1, y1, x2, y2 = lista[i-1].x(), lista[i-1].y(), lista[i].x(), lista[i].y()
            print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
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
        