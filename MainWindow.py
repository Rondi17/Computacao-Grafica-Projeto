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
        #self.setGeometry(100, 100, 800, 600)
        self.title = "Sistema Gráfico Interativo 2D"
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 600
        self.set_window_default_paramaters()
        self.initUI()

    def objects_test(self):
        # triangulo = {'opcao': 'Wireframe', 'nome': 'triangulo', 'x1': 0, 'y1': 0, 'x2': 200, 'y2': 0, 'x3': 100, 'y3': 100}
        # self.create_new_object(triangulo)

        # quadrado = {'opcao': 'Wireframe', 'nome': 'quadrado', 'x1': 200, 'y1': 300, 'x2': 500, 'y2': 300, 'x3': 500, 'y3': 500, 'x4': 200, 'y4': 500}
        # self.create_new_object(quadrado)

        # outside_triangle = {'opcao': 'Wireframe', 'nome': 'outside_triangle', 'x1': -1000, 'y1': -1000, 'x2': -1500, 'y2': 1200, 'x3': 500, 'y3': 1000}
        # self.create_new_object(outside_triangle)

        window_limit = {'opcao': 'Wireframe', 'nome': 'window_limit', 'x1': self.Window_mundo.x_min+100, 'y1': self.Window_mundo.y_min+100,
                                                                  'x2': self.Window_mundo.x_min+100, 'y2': self.Window_mundo.y_max-100,
                                                                  'x3': self.Window_mundo.x_max-100, 'y3': self.Window_mundo.y_max-100,
                                                                  'x4': self.Window_mundo.x_max-100, 'y4': self.Window_mundo.y_min+100}
        self.create_new_object(window_limit)

        # curve = {'opcao': 'Curva', 'nome': 'lal', 'num_curvas': 1, 'p10': '1,1', 'p40': '2,2', 'r10': '3,3', 'r40': '4,4'}
        curve = {'opcao': 'Curva', 'nome': 'minha-curva', 'num_curvas': 3, 
                 'p10': '100,100', 'p40': '300,200', 'r10': '150,0', 'r40': '0,100', 
                 'p11': '300,200', 'p41': '500,300', 'r11': '100,50', 'r41': '50,200', 
                 'p12': '500,300', 'p42': '600,400', 'r12': '50,150', 'r42': '0,100'}
        self.create_new_object(curve)

        curve_continue = {'opcao': 'Curva', 'nome': 'curva-continuidade4', 'num_curvas': 4, 'p10': '0,200', 'p40': '400,200', 'r10': '100,0', 'r40': '100,0', 'p11': '400,200', 'p41': '600,600', 'r11': '100,0', 'r41': '100,400', 'p12': '600,600', 'p42': '1000,200', 'r12': '100,400', 'r42': '100,0', 'p13': '1000,200', 'p43': '1200,200', 'r13': '100,0', 'r43': '100,0'}
        self.create_new_object(curve_continue)

    def initUI(self):
        self.wire_cord = []
        #Fator utilizado para zoom_in e zoom_out na viewport
        self.zoomFactor = 1.1
        #Fator utilizado para pan na viewport
        self.panFactor = 40.0
        self.objects = []
        self.open_save = FileObj()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_viewport()
        self.create_buttons()
        self.create_display_fileWidget()
        self.create_window()
        self.objects_test()
        self.create_window()
        self.show()

    #Cria o ListWidget responsável por representar o displayfile
    def create_display_fileWidget(self):
        self.display_fileWidget = QListWidget(self)
        self.display_fileWidget.setGeometry(0, 0, 200, 200)
        self.display_fileWidget.show()

    def create_window(self):
        self.window_obj = Window(-1,1,-1,1)
        self.scn()

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
            activated=self.new_zoom_out,
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
            activated=self.new_zoom_out,
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
        #Botão Right salvar projeto em obj 
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
        #Botão window left
        botaoLeft = QPushButton("←", self) 
        botaoLeft.move(10, 390)
        botaoLeft.resize(50, 30)
        botaoLeft.clicked.connect(self.window_pan_left)
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence('a')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.window_pan_left,
        )
        #Botão right
        botaoRight = QPushButton("→", self)
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
        botaoUp = QPushButton("↑", self)
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
        botaoDown = QPushButton("↓", self)
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
        label_degrees = QLabel("Graus: ", self)
        label_degrees.move(20, 450)
        self.input_graus = QLineEdit(self)
        self.input_graus.move(60, 450)

        label_file = QLabel("Arquivo: ", self)
        label_file.move(20, 300)
        self.file_name = QLineEdit(self)
        self.file_name.move(70, 300)

    @QtCore.pyqtSlot()
    def get_object_information(self): #tela para criar um novo objeto
        user_input = {}
        box = DialogBox()
        if box.exec():
            user_input = box.get_input()
            self.create_new_object(user_input)

    def new_zoom_in(self):
        zoom = 1.1
        scale_factor = 1.1
        print(f"Scale factor atual: {scale_factor}")
        halfx = self.window_obj.x_max - self.window_obj.x_min
        halfy = self.window_obj.y_max - self.window_obj.y_min
        self.window_obj.x_min += halfx * (1 - 1 / scale_factor)
        self.window_obj.y_min += halfy * (1 - 1 / scale_factor)
        self.window_obj.x_max -= halfx * (1 - 1 / scale_factor)
        self.window_obj.y_max -= halfy * (1 - 1 / scale_factor)
        self.view.centerOn(halfx, halfy)
        #self.Window.x_min += 60
        #self.Window.y_min += 50
        #self.Window.x_max -= 60
        #self.Window.y_max -= 50
        self.update_viewport()
        print("new zoom in")

    def new_zoom_out(self):
        scale_factor = 1.1
        print(f"Scale factor atual: {scale_factor}")
        halfx = self.window_obj.x_max - self.window_obj.x_min
        halfy = self.window_obj.y_max - self.window_obj.y_min
        self.window_obj.x_min -= halfx * (scale_factor - 1)
        self.window_obj.y_min -= halfy * (scale_factor - 1)
        self.window_obj.x_max += halfx * (scale_factor - 1)
        self.window_obj.y_max += halfy * (scale_factor - 1)
        self.view.centerOn(halfx, halfy)
        # self.Window.x_min = self.padrao_x_min * scale_factor
        # self.Window.y_min = self.padrao_y_min * scale_factor
        self.update_viewport()
        print("new zoom out")

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
            self.rotate_object(object, float(self.degreesInput.text()), centerX, centerY)
        elif option == 'Centro do mundo':
            self.rotate_object(object, float(self.degreesInput.text()), 0, 0)
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
                print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, final_matrix)
                vertice[0] =new_points[0]
                vertice[1] =new_points[1]
                print(f'Points after: x = {x}, y = {y}')
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
        object.calculateCenter() #Calcula centro do objeto
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
                # print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, final_matrix)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]
                # print(f'Points after: x = {x}, y = {y}')
            
            #Atualiza linhas do wireframe com base nos pontos atualizados
            for i in range(len(object.vertices)):
                x1, y1, x2, y2 = object.vertices[i-1][0], object.vertices[i-1][1], object.vertices[i][0], object.vertices[i][1]
                #print(f' 2- {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
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
                print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, translate_matrix)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]
                print(f'Points after: x = {x}, y = {y}')

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

    def window_pan_right(self):
        self.window_obj.pan_right()
        self.scn()
        #self.update_viewport() isso quem chama é ... 

    def window_pan_left(self):
        self.window_obj.pan_left()
        self.scn()

    def window_pan_up(self):
        self.window_obj.pan_up()
        self.scn()

    def window_pan_down(self):
        self.window_obj.pan_down()
        self.scn()
    
    def create_new_object(self, info):
        print("info: ", info)
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
        elif info["opcao"] == "Wireframe":
            lados = (len(info.keys()) - 2) / 2  # Quantidade de lados = quantidade de chaves, menos 2(opcao e nome) divido por dois(cada lado tem x e y)
            list = []
            vertices = []

            for i in range(int(lados)):
                point = QPointF(info[f'x{i+1}'], info[f'y{i+1}'])
                list.append(point)
                ponto = [info[f'x{i+1}'], info[f'y{i+1}'], 1]
                vertices.append(ponto)
            new_object = Wireframe(list, vertices)
            #self.draw_dispplay_file(new_object)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
            self.objects.append(new_object)

        elif info["opcao"] == "Curva":
            curves = []
            #info:  {'opcao': 'Curva', 'nome': 'my_curve', 'p1': [100, 100], 'p4': [400, 400], 'r1': [200, 0], 'r4': [0, 200]}
            for i in range((info["num_curvas"])):
                curve = [info[f'p1{i}'], info[f'p4{i}'], info[f'r1{i}'], info[f'r4{i}']]
                curves.append(curve)
            lista_de_inteiros = [[tuple(map(int, item.split(','))) for item in sublista] for sublista in curves]
            print("lista-de-inteiros: ", lista_de_inteiros)
            new_object = HermiteCurve(lista_de_inteiros)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
        self.scn()

    def set_window_default_paramaters(self):
        #window dimensions
        self.Window_mundo = Mundo(-800, 800, -800, 800)
        #viewport dimensions
        self.xv_min = 0
        self.xv_max = 600
        self.yv_min = 0
        self.yv_max = 500

        self.scale_acumulator = 1

    def create_viewport(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(200,0,600,500)
        #self.view.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        #Set noAnchor to GraphicsView, enabling the view to move
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor(0)) #ponto de ancoragem

    def viewport_transformation(self, xw, yw):
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
        self.view.centerOn(self.Window_mundo.x_max-self.Window_mundo.x_min, self.Window_mundo.y_max-self.Window_mundo.y_min)

    def rotate_window_right(self):
        degrees = self.get_degrees()
        self.window_obj.degrees += degrees
        self.scn()
    
    def rotate_window_left(self):
        degrees = self.get_degrees()
        self.window_obj.degrees -= degrees
        self.scn()

    def scn(self, degrees=0):
        combined = self.window_obj.scn(self.Window_mundo.centerX, self.Window_mundo.centerY)  #retorna a matriz composta
        #print('call update_normalized_coordinates')
        self.update_normalized_coordinates(combined)

    def update_normalized_coordinates(self, combined_matrix): #multiplica vertices * matriz composta
        self.define_region_codes()
        for obj in self.display_file:
            print(f'obj name = {obj.name}')
            if isinstance(obj, Wireframe):
                updated_vertices = []    
                for reta in obj.lines:
                    if reta.showing:
                        # print(f'showing = {reta.showing}')
                        # print(f'x1 = {reta.line().x1()}, y1 = {reta.line().y1()}, x2 = {reta.line().x2()}, y2 = {reta.line().y2()}')
                        # print(f'x1I = {reta.x1I}, y1I = {reta.y1I}, x2I = {reta.x2I}, y2I = {reta.y2I}')
                        vertice1 = np.array([reta.x1I, reta.y1I, 1])
                        vertice2 = np.array([reta.x2I, reta.y2I, 1])
                        vertice1_updated = np.matmul(vertice1, combined_matrix)
                        vertice2_updated = np.matmul(vertice2, combined_matrix)
                        updated_vertices.append(vertice1_updated)
                        updated_vertices.append(vertice2_updated)
                lista_retas = []
                for i in range(len(updated_vertices)):
                    x1, y1, x2, y2 = updated_vertices[i-1][0], updated_vertices[i-1][1], updated_vertices[i][0], updated_vertices[i][1]
                    lista_retas.append([x1, y1, x2, y2])
                obj.normalized_vertices = lista_retas

            elif isinstance(obj, HermiteCurve):
                #obj.points tem os pontos da curva
                up_vertices = []
                for sublist in obj.curve_points:
                #for list in obj.curve_clipping:
                    for list in sublist:
                        vertice = np.array([list[0], list[1], 1])
                        vertice_up = np.matmul(vertice, combined_matrix)
                        up_vertices.append(vertice_up)
                retas = []
                for i in range(len(up_vertices) - 1):
                    x1,y1,x2,y2 = up_vertices[i][0], up_vertices[i][1], up_vertices[i+1][0], up_vertices[i+1][1]
                    retas.append([x1, y1, x2, y2])
                obj.lines_curve = retas
                #print("obj-norma: ", obj.normalized_vertices) #ate aqui funfa
        self.update_viewport()

    def draw_dispplay_file(self, obj):
        if type(obj) == Wireframe:
            #print(f'obj_drawing = {obj.name}')
            #print('------------start wireframe transformation---------------')
            for line in obj.normalized_vertices:
                #print(f'line = {line}')
                new_x1, new_y1 = self.viewport_transformation(line[0], line[1])
                new_x2, new_y2 = self.viewport_transformation(line[2], line[3])
                #pen = l.pen() #??
                #print("depois: ", new_x1, new_y1, new_x2, new_y2)
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                if obj.color != None:
                    new.setPen(obj.color)
                #new.setPen(pen)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
            #print('------------finish wireframe transformation---------------')
        elif type(obj) == Reta:
            #print("antes: ", obj.line().x1(), obj.line().y1(), obj.line().x2(), obj.line().y2() )
            new_x1, new_y1 = self.viewport_transformation(obj.line().x1(), obj.line().y1())
            new_x2, new_y2 = self.viewport_transformation(obj.line().x2(), obj.line().y2())
            pen = obj.pen()
            #print("depois: ", new_x1, new_y1, new_x2, new_y2)

            new = Reta(new_x1, new_y1, new_x2, new_y2)
            new.setPen(pen)
            self.scene.addItem(new)
            self.onViewport.append(new)
            self.view.show()
        elif type(obj) == Ponto:
            print('reach point')
            #print(f'antes : x = {obj.x()}, y = {obj.y()}')
            new_x1, new_y1 = self.viewport_transformation(obj.x(), obj.y())
            print(f'x = {new_x1}, y = {new_y1}')
            new = Ponto(new_x1, new_y1)
            self.scene.addItem(new)
            self.onViewport.append(new)
            self.view.show()
            print("end setPoint")
        elif type(obj) == HermiteCurve:
            for line in obj.lines_curve:
                #print("antes: ",line[0], line[1], line[2], line[3])
                new_x1, new_y1 = self.viewport_transformation(line[0], line[1])
                new_x2, new_y2 = self.viewport_transformation(line[2], line[3])
                #print("depois: ", new_x1, new_y1, new_x2, new_y2)
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                if obj.color != None:
                    new.setPen(obj.color)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
    
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

    def point_clipping(self, point:Ponto):
        if self.window_obj.x_min <= point.x() <= self.window_obj.x_max:
            if self.window_obj.y_min <= point.y() <= self.window_obj.y_max:
                point.clipped = True

    #funcao que chama o metodo clipping dos objetos
    def define_region_codes(self):
        for item in self.display_file:
            if isinstance(item, Wireframe):
                for reta in item.lines:
                    self.defineIntersection(reta)
            elif isinstance(item, Reta):
                self.defineIntersection(item)
            elif isinstance(item, Ponto):
                self.point_clipping(item)
            elif isinstance(item, HermiteCurve):
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min +100, self.Window_mundo.y_min+100, self.Window_mundo.x_max - 100, self.Window_mundo.y_max -100
                item.clipping(xmin, ymin, xmax, ymax)

    def defineIntersection(self, item):
        top_left = 9
        top = 8
        top_right = 10

        left = 1
        center = 0
        right = 2

        bottom_left = 5
        bottom = 4
        bottom_right = 6

        if isinstance(item, Reta):
                x1, y1, x2, y2 = item.line().x1(), item.line().y1(), item.line().x2(), item.line().y2()
                #print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min +100, self.Window_mundo.y_min+100, self.Window_mundo.x_max - 100, self.Window_mundo.y_max -100
                x, y = x1, y1
                item.RC = ['', ''] #empty list with strings to be overwritten
                for _ in range(2):
                    if _ == 1: 
                        x, y = x2, y2
                    if x < xmin: #left
                        if y < ymin: #bottom
                            item.RC[_] = bottom_left
                        elif y > ymax: #top
                            item.RC[_] = top_left
                        else: # just left
                            item.RC[_] = left
                    
                    elif x > xmax: #right
                        if y < ymin: #bottom
                            item.RC[_] = bottom_right
                        elif y > ymax: #top
                            item.RC[_] = top_right
                        else: # just right
                            item.RC[_] = right
                    
                    else: #middle
                        if y < ymin: #bottom
                            item.RC[_] = bottom
                        elif y > ymax: #top
                            item.RC[_] = top
                        else: # center
                            item.RC[_] = center
                #print(f'item.RC[0] = {item.RC[0]}, item.RC[1] = {item.RC[1]}')
                if item.RC[0] == item.RC[1] == 0: #totalmente na janela 
                    item.clipped = False
                    item.showing = True
                elif item.RC[0] != item.RC[1]: #parcialmente visivel:
                    if item.RC[0] & item.RC[1] == 0:
                        #print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
                        #print(f'xmin = {xmin}, ymin = {ymin}, xmax = {xmax}, ymax = {ymax}')
                        m = (y2 - y1) / (x2 - x1)
                        intersection = item.RC[0] | item.RC[1] # logical OR
                        intersection = bin(intersection)[2:] # Get binary representation without '0b'
                        intersection += '0' * (4 - len(intersection)) # complete intersection with zeros on the left until reach 4 bits
                        #print(f'Variable intersection  = {intersection}')

                        if intersection[3] == '1': #Left intersection
                            x = xmin
                            y = m*(xmin - x1) + y1
                            if ymin < y < ymax:
                                item.clipped = True
                                item.showing = True
                                print(f'left intersection, x = {x}, y = {y}')
                                if x1 < x2:
                                    item.x1I = x
                                    item.y1I = y
                                else:
                                    item.x2I = x
                                    item.y2I = y
                        if intersection[2] == '1': # Right intersection
                            x = xmax
                            y = m*(xmax - x1) + y1
                            if ymin < y < ymax :
                                item.clipped = True
                                item.showing = True
                                if x1 > x2:
                                    item.x1I = x
                                    item.y1I = y
                                else:
                                    item.x2I = x
                                    item.y2I = y
                                print(f'right intersection, x = {x}, y = {y}')
                                
                        
                        if intersection[0] == '1': # Top intersection
                            y = ymax
                            x = x1 + (1/m)*(ymax - y1)
                            if xmin < x < xmax:
                                item.clipped = True
                                item.showing = True
                                if  y1> y2:
                                    item.x1I = x
                                    item.y1I = y
                                else: 
                                    item.x2I = x
                                    item.y2I = y
                                print(f'top intersection, x = {x}, y = {y}')

                        
                        if intersection[1] == '1': #Bottom intersection
                            y = ymin
                            x = x1 + (1/m)*(ymin - y1)
                            if xmin < x < xmax:
                                item.clipped = True
                                item.showing = True
                                if y1 < y2:
                                    item.x1I = x
                                    item.y1I = y
                                else: 
                                    item.x2I = x
                                    item.y2I = y
                                print(f'bottom intersection, x = {x}, y = {y}')
                        
                elif item.RC[0] & item.RC[1] != 0: #Completamente fora da janela
                    item.clipped = True
                    item.showing = False
                    print(f'reta not showing')

                    



