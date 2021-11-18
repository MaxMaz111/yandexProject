from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class Dialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setFixedSize(300, 50)
        self.setWindowTitle("Ошибка")
        self.layout.addWidget(QLabel(message))
        self.setLayout(self.layout)
        self.exec()
