import numpy as np
import pyqtgraph as pg
import pandas as pd

def init(self):
    #set up plot format

    plot = self.ui.graphBS1            
    plot.showGrid(x=True, y=True)
    # plot.setTitle("Balances vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time (Year-Month)')
    plot.addLegend(offset=(2, 2))

    plot = self.ui.graphBS2            
    plot.showGrid(x=True, y=True)
    # plot.setTitle("Totals vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time (Year-Month)')
    plot.addLegend(offset=(2, 2))    

    plot = self.ui.graphBS3           
    plot.showGrid(x=True, y=True)
    # plot.setTitle("Asset Breakdown")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Asset')
    plot.addLegend(offset=(2, 2))     

    plot = self.ui.graphIE1             
    plot.showGrid(x=True, y=True)
    # plot.setTitle("Income and Expense vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time (Year-Month)')
    plot.addLegend(offset=(2, 2)) 

    plot = self.ui.graphIE2            
    plot.showGrid(x=True, y=True)
    # plot.setTitle("Totals vs. Time")
    plot.setLabel('left', 'Amount (USD)')
    plot.setLabel('bottom', 'Time (Year-Month)')
    plot.addLegend(offset=(2, 2)) 

    plot = self.ui.graphIE3   
    plot.showGrid(x=True, y=True)
    # plot.setTitle("Expense Breakdown")
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
        "month": pd.DataFrame(),   #year-month labels                                              
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
            if (iM < monthIdx1 and iY == yearIdx1) or (iM > monthIdx2 and iY == yearIdx2):
                continue

            #extract and concatenate data
            bs = self.ps.db[year][str(iM +1)]["bs"]            
            bs_df = pd.DataFrame({item: [amount] for item, amount in zip(bs['Item'], bs['Amount'])})
            pdata["bs"] = pd.concat([pdata["bs"], bs_df], axis=0, ignore_index=True)    

            pdata["bs_met"] = pd.concat([pdata["bs_met"], pd.DataFrame([self.ps.db[year][str(iM +1)]["bs_met"]])], axis=0, ignore_index=True)
            pdata["ie_met"] = pd.concat([pdata["ie_met"], pd.DataFrame([self.ps.db[year][str(iM +1)]["ie_met"]])], axis=0, ignore_index=True)  
            pdata["ie_cat"] = pd.concat([pdata["ie_cat"], pd.DataFrame([self.ps.db[year][str(iM +1)]["ie_cat"]])], axis=0, ignore_index=True)   
            pdata["month"] = pd.concat([pdata["month"], pd.DataFrame([f"{year[2:4]}-{str(iM +1)}"])], axis=0, ignore_index=True)                    

    try:
        pdata["ie_cat"] = pdata["ie_cat"].drop('Transfer', axis=1)
    except:
        pass

    pdata["month"] = pdata["month"][0]

    #clear all plots
    self.ui.graphBS1.clear() 
    self.ui.graphBS2.clear() 
    self.ui.graphBS3.clear() 
    self.ui.graphIE1.clear() 
    self.ui.graphIE2.clear() 
    self.ui.graphIE3.clear() 

    #define color order for plotting
    colors = [
        '#00ff00',        
        '#ff0000',
        '#ffffff',     
        '#0066ff',           
        '#ff9900',
        '#9933ff',
        "#6acdff",
        "#e8abe8",
        '#b38600',
        '#339933',
        "#1628AA",        
        '#9999ff',
        '#800000',
        '#008080',
        '#c8ef7a',
        '#737373',
        '#9e9e03',
        '#ff66ff',
        "#4dc567", 
        "#024760",         
        "#ffd857", 
        "#57ffae",  
        "#ff5757", 
        "#5f3e0a",  
        "#33502D",          
        '#4d4dff',         
        "#433a2c",   
        "#25097f", 
        "#ccff00",  
        "#e4531a",                                                                   
    ]

    #----------------------------------------------------------------------------
    #replot for all figures

    #Balance sheet 1
    fig = self.ui.graphBS1  
    dtable = pdata["bs"]
    x = np.arange(len(pdata["bs"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1.5, pen=colors[i], name=key)
        # fig.plot(x=x, y=dtable[key], width=1, pen=colors[i], symbol='o', name=key)        

    # Custom x-axis labels
    ax = fig.getAxis('bottom') 
    ax.setTicks([[(i, month) for i, month in enumerate(pdata["month"])]])       

    #Balance sheet 2
    fig = self.ui.graphBS2  
    dtable = pdata["bs_met"]
    x = np.arange(len(pdata["bs_met"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1.5, pen=colors[i], name=key)
  
    # Custom x-axis labels
    ax = fig.getAxis('bottom') 
    ax.setTicks([[(i, month) for i, month in enumerate(pdata["month"])]]) 

    #Balance sheet 3
    fig = self.ui.graphBS3  

    # Data
    dtable = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"]
    # cats = list(dtable['Item'])

    x = np.arange(len(dtable['Item']))
    x_idx = 0
    labels = []

    for i, item in enumerate(dtable['Item']):  
        if dtable['Amount'][i] <= 0: #only plot negative vals for expenses, ignore transfers            
            continue
        else: #plot category
            bar = pg.BarGraphItem(x=x_idx, height=dtable['Amount'][i], width=1, brush=colors[i], pen='w')
            fig.addItem(bar)

            x_idx += 1            
            labels.append(item)

    # Custom x-axis labels  
    ax = fig.getAxis('bottom')
    ax.setTicks([[(i, label) for i, label in enumerate(labels)]])
    fig.setXRange(-0.6, len(labels) - 0.4) 

    #Income Expense 1
    fig = self.ui.graphIE1  
    dtable = pdata["ie_cat"]
    x = np.arange(len(pdata["ie_cat"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1.5, pen=colors[i], name=key)

    # Custom x-axis labels
    ax = fig.getAxis('bottom') 
    ax.setTicks([[(i, month) for i, month in enumerate(pdata["month"])]]) 

    #Income Expense 2
    fig = self.ui.graphIE2  
    dtable = pdata["ie_met"]
    x = np.arange(len(pdata["ie_met"]))

    for i, key in enumerate(dtable.keys()):
        fig.plot(x=x, y=dtable[key], width=1.5, pen=colors[i], name=key)

    # Custom x-axis labels
    ax = fig.getAxis('bottom') 
    ax.setTicks([[(i, month) for i, month in enumerate(pdata["month"])]]) 

    #Income Expense 3
    fig = self.ui.graphIE3  

    # Data
    dtable = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_cat"]
    try:
        dtable = dtable.pop('Transfer')
    except:
        pass

    cats = dtable.keys()

    x = np.arange(len(cats))
    x_idx = 0
    labels = []

    for i, cat in enumerate(cats):  
        if dtable[cat] >= 0 or cat == 'Transfer': #only plot negative vals for expenses, ignore transfers            
            continue
        else: #plot category
            bar = pg.BarGraphItem(x=x_idx, height=dtable[cat], width=1, brush=colors[i], pen='w')
            fig.addItem(bar)

            x_idx += 1            
            labels.append(cat)

    # Custom x-axis labels
    cats = dtable.keys()    
    ax = fig.getAxis('bottom')
    ax.setTicks([[(i, label) for i, label in enumerate(labels)]])
    fig.setXRange(-0.6, len(labels) - 0.4) 