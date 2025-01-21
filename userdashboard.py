from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from utils import username, user_id  # Import the global variables


class UserDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Dashboard")
        self.setGeometry(100, 100, 400, 300)

        # Create layout
        layout = QVBoxLayout()

        # Display user details
        self.user_label = QLabel(f"Welcome, {username} (ID: {user_id})", self)
        self.user_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.user_label)

        # Add more widgets as needed
        self.setLayout(layout)