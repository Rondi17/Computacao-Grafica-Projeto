import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QComboBox
import sys


class DialogBox(QDialog):
    def __init__(self,new_coordinate):
        super().__init__()

        self.setWindowTitle("Incluir novo objeto")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)        

        self.layout = QVBoxLayout()
        self.plus_button_activate = False
        self.build = False
        self.new_coordinate = new_coordinate
        self.init_box()

        self.fields_layout = QVBoxLayout()  # Layout para conter campos adicionais
        self.layout.addLayout(self.fields_layout)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.option_changed()

    def init_box(self):
        if self.new_coordinate == False:
            
            self.option_label = QLabel("Selecione um Objeto:")
            self.layout.addWidget(self.option_label)

            self.option_combo = QComboBox()  # Combo box para opcoes
            self.option_combo.addItems(["Ponto", "Reta", "Wireframe"])
            self.layout.addWidget(self.option_combo)

            self.option_combo.currentIndexChanged.connect(self.option_changed)
            self.option_combo.setCurrentIndex(0)

    def option_changed(self):
        self.clear_fields()

        if self.new_coordinate == True:
                pass
        else:
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
                self.plus_button.clicked.connect(self.on_plus)
                
                
                

    def on_plus(self):
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
