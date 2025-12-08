import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# class AnotherWindow(QWidget):
#     """
#     This "window" is a QWidget. If it has no parent, it
#     will appear as a free-floating window as we want.
#     """

#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         self.label = QLabel("Another Window")
#         layout.addWidget(self.label)
#         self.setLayout(layout)


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.button = QPushButton("Push for Window")
#         self.button.clicked.connect(self.show_new_window)
#         self.setCentralWidget(self.button)

#     def show_new_window(self, checked):
#         if self.w is None:
#             self.w = AnotherWindow()
#         self.w.show()


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()

from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)

        self.child = QLabel(self)
        # self.setCentralWidget(self.child)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.child.setGraphicsEffect(self.opacity_effect)

        # self.child.setStyleSheet("background-color:red;border-radius:15px;")
        # self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child.graphicsEffect(), b"opacity")
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setDuration(4000)

        self.child.setText("Animated Label")        
        self.anim.start()

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()        