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
from transformations import *
from clipping import Clipping

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
        self.zoomMode = False

    def objects_test(self):
        window_limit = {'opcao': 'Wireframe', 'nome': 'window_limit', 'x1': self.Window_mundo.x_min+50, 'y1': self.Window_mundo.y_min+50,
                                                                  'x2': self.Window_mundo.x_min+50, 'y2': self.Window_mundo.y_max-50,
                                                                  'x3': self.Window_mundo.x_max-50, 'y3': self.Window_mundo.y_max-50,
                                                                  'x4': self.Window_mundo.x_max-50, 'y4': self.Window_mundo.y_min+50}
        self.create_new_object(window_limit)

        triangulo = {'opcao': 'Wireframe', 'nome': 'triangulo', 'x1': 0, 'y1': 0, 'x2': 200, 'y2': 0, 'x3': 100, 'y3': 100}
        self.create_new_object(triangulo)

        quadrado = {'opcao': 'Wireframe', 'nome': 'quadrado', 'x1': 200, 'y1': 300, 'x2': 500, 'y2': 300, 'x3': 500, 'y3': 500, 'x4': 200, 'y4': 500}
        self.create_new_object(quadrado)

        outside_triangle = {'opcao': 'Wireframe', 'nome': 'outside_triangle', 'x1': -1000, 'y1': -1000, 'x2': -1500, 'y2': 1200, 'x3': 500, 'y3': 1000}
        self.create_new_object(outside_triangle)

        # curve = {'opcao': 'Curva', 'nome': 'lal', 'num_curvas': 1, 'p10': '1,1', 'p40': '2,2', 'r10': '3,3', 'r40': '4,4'}
        curve = {'opcao': 'Curva', 'nome': 'horizontal-curve', 'num_curvas': 3, 'p10': '-1200,0', 'p40': '-400,0', 'r10': '0,50', 'r40': '0,-50', 'p11': '-400,0', 'p41': '400,0', 'r11': '0,50', 'r41': '0,-50', 'p12': '400,0', 'p42': '1200,0', 'r12': '0,50', 'r42': '0,-50'}
        #self.create_new_object(curve)

        curve_continue = {'opcao': 'Curva', 'nome': 'curva-continuidade4', 'num_curvas': 4, 'p10': '0,200', 'p40': '400,200', 'r10': '100,0', 'r40': '100,0', 'p11': '400,200', 'p41': '600,600', 'r11': '100,0', 'r41': '100,400', 'p12': '600,600', 'p42': '1000,200', 'r12': '100,400', 'r42': '100,0', 'p13': '1000,200', 'p43': '1200,200', 'r13': '100,0', 'r43': '100,0'}
        self.create_new_object(curve_continue)
        
        curve_bspline = {'opcao': 'Curva-BSpline', 'nome': 'my-bspline1', 'num_control_points': 4, 'p1': '100,100', 'p2': '200,200', 'p3': '300,200', 'p4': '400,100'}
        self.create_new_object(curve_bspline)

        curve_bspline2 = {'opcao': 'Curva-BSpline', 'nome': 'my-bspline2', 'num_control_points': 10, 'p1': '0,0', 'p2': '100,100', 'p3': '200,100', 'p4': '300,0','p5': '400,0', 'p6': '500,200', 'p7': '600,200','p8': '700,0', 'p9': '800,0','p10': '900,0',}
        self.create_new_object(curve_bspline2)
        
        self.scn()

    def initUI(self):
        self.wire_cord = []
        #Fator utilizado para zoom_in e zoom_out na viewport
        self.zoomFactor = 1.1
        #Fator utilizado para pan na viewport
        self.panFactor = 40.0
        self.open_save = FileObj()
        self.transformations = Transformation3D()
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

    def remove_on_display_file(self, name):
        for i in range(self.display_fileWidget.count()):
            if self.display_fileWidget.item(i).text() == name:
                self.display_fileWidget.takeItem(i)
                self.display_fileWidget.update()
                break

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
            QtGui.QKeySequence(QtGui.QKeySequence('Alt+S')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.window_pan_down,
        )
        #Botão rotate window X
        botaoTranslate = QPushButton('X', self)
        botaoTranslate.move(10, 420)
        botaoTranslate.resize(30, 30)
        botaoTranslate.clicked.connect(self.rotate_window_right)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window_right,
        )

        #Botão rotate window Y
        botaoTranslate = QPushButton('Y', self)
        botaoTranslate.move(50, 420)
        botaoTranslate.resize(30, 30)
        botaoTranslate.clicked.connect(self.rotate_window_left)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window_left,
        )

        #Botao para rotacionar em Z
        botaoTranslate = QPushButton('Z', self)
        botaoTranslate.move(90, 420)
        botaoTranslate.resize(30, 30)
        botaoTranslate.clicked.connect(self.rotate_window_right)
        QtWidgets.QShortcut(
            #QtGui.QKeySequence(QtGui.QKeySequence('rw')),
            self.view,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.rotate_window_right,
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
        scale_factor = 0.05
        
        halfx = self.window_obj.getCenterX()
        halfy = self.window_obj.getCenterY()
        self.window_obj.x_min += halfx * scale_factor
        self.window_obj.y_min += halfy * scale_factor
        self.window_obj.x_max -= halfx * scale_factor
        self.window_obj.y_max -= halfy * scale_factor
        self.view.centerOn(halfx, halfy)
        self.update_window_limit('zoom_in')
        self.scn()
        #self.update_viewport()
        ##("new zoom in")

    def new_zoom_out(self):
        scale_factor = 0.05
        
        halfx = self.window_obj.getCenterX()
        halfy = self.window_obj.getCenterY()
        self.window_obj.x_min -= halfx * scale_factor
        self.window_obj.y_min -= halfy * scale_factor
        self.window_obj.x_max += halfx * scale_factor
        self.window_obj.y_max += halfy * scale_factor 
        self.view.centerOn(halfx, halfy)
        self.update_window_limit('zoom_out')
        self.scn()
        #self.update_viewport()
        #print("new zoom out")

    @QtCore.pyqtSlot()
    def changeColor_call(self):
        self.dialog = QDialog(self)

        self.dialog.setWindowTitle("Qual objeto deseja mudar de cor?")
        self.layout = QVBoxLayout(self.dialog)

        self.object_combo = QComboBox()
        for item in self.display_file:
            self.object_combo.addItem(item.name)
        self.layout.addWidget(self.object_combo)

        self.option_combo = QComboBox()
        self.option_combo.addItems(['Pen', 'Brush'])
        self.layout.addWidget(self.option_combo)

        submit_button = QPushButton('Ok')
        self.layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.colorDialog())
        
        self.dialog.exec_()

    def colorDialog(self):
        for item in self.display_file:
            if item.name == self.object_combo.currentText():
                object = item
                break
        option = self.option_combo.currentText()
        colorDialog = QColorDialog(self)
        colorDialog.setCurrentColor(Qt.red)
        if colorDialog.exec_() == QColorDialog.Accepted:
            color = colorDialog.selectedColor()
            if type(object) == Wireframe or HermiteCurve or BSplineCurve:
                if option == 'Pen':
                    object.color = color
                elif option == 'Brush':
                    object.brush = color
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
        #self.center_combo.addItems(['Centro do mundo', 'Centro do objeto', 'Ponto especifico'])
        self.center_combo.addItems(['Rotation x', 'Rotation y', 'Rotation z', 'Arbitrary Rotation'])
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
        elif option == "Rotation x":
            pass
        elif option == "Rotation y":
            pass
        elif option == "Rotation z":
            pass
        elif option == "Arbitrary Rotation":
            pass
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
        final_matrix = Transformation.get_final_rotate_matrix(Transformation, degrees, centerX, centerY)
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
                #print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, final_matrix)
                vertice[0] =new_points[0]
                vertice[1] =new_points[1]
                #print(f'Points after: x = {x}, y = {y}')
            object.recriateLines()
            #Atualiza linhas do wireframe com base nos pontos atualizados
            for i in range(len(object.vertices)):
                x1, y1, x2, y2 = object.vertices[i-1][0], object.vertices[i-1][1], object.vertices[i][0], object.vertices[i][1]
                object.normalized_vertices.append([x1, y1, x2, y2])
            self.scn()
        elif type(object) == Point3D:
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

        zLabel = QLabel('z:')
        layout.addWidget(zLabel)
        zInput = QLineEdit()
        layout.addWidget(zInput)

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
        final_matrix = Transformation.get_final_scale_matrix(Transformation, object, vector)
        print(final_matrix)
        if type(object) == Wireframe:
            #Aplica matriz de escala a cada ponto do wireframe
            for vertice in object.vertices:
                x = vertice[0]
                y = vertice[1]
                print(f'Points before: x = {vertice[0]}, y = {vertice[1]}')
                old_points = np.array([x, y, 1])
                print(old_points)
                new_points = np.matmul(old_points, final_matrix)
                print(new_points)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]
                print(f'Points after: x = {vertice[0]}, y = {vertice[1]}')
            object.recriateLines()
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

        elif type(object) == Point3D:
            #print("vertices antes: ", object.vertices)
            old_vertice = np.array([object.vertices[0], object.vertices[1], object.vertices[2]])
            new_vertice = np.matmul(old_vertice, final_matrix)
            object.vertices[0] = new_vertice[0]
            object.vertices[1] = new_vertice[1]
            object.vertices[2] = new_vertice[2]
            #print("vertices antes: ", object.vertices)
    
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

        zLabel = QLabel('z:')
        layout.addWidget(zLabel)
        zInput = QLineEdit()
        layout.addWidget(zInput)

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

        translate_matrix = Transformation.get_translate_matrix(vector)
        if type(object) == Wireframe:
            #Aplica matriz de tranlação a cada ponto do wireframe
            for vertice in object.vertices:
                x = vertice[0]
                y = vertice[1]
                #print(f'Points before: x = {x}, y = {y}')
                old_points = np.array([x, y, 1])
                new_points = np.matmul(old_points, translate_matrix)
                vertice[0] = new_points[0]
                vertice[1] = new_points[1]
                #print(f'Points after: x = {x}, y = {y}')
            object.recriateLines()
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
        elif type(object) == Point3D:
            #print("ANTES: ", object.vertices)
            translate_matrix = self.transformations.get_translate_matrix(vector)
            object.translate(translate_matrix)
            #print("DEPOIS: ", object.vertices)
        else:
            x, y = object.x(), object.y()
            old_points = np.array([x, y, 1])
            new_points = np.matmul(old_points, translate_matrix)
            rect = object.rect()
            object.setRect(QRectF(rect.x(), rect.y(), rect.width(), rect.height()))
            self.draw_dispplay_file(object)
            self.update_viewport()


    def window_pan_right(self):
        self.window_obj.pan_right()
        self.update_window_limit('pan_right')
        self.scn()

    def window_pan_left(self):
        self.window_obj.pan_left()
        self.update_window_limit('pan_left')
        self.scn()

    def window_pan_up(self):
        self.window_obj.pan_up()
        self.update_window_limit('pan_up')
        self.scn()

    def window_pan_down(self):
        self.window_obj.pan_down()
        self.update_window_limit('pan_down')
        self.scn()

    def update_window_limit(self, mode):
        if mode == 'pan_right':
            self.Window_mundo.x_min -= self.panFactor
            self.Window_mundo.x_max -= self.panFactor
        elif mode == 'pan_left':
            self.Window_mundo.x_min += self.panFactor
            self.Window_mundo.x_max += self.panFactor
        elif mode == 'pan_up':
            self.Window_mundo.y_min -= self.panFactor
            self.Window_mundo.y_max -= self.panFactor
        elif mode == 'pan_down':
            self.Window_mundo.y_min += self.panFactor
            self.Window_mundo.y_max += self.panFactor
        elif mode[:4] == 'zoom':
            self.zoomMode = True # Usado para fazer transformada de viewport específica na window_limit quando zoom é utilizado
            scale_factor = 0.05
            halfx = self.Window_mundo.getCenterX_padrao()
            halfy = self.Window_mundo.getCenterY_padrao()
            print(f'halfx = {halfx}, halfy = {halfy}')
            if mode == 'zoom_in':
                self.Window_mundo.setXmin(self.Window_mundo.getXmin() + halfx * scale_factor)
                self.Window_mundo.setYmin(self.Window_mundo.getYmin() + halfy * scale_factor) 
                self.Window_mundo.setXmax(self.Window_mundo.getXmax() - halfx * scale_factor) 
                self.Window_mundo.setYmax(self.Window_mundo.getYmax() - halfy * scale_factor) 
            
            elif mode == 'zoom_out':
                self.Window_mundo.setXmin(self.Window_mundo.getXmin() - halfx * scale_factor)
                self.Window_mundo.setYmin(self.Window_mundo.getYmin() - halfy * scale_factor) 
                self.Window_mundo.setXmax(self.Window_mundo.getXmax() + halfx * scale_factor) 
                self.Window_mundo.setYmax(self.Window_mundo.getYmax() + halfy * scale_factor)
            
            print(f'x_min = {self.Window_mundo.x_min}')
            print(f'y_min = {self.Window_mundo.y_min}')
            print(f'x_max = {self.Window_mundo.x_max}')
            print(f'y_max = {self.Window_mundo.y_max}')
            
            for item in self.display_file:
                if item.name == 'window_limit':
                    self.display_file.remove(item)
                    self.remove_on_display_file(item.name)
                    window_limit = {'opcao': 'Wireframe', 'nome': 'window_limit', 'x1': self.Window_mundo.x_min+50, 'y1': self.Window_mundo.y_min+50,
                                                                                    'x2': self.Window_mundo.x_min+50, 'y2': self.Window_mundo.y_max-50,
                                                                                    'x3': self.Window_mundo.x_max-50, 'y3': self.Window_mundo.y_max-50,
                                                                                    'x4': self.Window_mundo.x_max-50, 'y4': self.Window_mundo.y_min+50}
            self.create_new_object(window_limit)
            print('window_limit')
            print(f'x1 = {window_limit["x1"]}, y1 = {window_limit["y1"]}')
            print(f'x2 = {window_limit["x2"]}, y2 = {window_limit["y2"]}')
            print(f'x3 = {window_limit["x3"]}, y3 = {window_limit["y3"]}')
            print(f'x4 = {window_limit["x4"]}, y4 = {window_limit["y4"]}')
    
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
            if info["nome"] == 'window_limit':
                new_object.color = QColor(Qt.red)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
        elif info["opcao"] == "Curva":
            curves = []
            #info:  {'opcao': 'Curva', 'nome': 'my_curve', 'p1': [100, 100], 'p4': [400, 400], 'r1': [200, 0], 'r4': [0, 200]}
            for i in range((info["num_curvas"])):
                curve = [info[f'p1{i}'], info[f'p4{i}'], info[f'r1{i}'], info[f'r4{i}']]
                curves.append(curve)
            lista_de_inteiros = [[tuple(map(int, item.split(','))) for item in sublista] for sublista in curves]
            new_object = HermiteCurve(lista_de_inteiros)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
        elif info["opcao"] == "Curva-BSpline":
            control_points = []
            for i in range(1, info["num_control_points"] + 1):
                point = info[f'p{i}']
                converted_point = tuple(map(int, point.split(',')))
                control_points.append(converted_point)
            new_object = BSplineCurve(control_points)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
        elif info['opcao'] == "Point3D":
            vertices = [info['x'], info['y'], info['z']]
            new_object = Point3D(info["nome"], vertices)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])
        elif info['opcao']  == "BezierSurface":
            control_points_str = []
            for i in range(16):
                point = info[f'p{i}']
                control_points_str.append(point)
            control_points_float = [tuple(map(float, point.split(','))) for point in control_points_str]
            new_object = BezierSurface(control_points_float)
            self.display_file.append(new_object)
            self.add_on_display_file(new_object, info['nome'])

    def set_window_default_paramaters(self):
        #window dimensions
        self.Window_mundo = Mundo(0, 800, 0, 800)
        #viewport dimensions
        self.xv_min = 0
        self.xv_max = 300
        self.yv_min = 0
        self.yv_max = 250
        self.scale_acumulator = 1
        #600, 500

    def create_viewport(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(200,0,600,500)
        #self.view.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        #Set noAnchor to GraphicsView, enabling the view to move
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor(0)) #ponto de ancoragem

    def viewport_transformation(self, xw, yw, name):

        sx = (self.xv_max - self.xv_min) / (self.window_obj.x_max - self.window_obj.x_min)
        sy = (self.yv_max - self.yv_min) / (self.window_obj.y_max - self.window_obj.y_min)
        
        if name == 'window_limit' and not self.zoomMode:
            xv = self.xv_min + (xw - (-1)) * sx
            yv = self.yv_max - (self.yv_min + (yw - (-1)) * sy)
            return xv, yv
        xv = self.xv_min + (xw - self.window_obj.x_min) * sx
        yv = self.yv_max - (self.yv_min + (yw - self.window_obj.y_min) * sy)
        return xv, yv
   
    def update_viewport(self):
        for obj in self.onViewport:
            self.scene.removeItem(obj)
        self.onViewport = []
        for obj in self.display_file:
            self.draw_dispplay_file(obj)
        self.view.centerOn(self.Window_mundo.getCenterX(), self.Window_mundo.getCenterY())
        self.zoomMode = False

        '''print(f'window_obj:')
        print(f'xmin = {self.window_obj.x_min}, ymin = {self.window_obj.y_min}, xmax = {self.window_obj.x_max}, ymax = {self.window_obj.y_max}')
        print(f'Window_mundo')
        print(f'xmin = {self.Window_mundo.x_min}, ymin = {self.Window_mundo.y_min}, xmax = {self.Window_mundo.x_max}, ymax = {self.Window_mundo.y_max}')
        print(f'clipping')
        print(f'xmin = {self.clipping_x_min}, ymin = {self.clipping_y_min}, xmax = {self.clipping_x_max}, ymax = {self.clipping_y_max}')'''

    def rotate_window_right(self):
        degrees = self.get_degrees()
        self.window_obj.degrees += degrees
        self.scn()
    
    def rotate_window_left(self):
        degrees = self.get_degrees()
        self.window_obj.degrees -= degrees
        self.scn()

    def scn(self, degrees=0):
        combined = self.window_obj.scn(self.Window_mundo.getCenterX(), self.Window_mundo.getCenterY())  #retorna a matriz composta
        #print(f'--------------------\n xmin = {self.Window_mundo.getXmin()}, ymin = {self.Window_mundo.getYmin()}, xmax = {self.Window_mundo.getXmax()}, ymax = {self.Window_mundo.getYmax()}\n x = {self.Window_mundo.getCenterX()}, y = {self.Window_mundo.getCenterY()}\n --------------------')
        #print('call update_normalized_coordinates')
        self.update_normalized_coordinates(combined)

    def update_normalized_coordinates(self, combined_matrix): #multiplica vertices * matriz composta
        #self.define_region_codes()
        self.exec_liang_barsky()
        for obj in self.display_file:
            print(obj.name)
            if obj.name == 'window-limit':
                start, step = 1, 2
            else:
                start, step = 0, 1
            if isinstance(obj, Wireframe):
                updated_vertices = []    
                for reta in obj.lines:
                    if reta.showing:
                        vertice1 = np.array([reta.x1I, reta.y1I, 1])
                        vertice2 = np.array([reta.x2I, reta.y2I, 1])
                        vertice1_updated = np.matmul(vertice1, combined_matrix)
                        vertice2_updated = np.matmul(vertice2, combined_matrix)
                        updated_vertices.append(vertice1_updated)
                        updated_vertices.append(vertice2_updated)
                        #print(f'vertice1 = {vertice1}')
                        #print(f'vertice2 = {vertice2}')
                        #print(f'vertice1_updated = {vertice1_updated}')
                        #print(f'vertice2_updated = {vertice2_updated}')
                        
                lista_retas = []
                #print('listas')
                for i in range(start, len(updated_vertices), step):
                    x1, y1, x2, y2 = updated_vertices[i-1][0], updated_vertices[i-1][1], updated_vertices[i][0], updated_vertices[i][1]
                    lista_retas.append([x1, y1, x2, y2])
                    #print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
                obj.normalized_vertices = lista_retas

            elif isinstance(obj, HermiteCurve):
                up_vertices = []
                for list in obj.curve_clipping:
                        vertice = np.array([list[0], list[1], 1])
                        vertice_up = np.matmul(vertice, combined_matrix) #normalizando
                        up_vertices.append(vertice_up)
                retas = []
                for i in range(len(up_vertices) - 1):
                    x1,y1,x2,y2 = up_vertices[i][0], up_vertices[i][1], up_vertices[i+1][0], up_vertices[i+1][1]
                    retas.append([x1, y1, x2, y2])
                obj.curve_clipping = retas
            
            elif isinstance(obj, BSplineCurve):
                up_vertices = []
                for tuple_ in obj.curve_clipping:
                        vertice = np.array([tuple_[0], tuple_[1], 1])
                        vertice_up = np.matmul(vertice, combined_matrix) #normalizando
                        up_vertices.append(vertice_up)
                retas = []
                for i in range(len(up_vertices) - 1):
                    x1,y1,x2,y2 = up_vertices[i][0], up_vertices[i][1], up_vertices[i+1][0], up_vertices[i+1][1]
                    retas.append([x1, y1, x2, y2])
                obj.curve_clipping = retas
            elif isinstance(obj, Point3D):
                if(obj.clipped_point != []):
                    vertice = np.array([obj.clipped_point[0], obj.clipped_point[1], 1])
                    vertice_up = np.matmul(vertice, combined_matrix)
                    obj.normalized_point = vertice_up
            elif isinstance(obj, BezierSurface):
                up_vertices = []
                for tuple_ in obj.surface_points:
                        vertice = np.array([tuple_[0], tuple_[1], 1])
                        vertice_up = np.matmul(vertice, combined_matrix) #normalizando
                        up_vertices.append(vertice_up)
                obj.surface_normalized_points = up_vertices
                obj.organize()
        self.update_viewport()

    def draw_dispplay_file(self, obj):
        if type(obj) == Wireframe:
            pontos = []
            '''if obj.name == 'window_limit':
                print('window_obj')
                print(f'xmin = {self.window_obj.x_min}, ymin = {self.window_obj.y_min}, xmax = {self.window_obj.x_max}, ymax = {self.window_obj.y_max}')
                print('window limit: ')'''
            #print(obj.name)
            for line in obj.normalized_vertices:
                new_x1, new_y1 = self.viewport_transformation(line[0], line[1], obj.name)
                new_x2, new_y2 = self.viewport_transformation(line[2], line[3], obj.name)
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                #if obj.name == 'window_limit':
                    #print(len(obj.normalized_vertices))
                #print(f'x1 = {new_x1}, y1 = {new_y1}, x2 = {new_x2}, y2 = {new_y2}')
                if obj.color != None:
                    new.setPen(obj.color)
                if obj.brush != None:
                    pontos.append([new_x1, new_y1])
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
            if obj.brush != None:
                if obj.fillPolygon != None:
                        self.scene.removeItem(obj.fillPolygon)
                brush_area = QPolygonF(QPointF(ponto[0], ponto[1]) for ponto in pontos)
                for ponto in pontos:
                    print(f'------------ ponto_polygon --------------------- = {ponto[0], ponto[1]}') 
                brush_poligon = QGraphicsPolygonItem(brush_area)
                brush_poligon.setBrush(obj.brush)
                self.scene.addItem(brush_poligon)
                obj.fillPolygon = brush_poligon
        elif type(obj) == Reta:
            new_x1, new_y1 = self.viewport_transformation(obj.line().x1(), obj.line().y1(), obj.name)
            new_x2, new_y2 = self.viewport_transformation(obj.line().x2(), obj.line().y2(), obj.name)
            pen = obj.pen()
            new = Reta(new_x1, new_y1, new_x2, new_y2)
            new.setPen(pen)
            self.scene.addItem(new)
            self.onViewport.append(new)
            self.view.show()
        elif type(obj) == Ponto:
            new_x1, new_y1 = self.viewport_transformation(obj.x(), obj.y(), obj.name)
            new = Ponto(new_x1, new_y1)
            self.scene.addItem(new)
            self.onViewport.append(new)
            self.view.show()
        elif type(obj) == HermiteCurve:
            print("HermiteCurve draw << \n")
            print(len(obj.curve_clipping))
            for line in obj.curve_clipping:
                #print()
                #print(line[0], line[1])
                #print(line[2], line[3])
                new_x1, new_y1 = self.viewport_transformation(line[0], line[1], obj.name)
                new_x2, new_y2 = self.viewport_transformation(line[2], line[3], obj.name)
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                if obj.color != None:
                    new.setPen(obj.color)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
        elif type(obj) == BSplineCurve:
            print("BSplineCurve draw << \n")
            for line in obj.curve_clipping:
                new_x1, new_y1 = self.viewport_transformation(line[0], line[1], obj.name)
                new_x2, new_y2 = self.viewport_transformation(line[2], line[3], obj.name)
                new = Reta(new_x1, new_y1, new_x2, new_y2)
                if obj.color != None:
                    new.setPen(obj.color)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
        elif type(obj) == Point3D:
            print(">>>>> Desenhando ponto 3D <<<<<")
            print("normalized point ", obj.normalized_point)
            if(obj.normalized_point != []):
                x, y = self.viewport_transformation(obj.normalized_point[0], obj.normalized_point[1])
                new = Ponto(x, y)
                self.scene.addItem(new)
                self.onViewport.append(new)
                self.view.show()
        elif type(obj) == BezierSurface:
            print("Surface draw \n")
            for lista in obj.pontos_agrupados_x_f:
                for line in lista:
                    new_x1, new_y1 = self.viewport_transformation(line[0], line[1], obj.name)
                    new_x2, new_y2 = self.viewport_transformation(line[2], line[3], obj.name)
                    new = Reta(new_x1, new_y1, new_x2, new_y2)
                    if obj.color != None:
                        new.setPen(obj.color)
                    self.scene.addItem(new)
                    self.onViewport.append(new)
                    self.view.show()
            
            for lista in obj.pontos_agrupados_y_f:
                for line in lista:
                    new_x1, new_y1 = self.viewport_transformation(line[0], line[1], obj.name)
                    new_x2, new_y2 = self.viewport_transformation(line[2], line[3], obj.name)
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
                    Clipping.defineIntersection(reta, self.Window_mundo)
            elif isinstance(item, Reta):
                Clipping.defineIntersection(item, self.Window_mundo)
            elif isinstance(item, Ponto):
                self.point_clipping(item)
            elif isinstance(item, HermiteCurve):
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min +100, self.Window_mundo.y_min+100, self.Window_mundo.x_max - 100, self.Window_mundo.y_max -100
                item.clipping(xmin, ymin, xmax, ymax)
            elif isinstance(item, BSplineCurve):
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min + 100, self.Window_mundo.y_min + 100, self.Window_mundo.x_max - 100, self.Window_mundo.y_max - 100
                item.clipping(xmin, ymin, xmax, ymax)
            elif isinstance(item, Point3D):
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min + 100, self.Window_mundo.y_min + 100, self.Window_mundo.x_max - 100, self.Window_mundo.y_max - 100
                item.clipping(xmin, ymin, xmax, ymax)

    def exec_liang_barsky(self):
        for item in self.display_file:
            if item.name == 'window_limit':
                for reta in item.lines:
                    reta.showing = True
                continue
            print(f'item = {item.name}')
            if isinstance(item, Wireframe):
                for reta in item.lines:
                    Clipping.liang_barsky(reta, self.Window_mundo)
                    print()
                    print(f'x1I = {reta.x1I}, y1I = {reta.y1I}, x2I = {reta.x2I}, y2I = {reta.y2I}')
                    print(reta.showing)
            elif isinstance(item, Reta):
                Clipping.liang_barsky(item, self.Window_mundo)
            elif isinstance(item, Ponto):
                self.point_clipping(item)
            elif isinstance(item, HermiteCurve):
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min +50, self.Window_mundo.y_min+50, self.Window_mundo.x_max - 50, self.Window_mundo.y_max -50
                item.clipping(xmin, ymin, xmax, ymax)
            elif isinstance(item, BSplineCurve):
                xmin, ymin, xmax, ymax = self.Window_mundo.x_min + 50, self.Window_mundo.y_min + 50, self.Window_mundo.x_max - 50, self.Window_mundo.y_max - 50
                item.clipping(xmin, ymin, xmax, ymax)
            print()
            print()


    def weiler_atherton(self, obj:Wireframe):
        '''for line in obj.lines:
            self.liang_barsky(line)
            if line.x1I == self.Window_mundo.x_min:
                obj.clippingLocation.append('L')
                obj.clippingOrder.append('F-D')
            elif line.x1I == self.Window_mundo.x_max:
                obj.clippingLocation.append('R')
                obj.clippingOrder.append('F-D')

            if line.x2I == self.Window_mundo.x_min:
                obj.clippingLocation.append('L')
                obj.clippingOrder.append('D-F')
            elif line.x2I == self.Window_mundo.x_max:
                obj.clippingLocation.append('R')
                obj.clippingOrder.append('D-F')

            if line.y1I == self.Window_mundo.y_min:
                obj.clippingLocation.append('B')
                obj.clippingOrder.append('F-D')
            elif line.y1I == self.Window_mundo.y_max:
                obj.clippingLocation.append('T')
                obj.clippingOrder.append('F-D')

            if line.y2I == self.Window_mundo.y_min:
                obj.clippingLocation.append('B')
                obj.clippingOrder.append('D-F')
            elif line.y2I == self.Window_mundo.y_max:
                obj.clippingLocation.append('T')
                obj.clippingOrder.append('D-F')'''
        
        for line in obj.lines:
            x1, y1, x2, y2 = line.line().x1(), line.line().y1(), line.line().x2(), line.line().y2()
            line.x1I, line.y1I, line.x2I, line.y2I
            if x1 < self.Window_mundo.x_min and x1 != line.x1I:
                line.x1I = self.Window_mundo.x_min
            elif x1 > self.Window_mundo.x_max:
                line.x1I = self.Window_mundo.x_max
            
            if x2 < self.Window_mundo.x_min:
                line.x2I = self.Window_mundo.x_min
            elif x2 > self.Window_mundo.x_max:
                line.x2I = self.Window_mundo.x_max
            
            if y1 < self.Window_mundo.y_min:
                line.y1I = self.Window_mundo.y_min
            elif x1 > self.Window_mundo.x_max:
                line.y1I = self.Window_mundo.y_max
            
            if y2 < self.Window_mundo.y_min:
                line.y2I = self.Window_mundo.y_min
            elif x2 > self.Window_mundo.y_max:
                line.y2I = self.Window_mundo.y_max