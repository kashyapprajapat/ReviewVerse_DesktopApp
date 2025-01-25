from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
import requests
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # type: ignore
from collections import Counter


class AdminDashboard(QWidget):
    switch_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(400, 300, 5000, 6000) 

        # Main Layout
        main_layout = QVBoxLayout()

        # Navbar (Sticky at the top)
        navbar = QLabel("Welcome, Admin", self)
        navbar.setAlignment(Qt.AlignCenter)
        navbar.setStyleSheet(
            "font-size: 24px; font-weight: bold; background-color: #007BFF; color: white; padding: 10px;")
        main_layout.addWidget(navbar)

        # Content Layout
        content_layout = QHBoxLayout()

        # Left Panel
        left_panel = QWidget(self)
        left_panel.setFixedWidth(200)  # Adjusted width for better layout
        left_panel_layout = QVBoxLayout()

        users_button = QPushButton("Users", self)
        users_button.setStyleSheet(self.get_button_styles())
        users_button.clicked.connect(self.fetch_users)
        left_panel_layout.addWidget(users_button)

        health_button = QPushButton("Health", self)
        health_button.setStyleSheet(self.get_button_styles())
        health_button.clicked.connect(self.fetch_health)
        left_panel_layout.addWidget(health_button)

        left_panel.setLayout(left_panel_layout)
        content_layout.addWidget(left_panel)

        # Right Panel
        self.right_panel = QVBoxLayout()

        # Default Image
        pixmap = QPixmap("admin.jpg")  # Replace with your image path
        self.default_image = QLabel(self)
        self.default_image.setPixmap(pixmap)
        self.default_image.setScaledContents(True)
        self.default_image.setFixedSize(800, 600)  # Increased default image size
        self.right_panel.addWidget(self.default_image)

        # Table for displaying data
        self.table = QTableWidget(self)
        self.table.hide()
        self.set_table_styles()  # Apply the styles to the table
        self.right_panel.addWidget(self.table)

        content_layout.addLayout(self.right_panel)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def get_button_styles(self):
        """
        Returns the styles for the buttons.
        """
        return """
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                padding: 15px; 
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
    
    def set_table_styles(self):
        """
        Set custom styles for the table.
        """
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: #f4f4f4;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                font-weight: bold;
                padding: 10px;
            }
        """)

    def fetch_users(self):
        """
        Fetch and display users data from the API and display charts.
        """
        try:
            response = requests.get("https://reviewverse.onrender.com/users")
            response.raise_for_status()
            data = response.json()
            self.display_users(data["users"])
            self.display_user_charts(data["users"])
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch users data: {e}")

    def fetch_health(self):
        """
        Fetch and display health data from the API and display a graph.
        """
        try:
            response = requests.get("https://reviewverse.onrender.com/health")
            response.raise_for_status()
            data = response.json()
            self.display_health(data)
            self.display_health_graph(data)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch health data: {e}")

    def display_users(self, users):
        """
        Display users data in the table.
        """
        self.default_image.hide()
        self.table.show()

        self.table.setRowCount(len(users) + 1)  # Add one extra row for totals
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Username", "Gender", "Age", "Current Role"])

        # Populate table
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user["username"]))
            self.table.setItem(row, 1, QTableWidgetItem(user["gender"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(user["age"])))
            self.table.setItem(row, 3, QTableWidgetItem(user["currentrole"]))

        # Add totals row
        gender_counts = Counter(user["gender"] for user in users)
        self.table.setItem(len(users), 0, QTableWidgetItem("Total"))
        self.table.setItem(len(users), 1, QTableWidgetItem(str(sum(gender_counts.values()))))
        self.table.setItem(len(users), 2, QTableWidgetItem("-"))
        self.table.setItem(len(users), 3, QTableWidgetItem(str(len(users))))

    def display_user_charts(self, users):
        """
        Display charts for gender-wise, age-wise, and current role-wise data.
        """
        # Gender-wise distribution
        genders = [user["gender"] for user in users]
        gender_counts = Counter(genders)

        # Age distribution
        ages = [user["age"] for user in users]

        # Current role distribution
        roles = [user["currentrole"] for user in users]
        role_counts = Counter(roles)

        # Create charts
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # Increased figure size

        axs[0].pie(
            gender_counts.values(),
            labels=gender_counts.keys(),
            autopct='%1.1f%%',
            colors=["#FF9999", "#66B2FF", "#99FF99", "#FFD700", "#FF66CC"]
        )
        axs[0].set_title("Gender Distribution")

        axs[1].hist(ages, bins=5, color="#007BFF")  # Adjusted bins for age
        axs[1].set_title("Age Distribution")
        axs[1].set_xlabel("Age")
        axs[1].set_ylabel("Frequency")

        axs[2].bar(role_counts.keys(), role_counts.values(), color=["#FFC107", "#FF5733", "#28B463", "#3498DB"])
        axs[2].set_title("Current Role Distribution")
        axs[2].set_xlabel("Roles")
        axs[2].set_ylabel("Total")

        canvas = FigureCanvas(fig)
        self.right_panel.addWidget(canvas)

    def display_health(self, health):
        """
        Display health data in the table.
        """
        self.default_image.hide()
        self.table.show()

        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["CPU Usage (%)", "Memory Usage (%)", "Status"])

        self.table.setItem(0, 0, QTableWidgetItem(str(health["cpu_usage"])))
        self.table.setItem(0, 1, QTableWidgetItem(str(health["memory_usage"])))
        self.table.setItem(0, 2, QTableWidgetItem(health["status"]))

    def display_health_graph(self, health):
        """
        Display a graph for CPU and Memory Usage.
        """
        fig, ax = plt.subplots(figsize=(8, 5))  # Increased figure size

        ax.bar(["CPU Usage", "Memory Usage"], [health["cpu_usage"], health["memory_usage"]],
               color=["#007BFF", "#FFC107"])
        ax.set_ylabel("Usage (%)")
        ax.set_title("Health Metrics")

        canvas = FigureCanvas(fig)
        self.right_panel.addWidget(canvas)
