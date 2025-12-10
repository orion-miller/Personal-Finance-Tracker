import numpy as np
import pyqtgraph as pg
import pandas as pd

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
    #refresh all plots with current data

    '''
    initialize plotting data structures
    each of these will be a single title, including YYYY-MM (year-month) as one of the columns
    this way for plotting we can have a single table representing the time range required
    '''
    pdata = {
        "bs": {},      #balance sheet
        "bs_met": {},  #balance sheet metrics                    
        "ie_met": {},  #income + expense metrics   
        "ie_cat": {},  #income + expense categories                                             
    }

    #get time range, years and months
    yearIdx1 = self.year_list.index(self.ps.year_p1)
    yearIdx2 = self.year_list.index(self.ps.year_p2)

    monthIdx1 = self.year_list.index(self.ps.month_p1)
    monthIdx2 = self.year_list.index(self.ps.month_p2)

    #cycle through and pull data from months in range
    for iY, year in enumerate(self.ps.year_list):
        if iY < yearIdx1 or iY > yearIdx2:
            continue

        for iM, month in enumerate(self.ps.month_list):
            if (iM < monthIdx1 and iY == 0) or (iM > monthIdx2 and iY == len(self.year_list)-1):
                continue

            #extract and concatenate data
            pdata["bs"] = pd.concat(pdata["bs"], self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"])            
            pdata["bs_met"] = pd.concat(pdata["bs_met"], self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs_met"])
            pdata["ie_met"] = pd.concat(pdata["ie_met"], self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_met"])  
            pdata["ie_cat"] = pd.concat(pdata["ie_met"], self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_cat"])                       

    plot = self.ui.graphBS3  
    plot.clear()

    # Data
    dtable = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"]
    cats = list(dtable['Item'])

    x = np.arange(len(cats))
    bars = pg.BarGraphItem(x=x, height=list(dtable['Amount']), width=0.6, brush='#0066cc', pen='k')
    plot.addItem(bars)

    # Custom x-axis labels
    ax = plot.getAxis('bottom')
    ax.setTicks([[(i, cat) for i, cat in enumerate(cats)]])
    # ax.setTickLabelRotation(90)

    plot.setXRange(-0.6, len(cats) - 0.4) 



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