from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QRadioButton, QButtonGroup, QComboBox, QFileDialog
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import requests
import os
from utils import set_user_details

class RegisterPage(QWidget):
    switch_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(600, 500, 2050, 1500)  

        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # Left side: Form Layout
        form_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Register to ReviewVerse 📚", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        form_layout.addWidget(title_label)

        # Username Input (Required)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet(
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
        username_label = QLabel("Username: <font color='red'>*</font>", self)  # Red asterisk
        username_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)

        # Email Input (Required)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter Email")
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
        email_label = QLabel("Email: <font color='red'>*</font>", self)  # Red asterisk
        email_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)

        # Password Input (Required)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
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
        password_label = QLabel("Password: <font color='red'>*</font>", self)  # Red asterisk
        password_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        # Gender Radio Buttons (Required)
        gender_label = QLabel("Gender: <font color='red'>*</font>", self)  # Red asterisk
        gender_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        form_layout.addWidget(gender_label)

        # Create a horizontal layout for radio buttons
        gender_layout = QHBoxLayout()

        # Create the radio buttons 
        self.gender_group = QButtonGroup(self)
        male_radio = QRadioButton("Male", self)
        female_radio = QRadioButton("Female", self)
        other_radio = QRadioButton("Other", self)

        # Add the radio buttons to the group
        self.gender_group.addButton(male_radio, 1)
        self.gender_group.addButton(female_radio, 2)
        self.gender_group.addButton(other_radio, 3)

        # Add the radio buttons to the horizontal layout
        gender_layout.addWidget(male_radio)
        gender_layout.addWidget(female_radio)
        gender_layout.addWidget(other_radio)

        # Add the horizontal layout to the form layout
        form_layout.addLayout(gender_layout)

        # Age Input (Required)
        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("Enter Age")
        self.age_input.setStyleSheet(
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
        age_label = QLabel("Age: <font color='red'>*</font>", self)  # Red asterisk
        age_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        form_layout.addWidget(age_label)
        form_layout.addWidget(self.age_input)

        # Current Role Dropdown (Required)
        self.role_dropdown = QComboBox(self)
        self.role_dropdown.addItems(["student", "employee", "author", "other"])
        self.role_dropdown.setStyleSheet(
            """
            QComboBox {
                padding: 10px; 
                border: 2px solid #45a020; 
                border-radius: 15px;  /* Rounded corners */
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #4CAF50;  /* Hover effect */
            }
            """
        )
        role_label = QLabel("Current Role: <font color='red'>*</font>", self)  # Red asterisk
        role_label.setStyleSheet("font-weight: bold; font-size: 17px;")
        form_layout.addWidget(role_label)
        form_layout.addWidget(self.role_dropdown)

        # Profile Photo Upload
        self.profile_photo_label = QLabel("No file selected", self)
        self.profile_photo_label.setStyleSheet("font-style: italic; color: gray;")
        self.upload_button = QPushButton("Upload Profile Photo", self)
        self.upload_button.setStyleSheet(
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
        self.upload_button.clicked.connect(self.upload_photo)
        form_layout.addWidget(QLabel("Profile Photo:"))
        form_layout.addWidget(self.upload_button)
        form_layout.addWidget(self.profile_photo_label)

        # Register Button
        self.register_button = QPushButton("Register", self)
        self.register_button.setStyleSheet(
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
        self.register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_button)

        # Back to Login Link
        self.login_link = QPushButton("🔙 Back to Login", self)
        self.login_link.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: blue; 
                text-decoration: underline; 
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                color: darkblue; /* Slightly darker blue */
            }
            """
        )
        self.login_link.clicked.connect(self.switch_to_login.emit)
        form_layout.addWidget(self.login_link)

        form_layout.addStretch()  # Add stretch for alignment

        # Right side: Image
        image_label = QLabel(self)
        pixmap = QPixmap("registration.png")  # Ensure this image exists
        image_label.setPixmap(pixmap.scaled(400, 300))  # Resize image to fit
        image_label.setStyleSheet(
            """
            QLabel {
                margin-left: 40px;          /* Spacing between image and form */
            }
            """
        )

        main_layout.addLayout(form_layout)
        main_layout.addWidget(image_label)

        # Set Main Layout
        self.setLayout(main_layout)

    def upload_photo(self):
        """
        Handles file upload for profile photo.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Profile Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            if file_size > 5:
                QMessageBox.warning(self, "Error", "File size must be less than 5MB.")
            else:
                self.profile_photo_label.setText(file_path)  # Store full file path
                self.profile_photo_label.setStyleSheet("font-style: normal; color: black;")
                self.profile_photo_path = file_path  # Store file path for later use

    def handle_register(self):
        """
        Handles the form submission, validates the inputs, and sends the data to the backend.
        """
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        gender = self.gender_group.checkedId()
        age = self.age_input.text()
        role = self.role_dropdown.currentText()

        # Validation logic
        if not username or not email or not password or not gender or not age or not role:
            QMessageBox.warning(self, "Input Error", "Please fill in all the required fields.")
            return

        if not email.count('@') == 1 or not email.count('.') > 0:
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if not age.isdigit() or int(age) < 18:
            QMessageBox.warning(self, "Invalid Age", "Age must be a number greater than or equal to 18.")
            return

        if not hasattr(self, 'profile_photo_path') or not self.profile_photo_path:
            QMessageBox.warning(self, "Profile Photo", "Please upload a profile photo.")
            return

        # Simulate registration (send to backend)
        try:
            response = self.send_register_request(username, email, password, gender, age, role, self.profile_photo_path)
            if response.status_code == 200 or response.json().get("message") == "User registered successfully":
                response_data = response.json()
                print(f"Response data {response_data}")
                user_data = response_data.get("user")
                print(f"user data {user_data}")
                username = user_data.get("username")
                user_id = user_data.get("_id") 

                # Print the details
                print(f"Username is: {username}")
                print(f"User ID is: {user_id}")
                set_user_details(username, user_id)
                QMessageBox.information(self, "Success", "You have successfully registered!")
                self.switch_to_login.emit()
            else:
                QMessageBox.warning(self, "Error", "Failed to register. Please try again later.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to register. {str(e)}")

    @staticmethod
    def send_register_request(username, email, password, gender, age, current_role, profile_photo_path):
        """
        Sends a POST request to the register endpoint with multipart/form-data.
        """
        if gender == 1:
          gender = "male"
        elif gender == 2:
          gender = "female"
        else:
          gender = "other" 

        url = "https://reviewverse.onrender.com/register"
        headers = {
            "accept": "application/json"
        }
        files = {
            "username": (None, username),
            "email": (None, email),
            "password": (None, password),
            "gender": (None, gender),
            "age": (None, age),
            "currentrole": (None, current_role),
            "profilephoto": (os.path.basename(profile_photo_path), open(profile_photo_path, "rb"), "image/png")
        }

        response = requests.post(url, headers=headers, files=files)
        print(response)
        return response