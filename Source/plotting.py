import numpy as np
import pyqtgraph as pg

def init(self):
    #set up plot format

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
    plot.clear()

    # Data
    dtable = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_cat"]
    cats = dtable.keys()

    x = np.arange(len(cats))
    bars = pg.BarGraphItem(x=x, height=list(dtable.values()), width=0.6, brush='#0066cc', pen='k')
    plot.addItem(bars)

    # Custom x-axis labels
    ax = plot.getAxis('bottom')
    ax.setTicks([[(i, cat) for i, cat in enumerate(cats)]])
    # ax.setTickLabelRotation(90)

    plot.setXRange(-0.6, len(cats) - 0.4) 