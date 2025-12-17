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

# from PySide6.QtWidgets import QWidget
# from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect
# from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
# import pyqtgraph as pg
# import numpy as np

# class LivePlot(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.plot_widget = pg.PlotWidget()
#         # ... layout etc ...

#         self.curve1 = self.plot_widget.plot(pen='b')
#         self.curve2 = self.plot_widget.plot(pen='r')

#         self.x_data = []
#         self.y1_data = []
#         self.y2_data = []

#         # Call update() 30 times per second
#         timer = pg.QtCore.QTimer()
#         timer.timeout.connect(self.update)
#         timer.start(33)  # ~30 Hz

#     def update(self):
#         self.x_data.append(len(self.x_data))
#         self.y1_data.append(np.random.normal())
#         self.y2_data.append(np.random.normal() + 2)

#         self.curve1.setData(self.x_data, self.y1_data)
#         self.curve2.setData(self.x_data, self.y2_data)

# app = QApplication(sys.argv)
# window = LivePlot()
# window.show()
# app.exec()        




# import pyqtgraph.examples
# pyqtgraph.examples.run()


# from PySide6.QtWidgets import QApplication, QMainWindow
# import pyqtgraph as pg
# import sys

# class MainWindow(QMainWindow):

#     def __init__(self):
#         super().__init__()

#         self.graphWidget = pg.PlotWidget()
#         self.setCentralWidget(self.graphWidget)

#         hour = [1,2,3,4,5,6,7,8,9,10]
#         temperature = [30,32,34,32,33,31,29,32,35,45]

#         # plot data: x, y values
#         self.graphWidget.plot(hour, temperature)


# app = QApplication(sys.argv)
# w = MainWindow()
# w.show()
# app.exec()


import pyqtgraph as pg
import numpy as np

app = pg.mkQApp("Crosshair Example")
win = pg.GraphicsLayoutWidget(show=True)
label = pg.LabelItem(justify='right')
win.addItem(label)

p = win.addPlot(row=1, col=0)
data = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(size=1000, scale=0.1)
curve = p.plot(data, pen='y')

# Crosshair lines
vLine = pg.InfiniteLine(angle=90, movable=False, pen='g')
hLine = pg.InfiniteLine(angle=0, movable=False, pen='g')
p.addItem(vLine, ignoreBounds=True)
p.addItem(hLine, ignoreBounds=True)

def mouseMoved(evt):
    pos = evt[0]  # evt[0] is the scene position
    if p.sceneBoundingRect().contains(pos):
        mousePoint = p.vb.mapSceneToView(pos)
        index = np.argmin(np.abs(np.linspace(0, 10, len(data)) - mousePoint.x()))
        x_val = np.linspace(0, 10, len(data))[index]
        y_val = data[index]
        label.setText(f"x={x_val:.3f}, y={y_val:.3f}")
        vLine.setPos(x_val)
        hLine.setPos(y_val)

proxy = pg.SignalProxy(p.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
win.show()
app.exec()
