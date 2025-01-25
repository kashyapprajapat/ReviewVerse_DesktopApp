from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys
from login import LoginPage
from register import RegisterPage
from mainboard import MainBoardPage
from admindashboard import AdminDashboard

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.mainboard_page = MainBoardPage()
        self.admin_dashboard_page = AdminDashboard()

        self.addWidget(self.login_page)
        self.addWidget(self.register_page)
        self.addWidget(self.mainboard_page)
        self.addWidget(self.admin_dashboard_page)  # Add admin dashboard to stack

        self.login_page.switch_to_register.connect(self.show_register)
        self.login_page.switch_to_mainboard.connect(self.show_mainboard)
        self.login_page.switch_to_admin_dashboard.connect(self.show_admin_dashboard)  # Connect admin dashboard signal
        self.register_page.switch_to_login.connect(self.show_login)

        # Set the window title with logo/emoji
        self.setWindowTitle("ReviewVerse 📚")  # You can adjust the emoji to your desired one

    def show_login(self):
        self.setCurrentWidget(self.login_page)

    def show_register(self):
        self.setCurrentWidget(self.register_page)

    def show_mainboard(self):
        self.mainboard_page = MainBoardPage()  # Reload with updated data
        self.addWidget(self.mainboard_page)
        self.setCurrentWidget(self.mainboard_page)

    def show_admin_dashboard(self):
        self.setCurrentWidget(self.admin_dashboard_page)  # Switch to admin dashboard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
