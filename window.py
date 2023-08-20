import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QInputDialog

from graphicsitem import Line

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #self.display_file = []

        self.setGeometry(100, 100, 800, 600)
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 500
        self.top = 200
        self.width = 800
        self.height = 600
        
        self.initUI()
    
        #self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setFixedSize(QSize(400, 300))
        self.create_viewport()
        self.create_buttons()
        self.show()

    #funcao para criar botoes
    def create_buttons(self):
        #botao
        botao1 = QPushButton('NEW', self)
        botao1.move(100, 100)
        botao1.resize(40, 30)
        #botao1.setStyleSheet('QPushButton {background-color:#0FB328;font:bold; font-size:20px}')
        botao1.clicked.connect(self.create_new_object)

    #desenhar objetos do display_file
    def draw_display_file(self):
        pass
        #cria a viewport  e desenha os objetos na tela de acordo com o x e y calculados com a formula
        #objetos do display_file

    def create_viewport(self):
        self.scene = QGraphicsScene()
        view = QGraphicsView(self.scene, self)
        view.setGeometry(200,0,600,500)
        # for object in self.display_file:
        #     pass
            #desenha os objetos na tela
        #self.setCentralWidget(view)

    #tela para criar um novo objeto
    def create_new_object(self):
        print("new object!")

        # cria uma janelas para informacoes do novo objeto
        object_name, ok = QInputDialog.getText(self, "New Object", "Enter object name:")
        if ok:
            
            x, ok1 = QInputDialog.getInt(self, "Coordinates", "Enter x coordinate:")
            y, ok2 = QInputDialog.getInt(self, "Coordinates", "Enter y coordinate:")
            
            if ok1 and ok2:
                # Pergunta o tipo de objeto a ser criado ponto ou linha
                object_type, ok3 = QInputDialog.getItem(self, "Object Type", "Select object type:", ["Point", "Line"], 0, False)
                
                if ok3:
                    if object_type == "Point":
                        print("criar ponto")
                        #self.display_file.append(new_object)
                        #self.scene.addItem(new_object)
                    elif object_type == "Line":
                        x2, ok4 = QInputDialog.getInt(self, "Coordinates", "Enter ending x coordinate:")
                        y2, ok5 = QInputDialog.getInt(self, "Coordinates", "Enter ending y coordinate:")
                        
                        if ok4 and ok5:
                            new_object = Line(x, y, x2, y2)
                            #self.display_file.append(new_object)
                            self.scene.addItem(new_object)

    def zoom_in(self):
        print("mega-boga")
    
    def zoom_out(self):
        print("menos zoom")
    
    def right(self):
        print("vai para o lado direito")
    
    def left(self):
        print("vai para o lado esquerdo")



