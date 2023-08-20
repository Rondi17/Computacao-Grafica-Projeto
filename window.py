import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QInputDialog
from graphicsitem import Ponto, Reta
from window2 import DialogBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.display_file = []
        #self.setGeometry(100, 100, 800, 600)
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        #setGeometry(x inicial,y inicial,)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setFixedSize(QSize(400, 300))
        self.create_viewport()
        self.create_buttons()
        self.draw_objects()
        self.show()

    def create_buttons(self):
        #botao novo objeto
        botao1 = QPushButton('Novo Objeto', self)
        botao1.move(100, 100)
        botao1.resize(90, 30)
        #botao1.setStyleSheet('QPushButton {background-color:#0FB328;font:bold; font-size:20px}')
        botao1.clicked.connect(self.get_object_information)

    def create_viewport(self):
        self.scene = QGraphicsScene()
        view = QGraphicsView(self.scene, self)
        view.setGeometry(200,0,600,500)

    #tela para criar um novo objeto
    def get_object_information(self):
        print("new object!")

        box = DialogBox()
        if box.exec():
            user_input = box.get_input()
            print("Entrada: ", user_input)
            self.create_new_object(user_input)
        else:
            print("cancel!")
    
    #funcao recebe um dicionario ex:  {'opcao': 'Ponto', 'x': 10, 'y': 20}
    #e cria um novo objeto
    def create_new_object(self, info):
        if info['opcao'] == "Ponto":
            new_object = Ponto(info['x'], info['y'])
            self.display_file.append(new_object)
        elif info["opcao"] == "Reta":
            print("criar reta")
        else:
            print("outra coisa")

    def draw_objects(self):
        for object in self.display_file:
            self.scene.addItem(object)

