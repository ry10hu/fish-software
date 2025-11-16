import sqlite3, config
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
import sys

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

def write_fish_description(name, description):
    files.cursor.execute("UPDATE fish SET description = ? WHERE name = ?", (description, name))
    files.conn.commit()

def write_fish_name(name, new_name):
    files.cursor.execute("UPDATE fish SET name = ? WHERE name = ?", (new_name, name))
    files.conn.commit()


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