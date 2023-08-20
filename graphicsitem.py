from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QPoint

#obs: colocar tipo
class GraphicsItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ponto(QGraphicsEllipseItem):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10)
        self.setBrush(Qt.black)
        self.name = "Ponto"

class Reta(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.name = "Reta"
        