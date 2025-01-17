from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import utils

class MainBoardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Board")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        # Access global user details from utils
        self.username_label = QLabel(f"Username: {utils.username}", self)
        layout.addWidget(self.username_label)

        self.user_id_label = QLabel(f"User ID: {utils.user_id}", self)
        layout.addWidget(self.user_id_label)

        self.setLayout(layout)
