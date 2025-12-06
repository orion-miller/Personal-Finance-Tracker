import numpy as np
import pyqtgraph as pg

def init(self):

    plot = self.ui.graphBS1   
          
    plot.showGrid(x=True, y=True)
    plot.setTitle("Balances vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')

    plot = self.ui.graphBS2   
          
    plot.showGrid(x=True, y=True)
    plot.setTitle("Totals vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')

    plot = self.ui.graphBS3  
          
    plot.showGrid(x=True, y=True)
    plot.setTitle("Asset Breakdown")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Asset')

    plot = self.ui.graphIE1   
          
    plot.showGrid(x=True, y=True)
    plot.setTitle("Income and Expense vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')

    plot = self.ui.graphIE2   
          
    plot.showGrid(x=True, y=True)
    plot.setTitle("Totals vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')

    plot = self.ui.graphIE3   

    plot.showGrid(x=True, y=True)
    plot.setTitle("Expense Breakdown")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Category')

def refresh(self):

    plot = self.ui.graphIE3  
    
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