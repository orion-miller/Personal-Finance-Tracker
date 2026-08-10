import numpy as np
import pandas as pd

def calc_metrics(self, year, month):
    #calculate metrics from balance sheet and income expense data

    #initialize balance sheet fields
    self.ps.db[year][month]["bs_met"]["Assets"] = 0 
    self.ps.db[year][month]["bs_met"]["Debts"] = 0 
    self.ps.db[year][month]["bs_met"]["Assets - Debts"] = 0

    #populate balance sheet fields
    bs_amt = self.ps.db[year][month]["bs"]['Amount']
    if len(bs_amt) > 0:
        self.ps.db[year][month]["bs_met"] = {} #for error that sometimes happens when adding new month
        self.ps.db[year][month]["bs_met"]["Assets"] = np.sum(bs_amt[bs_amt > 0])  
        self.ps.db[year][month]["bs_met"]["Debts"] = np.sum(bs_amt[bs_amt < 0])  
        self.ps.db[year][month]["bs_met"]["Assets - Debts"] = self.ps.db[year][month]["bs_met"]["Assets"] + self.ps.db[year][month]["bs_met"]["Debts"]     

    #initialize income expense fields
    self.ps.db[year][month]["ie_met"]["Income"] = 0
    self.ps.db[year][month]["ie_met"]["Expense"] = 0
    self.ps.db[year][month]["ie_met"]["Income - Expense"] = 0

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
        self.ps.db[year][month]["ie_met"]["Income"] += np.sum(amounts[amounts > 0])  
        self.ps.db[year][month]["ie_met"]["Expense"] += np.sum(amounts[amounts < 0])  
        self.ps.db[year][month]["ie_met"]["Income - Expense"] += self.ps.db[year][month]["ie_met"]["Income"] + self.ps.db[year][month]["ie_met"]["Expense"]
        
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

