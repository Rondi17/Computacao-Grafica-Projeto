import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QSize, QPoint, QObject, QPointF, QRectF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from graphicsitem import Ponto, Reta, Wireframe
from window2 import DialogBox
from window import *
from descriptor_obj import FileObj
import numpy as np
import math

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.display_file = []
        self.onViewport = []
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 600
        self.set_window_default_paramaters()
        self.initUI()

    def objects_test(self):
        pass
        # triangulo = {'opcao': 'Wireframe', 'nome': 'triangulo', 'x1': 0, 'y1': 0, 'x2': 200, 'y2': 0, 'x3': 100, 'y3': 100}
        # self.create_new_object(triangulo)

        # new = {'opcao': 'Wireframe', 'nome': 'quadrado', 'x1': 200, 'y1': 300, 'x2': 500, 'y2': 300, 'x3': 500, 'y3': 500, 'x4': 200, 'y4': 500}
        # self.create_new_object(new)
        
    def set_window_default_paramaters(self):
        #window dimensions
        #self.Window = Window(0, 600, 0, 500)
        self.Window_mundo = Mundo(-800, 800, -800, 800)

        #viewport dimensions
        self.xv_min = 0
        self.xv_max = 600
        self.yv_min = 0
        self.yv_max = 500

        self.scale_acumulator = 1


    def initUI(self):
        self.wire_cord = []
        self.zoomFactor = 1.1   #Fator utilizado para zoom_in e zoom_out na viewport
        self.panFactor = 40.0   #Fator utilizado para pan na viewport
        self.objects = []
        self.open_save = FileObj()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_viewport()
        self.create_buttons()
        self.create_display_fileWidget()
        self.create_window()
        self.objects_test()
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
        botaoLeft = QPushButton("←", self)
        botaoLeft.move(10, 390)
        botaoLeft.resize(50, 30)
        botaoLeft.clicked.connect(self.pan_Left)
        #Shortcut = '←'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Left,
        )

        #Botão Right
        botaoRight = QPushButton("→", self)
        botaoRight.move(110, 390)
        botaoRight.resize(50, 30)
        botaoRight.clicked.connect(self.pan_Rigth)
        #Shortcut = '→'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToNextChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Rigth,
        )

        #Botão Up
        botaoUp = QPushButton("↑", self)
        botaoUp.move(60, 356)
        botaoUp.resize(50, 30)
        botaoUp.clicked.connect(self.pan_Up)
        #Shortcut = '↑'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousLine),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.pan_Up,
        )

        #Botão Down
        botaoDown = QPushButton("↓", self)
        botaoDown.move(60, 390)
        botaoDown.resize(50, 30)
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
        #novos
        #Botão window left
        botaoLeft = QPushButton("left", self)
        botaoLeft.move(10, 390)
        botaoLeft.resize(50, 30)
        botaoLeft.clicked.connect(self.window_pan_left)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('a')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.window_pan_left,
        )

        #Botão window right
        botaoRight = QPushButton("right", self)
        botaoRight.move(110, 390)
        botaoRight.resize(50, 30)
        botaoRight.clicked.connect(self.window_pan_right)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('d')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.window_pan_right,
        )

        #Botão window up
        botaoUp = QPushButton("up", self)
        botaoUp.move(60, 360)
        botaoUp.resize(50, 30)
        botaoUp.clicked.connect(self.window_pan_up)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('w')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.window_pan_up,
        )

        #Botão window down
        botaoDown = QPushButton("down", self)
        botaoDown.move(60, 390)
        botaoDown.resize(50, 30)
        botaoDown.clicked.connect(self.window_pan_down)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('s')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.window_pan_down,
        )
        #Botão rotate window right
        botaoTranslate = QPushButton('rotate right', self)
        botaoTranslate.move(10, 420)
        botaoTranslate.resize(90, 30)
        botaoTranslate.clicked.connect(self.rotate_window)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window,
        )
        #Botão rotate window right
        botaoTranslate = QPushButton('rotate left', self)
        botaoTranslate.move(110, 420)
        botaoTranslate.resize(90, 30)
        botaoTranslate.clicked.connect(self.rotate_window)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window,
        )
        #Botão para abrir arquivo 
        botaoLeft = QPushButton("open", self)
        botaoLeft.move(10, 330)
        botaoLeft.resize(50, 30)
        botaoLeft.clicked.connect(self.open_file)
        #Shortcut = '←'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToPreviousChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.open_file,
        )
        # salvar projeto em obj 
        botaoRight = QPushButton("save", self)
        botaoRight.move(110, 330)
        botaoRight.resize(50, 30)
        botaoRight.clicked.connect(self.save_project)
        #Shortcut = '→'
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.MoveToNextChar),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.save_project,
        )
        #Botão rotate window right
        botaoTranslate = QPushButton('rotate right', self)
        botaoTranslate.move(10, 420)
        botaoTranslate.resize(90, 30)
        botaoTranslate.clicked.connect(self.rotate_window_right)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window_right,
        )
        #Botão rotate window right
        botaoTranslate = QPushButton('rotate left', self)
        botaoTranslate.move(110, 420)
        botaoTranslate.resize(90, 30)
        botaoTranslate.clicked.connect(self.rotate_window_left)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window_left,
        )
        label_file = QLabel("Arquivo: ", self)
        label_file.move(20, 300)
        self.file_name = QLineEdit(self)
        self.file_name.move(70, 300)

        label_degrees = QLabel("Graus: ", self)
        label_degrees.move(20, 450)
        self.input_graus = QLineEdit(self)
        self.input_graus.move(60, 450)

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
        elif info["opcao"] == "Reta":
            new_object = Reta(info['x1'], info['y1'], info['x2'], info['y2'])
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
            self.draw_dispplay_file(new_object)
        else:
            lados = (len(info.keys()) - 2) / 2  # Quantidade de lados = quantidade de chaves, menos 2(opcao e nome) divido por dois(cada lado tem x e y)
            list = []
            vertices = [] #armazena uma lista de tuplas com os vertices
            for i in range(int(lados)):
                point = QPointF(info[f'x{i+1}'], info[f'y{i+1}'])
                list.append(point)
                ponto = (info[f'x{i+1}'], info[f'y{i+1}'], 1)
                vertices.append(ponto)
            new_object = Wireframe(list, vertices)
            self.draw_dispplay_file(new_object)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
            self.objects.append(new_object)
        self.scn()
    
    def viewport_transformation(self, xw, yw):
        #formula usada antes no 1.1 e 1.2
        # sx = (self.xv_max - self.xv_min) / (self.Window.x_max - self.Window.x_min)
        # sy = (self.yv_max - self.yv_min) / (self.Window.y_max - self.Window.y_min)
        # xv = self.xv_min + (xw - self.Window.x_min) * sx
        # yv = self.yv_max - (self.yv_min + (yw - self.Window.y_min) * sy)

        sx = (self.xv_max - self.xv_min) / (self.window_obj.x_max - self.window_obj.x_min)
        sy = (self.yv_max - self.yv_min) / (self.window_obj.y_max - self.window_obj.y_min)
        xv = self.xv_min + (xw - self.window_obj.x_min) * sx
        yv = self.yv_max - (self.yv_min + (yw - self.window_obj.y_min) * sy)
        return xv, yv

    def update_viewport(self):
        for obj in self.onViewport:
            self.scene.removeItem(obj)
        self.onViewport = []
        for obj in self.display_file:
            self.draw_dispplay_file(obj)
        self.view.centerOn(self.Window.x_max-self.Window.x_min, self.Window.y_max-self.Window.y_min)

    def zoom_in(self):
        zoom = 1.1
        scale_factor = 1.1
        #print(f"Scale factor atual: {scale_factor}")
        halfx = self.window_obj.x_max - self.window_obj.x_min
        halfy = self.window_obj.y_max - self.window_obj.y_min
        self.window_obj.x_min += halfx * (1 - 1 / scale_factor)
        self.window_obj.y_min += halfy * (1 - 1 / scale_factor)
        self.window_obj.x_max -= halfx * (1 - 1 / scale_factor)
        self.window_obj.y_max -= halfy * (1 - 1 / scale_factor)
        self.view.centerOn(halfx, halfy)
        self.update_viewport()

    def zoom_out(self):
        scale_factor = 1.1
        #print(f"Scale factor atual: {scale_factor}")
        halfx = self.Window.x_max - self.window_obj.x_min
        halfy = self.Window.y_max - self.window_obj.y_min
        self.window_obj.x_min -= halfx * (scale_factor - 1)
        self.window_obj.y_min -= halfy * (scale_factor - 1)
        self.window_obj.x_max += halfx * (scale_factor - 1)
        self.window_obj.y_max += halfy * (scale_factor - 1)
        self.view.centerOn(halfx, halfy)
        self.update_viewport()

    def draw_dispplay_file(self, obj):
        if type(obj) == Wireframe:
            #print('------------start wireframe transformation---------------')
            for line in obj.lines:
                new_x1, new_y1 = self.viewport_transformation(line[0], line[1])
                new_x2, new_y2 = self.viewport_transformation(line[2], line[3])
                pen = line.pen()
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                if obj.color != None:
                    new.setPen(pen)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
            #print('------------finish wireframe transformation---------------')
        elif type(obj) == Reta:
            print("antes: ", obj.line().x1(), obj.line().y1(), obj.line().x2(), obj.line().y2() )
            new_x1, new_y1 = self.viewport_transformation(obj.line().x1(), obj.line().y1())
            new_x2, new_y2 = self.viewport_transformation(obj.line().x2(), obj.line().y2())
            pen = obj.pen()
            print("depois: ", new_x1, new_y1, new_x2, new_y2)

            new = Reta(new_x1, new_y1, new_x2, new_y2)
            new.setPen(pen)
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
    def pan_Left(self):
        # self.Window.x_min += self.panFactor
        # self.Window.x_max += self.panFactor
        # self.update_viewport()
        self.window_obj.pan_left()
        self.scn()

    @QtCore.pyqtSlot()
    def pan_Rigth(self):
        # self.Window.x_min -= self.panFactor
        # self.Window.x_max -= self.panFactor
        # self.update_viewport()
        self.window_obj.pan_right()
        self.scn()

    @QtCore.pyqtSlot()
    def pan_Up(self):
        # self.Window.y_min -= self.panFactor
        # self.Window.y_max -= self.panFactor
        # self.update_viewport()
        self.window_obj.pan_up()
        self.scn()

    @QtCore.pyqtSlot()
    def pan_Down(self):
        # self.Window.y_min += self.panFactor
        # self.Window.y_max += self.panFactor
        # self.update_viewport()
        self.window_obj.pan_down()
        self.scn()

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
            if type(object) == Wireframe:
                object.color = color
            self.dialog.accept()
        self.scn()
            
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
        self.center_combo.currentIndexChanged.connect(self.option_changed)

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
            centerX, centerY = int(self.xInput.text()), int(self.yInput.text())
            self.rotate_object(float(self.degreesInput.text()), object, centerX, centerY)
        elif option == 'Centro do mundo':
            self.rotate_object(float(self.degreesInput.text()), object, 0, 0)
        else:
            object.centerX = 0
            object.centerY = 0
            if type(object) == Wireframe:
                for point in object.points:
                    object.centerX += point.x()
                    object.centerY += point.y()
                object.centerX = object.centerX / len(object.points)
                object.centerY = object.centerY / len(object.points)
                self.rotate_object(object, float(self.degreesInput.text()), object.centerX, object.centerY)
            elif type(object) == Reta:
                object.centerX = (object.line().x1() + object.line().x2()) / 2
                object.centerY = (object.line().y1() + object.line().y2()) / 2
                self.rotate_object(object, float(self.degreesInput.text()), object.centerX, object.centerY)
    
    def ask_point(self):
        self.xLabel = QLabel('x:')
        self.layout.addWidget(self.xLabel)
        self.xInput = QLineEdit()
        self.layout.addWidget(self.xInput)

        self.yLabel = QLabel('y:')
        self.layout.addWidget(self.yLabel)
        self.yInput = QLineEdit()
        self.layout.addWidget(self.yInput)

    def option_changed(self):
        option = self.center_combo.currentText()
        if option == 'Ponto especifico':
            self.ask_point()
        else:
            try:
                self.layout.removeWidget(self.xLabel)
                self.xLabel.deleteLater()
                self.layout.removeWidget(self.xInput)
                self.xInput.deleteLater()
                self.layout.removeWidget(self.yLabel)
                self.yLabel.deleteLater()
                self.layout.removeWidget(self.yInput)
                self.yInput.deleteLater()
                self.dialog.adjustSize()
            except (AttributeError, RuntimeError):
                pass

    def rotate_object(self, object, degrees, centerX, centerY):
        self.dialog.accept()
        
        final_matrix = self.get_final_rotate_matrix(degrees, centerX, centerY)

        if type(object) == Reta:
            x1, y1, x2, y2 = object.line().x1(), object.line().y1(), object.line().x2(), object.line().y2()
            old_l1 = np.array([x1, y1, 1])
            old_l2 = np.array([x2, y2, 1])
            new_l1 = np.matmul(old_l1, final_matrix)
            new_l2 = np.matmul(old_l2, final_matrix)
            x1 = new_l1[0]
            y1 = new_l1[1]
            x2 = new_l2[0]
            y2 = new_l2[1]
            object.setLine(x1, y1, x2, y2)
            self.scn()
        if type(object) == Wireframe:
            #Aplica matriz de rotação a cada ponto do wireframe
            for vertice in object.vertices:
                x = vertice[0]
                y = vertice[1]
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, final_matrix)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]            
            #Atualiza linhas do wireframe com base nos pontos atualizados
            for i in range(len(object.vertices)):
                x1, y1, x2, y2 = object.vertices[i-1][0], object.vertices[i-1][1], object.vertices[i][0], object.vertices[i][1]
                object.normalized_vertices.append([x1, y1, x2, y2])
            self.scn()

    def get_final_rotate_matrix(self, degrees, centerX, centerY):
        translate_toOrigin_matrix = self.get_translate_toOrigin_matrix([centerX, centerY])
        rotate_matrix = self.get_rotate_matrix(degrees)
        translate_back = self.get_translate_matrix([centerX, centerY])
        final_matrix = np.matmul(translate_toOrigin_matrix, rotate_matrix)
        final_matrix = np.matmul(final_matrix, translate_back)
        return final_matrix

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
        # Seleciona object com base na escolha to usuário na QComboBox sel.option_combo
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        #Calcula centro do objeto
        object.calculateCenter()
        translate_toOrigin_matrix = self.get_translate_toOrigin_matrix(object.getCenter())
        scale_matrix = self.get_scale_matrix(vector)
        translate_back = self.get_translate_matrix(object.getCenter())
        final_matrix = np.matmul(translate_toOrigin_matrix, scale_matrix)
        final_matrix = np.matmul(final_matrix, translate_back)

        if type(object) == Wireframe:
            #Aplica matriz de escala a cada ponto do wireframe
            for vertice in object.vertices:
                x = vertice[0]
                y = vertice[1]
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, final_matrix)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]
            
            #Atualiza linhas do wireframe com base nos pontos atualizados
            for i in range(len(object.lines)):
                x1, y1, x2, y2 = object.vertices[i-1][0], object.vertices[i-1][1], object.vertices[i][0], object.vertices[i][1]
                object.normalized_vertices.append([x1, y1, x2, y2])
                self.scn()
        elif type(object) == Reta:
            x1, y1, x2, y2 = object.line().x1(), object.line().y1(), object.line().x2(), object.line().y2()
            old_l1 = np.array([x1, y1, 1])
            old_l2 = np.array([x2, y2, 1])
            new_l1 = np.matmul(old_l1, final_matrix)
            new_l2 = np.matmul(old_l2, final_matrix)
            x1 = new_l1[0]
            y1 = new_l1[1]
            x2 = new_l2[0]
            y2 = new_l2[1]
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
        # Seleciona object com base na escolha to usuário na QComboBox sel.option_combo
        for item in self.display_file:
            if item.name == self.option_combo.currentText():
                object = item
                break
        
        translate_matrix = self.get_translate_matrix(vector)
        if type(object) == Wireframe:
            #Aplica matriz de tranlação a cada ponto do wireframe
            for vertice in object.vertices:
                x = vertice[0]
                y = vertice[1]
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, translate_matrix)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]

            #Atualiza linhas do wireframe com base nos pontos atualizados
            for i in range(len(object.vertices)):
                x1, y1, x2, y2 = object.vertices[i-1][0], object.vertices[i-1][1], object.vertices[i][0], object.vertices[i][1]
                object.normalized_vertices.append([x1, y1, x2, y2])
                self.scn()
        
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
    
    def get_translate_toOrigin_matrix(self, vector):
        return np.array(([[1, 0, 0],
                        [0, 1, 0],
                        [-vector[0], -vector[1], 1]]))
    
    def gerar_SCN(self):
        #0. Crie ou mova a window onde deseja
        self.Window = Window(100, 600, 100, 500) #Pegar coordenadas de onde se deseja criar o mundo e angulo?
        #1. Translate Wc para origem(translade o mundo para o centro do objeto)
        translate_matrix = self.get_translate_matrix([-self.Window.centerX, -self.Window.centerY])

        #2. Determine Vup e angulo de Vup com Y
        #Define Vup como aresta esquerda da window, e então rotaciona a aresta
        self.Window.Vup = Reta(self.Window.x_min, self.Window.y_min, self.Window.x_min, self.Window.y_max)
        degrees = 30.0
        rotate_matrix = self.get_rotate_matrix(degrees)
        scale_matrix = self.get_scale_matrix([self.Window.centerX, self.Window.centerY])
        
        final_matrix = np.matmul(translate_matrix, rotate_matrix)
        final_matrix = np.matmul(final_matrix, scale_matrix)

        #Precisa definir vetor e alinhar mundo com vetor
        #3. Rotacione o mundo de forma a alinhar Vup com o eixo Y
        for item in self.display_file:
            if type(item) == Reta:
                x1, y1, x2, y2 = item.line.x1(), item.line.y1(), item.line.x2(), item.line.y2()
                old_l1 = np.array([x1, y1, 1])
                old_l2 = np.array([x2, y2, 1])
                new_l1 = np.matmul(old_l1, final_matrix)
                new_l2 = np.matmul(old_l2, final_matrix)
                item.x1N = new_l1[0]
                item.y1N = new_l1[1]
                item.x2N = new_l2[0]
                item.y2N = new_l2[1]

                #self.draw_dispplay_file(item) ???
                #Deve-se desenhar o objeto na window com coordenadas normalizadas?

            if type(item) == Wireframe:
                for reta in item.lines:
                    x1, y1, x2, y2 = reta.line.x1(), reta.line.y1(), reta.line.x2(), reta.line.y2()
                    reta.x1N = x1
                    reta.y1N = y1
                    reta.x2N = x2
                    reta.y2N = y2

    def create_window(self):
        self.window_obj = Window(-1,1,-1,1)
        self.scn()

    def window_pan_right(self):
        dx = self.reference.pan_right()
        self.move_window(0, dx, 0)

    def window_pan_left(self):
        self.reference.pan_left()
        self.move_window()

    def window_pan_up(self):
        self.reference.pan_up()
        self.move_window()

    def window_pan_down(self):
        self.reference.pan_down()
        self.move_window()

    def rotate_window_right(self):
        degrees = self.get_degrees()
        self.window_obj.degrees += degrees
        self.scn()
    
    def rotate_window_left(self):
        degrees = self.get_degrees()
        self.window_obj.degrees -= degrees
        self.scn()
    
    def move_window(self, degrees, dx, dy):
        combined = self.reference.move(degrees, dx, dy)  #retorna a matriz composta
        self.update_normalized_coord(combined)

    def update_normalized_coord(self, combined_matrix):
        for obj in self.display_file: 
            updated_vertices = []
            if isinstance(obj, Wireframe):
                vertices = obj.vertices
                for vertex in vertices:
                    v = np.append(vertex, 1.0)
                    transformed_vertex = np.dot(combined_matrix, v)
                    resultado = v * combined_matrix
                    updated_vertices.append(resultado)
    
    def get_degrees(self):
        degrees_text = self.input_graus.text()
        try:
            degrees = float(degrees_text)
        except ValueError:
            QMessageBox.warning(self, 'Aviso', 'Digite um número válido!')
        self.input_graus.clear()
        return degrees
    
    def get_degrees(self):
        degrees_text = self.input_graus.text()
        try:
            degrees = float(degrees_text)
        except ValueError:
            QMessageBox.warning(self, 'Aviso', 'Digite um número válido!')
        self.input_graus.clear()
        return degrees

    def get_file_name(self):
        file_name = self.file_name.text()
        try:
            file = file_name
        except ValueError:
            QMessageBox.warning(self, 'Aviso', 'Digite um nome válido! (name.obj)')
        self.file_name.clear()
        return file

    def save_project(self):
        file_name = self.get_file_name()
        if isinstance(file_name, str):
            self.open_save.save_file(self.display_file, file_name)

    def open_file(self):
        file_name = self.get_file_name()
        if isinstance(file_name, str):
            dic = self.open_save.open_file(file_name)
            if dic["name"] != "" and dic["vertices"] != "":
                vertices = dic["vertices"]
                new = {}
                for i in range(len(vertices)):
                    new[f'x{i+1}'] = vertices[i][0]
                    new[f'y{i+1}'] = vertices[i][1]
                new["opcao"] = 'Wireframe'
                new["nome"] = dic["name"]
                self.create_new_object(new)

    def scn(self, degrees=0):
        combined = self.window_obj.scn(self.Window_mundo.centerX, self.Window_mundo.centerY)  #retorna a matriz composta
        self.update_normalized_coordinates(combined)

    def update_normalized_coordinates(self, combined_matrix): #multiplica vertices * matriz composta
        for obj in self.display_file: 
            if isinstance(obj, Wireframe):
                updated_vertices = []
                vertices = obj.vertices #pega sempre as coordenadas originais
                for vertex in vertices:
                    vertex_homogeneous = np.array([vertex[0], vertex[1], vertex[2]])
                    vertex_updated = np.matmul(vertex_homogeneous, combined_matrix)
                    #vertex_updated = np.dot(vertex_homogeneous, combined_matrix)
                    updated_vertices.append(vertex_updated)
                lista_retas = []
                for i in range(len(updated_vertices)):
                    x1, y1, x2, y2 = updated_vertices[i-1][0], updated_vertices[i-1][1], updated_vertices[i][0], updated_vertices[i][1]
                    lista_retas.append([x1, y1, x2, y2])
                obj.normalized_vertices = lista_retas
        self.update_viewport()