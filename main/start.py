import sys, config
from logic.main import  *
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file into the window
        uic.loadUi("main/gui/main.ui", self)
        files  # Initialize the database connection
        refresh_list(self.fishListWidget)  # Refresh the fish list on startup

        self.fishSearchBar.textChanged.connect(
            lambda text: filter_list(self.fishListWidget, text)
        )
        
        self.fishDescription.textChanged.connect(
            lambda: (
                write_fish_description(
                    self.fishListWidget.currentItem().text()
                    if self.fishListWidget.currentItem() else "",
                    self.fishDescription.toPlainText()
                ) if self.fishListWidget.currentItem() else None
            )
        )
        # Broken code for fish name editing
        # self.fishNameTextEdit.textChanged.connect(
        #     lambda: (
        #         write_fish_name(
        #             self.fishListWidget.currentItem().text()
        #             if self.fishListWidget.currentItem() else "",
        #             self.fishNameTextEdit.toPlainText()
        #         ) if self.fishListWidget.currentItem() else None
        #     )
        # )

        self.fishListWidget.itemClicked.connect(lambda _: fill_fish_details(
            self.fishNameTextEdit,
            self.fishDescription,
            self.fishGraphicsView,
            self.fishListWidget.currentItem().text() if self.fishListWidget.currentItem() else ""
        ))

        self.artButton.clicked.connect(
            lambda _:(
                toggle_art(self),
                fill_fish_details(
                    self.fishNameTextEdit,
                    self.fishDescription,
                    self.fishGraphicsView,
                    self.fishListWidget.currentItem().text() if self.fishListWidget.currentItem() else ""
                )
            )
        )
        self.photoButton.clicked.connect(
            lambda _:(
                toggle_photo(self),
                fill_fish_details(
                    self.fishNameTextEdit,
                    self.fishDescription,
                    self.fishGraphicsView,
                    self.fishListWidget.currentItem().text() if self.fishListWidget.currentItem() else ""
                )
            )
        )
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
