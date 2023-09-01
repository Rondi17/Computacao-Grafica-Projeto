import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize, QPoint, QObject, QPointF, QRectF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from graphicsitem import Ponto, Reta, Wireframe
from window2 import DialogBox
import numpy as np
import math

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.display_file = []
        self.onViewport = []
        #self.setGeometry(100, 100, 800, 600)
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 600
        self.set_window_default_paramaters()
        self.initUI()
        self.testes()
        self.wire_cord = []

        #Fator utilizado para zoom_in e zoom_out na viewport
        self.zoomFactor = 1.1
        #Fator utilizado para pan na viewport
        self.panFactor = 40.0

        self.objects = []
    
    def testes(self):
        dic = {'opcao': 'Reta', 'nome': 'retaA', 'x1': 10, 'y1': 10, 'x2': 100, 'y2': 100}
        self.create_new_object(dic)

        # new = {'opcao': 'Wireframe', 'nome': 'quadrado', 'x1': 100, 'y1': 100, 'x2': 100, 'y2': 200, 'x3': 200, 'y3': 100, 'x4': 200, 'y4': 200}
        # self.create_new_object(new)
        
    def set_window_default_paramaters(self):
        #window dimensions
        self.xw_min = 0
        self.xw_max = 600
        self.yw_min = 0
        self.yw_max = 500

        #viewport dimensions
        self.xv_min = 0
        self.xv_max = 600
        self.yv_min = 0
        self.yv_max = 500

        #window default
        self.padrao_x_max = 600
        self.padrao_y_max = 500

        self.padrao_x_min = 0
        self.padrao_y_min = 0
        self.scale_acumulator = 1


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
    def add_on_display_file(self, object, nome):
        objeto = QListWidgetItem(self.display_fileWidget)
        objeto.setText(nome)
        object.name = nome
        self.display_fileWidget.addItem(objeto)
        self.display_fileWidget.update()

    def create_buttons(self):
        #botao novo objeto
        botao1 = QPushButton('Novo Objeto', self)
        botao1.move(100, 200)
        botao1.resize(90, 30)
        botao1.clicked.connect(self.get_object_information)
        #Shortcut = 'n' or 'N'
        QtWidgets.QShortcut(
            QtGui.QKeySequence('n'),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.get_object_information,
        )
        
        #Botão zoom_in
        botaoZoomIn = QPushButton("Zoom in", self)
        botaoZoomIn.move(100, 235)
        botaoZoomIn.resize(90, 30)
        botaoZoomIn.clicked.connect(self.new_zoom_in)
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
        botaoZoomOut.clicked.connect(self.new_zoom_out)
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

        #Botão Translate
        botaoTranslate = QPushButton('Translate', self)
        botaoTranslate.move(45, 500)
        botaoTranslate.resize(90, 30)
        botaoTranslate.clicked.connect(self.translate_call)
        #Shortcut = 't' or 'T'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('t')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.translate_call,
        )

        #Botão Scale
        botaoScale = QPushButton('Scale', self)
        botaoScale.move(45, 530)
        botaoScale.resize(90, 30)
        botaoScale.clicked.connect(self.scale_call)
        #Shortcut = 's' or 'S'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('s')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.scale_call,
        )

        #Botão Rotate
        botaoRotate = QPushButton('Rotate', self)
        botaoRotate.move(45, 560)
        botaoRotate.resize(90, 30)
        botaoRotate.clicked.connect(self.rotate_call)
        #Shortcut = 's' or 'S'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('r')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_call,
        )

        #Botão Change Color
        botaoChangeColor = QPushButton('Change Color', self)
        botaoChangeColor.move(135, 530)
        botaoChangeColor.resize(90, 30)
        botaoChangeColor.clicked.connect(self.changeColor_call)
        #Shortcut = 'c' or 'C'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('c')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.changeColor_call,
        )

    def create_viewport(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(200,0,600,500)
        #self.view.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        #Set noAnchor to GraphicsView, enabling the view to move
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor(0)) #ponto de ancoragem

    #tela para criar um novo objeto
    @QtCore.pyqtSlot()
    def get_object_information(self):
        user_input = {}
        box = DialogBox()
        if box.exec():
            user_input = box.get_input()
            self.create_new_object(user_input)

    def create_new_object(self, info):
        if info['opcao'] == "Ponto":
            new_object = Ponto(info['x'], info['y'])
            print(f'on instantiantion {new_object}, {new_object.y()}')
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
            self.draw_dispplay_file(new_object)
            #self.scene.addItem(new_object)
        elif info["opcao"] == "Reta":
            new_object = Reta(info['x1'], info['y1'], info['x2'], info['y2'])
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
            self.draw_dispplay_file(new_object)
            #self.scene.addItem(new_object)
        else:
            lados = (len(info.keys()) - 2) / 2  # Quantidade de lados = quantidade de chaves, menos 2(opcao e nome) divido por dois(cada lado tem x e y)
            list = []
            for i in range(int(lados)):
                point = QPointF(info[f'x{i+1}'], info[f'y{i+1}'])
                list.append(point)
            new_object = Wireframe(list)
            self.draw_dispplay_file(new_object)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
            self.objects.append(new_object)
    
    def viewport_transformation(self, xw, yw):
        #print("viewport transformation")
        #xv = ((xw - self.xw_min) / (self.xw_max - self.xw_min)) * (self.xv_max - self.xv_min)
        #yv = (1- ((yw - self.yw_min) / (self.yw_max - self.yw_min)) ) * (self.yv_max - self.yv_min)

        sx = (self.xv_max - self.xv_min) / (self.xw_max - self.xw_min)
        sy = (self.yv_max - self.yv_min) / (self.yw_max - self.yw_min)

        xv = self.xv_min + (xw - self.xw_min) * sx
        yv = self.yv_max - (self.yv_min + (yw - self.yw_min) * sy)
        return xv, yv

    def update_viewport(self):
        ##print(f'lenVP = {len(self.onViewport)}, {self.onViewport}')
        for obj in self.onViewport:
            self.scene.removeItem(obj)
        self.onViewport = []
        ##print(f'lenVP = {len(self.onViewport)}, {self.onViewport}')
        ##print(f'lenDF = {len(self.display_file)}, {self.display_file}')
        for obj in self.display_file:
            self.draw_dispplay_file(obj)
        ##print(f'lenDF = {len(self.display_file)}, {self.display_file}')
        self.view.centerOn(self.xw_max-self.xw_min, self.yw_max-self.yw_min)

    def new_zoom_in(self):
        #antes
        # self.xw_max = self.xw_max * (-self.zoomFactor)
        # self.yw_max = self.yw_max * (-self.zoomFactor)
        zoom = 1.1
        scale_factor = 1.1
        
        print(f"Scale factor atual: {scale_factor}")
        halfx = self.xw_max - self.xw_min
        halfy = self.yw_max - self.yw_min
        self.xw_min += halfx * (1 - 1 / scale_factor)
        self.yw_min += halfy * (1 - 1 / scale_factor)
        self.xw_max -= halfx * (1 - 1 / scale_factor)
        self.yw_max -= halfy * (1 - 1 / scale_factor)
        self.view.centerOn(halfx, halfy)
        #self.xw_min += 60
        #self.yw_min += 50
        #self.xw_max -= 60
        #self.yw_max -= 50
        self.update_viewport()
        print("new zoom in")

    def new_zoom_out(self):
        scale_factor = 1.1
        print(f"Scale factor atual: {scale_factor}")
        halfx = self.xw_max - self.xw_min
        halfy = self.yw_max - self.yw_min
        self.xw_min -= halfx * (scale_factor - 1)
        self.yw_min -= halfy * (scale_factor - 1)
        self.xw_max += halfx * (scale_factor - 1)
        self.yw_max += halfy * (scale_factor - 1)
        self.view.centerOn(halfx, halfy)

        # self.xw_min = self.padrao_x_min * scale_factor
        # self.yw_min = self.padrao_y_min * scale_factor

        self.update_viewport()
        print("new zoom out")
    
