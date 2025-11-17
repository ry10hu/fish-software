import sys
from logic.main import  *
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt6 import uic
import os, sys

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file into the window
        uic.loadUi(resource_path("gui/main.ui"), self)
        files  # Initialize the database connection
        self.fishListWidget.setSortingEnabled(True)

        refresh_list(self.fishListWidget)  # Refresh the fish list on startup

        self.fishSearchBar.textChanged.connect(
            lambda text: filter_list(self.fishListWidget, text)
        )
        
        self.fishDescription.textChanged.connect(
            lambda: (
                set_fish_description(
                    self.fishListWidget.currentItem().text()
                    if self.fishListWidget.currentItem() else "",
                    self.fishDescription.toPlainText()
                ) if self.fishListWidget.currentItem() else None
            )
        )
        
        self.fishGraphicsView.mouseDoubleClickEvent = lambda event: (
            set_image(
                self,
                self.fishListWidget.currentItem().text()
                if self.fishListWidget.currentItem() else ""
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
        self.deleteFishButton.clicked.connect(
            lambda: delete_fish(self, self.fishListWidget.currentItem().text() if self.fishListWidget.currentItem() else ""
        ))
        self.actionNew_fish.triggered.connect(
            lambda: NewFishWindow(self).show()
        )
class NewFishWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi(resource_path("gui/new.ui"), self)
        self.main_window = main_window  # store reference
        self.name = ""
        self.description = ""
        self.image_path = ""
        self.art_path = ""

        # Connect signals correctly
        self.newFishDescriptionTextEdit.document().contentsChanged.connect(self.update_description)
        self.newFishNameTextEdit.document().contentsChanged.connect(self.update_name)
        
        self.newFishGraphicsView.mouseDoubleClickEvent = self.choose_png
        self.saveButton.clicked.connect(self.add_fish)
        self.artButton.clicked.connect(self.toggle_art2)
        self.photoButton.clicked.connect(self.toggle_photo2)


    
    # --- slots ---
    def update_description(self):
        self.description = self.newFishDescriptionTextEdit.toPlainText()

    def update_name(self):
        self.name = self.newFishNameTextEdit.toPlainText()
    
    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select image", "",
                        "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            setGraphicsView(self.newFishGraphicsView, file_path)

    def choose_art(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select art", "",
                        "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.art_path = file_path
            setGraphicsView(self.newFishGraphicsView, file_path)
    def choose_png(self, event):
        if art:
            self.choose_art()
        else:
            self.choose_image()
    def toggle_photo2(self):
        global art
        art = False
        setGraphicsView(self.newFishGraphicsView, self.image_path)
    def toggle_art2(self):
        global art
        art = True
        setGraphicsView(self.newFishGraphicsView, self.art_path)

    def add_fish(self):
        make_new_fish(self.name,
                      self.description,
                      self.image_path,
                      self.art_path)
        refresh_list(self.main_window.fishListWidget)
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
