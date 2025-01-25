from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal

class AdminDashboard(QWidget):
    switch_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(700, 700, 2500, 2000)  # Set the window size

        # Main Layout
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Welcome to the Admin Dashboard", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Info Label
        info_label = QLabel("Here, you can manage users, view statistics, and perform administrative tasks.", self)
        info_label.setStyleSheet("font-size: 16px; margin-bottom: 30px;")
        layout.addWidget(info_label)

        # Manage Users Button
        manage_users_button = QPushButton("Manage Users", self)
        manage_users_button.setStyleSheet(
            """
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                padding: 10px; 
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )
        manage_users_button.clicked.connect(self.manage_users)
        layout.addWidget(manage_users_button)

        # View Reports Button
        view_reports_button = QPushButton("View Reports", self)
        view_reports_button.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745; 
                color: white; 
                padding: 10px; 
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            """
        )
        view_reports_button.clicked.connect(self.view_reports)
        layout.addWidget(view_reports_button)

        # Logout Button
        logout_button = QPushButton("Logout", self)
        logout_button.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545; 
                color: white; 
                padding: 10px; 
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            """
        )
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        # Set the layout
        self.setLayout(layout)

    def manage_users(self):
        """
        Functionality to manage users.
        """
        QMessageBox.information(self, "Manage Users", "This feature is under development.")

    def view_reports(self):
        """
        Functionality to view reports.
        """
        QMessageBox.information(self, "View Reports", "This feature is under development.")

    def logout(self):
        """
        Logs out the admin and switches back to the login page.
        """
        confirm = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.switch_to_login.emit()
