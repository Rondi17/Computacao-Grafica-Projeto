import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QComboBox


class DialogBox(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Incluir novo objeto")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        self.option_label = QLabel("Selecione um Objeto:")
        self.layout.addWidget(self.option_label)

        self.option_combo = QComboBox()  # Combo box para opcoes
        self.option_combo.addItems(["Ponto", "Reta", "Wireframe"])
        self.layout.addWidget(self.option_combo)

        self.fields_layout = QVBoxLayout()  # Layout para conter campos adicionais
        self.layout.addLayout(self.fields_layout)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.option_combo.currentIndexChanged.connect(self.option_changed)
        self.option_combo.setCurrentIndex(0)
        self.option_changed()

    def option_changed(self):
        self.clear_fields()
        option = self.option_combo.currentText()

        if option == "Ponto":
            self.fields_layout.addWidget(QLabel("Digite x e y:"))
            self.x_input = QLineEdit()
            self.y_input = QLineEdit()
            self.fields_layout.addWidget(self.x_input)
            self.fields_layout.addWidget(self.y_input)
        elif option == "Reta":
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
            self.cnt = 1
            self.listX = []
            self.listY = []
            while True:
                self.fields_layout.addWidget(QLabel(f"Ponto {self.cnt}(x{self.cnt}, y{self.cnt}):"))
                x = QLineEdit()
                y = QLineEdit()
                self.fields_layout.addWidget(x)
                self.fields_layout.addWidget(y)
                self.listX.append(x)
                self.listY.append(y)
                self.cnt+= 1
                if self.cnt >=5:
                    break


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
                "x": int(self.x_input.text()),
                "y": int(self.y_input.text())
            }
        elif option == "Reta":
            return {
                "opcao": option,
                "x1": int(self.x1_input.text()),
                "y1": int(self.y1_input.text()),
                "x2": int(self.x2_input.text()),
                "y2": int(self.y2_input.text())
            }
        else:
            dic = dict()
            dic["opcao"] =  option
            for i in range(self.cnt-1):
                dic[f'x{i}'] =  int(self.listX[i].text())
                dic[f'y{i}'] =  int(self.listY[i].text())
            return dic