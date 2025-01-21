from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QLineEdit, QPushButton, QMessageBox, QScrollArea, QComboBox, QCheckBox, QTextEdit
)
from PyQt5.QtCore import Qt
import requests


class MainBoardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Board")
        self.setGeometry(800, 700, 5050, 1200)

        # Pagination variables
        self.current_page = 1
        self.limit = 10  # Number of reviews per page

        # Create main layout
        self.layout = QVBoxLayout()  # Use QVBoxLayout for top (navbar/search) and bottom (left/right) sections

        # Create a horizontal layout for the navbar
        navbar = QHBoxLayout()

        # Add "ReviewVerse 📚" at the left side with enhanced styling
        self.navbar_title = QLabel("ReviewVerse 📚", self)
        self.navbar_title.setAlignment(Qt.AlignLeft)
        self.navbar_title.setStyleSheet("""
            QLabel {
                font-family: 'Arial', sans-serif;
                font-size: 30px;  /* Larger font size */
                font-weight: 700;  /* Bold font */
            }
            QLabel:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049,  /* Darker green on hover */
                    stop:1 #4CAF50
                );
                border: 2px solid #3e8e41;  /* Darker border on hover */
            }
        """)
        navbar.addWidget(self.navbar_title)

        # Add a stretch to push the circle to the right
        navbar.addStretch()

        # Add a circle with black color on the right side
        circle = QFrame(self)
        circle.setFixedSize(20, 20)  # Fixed size for the circle
        circle.setStyleSheet("background-color: black; border-radius: 10px;")  # Circle styling
        navbar.addWidget(circle)

        # Add navbar to the main layout
        self.layout.addLayout(navbar)

        # Create a horizontal layout for the search bar and button
        search_layout = QHBoxLayout()

        # Add search bar
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search by book name, author")  # Placeholder text
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; 
                border: 2px solid #45a020; 
                border-radius: 15px;  /* Rounded corners */
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #4CAF50;  /* Hover effect */
            }
        """)
        search_layout.addWidget(self.search_input)

        # Add search button
        self.search_button = QPushButton("Search", self)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Light green */
                color: white; 
                padding: 13px 20px; 
                border: none; 
                border-radius: 15px; /* Rounded corners */
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Slightly darker green */
                font-weight: bold; /* Bold white text */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Even darker green */
                font-weight: bold; /* Bold white text */
            }
        """)
        self.search_button.clicked.connect(self.handle_search)
        search_layout.addWidget(self.search_button)

        # Add search layout to the main layout
        self.layout.addLayout(search_layout)

        # Create a horizontal layout for the left and right sections
        content_layout = QHBoxLayout()

        # Left side layout for filters
        left_layout = QVBoxLayout()

        # Add filter options to the left side
        filter_label = QLabel("Filters", self)
        filter_label.setStyleSheet("""
            QLabel {
                font-size: 20px; 
                font-weight: bold; 
                margin-top: 50px;
                margin-bottom: 20px;
                color: #008ce3;  /* Updated color */
            }
        """)
        left_layout.addWidget(filter_label)

        # Add Reading Status dropdown
        self.reading_status_dropdown = QComboBox(self)
        self.reading_status_dropdown.addItems(["All", "start", "continue", "finished"])
        self.reading_status_dropdown.setPlaceholderText("Reading Status")
        self.reading_status_dropdown.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #008ce3;  /* Updated color */
                border-radius: 10px;
                font-size: 14px;
                margin-bottom: 15px;  /* Add margin below */
            }
            QComboBox:hover {
                border-color: #0077c2;  /* Darker shade on hover */
            }
        """)
        left_layout.addWidget(self.reading_status_dropdown)

        # Add Rating dropdown
        self.rating_dropdown = QComboBox(self)
        self.rating_dropdown.addItems(["All", "1", "2", "3", "4", "5"])
        self.rating_dropdown.setPlaceholderText("Rating")
        self.rating_dropdown.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #008ce3;  /* Updated color */
                border-radius: 10px;
                font-size: 14px;
                margin-bottom: 15px;  /* Add margin below */
            }
            QComboBox:hover {
                border-color: #0077c2;  /* Darker shade on hover */
            }
        """)
        left_layout.addWidget(self.rating_dropdown)

        # Add Buy Place dropdown
        self.buyplace_dropdown = QComboBox(self)
        self.buyplace_dropdown.addItems(["All", "online", "offline"])
        self.buyplace_dropdown.setPlaceholderText("Buy Place")
        self.buyplace_dropdown.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #008ce3;  /* Updated color */
                border-radius: 10px;
                font-size: 14px;
                margin-bottom: 15px;  /* Add margin below */
            }
            QComboBox:hover {
                border-color: #0077c2;  /* Darker shade on hover */
            }
        """)
        left_layout.addWidget(self.buyplace_dropdown)

        # Add Satisfaction checkbox
        self.satisfied_checkbox = QCheckBox("Satisfied", self)
        self.satisfied_checkbox.setStyleSheet("""
            QCheckBox {
                padding: 8px;
                font-size: 14px;
                color: #008ce3;  /* Updated color */
                margin-bottom: 15px;  /* Add margin below */
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #008ce3;  /* Updated color */
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #008ce3;  /* Updated color */
            }
        """)
        left_layout.addWidget(self.satisfied_checkbox)

        # Add Apply button
        self.apply_button = QPushButton("Apply", self)
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #008ce3; /* Updated color */
                color: white; 
                padding: 10px 20px; 
                border: none; 
                border-radius: 15px; /* Rounded corners */
                font-size: 14px;
                margin-bottom: 15px;  /* Add margin below */
            }
            QPushButton:hover {
                background-color: #0077c2; /* Darker shade on hover */
                font-weight: bold; /* Bold white text */
            }
            QPushButton:pressed {
                background-color: #0066b3; /* Even darker shade */
                font-weight: bold; /* Bold white text */
            }
        """)
        self.apply_button.clicked.connect(self.handle_apply)
        left_layout.addWidget(self.apply_button)

        # Add stretch to push filters to the top
        left_layout.addStretch()

        # Add left layout to the content layout
        content_layout.addLayout(left_layout)

        # Right side layout for cards
        right_layout = QVBoxLayout()

        # Create a scroll area to display the cards
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        # Add scroll area to the right layout
        right_layout.addWidget(self.scroll_area)

        # Add pagination controls
        pagination_layout = QHBoxLayout()
        self.previous_button = QPushButton("Previous", self)
        self.previous_button.setStyleSheet("""
            QPushButton {
                background-color: #008ce3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0077c2;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #0066b3;
                font-weight: bold;
            }
        """)
        self.previous_button.clicked.connect(self.handle_previous)
        pagination_layout.addWidget(self.previous_button)

        self.page_label = QLabel(f"Page {self.current_page}", self)
        self.page_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        pagination_layout.addWidget(self.page_label)

        self.next_button = QPushButton("Next", self)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #008ce3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0077c2;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #0066b3;
                font-weight: bold;
            }
        """)
        self.next_button.clicked.connect(self.handle_next)
        pagination_layout.addWidget(self.next_button)

        right_layout.addLayout(pagination_layout)

        # Add right layout to the content layout
        content_layout.addLayout(right_layout)

        # Add content layout to the main layout
        self.layout.addLayout(content_layout)

        # Set the layout for the page
        self.setLayout(self.layout)

        # Load initial reviews
        self.load_reviews()

    def load_reviews(self):
        """
        Loads reviews for the current page.
        """
        url = "https://reviewverse.onrender.com/get-reviews"
        params = {
            "page": self.current_page,
            "limit": self.limit
        }

        try:
            response = requests.get(url, params=params, headers={"accept": "application/json"})
            if response.status_code == 200:
                data = response.json()
                self.display_reviews(data)
            else:
                QMessageBox.warning(self, "API Error", f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def handle_previous(self):
        """
        Handles the Previous button click event.
        """
        if self.current_page > 1:
            self.current_page -= 1
            self.page_label.setText(f"Page {self.current_page}")
            self.load_reviews()

    def handle_next(self):
        """
        Handles the Next button click event.
        """
        self.current_page += 1
        self.page_label.setText(f"Page {self.current_page}")
        self.load_reviews()

    def handle_search(self):
        """
        Handles the search button click event.
        """
        search_text = self.search_input.text().strip()

        # Validation: Check if the search input is empty
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Please enter a book name or author to search.")
            return

        # Call the API
        self.call_api(search_text)

    def handle_apply(self):
        """
        Handles the Apply button click event for filters.
        """
        # Get filter values
        reading_status = self.reading_status_dropdown.currentText()
        rating = self.rating_dropdown.currentText()
        buyplace = self.buyplace_dropdown.currentText()
        satisfied = self.satisfied_checkbox.isChecked()

        # Prepare API parameters
        params = {
            "page": self.current_page,
            "limit": self.limit
        }

        # Add filters to parameters if not "All"
        if reading_status != "All":
            params["readingstatus"] = reading_status
        if rating != "All":
            params["rating"] = float(rating)
        if buyplace != "All":
            params["buyplace"] = buyplace
        if satisfied:
            params["satisfied"] = str(satisfied).lower()  # Convert to lowercase string

        # Call the API with filters
        self.call_api_with_filters(params)

    def call_api(self, search_text):
        """
        Calls the API with the search text and displays the results.
        """
        url = "https://reviewverse.onrender.com/filter"
        params = {
            "page": self.current_page,
            "limit": self.limit
        }

        # Add bookname or bookauthor based on input
        if " " in search_text:  # If input contains spaces, assume it's a book name
            params["bookname"] = search_text
        else:  # Otherwise, assume it's an author name
            params["bookauthor"] = search_text

        headers = {
            "accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.display_reviews(data)
            else:
                QMessageBox.warning(self, "API Error", f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def call_api_with_filters(self, params):
        """
        Calls the API with the selected filters and displays the results.
        """
        url = "https://reviewverse.onrender.com/filter"
        headers = {
            "accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.display_reviews(data)
            else:
                QMessageBox.warning(self, "API Error", f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def display_reviews(self, data):
        """
        Displays the reviews in a card format.
        """
        # Clear previous results
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # Check if there are reviews
        if not data.get("reviews"):
            QMessageBox.information(self, "No Results", "No reviews found for the given filters.")
            return

        # Display each review in a card
        for review in data["reviews"]:
            # Create the main card frame
            card = QFrame(self)
            card.setStyleSheet("""
                QFrame {
                               
                    background-color: #f9f9f9;
                    border: 1px solid;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px;
                }
            """)
            card_layout = QHBoxLayout(card)  # Use QHBoxLayout for left (photo) and right (content) sections

            # Right side: Content
            content_layout = QVBoxLayout()

            # First row: Book Name (left) and Rating (right)
            first_row = QHBoxLayout()
            bookname_label = QLabel(f"<b>📖 {review['bookname']}</b>", self)
            bookname_label.setStyleSheet("font-size: 16px;")
            first_row.addWidget(bookname_label)

            rating_label = QLabel(f"<b>⭐ {review['rating']}/5</b>", self)
            rating_label.setStyleSheet("font-size: 16px;")
            first_row.addStretch()  # Push rating to the right
            first_row.addWidget(rating_label)
            content_layout.addLayout(first_row)

            # Second row: Author (left) and Satisfied (right)
            second_row = QHBoxLayout()
            author_label = QLabel(f"<b>✍🏻 {review['bookauthor']}</b>", self)
            author_label.setStyleSheet("font-size: 14px;")
            second_row.addWidget(author_label)

            satisfied_label = QLabel(f"<b>👌🏻 {'Satisfied' if review['satisfied'] else 'Not Satisfied'}</b>", self)
            satisfied_label.setStyleSheet("font-size: 14px;")
            second_row.addStretch()  # Push satisfied to the right
            second_row.addWidget(satisfied_label)
            content_layout.addLayout(second_row)

            # Third row: Experience (textarea-like)
            experience_label = QLabel("<b>Experience:</b>", self)
            content_layout.addWidget(experience_label)

            experience_text = QTextEdit(self)
            experience_text.setText(review["experience"])
            experience_text.setReadOnly(True)  # Make it read-only
            experience_text.setFixedHeight(80)  # Set a fixed height for the text area
            experience_text.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #999;  /* Border for the experience section */
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            content_layout.addWidget(experience_text)

            # Fourth row: Reading Status (left) and Buy Place (right)
            fourth_row = QHBoxLayout()
            reading_status_label = QLabel(f"<b>📑 {review['readingstatus']}</b>", self)
            reading_status_label.setStyleSheet("font-size: 14px;")
            fourth_row.addWidget(reading_status_label)

            buyplace_label = QLabel(f"<b>🛒 {review['buyplace']}</b>", self)
            buyplace_label.setStyleSheet("font-size: 14px;")
            fourth_row.addStretch()  # Push buyplace to the right
            fourth_row.addWidget(buyplace_label)
            content_layout.addLayout(fourth_row)

            # Add content layout to the card layout
            card_layout.addLayout(content_layout)

            # Add card to the scroll layout
            self.scroll_layout.addWidget(card)

        # Add stretch to push cards to the top
        self.scroll_layout.addStretch()

     ##############   Book IMage displayed .





    # def load_photo(self, photo_url, photo_label):
    #     """
    #     Loads the book photo from the URL and sets it in the QLabel.
    #     Displays a placeholder text until the image is loaded.
    #     """
    #     # Set placeholder text while the image is loading
    #     photo_label.setText("Book Cover Photo")
    #     photo_label.setAlignment(Qt.AlignCenter)  # Center the placeholder text
    #     photo_label.setStyleSheet("""
    #     QLabel {
    #         background-color: #ccc;
    #         border: 2px solid #999;  /* Border for the image */
    #         border-radius: 5px;
    #         font-size: 14px;
    #         color: #333;
    #     }
    #     """)

    #     # Use QNetworkAccessManager to load the image
    #     network_manager = QNetworkAccessManager(self)
    #     request = QNetworkRequest(QUrl(photo_url))
    #     reply = network_manager.get(request)
    #     reply.finished.connect(lambda: self.set_photo(reply, photo_label))


    # def set_photo(self, reply, photo_label):
    #     """
    #     Sets the photo in the QLabel after loading it from the network reply.
    #     Removes the placeholder text once the image is loaded.
    #     """
    #     if reply.error() == QNetworkReply.NoError:
    #       data = reply.readAll()
    #       pixmap = QPixmap()
    #       pixmap.loadFromData(data)
    #       photo_label.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio))
    #       photo_label.setStyleSheet("""
    #         QLabel {
    #             background-color: #ccc;
    #             border: 2px solid #999;  /* Border for the image */
    #             border-radius: 5px;
    #         }
    #         """)
    #     else:
    #        # If there's an error loading the image, keep the placeholder text
    #        photo_label.setText("Failed to Load Image")
    #     reply.deleteLater()
