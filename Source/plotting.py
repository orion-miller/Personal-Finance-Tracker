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
    plot.addLegend(offset=(2, 2))

    plot = self.ui.graphBS2            
    plot.showGrid(x=True, y=True)
    plot.setTitle("Totals vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')
    plot.addLegend(offset=(2, 2))    

    plot = self.ui.graphBS3           
    plot.showGrid(x=True, y=True)
    plot.setTitle("Asset Breakdown")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Asset')
    plot.addLegend(offset=(2, 2))     

    plot = self.ui.graphIE1             
    plot.showGrid(x=True, y=True)
    plot.setTitle("Income and Expense vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')
    plot.addLegend(offset=(2, 2)) 

    plot = self.ui.graphIE2            
    plot.showGrid(x=True, y=True)
    plot.setTitle("Totals vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time')
    plot.addLegend(offset=(2, 2)) 

    plot = self.ui.graphIE3   
    plot.showGrid(x=True, y=True)
    plot.setTitle("Expense Breakdown")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Category')
    plot.addLegend(offset=(2, 2)) 

def refresh(self):
    #refresh all plots with current data

    '''
    initialize plotting data structures
    each of these will be a single title, including YYYY-MM (year-month) as one of the columns
    this way for plotting we can have a single table representing the time range required
    '''
    pdata = {
        "bs": pd.DataFrame(),      #balance sheet
        "bs_met": pd.DataFrame(),  #balance sheet metrics                    
        "ie_met": pd.DataFrame(),  #income + expense metrics   
        "ie_cat": pd.DataFrame(),  #income + expense categories                                             
    }

    #get time range, years and months
    yearIdx1 = self.ps.year_list.index(self.ps.year_p1)
    yearIdx2 = self.ps.year_list.index(self.ps.year_p2)

    # monthIdx1 = self.ps.month_list.index(self.ps.month_p1)
    # monthIdx2 = self.ps.month_list.index(self.ps.month_p2)

    monthIdx1 = int(self.ps.month_p1) - 1
    monthIdx2 = int(self.ps.month_p2) - 1   

    #cycle through and pull data from months in range
    for iY, year in enumerate(self.ps.year_list):
        if iY < yearIdx1 or iY > yearIdx2:
            continue

        for iM, month in enumerate(self.ps.month_list):
            if (iM < monthIdx1 and iY == 0) or (iM > monthIdx2 and iY == len(self.year_list)-1):
                continue

            #extract and concatenate data
            # bs_transformed = self.ps.db[year][str(iM +1)]["bs"].set_index('Item')['Amount'].to_frame().T
            bs = self.ps.db[year][str(iM +1)]["bs"]            
            bs_df = pd.DataFrame({item: [amount] for item, amount in zip(bs['Item'], bs['Amount'])})
            pdata["bs"] = pd.concat([pdata["bs"], bs_df], axis=0, ignore_index=True)    

            pdata["bs_met"] = pd.concat([pdata["bs_met"], pd.DataFrame([self.ps.db[year][str(iM +1)]["bs_met"]])], axis=0, ignore_index=True)
            pdata["ie_met"] = pd.concat([pdata["ie_met"], pd.DataFrame([self.ps.db[year][str(iM +1)]["ie_met"]])], axis=0, ignore_index=True)  
            pdata["ie_cat"] = pd.concat([pdata["ie_cat"], pd.DataFrame([self.ps.db[year][str(iM +1)]["ie_cat"]])], axis=0, ignore_index=True)                       

    #clear all plots
    self.ui.graphBS1.clear() 
    self.ui.graphBS2.clear() 
    self.ui.graphBS3.clear() 
    self.ui.graphIE1.clear() 
    self.ui.graphIE2.clear() 
    self.ui.graphIE3.clear() 

    colors = ['g', 'r', 'y', 'c', 'm', 'w', 'orange', 'pink', 'gray', 'g', 'r', 'y', 'c', 'm', 'w', 'orange', 'pink', 'gray'] #shouldnt repeat

    #----------------------------------------------------------------------------
    #replot for all figures

    # #Balance sheet 1
    fig = self.ui.graphBS1  
    dtable = pdata["bs"]
    x = np.arange(len(pdata["bs"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1, pen=colors[i], name=key)

    #Balance sheet 2
    fig = self.ui.graphBS2  
    dtable = pdata["bs_met"]
    x = np.arange(len(pdata["bs_met"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1, pen=colors[i], name=key)
  
    #Balance sheet 3
    plot = self.ui.graphBS3  

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

    #Income Expense 1
    fig = self.ui.graphIE1  
    dtable = pdata["ie_cat"]
    x = np.arange(len(pdata["ie_cat"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1, pen=colors[i], name=key)

    #Income Expense 2
    fig = self.ui.graphIE2  
    dtable = pdata["ie_met"]
    x = np.arange(len(pdata["ie_met"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1, pen=colors[i], name=key)

    #Income Expense 3
    plot = self.ui.graphIE3  

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