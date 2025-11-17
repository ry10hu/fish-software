import sqlite3, config
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QApplication, QMainWindow
import sys, shutil

class files:
    conn = sqlite3.connect(f"{config.workspace}/fish.db")
    cursor = conn.cursor()

global art
art = True

def toggle_art(self):
    global art
    art = True

def toggle_photo(self):
    global art
    art = False

def refresh_list(widget):
    widget.clear()
    widget.addItems([row[0] for row in files.cursor.execute("SELECT name FROM fish").fetchall()])

def filter_list(widget, keyword):
    widget.clear()
    widget.addItems([row[0] for row in files.cursor.execute("SELECT name FROM fish WHERE name LIKE ?", (f"%{keyword}%",)).fetchall()])

def setGraphicsView(graphicsView, image_path):
    scene = QtWidgets.QGraphicsScene()
    pixmap = QPixmap(image_path)
    scene.addPixmap(pixmap)
    graphicsView.setScene(scene)
    graphicsView.fitInView(scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

def set_fish_description(name, description):
    files.cursor.execute("UPDATE fish SET description = ? WHERE name = ?", (description, name))
    files.conn.commit()

def set_fish_name(name, new_name):
    files.cursor.execute("UPDATE fish SET name = ? WHERE name = ?", (new_name, name))
    files.conn.commit()

def set_image(self, name):
    file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            "",
            "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg)"
        )
    if file_path:
        if file_path.split("/")[-2] != "art" or "photograph":
            shutil.copy(file_path, config.image_path if not art else config.art_path)
        if art:
            files.cursor.execute("UPDATE fish SET art_filename = ? WHERE name = ?", (file_path.split("/")[-1], name))
        else:
            files.cursor.execute("UPDATE fish SET image_filename = ? WHERE name = ?", (file_path.split("/")[-1], name))
        files.conn.commit()
        fill_fish_details(
            self.fishNameTextEdit,
            self.fishDescription,
            self.fishGraphicsView,
            name
        )

def fill_fish_details( fishTextEdit, descriptionPlainTextEdit, graphicsView, name):
    details = files.cursor.execute("SELECT * FROM fish WHERE name = ?", (name,)).fetchone()
    if details:
        fishTextEdit.setPlainText(details[1])  
        descriptionPlainTextEdit.setPlainText(details[2])  # Assuming details[2] is a description
        if art:
            if details[4] != None:
                setGraphicsView(graphicsView, config.art_path + "/" + details[4])  # Assuming details[4] is the image filename
            else:
                graphicsView.setScene(None)
        else:
            if details[3] != None:
                setGraphicsView(graphicsView, config.image_path + "/" + details[3])  # Assuming details[4] is the photograph filename
            else:
                graphicsView.setScene(None)


def make_new_fish(name, description, image_path, art_path):
    print(f"Type of art_path: {type(art_path)}")
    print(f"Type of image_path: {type(image_path)}")
    print(f"Art path: {art_path}")
    print(f"Image path: {image_path}")
    image_filename = None
    art_filename = None
    if art_path != None and art_path.endswith((".png", ".jpg", ".jpeg")):
        if art_path.split("/")[-2] != "art":
            shutil.copy(art_path, config.art_path)
            art_filename = art_path.split("/")[-1]
        else:
            art_filename = art_path.split("/")[-1]

    if image_path != None and image_path.endswith((".png", ".jpg", ".jpeg")):
        if image_path.split("/")[-2] != "photographs":
            shutil.copy(image_path, config.image_path)
            image_filename = image_path.split("/")[-1]
        else:
            image_filename = image_path.split("/")[-1]
    files.cursor.execute(
        "INSERT INTO fish (name, description, image_filename, art_filename) VALUES (?, ?, ?, ?)",
        (name, description, image_filename, art_filename)
    )
    
    files.conn.commit()

def delete_fish(self, name):
    files.cursor.execute("DELETE FROM fish WHERE name = ?", (name,))
    files.conn.commit()
    refresh_list(self.fishListWidget)