#eu vou mecher nas coordenadas do objeto
#mas manter as coordenadas originais
    def draw_dispplay_file(self, obj):
        #antes de dsenhar faz a trasformada 
        if type(obj) == Wireframe:
            #print('------------start wireframe transformation---------------')
            for l in obj.lines:
                #print("antes: ", l.line().x1(), l.line().y1(), l.line().x2(), l.line().y2() )
                new_x1, new_y1 = self.viewport_transformation(l.line().x1(), l.line().y1())
                new_x2, new_y2 = self.viewport_transformation(l.line().x2(), l.line().y2())
                #print("depois: ", new_x1, new_y1, new_x2, new_y2)
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
            #print('------------finish wireframe transformation---------------')
        elif type(obj) == Reta:
            print("antes: ", obj.line().x1(), obj.line().y1(), obj.line().x2(), obj.line().y2() )
            new_x1, new_y1 = self.viewport_transformation(obj.line().x1(), obj.line().y1())
            new_x2, new_y2 = self.viewport_transformation(obj.line().x2(), obj.line().y2())
            print("depois: ", new_x1, new_y1, new_x2, new_y2)

            new = Reta(new_x1, new_y1, new_x2, new_y2)
            self.scene.addItem(new)
            self.onViewport.append(new)
            self.view.show()
            print("end setline")
        elif type(obj) == Ponto:
            print('reach point')
            print(f'antes : x = {obj.x()}, y = {obj.y()}')
            new_x1, new_y1 = self.viewport_transformation(obj.x(), obj.y())
            print(f'x = {new_x1}, y = {new_y1}')
            new = Ponto(new_x1, new_y1)
            self.scene.addItem(new)
            self.onViewport.append(new)
            self.view.show()
            print("end setPoint")

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
        self.xw_min += self.panFactor
        self.xw_max += self.panFactor
        self.update_viewport()

    @QtCore.pyqtSlot()
    def pan_Rigth(self):
        self.xw_min -= self.panFactor
        self.xw_max -= self.panFactor
        self.update_viewport()

    @QtCore.pyqtSlot()
    def pan_Up(self):
        self.yw_min -= self.panFactor
        self.yw_max -= self.panFactor
        self.update_viewport()

    @QtCore.pyqtSlot()
    def pan_Down(self):
        self.yw_min += self.panFactor
        self.yw_max += self.panFactor
        self.update_viewport()

    @QtCore.pyqtSlot()
    def changeColor_call(self):
        self.dialog = QDialog(self)

        self.dialog.setWindowTitle("Qual objeto deseja mudar de cor?")
        self.layout = QVBoxLayout(self.dialog)

        self.option_combo = QComboBox()
        for item in self.display_file:
            self.option_combo.addItem(item.name)
        self.layout.addWidget(self.option_combo)

        submit_button = QPushButton('Ok')
        self.layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.colorDialog())
        
        self.dialog.exec_()

    def colorDialog(self):
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        colorDialog = QColorDialog(self)
        colorDialog.setCurrentColor(Qt.red)
        if colorDialog.exec_() == QColorDialog.Accepted:
            color = colorDialog.selectedColor()

            pen = QPen(color)
            if type(object) == Wireframe:
                for line in object.lines:
                    print(line)
                    print(type(line))
                    line.setPen(color)
                    #line.update()
            else:
                object.setPen(pen)
            self.dialog.accept()
            
    @QtCore.pyqtSlot()
    def rotate_call(self):
        self.dialog = QDialog(self)
        
        self.dialog.setWindowTitle("Informe quantos graus deseja rodar o objeto")
        self.layout = QVBoxLayout(self.dialog)

        degreesLabel = QLabel('Graus:')
        self.layout.addWidget(degreesLabel)
        self.degreesInput = QLineEdit()
        self.layout.addWidget(self.degreesInput)

        translateLabel = QLabel('Selecione qual objeto transladar:')
        self.layout.addWidget(translateLabel)
        self.option_combo = QComboBox()
        for item in self.display_file:
            self.option_combo.addItem(item.name)
        self.layout.addWidget(self.option_combo)

        self.center_combo = QComboBox()
        self.center_combo.addItems(['Centro do mundo', 'Centro do objeto', 'Ponto especifico'])
        self.layout.addWidget(self.center_combo)

        submit_button = QPushButton('Ok')
        self.layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.validate_center())

        self.dialog.exec_()

    @QtCore.pyqtSlot()
    def validate_center(self):
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        option = self.center_combo.currentText()
        if option == 'Ponto especifico':
            centerX, centerY = self.ask_point()
            self.rotate_object(float(self.degreesInput.text()), centerX, centerY)
        elif option == 'Centro do mundo':
            self.rotate_object(float(self.degreesInput.text()), 0, 0)
        else:
            centerX = 0
            centerY = 0
            if type(object) == Wireframe:
                for point in object.points:
                    centerX += point.x()
                    centerY += point.y()
                centerX = centerX / len(object.points)
                centerY = centerY / len(object.points)
                self.rotate_object(float(self.degreesInput.text()), centerX, centerY)
            elif type(object) == Reta:
                centerX = (object.line().x1() + object.line().x2()) / 2
                centerY = (object.line().y1() + object.line().y2()) / 2
                self.rotate_object(float(self.degreesInput.text()), centerX, centerY)
    
    def ask_point(self):
        xLabel = QLabel('x:')
        self.layout.addWidget(xLabel)
        xInput = QLineEdit()
        self.layout.addWidget(xInput)

        yLabel = QLabel('y:')
        self.layout.addWidget(yLabel)
        yInput = QLineEdit()
        self.layout.addWidget(yInput)
        return int(xInput.text()), int(yInput.text())

    def rotate_object(self, degrees, centerX, centerY):
        self.dialog.accept()
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        rotate_matrix = self.get_rotate_matrix(degrees)
        if type(object) == Reta:
            x1, y1, x2, y2 = object.line().x1(), object.line().y1(), object.line().x2(), object.line().y2()
            x1 -= centerX
            y1 -= centerY
            x2 -= centerX
            y2 -= centerY
            old_l1 = np.array([x1, y1, 1])
            old_l2 = np.array([x2, y2, 1])
            new_l1 = np.matmul(old_l1, rotate_matrix)
            new_l2 = np.matmul(old_l2, rotate_matrix)
            x1 = new_l1[0] + centerX
            y1 = new_l1[1] + centerY
            x2 = new_l2[0] + centerX
            y2 = new_l2[1] + centerY
            object.setLine(x1, y1, x2, y2)
            self.draw_dispplay_file(object)
            self.update_viewport()

        if type(object) == Wireframe:
            for point in object.points:
                #print(f'Points before: x = {x}, y = {y}')
                x = point.x() - centerX
                y = point.y() - centerY
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, rotate_matrix)
                point.setX(new_points[0] + centerX)
                point.setY(new_points[1] + centerY)
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
                self.draw_dispplay_file(object.lines[i])
                self.update_viewport()
            
    def get_rotate_matrix(self, degrees):
        return np.array([[math.cos(math.radians(degrees)), -(math.sin(math.radians(degrees))), 0],
                         [math.sin(math.radians(degrees)), math.cos(math.radians(degrees)), 0],
                         [0, 0, 1]])

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

        scaleLabel = QLabel('Selecione qual objeto dimensionar:')
        layout.addWidget(scaleLabel)
        self.option_combo = QComboBox()
        for item in self.display_file:
            self.option_combo.addItem(item.name)
        layout.addWidget(self.option_combo)


        submit_button = QPushButton('Ok')
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.scale_object([float(xInput.text()), float(yInput.text())]))

        self.dialog.exec_()


    def scale_object(self, vector):
        self.dialog.accept()
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        scale_matrix = self.get_scale_matrix(vector)
        if type(object) == Wireframe:
            vectorArray = np.array(vector)
            vectorArray = np.append(vectorArray, 1)
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
                point.setY(new_points[1] + centerY)
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
                self.draw_dispplay_file(object.lines[i])
                self.update_viewport()
        elif type(object) == Reta:
            x1, y1, x2, y2 = object.line().x1(), object.line().y1(), object.line().x2(), object.line().y2()
            centerX = (x1 + x2) / 2
            centerY = (y1 + y2) / 2
            x1 -= centerX
            y1 -= centerY
            x2 -= centerX
            y2 -= centerY
            old_l1 = np.array([x1, y1, 1])
            old_l2 = np.array([x2, y2, 1])
            new_l1 = np.matmul(old_l1, scale_matrix)
            new_l2 = np.matmul(old_l2, scale_matrix)
            x1 = new_l1[0] + centerX
            y1 = new_l1[1] + centerY
            x2 = new_l2[0] + centerX
            y2 = new_l2[1] + centerY
            object.setLine(x1, y1, x2, y2)
            self.draw_dispplay_file(object)
            self.update_viewport()

    def get_scale_matrix(self, vector):
        return np.array([[vector[0], 0, 0],
                                     [0, vector[1], 0],
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

        translateLabel = QLabel('Selecione qual objeto transladar:')
        layout.addWidget(translateLabel)
        self.option_combo = QComboBox()
        for item in self.display_file:
            self.option_combo.addItem(item.name)
        layout.addWidget(self.option_combo)

        submit_button = QPushButton('Ok')
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.translate_object([int(xInput.text()), int(yInput.text())]))

        self.dialog.exec_()

    def translate_object(self, vector):
        self.dialog.accept()
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        translate_matrix = self.get_translate_matrix(vector)
        if type(object) == Wireframe:
            vectorArray = np.array([vector])
            vectorArray = np.append(vectorArray, 1)
            
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
                self.draw_dispplay_file(object.lines[i])
                self.update_viewport()
        
        elif type(object) == Reta:
            x1, y1, x2, y2 = object.line().x1(), object.line().y1(), object.line().x2(), object.line().y2()
            old_l1 = np.array([x1, y1, 1])
            old_l2 = np.array([x2, y2, 1])
            new_l1 = np.matmul(old_l1, translate_matrix)
            new_l2 = np.matmul(old_l2, translate_matrix)
            x1 = new_l1[0]
            y1 = new_l1[1]
            x2 = new_l2[0]
            y2 = new_l2[1]
            object.setLine(x1, y1, x2, y2)
            self.draw_dispplay_file(object)
            self.update_viewport()
        else:
            x, y = object.x(), object.y()
            old_points = np.array([x, y, 1])
            new_points = np.matmul(old_points, translate_matrix)
            rect = object.rect()
            object.setRect(QRectF(rect.x(), rect.y(), rect.width(), rect.height()))
            self.draw_dispplay_file(object)
            self.update_viewport()


    def get_translate_matrix(self, vector):
        return np.array([[1, 0, 0],
                        [0, 1, 0],
                        [vector[0], vector[1], 1]])