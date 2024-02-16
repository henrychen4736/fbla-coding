import sys
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtQml import QQmlApplicationEngine
import sys

app = QApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.load('main.qml')

if not engine.rootObjects():
    sys.exit(-1)

with open('style.qss', 'r') as style_file:
    app.setStyleSheet(style_file.read())

sys.exit(app.exec())
