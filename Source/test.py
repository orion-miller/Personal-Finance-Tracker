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



# import pyqtgraph as pg
# import numpy as np

# app = pg.mkQApp("Crosshair Example")
# win = pg.GraphicsLayoutWidget(show=True)
# label = pg.LabelItem(justify='right')
# win.addItem(label)

# p = win.addPlot(row=1, col=0)
# data = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(size=1000, scale=0.1)
# curve = p.plot(data, pen='y')

# # Crosshair lines
# vLine = pg.InfiniteLine(angle=90, movable=False, pen='g')
# hLine = pg.InfiniteLine(angle=0, movable=False, pen='g')
# p.addItem(vLine, ignoreBounds=True)
# p.addItem(hLine, ignoreBounds=True)

# def mouseMoved(evt):
#     pos = evt[0]  # evt[0] is the scene position
#     if p.sceneBoundingRect().contains(pos):
#         mousePoint = p.vb.mapSceneToView(pos)
#         index = np.argmin(np.abs(np.linspace(0, 10, len(data)) - mousePoint.x()))
#         x_val = np.linspace(0, 10, len(data))[index]
#         y_val = data[index]
#         label.setText(f"x={x_val:.3f}, y={y_val:.3f}")
#         vLine.setPos(x_val)
#         hLine.setPos(y_val)

# proxy = pg.SignalProxy(p.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
# win.show()
# app.exec()



# import numpy
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtGui, QtCore

# def gaussian(A, B, x):
#   return A * numpy.exp(-(x/(2. * B))**2.)

# def mouseMoved(evt):
#   mousePoint = p.vb.mapSceneToView(evt[0])
#   label.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))


# # Initial data frame
# x = numpy.linspace(-5., 5., 10000)
# y = gaussian(5., 0.2, x)


# # Generate layout
# win = pg.GraphicsView()
# label = pg.LabelItem(justify = "right")
# win.addItem(label)

# p = win.addPlot(row = 1, col = 0)

# plot = p.plot(x, y, pen = "y")

# proxy = pg.SignalProxy(p.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

# win.show()

# # Update layout with new data
# i = 0
# while i < 500:
#   noise = numpy.random.normal(0, .2, len(y))
#   y_new = y + noise

#   plot.setData(x, y_new, pen = "y", clear = True)
#   p.enableAutoRange("xy", False)

#   pg.QtGui.QApplication.processEvents()

#   i += 1

# win.close()



# from PySide6.QtGui import QCursor
# import pyqtgraph as pg


# def get_mouse_pos(pixel_mode=False) -> tuple:
#     pos = window.mapFromGlobal(QCursor.pos())
#     if pixel_mode:
#         return pos.toTuple()
#     else:
#         return plot.getViewBox().mapSceneToView(pos).toTuple()


# def update():
#     pos = get_mouse_pos()
#     x.append(pos[0])
#     y.append(pos[1])
#     curve.setData(x, y)


# x = []
# y = []
# window = pg.GraphicsLayoutWidget()
# plot = window.addPlot()
# curve = plot.plot(x, y)

# timer = pg.QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start()

# plot.setXRange(0, 1)
# plot.setYRange(0, 1)

# window.show()
# pg.exec()


# import pyqtgraph.examples
# pyqtgraph.examples.run()



import logging
import sys
from pathlib import Path
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
)


class QtLogHandler(logging.Handler):
    """Thread-safe handler that appends messages to QTextEdit via timer/queued connection"""
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit
        self.queue = []
        # Use a very short timer to batch & update GUI in main thread
        self.timer = QTimer()
        self.timer.setInterval(50)           # ~20 updates/sec max
        self.timer.timeout.connect(self._flush_queue)
        self.timer.start()

    def emit(self, record):
        msg = self.format(record)
        self.queue.append(msg)
        # No direct GUI write here → safe from any thread

    def _flush_queue(self):
        if not self.queue:
            return
        text = "".join(self.queue)
        self.queue.clear()

        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.insertPlainText(text)
        self.text_edit.ensureCursorVisible()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diary-like logging demo")
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        btn = QPushButton("Run long task")
        btn.clicked.connect(self.run_demo)
        layout.addWidget(btn)

        # Setup logging once
        self.setup_logging()

    def setup_logging(self):
        logger = logging.getLogger()           # root logger
        logger.setLevel(logging.INFO)

        # File handler (always safe)
        file_handler = logging.FileHandler("app_diary_2026.log", mode="a", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s  %(message)s"))
        logger.addHandler(file_handler)

        # GUI handler
        qt_handler = QtLogHandler(self.log_view)
        qt_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(qt_handler)

        # Optional: also see output in terminal
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(stream_handler)

    def run_demo(self):
        import time
        logger = logging.getLogger()

        logger.info("Starting long operation…")
        for i in range(1, 21):
            time.sleep(0.4)                    # simulate work
            logger.info(f"Step {i:02d}/20  –  {i*5}%")
        logger.info("Done!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(700, 500)
    window.show()
    sys.exit(app.exec())