import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from graphicsitem import Ponto, Reta
from window2 import DialogBox

class Resize(QWidget):
    def paintEvent(self, event):
        QP= QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black), 5)
        QP.setPen(pen)
        QP.drawRect()


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

        self.factor = 1.25

    def initUI(self):
        self.setWindowTitle(self.title)
        #setGeometry(x inicial,y inicial,)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setFixedSize(QSize(400, 300))
        self.create_viewport()
        self.create_buttons()
        self.create_objects_widget()
        self.draw_objects()
        self.show()

    def create_objects_widget(self):
        self.objects_widget = QListWidget(self)
        self.objects_widget.setGeometry(0, 0, 200, 200)
        self.objects_widget.show()

    def draw_display_file(self, object):
        objeto = QListWidgetItem(self.objects_widget)
        objeto.setText(object.name)
        self.objects_widget.addItem(objeto)
        #button.clicked.connect(self.showElement_onViewPort)
        self.objects_widget.update()
        #cria a viewport  e desenha os objetos na tela de acordo com o x e y calculados com a formula
        #objetos do display_file

    def create_buttons(self):
        #botao novo objeto
        botao1 = QPushButton('Novo Objeto', self)
        botao1.move(100, 200)
        botao1.resize(90, 30)
        #botao1.setStyleSheet('QPushButton {background-color:#0FB328;font:bold; font-size:20px}')
        botao1.clicked.connect(self.get_object_information)

    def create_viewport(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(200,0,600,500)

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomIn),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoom_in,
        )

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomOut),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoom_out,
        )

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
            self.draw_display_file(new_object)
            self.scene.addItem(new_object)
        elif info["opcao"] == "Reta":
            print("criar reta")
            new_object = Reta(info['x1'], info['y1'], info['x2'], info['y2'])
            self.draw_display_file(new_object)
            self.scene.addItem(new_object)
        else:
            print("outra coisa")

    def draw_objects(self):
        for object in self.display_file:
            self.scene.addItem(object)


    @QtCore.pyqtSlot()
    def zoom_in(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.factor, self.factor)

        tr = self.view.transform() * scale_tr
        self.view.setTransform(tr)

    @QtCore.pyqtSlot()
    def zoom_out(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.factor, self.factor)

        scale_inverted, invertible = scale_tr.inverted()

        if invertible:
            tr = self.view.transform() * scale_inverted
            self.view.setTransform(tr)