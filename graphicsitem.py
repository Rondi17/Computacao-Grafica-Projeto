from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPoint

#obs: colocar tipo
class GraphicsItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ponto(QGraphicsEllipseItem):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1)
        self.setBrush(Qt.black)
        self.name : str
        self.z1 = 1
        


class Reta(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.name:str
        self.z1 = 1
        self.z2 = 1


class Wireframe():
    def __init__(self, lista):
        self.lines = []
        self.criar(lista)
        self.name :str
        self.points = lista

    def criar(self, lista):
        for i in range(len(lista)):
            x1, y1, x2, y2 = lista[i-1].x(), lista[i-1].y(), lista[i].x(), lista[i].y()
            print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
            self.lines.append(Reta(x1, y1, x2, y2))
        