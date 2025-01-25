import os
import requests
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QTextEdit, QCheckBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from utils import username, user_id

class WriteReview(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Write Review")
        self.setGeometry(500, 500, 1000, 700)

        # users username and user_id
        self.username = username
        self.user_id = user_id

        # Layout
        layout = QVBoxLayout()

        # Book Name
        layout.addWidget(QLabel("Book Name:"))
        self.bookname_input = QLineEdit()
        self.bookname_input.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.bookname_input)

        # Book Author
        layout.addWidget(QLabel("Book Author:"))
        self.bookauthor_input = QLineEdit()
        self.bookauthor_input.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.bookauthor_input)

        # Experience
        layout.addWidget(QLabel("Experience:"))
        self.experience_input = QTextEdit()
        self.experience_input.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.experience_input)

        # Reading Status
        layout.addWidget(QLabel("Reading Status:"))
        self.reading_status_input = QComboBox()
        self.reading_status_input.addItems(["start", "continue", "finished"])
        self.reading_status_input.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.reading_status_input)

        # Rating
        layout.addWidget(QLabel("Rating (1-5):"))
        self.rating_input = QLineEdit()
        self.rating_input.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.rating_input)

        # Buy Place (Dropdown: Online, Offline)
        layout.addWidget(QLabel("Buy Place:"))
        self.buy_place_input = QComboBox()
        self.buy_place_input.addItems(["Online", "Offline"])
        self.buy_place_input.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.buy_place_input)

        # Satisfied
        self.satisfied_input = QCheckBox("Satisfied")
        layout.addWidget(self.satisfied_input)

        # Book Photo
        layout.addWidget(QLabel("Book Photo:"))
        self.bookphoto_path = QLineEdit()
        self.bookphoto_path.setStyleSheet("border: 2px solid green; border-radius: 8px; padding: 5px;")
        layout.addWidget(self.bookphoto_path)

        self.upload_button = QPushButton("Upload Photo")
        self.upload_button.clicked.connect(self.upload_photo)
        layout.addWidget(self.upload_button)

        # Submit Button
        self.submit_button = QPushButton("Add Review")
        self.submit_button.clicked.connect(self.add_review)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Book Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.bookphoto_path.setText(file_path)

    def add_review(self):
        # Validate inputs
        bookname = self.bookname_input.text().strip()
        bookauthor = self.bookauthor_input.text().strip()
        experience = self.experience_input.toPlainText().strip()
        reading_status = self.reading_status_input.currentText()
        rating = self.rating_input.text().strip()
        buy_place = self.buy_place_input.currentText().lower()
        satisfied = self.satisfied_input.isChecked()
        bookphoto = self.bookphoto_path.text().strip()

        if not bookname:
            QMessageBox.warning(self, "Error", "Book Name is required!")
            return
        if not bookauthor:
            QMessageBox.warning(self, "Error", "Book Author is required!")
            return
        if not experience:
            QMessageBox.warning(self, "Error", "Experience is required!")
            return
        if not rating:
            QMessageBox.warning(self, "Error", "Rating is required!")
            return
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Rating must be an integer between 1 and 5!")
            return
        if not bookphoto:
            QMessageBox.warning(self, "Error", "Book Photo is required!")
            return

        # Prepare form data
        form_data = {
            "buyplace": buy_place,
            "experience": experience,
            "user_id": self.user_id,
            "satisfied": str(satisfied).lower(),
            "bookname": bookname,
            "bookauthor": bookauthor,
            "rating": str(rating),
            "readingstatus": reading_status,
        }

        # Prepare file data
        files = {
            "bookphoto": (os.path.basename(bookphoto), open(bookphoto, "rb"), "image/jpeg")
        }

        # Send POST request
        try:
            response = requests.post(
                "https://reviewverse.onrender.com/add-review",
                data=form_data,
                files=files,
                headers={"accept": "application/json"}
            )
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "BookReview added successfully!")
                self.close() 
            else:
                QMessageBox.warning(self, "Error", f"Failed to add review: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            if 'files' in locals():
                files["bookphoto"][1].close()  # Close the file after the request
