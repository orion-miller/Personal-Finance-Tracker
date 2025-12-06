import numpy as np
import pyqtgraph as pg

def refresh(self):
    # This is the widget you promoted in Designer!
    # plot = self.ui.findChild(pg.PlotWidget, "PlotWidget")  # or whatever ObjectName you gave it
    plot = self.ui.graphIE3         
    # If you didn't set an objectName, use: plot = self.ui.your_placeholder_widget_name

    # Optional styling
    # plot.setBackground('b')
    plot.showGrid(x=True, y=True)
    plot.setTitle("Expense Breakdown")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Category')

    # Data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    values = [120, 190, 150, 230, 210, 280]

    x = np.arange(len(months))
    bars = pg.BarGraphItem(x=x, height=values, width=0.6, brush='#0066cc', pen='k')
    plot.addItem(bars)

    # Custom x-axis labels
    ax = plot.getAxis('bottom')
    ax.setTicks([[(i, month) for i, month in enumerate(months)]])

    plot.setXRange(-0.6, len(months) - 0.4) 