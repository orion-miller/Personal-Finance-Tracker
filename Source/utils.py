import numpy as np
import pandas as pd

def calc_metrics(self, year, month):
    #calculate metrics from balance sheet and income expense data

    self.ps.db[year][month]["bs_met"]["assets"] = 0 
    self.ps.db[year][month]["bs_met"]["debts"] = 0 
    self.ps.db[year][month]["bs_met"]["assets - debts"] = 0

    bs_amt = self.ps.db[year][month]["bs"]['Amount']
    if len(bs_amt) > 0:
        self.ps.db[year][month]["bs_met"]["assets"] = np.sum(bs_amt[bs_amt > 0])  
        self.ps.db[year][month]["bs_met"]["debts"] = np.sum(bs_amt[bs_amt < 0])  
        self.ps.db[year][month]["bs_met"]["assets - debts"] = self.ps.db[year][month]["bs_met"]["assets"] + self.ps.db[year][month]["bs_met"]["debts"]     

    #initialize income expense fields
    self.ps.db[year][month]["ie_met"]["income"] = 0
    self.ps.db[year][month]["ie_met"]["expense"] = 0
    self.ps.db[year][month]["ie_met"]["income - expense"] = 0

    for sheet in self.ps.db[year][month]["ie"]:
        ie = self.ps.db[year][month]["ie"][sheet]
        for cat in self.ps.income_types:
            catlist = ie["Type"]
            self.ps.db[year][month]["ie_cat"][f"{cat}"] = 0  

        for cat in self.ps.expense_types:
            catlist = ie["Type"]
            self.ps.db[year][month]["ie_cat"][f"{cat}"] = 0            

    #populate income expense fields, need to loop through all sheets loaded for that month
    for sheet in self.ps.db[year][month]["ie"]:
        ie = self.ps.db[year][month]["ie"][sheet]
        amounts = pd.to_numeric(ie["Amount"], errors='coerce')
        self.ps.db[year][month]["ie_met"]["income"] += np.sum(amounts[amounts > 0])  
        self.ps.db[year][month]["ie_met"]["expense"] += np.sum(amounts[amounts < 0])  
        self.ps.db[year][month]["ie_met"]["income - expense"] += self.ps.db[year][month]["ie_met"]["income"] + self.ps.db[year][month]["ie_met"]["expense"]
        
        #find totals for each category
        for cat in self.ps.income_types:
            catlist = ie["Type"]
            indices = catlist[catlist == cat].index #also ensure values are positive
            if not indices.empty:
                self.ps.db[year][month]["ie_cat"][f"{cat}"] += np.sum(ie["Amount"].loc[indices]) 

        for cat in self.ps.expense_types:
            catlist = ie["Type"]
            indices = catlist[catlist == cat].index #also ensure values are negative
            if not indices.empty:            
                self.ps.db[year][month]["ie_cat"][f"{cat}"] += np.sum(ie["Amount"].loc[indices]) 

