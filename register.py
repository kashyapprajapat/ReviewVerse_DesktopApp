from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal 
import requests

class RegisterPage(QWidget):
    switch_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter Email")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.login_link = QPushButton("Back to Login")
        self.login_link.clicked.connect(self.switch_to_login.emit)
        layout.addWidget(self.login_link)

        self.setLayout(layout)

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        response = self.send_register_request(email, password)
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Registration successful!")
            self.switch_to_login.emit()
        else:
            QMessageBox.warning(self, "Error", "Registration failed. Please try again.")

    @staticmethod
    def send_register_request(email, password):
        """
        Sends a POST request to the register endpoint.
        """
        url = "https://example.com/api/register"  # Replace with your API endpoint
        response = requests.post(url, json={"email": email, "password": password})
        return response
