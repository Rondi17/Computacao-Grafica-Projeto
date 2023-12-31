import sys
from PyQt5.QtWidgets import *
import sys


class DialogBox(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Incluir novo objeto")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.init_box()

        self.fields_layout = QVBoxLayout()  # Layout para conter campos adicionais
        self.layout.addLayout(self.fields_layout)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.option_changed()

    def init_box(self):    
        self.option_label = QLabel("Selecione um Objeto:")
        self.layout.addWidget(self.option_label)

        self.option_combo = QComboBox()  # Combo box para opcoes
        self.option_combo.addItems(["Wireframe", "Ponto", "Reta", "Curva-Hermite", "Curva-BSpline", "Point3D"])
        self.layout.addWidget(self.option_combo)

        self.option_combo.currentIndexChanged.connect(self.option_changed)
        self.option_combo.setCurrentIndex(0)

    def option_changed(self):
        self.clear_fields()
        option = self.option_combo.currentText()
        if option == "Ponto":
            self.fields_layout.addWidget(QLabel("Nome:"))
            self.nome = QLineEdit()
            self.fields_layout.addWidget(self.nome)
            self.fields_layout.addWidget(QLabel("Digite x e y:"))
            self.x_input = QLineEdit()
            self.y_input = QLineEdit()
            self.fields_layout.addWidget(self.x_input)
            self.fields_layout.addWidget(self.y_input)
        elif option == "Reta":
            self.fields_layout.addWidget(QLabel("Nome:"))
            self.nome = QLineEdit()
            self.fields_layout.addWidget(self.nome)
            self.fields_layout.addWidget(QLabel("Ponto inicial (x1, y1):"))
            self.x1_input = QLineEdit()
            self.y1_input = QLineEdit()
            self.fields_layout.addWidget(self.x1_input)
            self.fields_layout.addWidget(self.y1_input)

            self.fields_layout.addWidget(QLabel("Ponto final (x2, y2):"))
            self.x2_input = QLineEdit()
            self.y2_input = QLineEdit()
            self.fields_layout.addWidget(self.x2_input)
            self.fields_layout.addWidget(self.y2_input)
        elif option == "Wireframe":
            self.nLados_label = QLabel("Informe a quantidade de lados do polígono:")
            self.fields_layout.addWidget(self.nLados_label)
            
            self.nLados_input = QLineEdit()
            self.fields_layout.addWidget(self.nLados_input)

            self.plus_button = QPushButton("+", self)
            self.fields_layout.addWidget(self.plus_button)
            self.plus_button.clicked.connect(lambda: self.on_plus("wireframe"))
        elif option == "Curva-Hermite":
            self.curve = QLabel("Número de curvas de continuidade: ")
            self.fields_layout.addWidget(self.curve)
            
            self.num_curves = QLineEdit()
            self.fields_layout.addWidget(self.num_curves)

            self.plus_button = QPushButton("+", self)
            self.fields_layout.addWidget(self.plus_button)
            self.plus_button.clicked.connect(lambda: self.on_plus("Curva-Hermite"))
        elif option == "Curva-BSpline":
            self.control_points = QLabel("Número de pontos de controle")
            self.fields_layout.addWidget(self.control_points)

            self.num_control_points = QLineEdit()
            self.fields_layout.addWidget(self.num_control_points)

            self.plus_button = QPushButton("+", self)
            self.fields_layout.addWidget(self.plus_button)
            self.plus_button.clicked.connect(lambda: self.on_plus("Curva-BSpline"))
        elif option == "Point3D":
            self.fields_layout.addWidget(QLabel("Name:"))
            self.nome = QLineEdit()
            self.fields_layout.addWidget(self.nome)
            self.fields_layout.addWidget(QLabel("Digite x,y,z:"))
            self.x_input = QLineEdit()
            self.y_input = QLineEdit()
            self.z_input = QLineEdit()
            self.fields_layout.addWidget(self.x_input)
            self.fields_layout.addWidget(self.y_input)
            self.fields_layout.addWidget(self.z_input)

    def on_plus(self, type_object):

        if type_object == "wireframe":
            self.nLados = int(self.nLados_input.text())
            
            self.fields_layout.removeWidget(self.nLados_label)
            self.nLados_label.deleteLater()
            self.fields_layout.removeWidget(self.nLados_input)
            self.nLados_input.deleteLater()
            self.fields_layout.removeWidget(self.plus_button)
            self.plus_button.deleteLater()

            if self.nLados < 3:
                return # O poligono deve ter pelo menos 3 lados
            
            self.fields_layout.addWidget(QLabel("Nome:"))
            self.nome = QLineEdit()
            self.fields_layout.addWidget(self.nome)
            self.listX = []
            self.listY = []
            for i in range(self.nLados):
                self.fields_layout.addWidget(QLabel(f"Ponto (x{i+1}, y{i+1}):"))
                self.xInput = QLineEdit()
                self.yInput = QLineEdit()
                self.fields_layout.addWidget(self.xInput)
                self.fields_layout.addWidget(self.yInput)
                self.listX.append(self.xInput)
                self.listY.append(self.yInput)
        elif type_object == "Curva-Hermite":
            self.fields_layout.addWidget(QLabel("Nome:"))
            self.nome = QLineEdit()
            self.fields_layout.addWidget(self.nome)

            self.p1_list = []
            self.p4_list = []
            self.r1_list = []
            self.r4_list = []

            self.n_curves = int(self.num_curves.text())

            for i in range(self.n_curves):
                self.fields_layout.addWidget(QLabel(f"Curva {i+1}: p1,p4,r1,r4 "))
                self.p1_input = QLineEdit()
                self.p4_input = QLineEdit()
                self.r1_input = QLineEdit()
                self.r4_input = QLineEdit()
                self.fields_layout.addWidget(self.p1_input)
                self.fields_layout.addWidget(self.p4_input)
                self.fields_layout.addWidget(self.r1_input)
                self.fields_layout.addWidget(self.r4_input)
                self.p1_list.append(self.p1_input)
                self.p4_list.append(self.p4_input)
                self.r1_list.append(self.r1_input)
                self.r4_list.append(self.r4_input)
        
        elif type_object == "Curva-BSpline":
            self.fields_layout.addWidget(QLabel("Nome:"))
            self.nome = QLineEdit()
            self.fields_layout.addWidget(self.nome)

            self.p_list = []
            self.n_control_points = int(self.num_control_points.text())

            for i in range(self.n_control_points):
                self.fields_layout.addWidget(QLabel(f"Control Point {i+1}:  "))
                self.p_input = QLineEdit()
                self.fields_layout.addWidget(self.p_input)
                self.p_list.append(self.p_input)
                

    def clear_fields(self):
        for i in reversed(range(self.fields_layout.count())):
            widget = self.fields_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def get_input(self):
        option = self.option_combo.currentText()

        if option == "Ponto":
            return {
                "opcao": option,
                "nome": self.nome.text(),
                "x": int(self.x_input.text()),
                "y": int(self.y_input.text()),
            }
        elif option == "Reta":
            return {
                "opcao": option,
                "nome": self.nome.text(),
                "x1": int(self.x1_input.text()),
                "y1": int(self.y1_input.text()),
                "x2": int(self.x2_input.text()),
                "y2": int(self.y2_input.text()),
            }
        elif option == "Wireframe":
            dic = dict()
            dic['opcao'] = option
            dic['nome'] = self.nome.text()
            for i in range(self.nLados):
                dic[f'x{i+1}'] = int(self.listX[i].text())
                dic[f'y{i+1}'] = int(self.listY[i].text())
            return dic
        elif option == "Curva-Hermite":
            dic = dict()
            dic['opcao'] = option
            dic['nome'] = self.nome.text()
            dic['num_curvas'] = self.n_curves
            for i in range(self.n_curves):
                dic[f'p1{i}'] = (self.p1_list[i].text())
                dic[f'p4{i}'] = (self.p4_list[i].text())
                dic[f'r1{i}'] = (self.r1_list[i].text())
                dic[f'r4{i}'] = (self.r4_list[i].text())
            return dic
        
        elif option == "Curva-BSpline":
            dic = dict()
            dic['opcao'] = option
            dic['nome'] = self.nome.text()
            dic['num_control_points'] = self.n_control_points
            for i in range(self.n_control_points):
                dic[f'p{i+1}'] = (self.p_list[i].text())
            return dic
        if option == "Point3D":
            return {
                "opcao": option,
                "nome": self.nome.text(),
                "x": int(self.x_input.text()),
                "y": int(self.y_input.text()),
                "z": int(self.z_input.text())
            }