from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt

#obs: colocar tipo
class GraphicsItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ponto(QGraphicsEllipseItem):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10)
        self.setBrush(Qt.black)

class Reta(QGraphicsLineItem):
    def __init__(self, x1, y1):
        super().__init__(x1, y1, 700, 250)
        