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

import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QMainWindow


class CrosshairDataCursor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtGraph — Data Cursor / Crosshair")
        self.resize(900, 650)

        # === Plot setup ===
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        # Example data
        x = np.linspace(0, 10, 500)
        y = np.sin(x * 2.3) * x + np.random.normal(0, 0.4, len(x))

        self.curve = self.plot_widget.plot(
            x, y,
            pen=pg.mkPen('y', width=1.5),
            name="Noisy signal"
        )

        # Grid & labels
        self.plot_widget.showGrid(x=True, y=True, alpha=0.4)
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'Time (s)')

        # === Crosshair elements ===
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('r', width=1, style=pg.QtCore.Qt.DashLine))
        self.hline = pg.InfiniteLine(angle=0,  movable=False, pen=pg.mkPen('r', width=1, style=pg.QtCore.Qt.DashLine))

        self.plot_widget.addItem(self.vline)
        self.plot_widget.addItem(self.hline)

        # Label for coordinates (will follow mouse)
        self.label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )
        self.plot_widget.addItem(self.label, ignoreBounds=True)

        # Hide by default
        self.vline.hide()
        self.hline.hide()
        self.label.hide()

        # === Mouse tracking ===
        self.proxy = pg.SignalProxy(
            self.plot_widget.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=self.on_mouse_moved
        )

    def on_mouse_moved(self, evt):
        pos = evt[0]  # position in scene coordinates

        # Check if mouse is inside plot area
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            x, y = mouse_point.x(), mouse_point.y()

            # Update crosshair
            self.vline.setPos(x)
            self.hline.setPos(y)

            # Update coordinate label (positioned slightly above & right of cursor)
            self.label.setText(f"x: {x:.3f}\ny: {y:.3f}")
            self.label.setPos(x + 0.1, y + 0.3)  # small offset — adjust as needed

            # Show everything
            self.vline.show()
            self.hline.show()
            self.label.show()
        else:
            # Hide when mouse leaves plot area
            self.vline.hide()
            self.hline.hide()
            self.label.hide()


if __name__ == '__main__':
    # Optional: dark mode look (very popular)
    pg.setConfigOptions(
        background='k',
        foreground='w',
        antialias=True
    )

    app = QApplication(sys.argv)
    window = CrosshairDataCursor()
    window.show()
    sys.exit(app.exec())