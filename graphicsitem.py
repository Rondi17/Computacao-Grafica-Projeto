from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPoint

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

        self.clipped = True
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


class Wireframe():
    def __init__(self, lista, vertices):
        self.lines = []
        self.vertices = vertices  #vai ter a lista de listas com os vertices
        self.points = lista
        self.normalized_vertices = [] #vai ter [(x1, y1,x2, y2)] retas que formam
        self.criar(lista, vertices)
        self.color = None

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

# curves recebe por exemplo [[(1, 1), (2, 2), (3, 3), (4, 4)]]
class HermiteCurve():
    def __init__(self, curves:list):
        self.curves = curves
        print("self.curves: ", self.curves)
        #self.curves:  [[(100, 100), (300, 200), (150, 0), (0, 100)], [(300, 200), (500, 300), (100, 50), (50, 200)], [(500, 300), (600, 400), (50, 150), (0, 100)]]
        self.curve_points = [] #pontos de todas as curvas
        self.lines_curve = [] #retas que formam a curva
        self.curve_clipping = []
        self.color = None
        self.evaluate()
        print("self.curve_points", self.curve_points)
        print("ENDEND")

    #funcao para calcular a posicao da curva de Hermite em t [0, 1]
    def point_on_curve(self,p1:tuple, p4:tuple, r1:tuple, r4:tuple, t:float):
        t2 = t * t
        t3 = t2 * t
        h1 = 2 * t3 - 3 * t2 + 1
        h2 = -2 * t3 + 3 * t2
        h3 = t3 - 2 * t2 + t
        h4 = t3 - t2

        x = h1 * p1[0] + h2 * p4[0] + h3 * r1[0] + h4 * r4[0]
        y = h1 * p1[1] + h2 * p4[1] + h3 * r1[1] + h4 * r4[1]
        return x,y

    #avalie a curva em varios valores de t
    def evaluate(self):
        for curve in self.curves:
            points = [] #armazena os pontos que formam a curva
            for t in range(0,100):
                x, y = self.point_on_curve(curve[0], curve[1], curve[2], curve[3], t/100.0)
                points.append([x,y])
            self.curve_points.append(points)
    
    #clipping de curvas so desenha se x,y do ponto da curva estiverem dentro dos limites
    #uma curva tem varios pontos, e esses pontos sao ligados por retas
    def clipping(self, xmin, ymin, xmax, ymax):
        for list in self.curve_points:
            print("list: ", list)
            for sub in list:
                #sub = [x,y]
                if (xmin <= sub[0] <= xmax and ymin <= sub[1] <= ymax):
                    self.curve_clipping.append(sub)
                
