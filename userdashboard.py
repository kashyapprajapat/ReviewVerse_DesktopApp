import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView, QSizePolicy, QTextEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl
from utils import username, user_id

# Hardcoded username and user_id
username = username
user_id = user_id

class UserDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Dashboard")
        self.setGeometry(500, 500, 1200, 800)  # Adjusted window size

        # Create the main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Header layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Username label at top-right
        self.username_label = QLabel(f"Welcome 🥳, {username}")
        self.username_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.username_label, alignment=Qt.AlignRight)

        # Add "Write Review" button
        self.add_review_button = QPushButton("Write Review")
        self.add_review_button.setStyleSheet("padding: 8px 15px; font-size: 16px;")
        self.add_review_button.clicked.connect(self.open_write_review)
        header_layout.addWidget(self.add_review_button, alignment=Qt.AlignRight)

        # Add header layout to main layout
        layout.addLayout(header_layout)

        # Table to display reviews
        self.reviews_table = QTableWidget()
        self.reviews_table.setColumnCount(8)  # Columns for data + Delete button
        self.reviews_table.setHorizontalHeaderLabels([
            "Book Name", "Author", "Photo", "Experience", "Status", "Rating", "Buy Place", "Actions"
        ])
        self.reviews_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.reviews_table.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px;
            }
            QTableWidget {
                font-size: 14px;
            }
        """)
        self.reviews_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.reviews_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.reviews_table)

        # Fetch and display reviews
        self.fetch_reviews()

        # Set the main layout
        self.setLayout(layout)

    def open_write_review(self):
        """
        Open writereview.py.
        """
        from writereview import WriteReview  # Import the WriteReview class
        self.write_review_window = WriteReview()  # Create an instance of WriteReview
        self.write_review_window.show()  # Show the WriteReview window

    def fetch_reviews(self):
        """
        Fetch reviews from the API and populate the table.
        """
        try:
            url = f"https://reviewverse.onrender.com/get-reviews/{user_id}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and "reviews" in data:
                reviews = data["reviews"]
                self.populate_table(reviews)
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch reviews.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def populate_table(self, reviews):
        """
        Populate the table with reviews.
        """
        self.reviews_table.setRowCount(len(reviews))

        for row, review in enumerate(reviews):
            # Populate review data
            self.reviews_table.setItem(row, 0, QTableWidgetItem(review["bookname"]))
            self.reviews_table.setItem(row, 1, QTableWidgetItem(review["bookauthor"]))

            # Display book photo
            photo_label = QLabel()
            placeholder_pixmap = QPixmap(70, 70)
            placeholder_pixmap.fill(Qt.lightGray)
            photo_label.setPixmap(placeholder_pixmap)
            photo_label.setScaledContents(True)

            self.load_image(review["bookphoto"], photo_label)
            self.reviews_table.setCellWidget(row, 2, photo_label)

            # Display Experience using QTextEdit
            experience_text = QTextEdit()
            experience_text.setText(review["experience"])
            experience_text.setReadOnly(True)  # Make it read-only
            experience_text.setStyleSheet("font-size: 14px; padding: 5px;")
            self.reviews_table.setCellWidget(row, 3, experience_text)
            self.reviews_table.setItem(row, 4, QTableWidgetItem(review["readingstatus"]))
            self.reviews_table.setItem(row, 5, QTableWidgetItem(str(review["rating"])))
            self.reviews_table.setItem(row, 6, QTableWidgetItem(review["buyplace"]))

            # Add Delete button
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("padding: 5px; font-size: 14px; color: white; background-color: red;")
            delete_button.clicked.connect(lambda _, r=row, review_id=review["_id"]: self.delete_review(r, review_id))
            self.reviews_table.setCellWidget(row, 7, delete_button)

    def load_image(self, url, label):
        """
        Load an image from a URL and display it in a QLabel.
        """
        manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        reply = manager.get(request)

        reply.finished.connect(lambda: self.display_image(reply, label))

    def display_image(self, reply, label):
        """
        Display the fetched image in the QLabel.
        """
        if reply.error() == QNetworkReply.NoError:
            pixmap = QPixmap()
            pixmap.loadFromData(reply.readAll())
            label.setPixmap(pixmap.scaled(70, 70, Qt.KeepAspectRatio))
        else:
            print("Failed to load image.")

    def delete_review(self, row, review_id):
        """
        Handle deleting a review after confirmation.
        """
        # Ask for confirmation
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this review?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Default to "No" to avoid accidental deletions
        )

        # Proceed only if the user confirms
        if confirm == QMessageBox.Yes:
            try:
                url = f"https://reviewverse.onrender.com/delete-review/{user_id}/{review_id}"
                response = requests.delete(url)

                if response.status_code == 200:
                    QMessageBox.information(self, "Success", "Review deleted successfully.")
                    self.fetch_reviews()  # Refresh the table
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete review.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")


