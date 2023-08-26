import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize, QPoint, QObject, QPointF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from graphicsitem import Ponto, Reta, Wireframe
from window2 import DialogBox
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.display_file = []
        #self.setGeometry(100, 100, 800, 600)
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
        self.wire_cord = []

        #Fator utilizado para zoom_in e zoom_out na viewport
        self.zoomFactor = 1.25
        #Fator utilizado para pan na viewport
        self.panFactor = 40.0

        self.objects = []

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_viewport()
        self.create_buttons()
        self.create_display_fileWidget()
        self.show()

    #Cria o ListWidget responsável por representar o displayfile
    def create_display_fileWidget(self):
        self.display_fileWidget = QListWidget(self)
        self.display_fileWidget.setGeometry(0, 0, 200, 200)
        self.display_fileWidget.show()

    #Adiciona o objeto passado como parâmetro ao display file
    def add_on_display_file(self, object):
        objeto = QListWidgetItem(self.display_fileWidget)
        objeto.setText(object.name)
        self.display_fileWidget.addItem(objeto)
        self.display_fileWidget.update()

    def create_buttons(self):
        #botao novo objeto
        botao1 = QPushButton('Novo Objeto', self)
        botao1.move(100, 200)
        botao1.resize(90, 30)
        botao1.clicked.connect(self.get_object_information)
        
        #Botão zoom_in
        botaoZoomIn = QPushButton("Zoom in", self)
        botaoZoomIn.move(100, 235)
        botaoZoomIn.resize(90, 30)
        botaoZoomIn.clicked.connect(self.zoom_in)
        #Shortcut = 'ctrl +'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomIn),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoom_in,
        )
        
        #Botão zoom_out
        botaoZoomOut = QPushButton("Zoom out", self)
        botaoZoomOut.move(100, 270)
        botaoZoomOut.resize(90, 30)
        botaoZoomOut.clicked.connect(self.zoom_out)
        #Shortcut = 'ctrl -'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomOut),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoom_out,
        )
        
        #Botão left
        botaoLeft = QPushButton("Left", self)
        botaoLeft.move(10, 380)
        botaoLeft.resize(70, 30)
        botaoLeft.clicked.connect(self.pan_Left)
        #Shortcut = '←'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Left,
        )

        #Botão Right
        botaoRight = QPushButton("Rigth", self)
        botaoRight.move(80, 380)
        botaoRight.resize(70, 30)
        botaoRight.clicked.connect(self.pan_Rigth)
        #Shortcut = '→'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToNextChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Rigth,
        )

        #Botão Up
        botaoUp = QPushButton("Up", self)
        botaoUp.move(45, 350)
        botaoUp.resize(70, 30)
        botaoUp.clicked.connect(self.pan_Up)
        #Shortcut = '↑'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousLine),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Up,
        )

        #Botão Down
        botaoDown = QPushButton("Down", self)
        botaoDown.move(45, 410)
        botaoDown.resize(70, 30)
        botaoDown.clicked.connect(self.pan_Down)
        #Shortcut = '↓'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToNextLine),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Down,
        )

        botaoTranslate = QPushButton('Translate', self)
        botaoTranslate.move(45, 500)
        botaoTranslate.resize(90, 30)
        botaoTranslate.clicked.connect(self.translate_call)

        botaoScale = QPushButton('Scale', self)
        botaoScale.move(45, 530)
        botaoScale.resize(90, 30)
        botaoScale.clicked.connect(self.scale_call)


    def create_viewport(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(200,0,600,500)

        #Set noAnchor to GraphicsView, enabling the view to move
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor(0))

    #tela para criar um novo objeto
    def get_object_information(self, new):
        user_input = {}
        box = DialogBox(new)
        if box.exec():
            user_input = box.get_input()
            self.create_new_object(user_input)

    def create_new_object(self, info):
        if info['opcao'] == "Ponto":
            new_object = Ponto(info['x'], info['y'])
            self.display_file.append(new_object)
            self.add_on_display_file(new_object)
            self.scene.addItem(new_object)
        elif info["opcao"] == "Reta":
            new_object = Reta(info['x1'], info['y1'], info['x2'], info['y2'])
            self.add_on_display_file(new_object)
            self.scene.addItem(new_object)
        else:
            lados = (len(info.keys()) - 2) / 2  # Quantidade de lados = quantidade de chaves, menos 2(opcao e nome) divido por dois(cada lado tem x e y)
            list = []
            for i in range(int(lados)):
                point = QPointF(info[f'x{i+1}'], info[f'y{i+1}'])
                list.append(point)
            new_object = Wireframe(list)
            for line in new_object.lines:
                self.scene.addItem(line)
            self.add_on_display_file(new_object)
            self.objects.append(new_object)

    @QtCore.pyqtSlot()
    def zoom_in(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.zoomFactor, self.zoomFactor)

        tr = self.view.transform() * scale_tr
        self.view.setTransform(tr)

    @QtCore.pyqtSlot()
    def zoom_out(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.zoomFactor, self.zoomFactor)

        scale_inverted, invertible = scale_tr.inverted()

        if invertible:
            tr = self.view.transform() * scale_inverted
            self.view.setTransform(tr)

    @QtCore.pyqtSlot()
    def pan_Left(self):
        self.view.translate(self.panFactor, 0)
        self.view.update()

    @QtCore.pyqtSlot()
    def pan_Rigth(self):
        self.view.translate(-self.panFactor, 0)
        self.view.update()

    @QtCore.pyqtSlot()
    def pan_Up(self):
        self.view.translate(0, self.panFactor)
        self.view.update()

    @QtCore.pyqtSlot()
    def pan_Down(self):
        self.view.translate(0, -self.panFactor)
        self.view.update()

    def transform_3D(self, object):
        if object.type() == Wireframe:
            for point in object.points:
                pass

    @QtCore.pyqtSlot()
    def scale_call(self):
        self.dialog = QDialog(self)
        

        self.dialog.setWindowTitle("Informe o vetor de escala")
        layout = QVBoxLayout(self.dialog)

        xLabel = QLabel('x:')
        layout.addWidget(xLabel)
        xInput = QLineEdit()
        layout.addWidget(xInput)

        yLabel = QLabel('y:')
        layout.addWidget(yLabel)
        yInput = QLineEdit()
        layout.addWidget(yInput)


        submit_button = QPushButton('Ok')
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.scale_object([float(xInput.text()), float(yInput.text())], self.objects[0]))

        self.dialog.exec_()


    def scale_object(self, vector2D, object):
        self.dialog.accept()
        if type(object) == Wireframe:
            vectorArray = np.array(vector2D)
            vectorArray = np.append(vectorArray, 1)
            scale_matrix = self.get_scale_matrix(vectorArray)
            centerX = 0
            centerY = 0
            for point in object.points:
                centerX += point.x()
                centerY += point.y()
            centerX = centerX / len(object.points)
            centerY = centerY / len(object.points)

            for point in object.points:
                x = point.x() - centerX
                y = point.y() - centerY
                print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, scale_matrix)
                point.setX(new_points[0] + centerX)
                point.setY(new_points[1] + centerX)
                x = point.x()
                y = point.y()
                print(f'Points after: x = {x}, y = {y}')
            
            for i in range(len(object.lines)):

                x1 = object.points[i-1].x()
                y1 = object.points[i-1].y()
                x2 = object.points[i].x()
                y2 = object.points[i].y()
                object.lines[i].setLine(x1, y1, x2, y2)
                print('line updated')

    def get_scale_matrix(self, vectorArray):
        return np.array([[vectorArray[0], 0, 0],
                                     [0, vectorArray[1], 0],
                                     [0, 0, 1]])
    
    @QtCore.pyqtSlot()
    def translate_call(self):
        self.dialog = QDialog(self)
        

        self.dialog.setWindowTitle("Informe o vetor de translocação")
        layout = QVBoxLayout(self.dialog)

        xLabel = QLabel('x:')
        layout.addWidget(xLabel)
        xInput = QLineEdit()
        layout.addWidget(xInput)

        yLabel = QLabel('y:')
        layout.addWidget(yLabel)
        yInput = QLineEdit()
        layout.addWidget(yInput)


        submit_button = QPushButton('Ok')
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.translate_object([int(xInput.text()), int(yInput.text())], self.objects[0]))




        self.dialog.exec_()



    def translate_object(self, vector2D, object):
        self.dialog.accept()
        if type(object) == Wireframe:
            vectorArray = np.array([vector2D])
            vectorArray = np.append(vectorArray, 1)
            translate_matrix = np.array([[1, 0, 0],
                                        [0, 1, 0],
                                        vectorArray])
            for point in object.points:
                x = point.x()
                y = point.y()
                print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, translate_matrix)
                point.setX(new_points[0])
                point.setY(new_points[1])

                x = point.x()
                y = point.y()
                print(f'Points after: x = {x}, y = {y}')
            
            for i in range(len(object.lines)):
                x1 = object.points[i-1].x()
                y1 = object.points[i-1].y()
                x2 = object.points[i].x()
                y2 = object.points[i].y()
                object.lines[i].setLine(x1, y1, x2, y2)
                print('line updated')
                

        
            

                
