from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import requests
import utils  # Ensure you have this module or replace with your desired implementation

class LoginPage(QWidget):
    switch_to_register = pyqtSignal()
    switch_to_mainboard = pyqtSignal()
    switch_to_admin_dashboard = pyqtSignal() 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(800, 700, 5050, 1200)  # Adjusted window size


        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # Left side: Image
        image_label = QLabel(self)
        pixmap = QPixmap("login.jpg")
        image_label.setPixmap(pixmap.scaled(400, 400))  # Resize image to fit
        image_label.setStyleSheet(
            """
            QLabel {
                margin-right: 40px;          
            }
            """
        )
        main_layout.addWidget(image_label)

        # Right side: Form Layout
        form_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Login to ReviewVerse 📚", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;margin-top:150px")
        form_layout.addWidget(title_label)

        # Email Input
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setToolTip("Please enter your registered email address.")
        self.email_input.setStyleSheet(
            """
            QLineEdit {
                padding: 10px; 
                border: 2px solid #45a020; 
                border-radius: 15px;  /* Rounded corners */
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #4CAF50;  /* Hover effect */
            }
            """
        )
        email_label = QLabel("Email:", self)
        email_label.setStyleSheet("font-weight: bold; font-size: 17px;")  # Bold label
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)

        # Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setToolTip("Enter your password. Ensure it's correct to avoid login issues.")
        self.password_input.setStyleSheet(
            """
            QLineEdit {
                padding: 10px; 
                border: 2px solid #45a020; 
                border-radius: 15px;  /* Rounded corners */
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #4CAF50;  /* Hover effect */
            }
            """
        )
        password_label = QLabel("Password:", self)
        password_label.setStyleSheet("font-weight: bold; font-size: 17px; margin-top: 10px;")  # Bold label
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; /* Light green */
                color: white; 
                padding: 10px; 
                border: none; 
                border-radius: 15px; /* Rounded corners */
                font-size: 16px;
                margin-top: 10px; /* Add some spacing at the top */
            }
            QPushButton:hover {
                background-color: #45a049; /* Slightly darker green */
                font-weight: bold; /* Bold white text */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Even darker green */
                font-weight: bold; /* Bold white text */
            }
            """
        )
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)

        # Register Link
        register_label = QLabel('Don\'t have an account? <a href="#"><strong>Register Yourself</strong></a> to get started!', self)
        register_label.setToolTip("Click to create a new account with ReviewVerse.")
        register_label.setStyleSheet(
            """
            QLabel {
                margin-top: 30px;
            }
            QLabel a {
                color: blue; 
                text-decoration: underline; 
                font-size: 14px;
            }
            """
        )
        register_label.setOpenExternalLinks(False)
        register_label.linkActivated.connect(lambda: self.switch_to_register.emit())
        form_layout.addWidget(register_label)

        form_layout.addStretch()  # Add stretch for alignment
        main_layout.addLayout(form_layout)

        # Set Main Layout
        self.setLayout(main_layout)

    def handle_login(self):
        """
        Handles the login logic.
        """
        email = self.email_input.text()
        password = self.password_input.text()

        #Admin login
        if email == "admin" and password == "Admin@123":
            QMessageBox.information(self, "Admin Login", "Welcome, Admin!")
            self.switch_to_admin_dashboard.emit()
            return


        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return

        response = self.send_login_request(email, password)

        if response and response.status_code == 200:
            try:
                data = response.json()
                if "user" in data:
                    user = data["user"]
                    utils.set_user_details(user.get("username", ""), user.get("id", ""))
                    QMessageBox.information(self, "Success", "Login successful! Welcome back!")
                    self.switch_to_mainboard.emit()
                else:
                    QMessageBox.warning(self, "Error", "Unexpected response format.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to parse response: {e}")
        elif response:
            QMessageBox.warning(self, "Error", f"Login failed: {response.json().get('detail', 'Unknown error')}")
        else:
            QMessageBox.critical(self, "Error", "Reviewverse not found Please Register yourself.")

    @staticmethod
    def send_login_request(email, password):
        """
        Sends a POST request to the login endpoint.
        """
        try:
            url = "https://reviewverse.onrender.com/login"  # Replace with your API endpoint
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            payload = {"email": email, "password": password}
            response = requests.post(url, data=payload, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(None, "Error", f"Failed to connect to server: {e}")
            return None
