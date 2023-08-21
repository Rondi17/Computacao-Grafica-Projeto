import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize, QPoint, QObject, QPointF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from graphicsitem import Ponto, Reta
from window2 import DialogBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.display_file = []
        #self.setGeometry(100, 100, 800, 600)
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 100
        self.top = 100
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

        botaoZoomIn = QPushButton("Zoom in", self)
        botaoZoomIn.move(100, 235)
        botaoZoomIn.resize(90, 30)
        botaoZoomIn.clicked.connect(self.zoom_in)

        botaoZoomOut = QPushButton("Zoom out", self)
        botaoZoomOut.move(100, 270)
        botaoZoomOut.resize(90, 30)
        botaoZoomOut.clicked.connect(self.zoom_out)

        botaoLeft = QPushButton("Left", self)
        botaoLeft.move(10, 380)
        botaoLeft.resize(70, 30)
        botaoLeft.clicked.connect(self.pan_Left)

        botaoRight = QPushButton("Rigth", self)
        botaoRight.move(80, 380)
        botaoRight.resize(70, 30)
        botaoRight.clicked.connect(self.pan_Rigth)

        botaoUp = QPushButton("Up", self)
        botaoUp.move(45, 350)
        botaoUp.resize(70, 30)
        botaoUp.clicked.connect(self.pan_Up)

        botaoDown = QPushButton("Down", self)
        botaoDown.move(45, 410)
        botaoDown.resize(70, 30)
        botaoDown.clicked.connect(self.pan_Down)



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

        #Left_shortcut
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Left,
        )

        #Right_shortcut
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToNextChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Rigth,
        )

        #Up_shortcut
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousLine),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Up,
        )

        #Down_shortcut
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToNextLine),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Down,
        )

        #Set noAnchor to GraphicsView, enabling the view to move
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor(0))
        


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
            tam = (len(info.items()) // 2)
            for i in range(int(tam - 1)):
                new_object = Reta(info[f'x{i}'], info[f'y{i}'], info[f'x{i+1}'], info[f'y{i+1}'])
                self.draw_display_file(new_object)
                self.scene.addItem(new_object)
            new_object = Reta(info[f'x{0}'], info[f'y{0}'], info[f'x{tam-1}'], info[f'y{tam-1}'])
            self.draw_display_file(new_object)
            self.scene.addItem(new_object)

    def draw_objects(self):
        for object in self.display_file:
            #self.view.mapToScene(0, 0)
            pass


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

    @QtCore.pyqtSlot()
    def pan_Left(self):
        self.view.translate(20.0, 0)
        self.view.update()

    @QtCore.pyqtSlot()
    def pan_Rigth(self):
        self.view.translate(-20.0, 0)
        self.view.update()

    @QtCore.pyqtSlot()
    def pan_Up(self):
        self.view.translate(0, 20.0)
        self.view.update()

    @QtCore.pyqtSlot()
    def pan_Down(self):
        self.view.translate(0, -20.0)
        self.view.update()

'''class PanGestureRecognizer(QGestureRecognizer):
    startPoint = QPointF()
    panning = False

    gesture = QGesture(QObject())
    
    def '''