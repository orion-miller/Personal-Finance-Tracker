import numpy as np

def calc_metrics(self):

    bs = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"]
    self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs_met"]["assets"] = np.sum(bs[bs > 0])  
    self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs_met"]["debts"] = np.sum(bs[bs < 0])  
    self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs_met"]["assets - debts"] = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs_met"]["assets"] + self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs_met"]["debts"]     

    ie = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"]
    self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_met"]["income"] = np.sum(ie[ie > 0])  
    self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_met"]["expense"] = np.sum(ie[ie < 0])  
    self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_met"]["income - expense"] = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_met"]["income"] + self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie_met"]["expense"]
