#built in modules
import sys
import os
from pathlib import Path
import ctypes

#GUI modules
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox,
    QStyledItemDelegate, QComboBox, QProgressBar, QGraphicsOpacityEffect,
    QStatusBar, QLabel, QHeaderView
)
from PySide6.QtUiTools import QUiLoader   # ← not needed anymore
# from PySide6 import QtUiTools
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QTimer, QModelIndex,
    QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import QIcon
from mainwindow import Ui_OrionsApp
import PySide6
import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock

#other modules
import pandas as pd
import numpy as np
import ollama 

#external fcns
import plotting
import utils
import status

#COMPILATION CMD:
# pyside6-uic mainwindow.ui -o mainwindow.py

class Properties:
    def __init__(self):
        self.APP_VERSION = "1.0"
        self.data_folder = "D:\\!Orion_Documents\\Financial\\!OM_Finance_Tracker" 
        self.income_types = ["Work", "Investment", "Sales", "Rewards"] #make editable through ui later
        self.expense_types = ["Transfer", "Bills", "Groceries","Takeout","Car","Travel","Entertainment","Other"] #make editable through ui later
        self.income_expense_types = self.income_types + self.expense_types   
        self.bs_format = pd.DataFrame({
            "Item":   ["New"],
            "Amount": [0.00]})              
        self.db = {
            "2025": { #year
                "12": { #month
                    "bs": self.bs_format,      #balance sheet
                    "bs_met": {},  #balance sheet metrics                    
                    "ie": {},      #income + expense
                    "ie_met": {},  #income + expense metrics   
                    "ie_cat": {},  #income + expense categories                                      
                    "notes": ""    #general notes
                }           
        }   
        }
        self.year_list = ["2020", "2021", "2022", "2023", "2024", "2025"] #make editable through ui later
        self.month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] #make editable through ui later
        self.year_sel = "2025"
        self.month_sel = "12"
        self.year_p1 = "2024"
        self.month_p1 = "12"
        self.year_p2 = "2025"
        self.month_p2 = "12"    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_OrionsApp()
        self.ui.setupUi(self)        

        #Startup tasks

        #Properties
        self.ps = Properties()

        #initialize data base with blank template
        MainWindow.db_init(self)

        try: #load db file from working directory if present, to overwrite blank template
            self.ps.db = np.load(os.path.join(self.ps.data_folder,"db.npz"), allow_pickle=True)["db"].item()
        except:
            pass

        #Set initial component properties
        self.setWindowTitle(f"Finance Tracker {self.ps.APP_VERSION}")

        self.ui.tabWidget.setTabText(0, "Balance Sheet")
        self.ui.tabWidget.setTabText(1, "Income + Expense")    
        self.ui.tabWidget_2.setTabText(0, "Balance Sheet")
        self.ui.tabWidget_2.setTabText(1, "Income + Expense")        

        self.ui.sheetTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.ui.comboBox_year.addItems(self.ps.year_list)        
        self.ui.comboBox_month.addItems(self.ps.month_list)
        # self.ui.comboBox_month.setItemData([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])        
        self.ui.comboBox_year.setCurrentText("2025")
        self.ui.comboBox_month.setCurrentText("Dec")
        self.ui.comboBox_year_2.addItems(self.ps.year_list)        
        self.ui.comboBox_month_2.addItems(self.ps.month_list)
        # self.ui.comboBox_month_2.setItemData(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)          
        self.ui.comboBox_year_2.setCurrentText("2025")
        self.ui.comboBox_month_2.setCurrentText("Jan")
        self.ui.comboBox_year_3.addItems(self.ps.year_list)        
        self.ui.comboBox_month_3.addItems(self.ps.month_list)
        # self.ui.comboBox_month_3.setItemData(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)          
        self.ui.comboBox_year_3.setCurrentText("2025")
        self.ui.comboBox_month_3.setCurrentText("Dec")   

        self.ui.tableBS.setAlternatingRowColors(True)
        self.ui.sheetTable.setAlternatingRowColors(True)
        self.ui.tableBS.setShowGrid(False)        
        self.ui.sheetTable.setShowGrid(False)     

        self.statusBar().setStyleSheet("""
            QStatusBar::item { border: none; }
            QStatusBar { border: none; }
        """)

        #Add figure docks
        self.ui.dock_BS1 = Dock("Balances vs. Time")
        self.ui.dock_BS2 = Dock("Totals vs. Time")
        self.ui.dock_BS3 = Dock("Asset Breakdown")        

        self.ui.graphBS1 = pg.PlotWidget()
        self.ui.graphBS2 = pg.PlotWidget()
        self.ui.graphBS3 = pg.PlotWidget()  

        self.ui.dock_BS1.addWidget(self.ui.graphBS1) 
        self.ui.dock_BS2.addWidget(self.ui.graphBS2)
        self.ui.dock_BS3.addWidget(self.ui.graphBS3)        

        self.ui.BS_area.addDock(self.ui.dock_BS1, 'top')
        self.ui.BS_area.addDock(self.ui.dock_BS2, 'bottom')
        self.ui.BS_area.addDock(self.ui.dock_BS3, 'right')  

        self.ui.dock_IE1 = Dock("Income and Expense vs. Time")
        self.ui.dock_IE2 = Dock("Totals vs. Time")
        self.ui.dock_IE3 = Dock("Expense Breakdown")  

        self.ui.graphIE1 = pg.PlotWidget()
        self.ui.graphIE2 = pg.PlotWidget()
        self.ui.graphIE3 = pg.PlotWidget()  

        self.ui.dock_IE1.addWidget(self.ui.graphIE1) 
        self.ui.dock_IE2.addWidget(self.ui.graphIE2)
        self.ui.dock_IE3.addWidget(self.ui.graphIE3)               

        self.ui.IE_area.addDock(self.ui.dock_IE1, 'top')
        self.ui.IE_area.addDock(self.ui.dock_IE2, 'bottom')
        self.ui.IE_area.addDock(self.ui.dock_IE3, 'right')   

        plotting.init(self)        

        #Callbacks
        MainWindow.year_changed(self)
        MainWindow.month_changed(self)        

        #Connections
        self.ui.actionOpen.triggered.connect(self.pick_folder)
        self.ui.actionAbout.triggered.connect(self.show_info)
        self.ui.sheetLoad.clicked.connect(self.load_csv)
        self.ui.sheetSave.clicked.connect(self.save_csv)
        self.ui.sheetDelete.clicked.connect(self.delete_csv)   
        self.ui.sheetDropdown.currentIndexChanged.connect(self.changed_csv)     
        self.ui.pushButton_refresh.clicked.connect(self.refresh_plots)    
        self.ui.pushButton_loadmonth.clicked.connect(self.load_month)            
        self.ui.pushButton_savemonth.clicked.connect(self.save_month)
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.ui.tabWidget_2.currentChanged.connect(self.on_tab_changed_2)
        self.ui.comboBox_month.currentIndexChanged.connect(self.month_changed)
        self.ui.comboBox_month_2.currentIndexChanged.connect(self.month_changed)    
        self.ui.comboBox_month_3.currentIndexChanged.connect(self.month_changed)
        self.ui.comboBox_year.currentIndexChanged.connect(self.year_changed)
        self.ui.comboBox_year_2.currentIndexChanged.connect(self.year_changed)      
        self.ui.comboBox_year_3.currentIndexChanged.connect(self.year_changed)
        self.ui.pushButton_add_row.clicked.connect(self.add_bs_row)
        self.ui.pushButton_copy_previous.clicked.connect(self.bs_copy_previous)        
        self.ui.pushButton_saveBS.clicked.connect(self.save_bs_month)

        self.ui.graphBS1.scene().sigMouseClicked.connect(self.change_plot_focus)

    #----------------------------------------------------------
    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            parent=self,                                   # your MainWindow or widget
            caption="Choose a folder",                     # title bar text
            dir=self.ps.data_folder                                      
        )

        if folder:                                         # user clicked OK (not Cancel)
            self.ps.data_folder = folder 
            status.msg.show(self, f"Workspace directory set: {folder}", "green")                           
    #----------------------------------------------------------
    def show_info(self):
        QMessageBox.information(
            self,
            "About",
            f"Finance Tracker\nVersion: {self.ps.APP_VERSION}\n\nContact: orion.miller@outlook.com"
        )
    #----------------------------------------------------------
    def on_tab_changed(self, index):
        tab_name = self.ui.tabWidget.tabText(index)

        match tab_name:
            case "Balance Sheet":
                self.ui.tabWidget_2.setCurrentIndex(0)
            case "Income + Expense":        
                self.ui.tabWidget_2.setCurrentIndex(1)
    #----------------------------------------------------------
    def on_tab_changed_2(self, index):
        tab_name = self.ui.tabWidget_2.tabText(index)

        match tab_name:
            case "Balance Sheet":
                self.ui.tabWidget.setCurrentIndex(0)
            case "Income + Expense":        
                self.ui.tabWidget.setCurrentIndex(1)      
    #----------------------------------------------------------
    def bs_copy_previous(self):
        #copy balance sheet from previous month into current month

        # month_idx = self.ps.month_list.index(self.ps.month_sel)
        year_idx = self.ps.year_list.index(self.ps.year_sel)

        if int(self.ps.month_sel) == 1:
            month_prev = "12"
            year_prev = self.ps.year_list[year_idx - 1]
        else:
            month_prev = str(int(self.ps.month_sel) - 1) #these conversions are fucked, need to simplify
            year_prev = self.ps.year_sel

        self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"] = self.ps.db[year_prev][month_prev]["bs"].copy()

        status.msg.show(self, "Previous month copied") 

        #may need to call load month here

    #----------------------------------------------------------
    def add_bs_row(self):  
        #add row to balance sheet table
        try:
            self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"] = pd.concat(
                [self.ui.tableBS.model()._df,
                self.ps.bs_format],
                ignore_index=True
            )     

            # Show bs table - duplicated in load month below
            df = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"]
            model = TableModel(df)
            self.ui.tableBS.setModel(model)
            self.ui.tableBS.resizeColumnsToContents()   

            # Set column widths
            BSheader = self.ui.tableBS.horizontalHeader()
            BSheader.setSectionResizeMode(0, QHeaderView.Stretch)  #"item" column stretches 
            self.ui.tableBS.setColumnWidth(1, 140)                 #fixed width      

            status.msg.show(self, "Balance sheet row added")
        except:
            status.msg.show(self, "Error adding balance sheet row - ensure to load a month first", "red")
    #----------------------------------------------------------
    def save_bs_month(self):  
        #save bs table data for month
       
        self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"] = self.ui.tableBS.model()._df.copy()

        status.msg.show(self, "Balance sheet table saved")            
    #----------------------------------------------------------
    def db_init(self):
        #cycle through years and months, populate basic db structure with blank entries

        for year in self.ps.year_list:
            if year not in self.ps.db:
                self.ps.db[year] = {}
            for iM, month in enumerate(self.ps.month_list):
                if month not in self.ps.db[year]:
                    df = pd.DataFrame({
                        "Item":   ["New"],
                        "Amount": [0.00]})

                    self.ps.db[year][str(iM+1)] = {
                        "bs": df,      #balance sheet
                        "bs_met": {},  #balance sheet metrics                    
                        "ie": {},      #income + expense
                        "ie_met": {},  #income + expense metrics 
                        "ie_cat": {},  #income + expense categories                  
                        "notes": ""    #general notes
                        }   

                    #calculate metrics
                    utils.calc_metrics(self, year, str(iM+1))        
             
    #----------------------------------------------------------
    def load_month(self):

        #create blank entries in database if month does not exist - should be able to remove this later
        if self.ps.year_sel not in self.ps.db:
            self.ps.db[self.ps.year_sel] = {}
       
        if self.ps.month_sel not in self.ps.db[self.ps.year_sel]:
            df = pd.DataFrame({
                "Item":   ["New"],
                "Amount": [0.00]})

            self.ps.db[self.ps.year_sel][self.ps.month_sel] = {
                "bs": {},      #balance sheet
                "bs_met": df,  #balance sheet metrics                    
                "ie": {},      #income + expense
                "ie_met": {},  #income + expense metrics 
                "ie_cat": {},  #income + expense categories                  
                "notes": ""    #general notes
                }         

        #balance sheet setup
        if len(self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"]) > 0:
            # Show bs table
            df = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"]
            model = TableModel(df)
            self.ui.tableBS.setModel(model)
            self.ui.tableBS.resizeColumnsToContents()   

            # Set column widths
            BSheader = self.ui.tableBS.horizontalHeader()
            BSheader.setSectionResizeMode(0, QHeaderView.Stretch)  #"item" column stretches 
            self.ui.tableBS.setColumnWidth(1, 140)                 #fixed width         
        else:
            #clear table
            self.ui.tableBS.setModel(TableModel(pd.DataFrame()))

        #income + expense setup
        if len(self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"]) > 0:
            #set ui elements with existing data
            self.ui.textEdit.setPlainText(self.ps.db[self.ps.year_sel][self.ps.month_sel]["notes"])  
         
            # Show ie table
            first_key = list(self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"].keys())[0]
            df = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"][first_key]
            model = TableModel(df)
            self.ui.sheetTable.setModel(model)
            self.ui.sheetTable.resizeColumnsToContents()

            if "Type" in df.columns:
                col_idx = df.columns.get_loc("Type")
                delegate = ComboBoxDelegate(self.ps.income_expense_types, self.ui.sheetTable)
                self.ui.sheetTable.setItemDelegateForColumn(col_idx, delegate)    

            #clear dropdown
            self.ui.sheetDropdown.clear()
            # Add sheet(s) to dropdown
            self.ui.sheetDropdown.addItems(self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"].keys())
            self.ui.sheetDropdown.setCurrentIndex(0)
        else:
            #clear notes
            self.ui.textEdit.setPlainText("")
            #clear table
            self.ui.sheetTable.setModel(TableModel(pd.DataFrame()))
            #clear dropdown
            self.ui.sheetDropdown.clear()
             
        status.msg.show(self, f"{self.ui.comboBox_month.currentText()} {self.ps.year_sel} data loaded") 
    #----------------------------------------------------------
    def save_month(self):

        self.ps.db[self.ps.year_sel][self.ps.month_sel]["notes"] = self.ui.textEdit.toPlainText() 

        #calculate metrics
        utils.calc_metrics(self, self.ps.year_sel, self.ps.month_sel)

        #write out to file
        np.savez_compressed(os.path.join(self.ps.data_folder,"db.npz"), db=self.ps.db)

        status.msg.show(self, f"{self.ui.comboBox_month.currentText()} {self.ps.year_sel} data saved")  

        # msg = QMessageBox(QMessageBox.NoIcon, "Month Saved Successfully", "")
        # msg.setIcon(QMessageBox.Information)
        # msg.setText("Your changes have been saved")
        # msg.exec()   
    #----------------------------------------------------------
    def year_changed(self):
        self.ps.year_sel = self.ui.comboBox_year.currentText()
        self.ps.year_p1 = self.ui.comboBox_year_2.currentText()
        self.ps.year_p2 = self.ui.comboBox_year_3.currentText()          
    #----------------------------------------------------------
    def month_changed(self):
        self.ps.month_sel = str(self.ui.comboBox_month.currentIndex() + 1)
        self.ps.month_p1 = str(self.ui.comboBox_month_2.currentIndex() + 1)
        self.ps.month_p2 = str(self.ui.comboBox_month_3.currentIndex() + 1)  
    #----------------------------------------------------------
    def changed_csv(self):
        sheet = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"][self.ui.sheetDropdown.currentText()]
        self.ui.sheetTable.setModel(TableModel(sheet))                                 
    #----------------------------------------------------------
    def save_csv(self):
        if self.ui.sheetDropdown.count() > 0:
            sheet_name = self.ui.sheetDropdown.currentText()        
            self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"][sheet_name] = self.ui.sheetTable.model()._df.copy()

            # self.setCentralWidget(self.ui.graphBS1)

            status.msg.show(self, f"Sheet saved: {sheet_name}") 
    #----------------------------------------------------------
    def delete_csv(self):
        #delete entry from database
        if self.ui.sheetDropdown.count() > 0:
            sheet_name = self.ui.sheetDropdown.currentText()
            self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"].pop(sheet_name, None)

            #clear table
            self.ui.sheetTable.setModel(TableModel(pd.DataFrame()))

            #remove entry from dropdown  
            self.ui.sheetDropdown.removeItem(self.ui.sheetDropdown.currentIndex())  
 
            status.msg.show(self, f"Sheet deleted: {sheet_name}")              
    #----------------------------------------------------------
    def load_csv(self):
        # File dialog with CSV filter
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            self.ps.data_folder,
            "CSV Files (*.csv)"
        )

        if not file_path:
            return  # User cancelled
        
        # try:
        df = pd.read_csv(
            file_path, header=None, names=['Date', 'Amount', 'x', 'y','Description']
        )
        # remove unneeded columns then insert "type" column between Date and Amount
        df.drop(df.columns[[2,3]], axis=1, inplace=True)
        df.insert(2, "Type", "-")

        TB = status.prog(self)
        
        for i in range(len(df)):
            prog_value = int(100*(i+1)/len(df))
            status.prog.update_val(TB, self, "Processing expenses", prog_value)

            # assign initial categorizations of items using ollama
            if df['Amount'][i] > 0:
                response = ollama.chat(model='gemma3:4b', messages=[{
                    'role': 'user',
                    'content': f"Return only one category from this list that best matches the expense. Return only the category itself. List: {', '.join(self.ps.income_types)}\n\nDescription: {df['Description'][i]}\n\nCategory:"
                }])
            else:
                response = ollama.chat(model='gemma3:4b', messages=[{
                    'role': 'user',
                    'content': f"Return only one category from this list that best matches the expense. Return only the category itself. List: {', '.join(self.ps.expense_types)}\n\nDescription: {df['Description'][i]}\n\nCategory:"
                }])

            response_isolated = response['message']['content'].strip() 

            if response_isolated in self.ps.expense_types:
                df['Type'].loc[i] = response_isolated                                   

        status.prog.close(TB, self)      

        # Show in table
        model = TableModel(df)
        self.ui.sheetTable.setModel(model)
        self.ui.sheetTable.resizeColumnsToContents()

        if "Type" in df.columns:
            col_idx = df.columns.get_loc("Type")
            delegate = ComboBoxDelegate(self.ps.income_expense_types, self.ui.sheetTable)
            self.ui.sheetTable.setItemDelegateForColumn(col_idx, delegate)     

        # Add sheet to dropdown
        self.ui.sheetDropdown.addItem(Path(file_path).stem)
        self.ui.sheetDropdown.setCurrentIndex(self.ui.sheetDropdown.count() - 1)

        #auto save sheet to database
        self.save_csv()

        # except Exception as e:
        #     QMessageBox.critical(self, "Error Loading CSV", str(e))  
    #----------------------------------------------------------
    def refresh_plots(self):   
        #check that the time range selected on the dropdowns is valid - end date must be after start date
        if (self.ui.comboBox_year_3.currentIndex() < self.ui.comboBox_year_2.currentIndex()):
            status.msg.show(self, "Specified time range for plotting is invalid", "red") 
        elif (self.ui.comboBox_year_3.currentIndex() == self.ui.comboBox_year_2.currentIndex()) and (self.ui.comboBox_month_3.currentIndex() < self.ui.comboBox_month_2.currentIndex()):             
            status.msg.show(self, "Specified time range for plotting is invalid", "red")        
        else:
            plotting.refresh(self)           
            status.msg.show(self, "Plots refreshed")      
    #----------------------------------------------------------
    def change_plot_focus(self, event): 
        #unused       
        if event.double():
            if self.isFullScreen():
                # self.showNormal()
                self.ui.tabWidget.setCentralWidget(self.ui.graphBS1)
            else:
                # self.showFullScreen()  # True full screen (no title bar)
                # Or self.showMaximized() for maximized window
                pass

    #----------------------------------------------------------

class TableModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame()):
        super().__init__()
        self._df = df.copy()

    def rowCount(self, parent=QModelIndex()): return len(self._df)
    def columnCount(self, parent=QModelIndex()): return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid(): return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self._df.iat[index.row(), index.column()]
            return "" if pd.isna(value) else str(value)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            if self._df.keys()[index.column()] == "Amount":
                try: #convert entry to float if its an amount for either table
                    self._df.iat[index.row(), index.column()] = float(value)
                except: #make value zero if number wasnt entered
                    self._df.iat[index.row(), index.column()] = float(0.00)  
                    status.msg.show(self, "Invalid amount entered in cell, set to 0.00 instead", "yellow")                                       
            else:
                self._df.iat[index.row(), index.column()] = value                
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole: return None
        if orientation == Qt.Horizontal:
            return str(self._df.columns[section])
        return str(self._df.index[section])

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options  # list of strings, e.g. ["Red", "Green", "Blue"]

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.options)
        combo.setEditable(False)  # optional: prevent typing
        return combo

    def setEditorData(self, editor: QComboBox, index):
        value = index.model().data(index, Qt.EditRole)
        if value:
            editor.setCurrentText(str(value))

    def setModelData(self, editor: QComboBox, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #set app properties
    #allow app icon to show properly on windows taskbar
    if sys.platform.startswith("win"):
        myappid = "finance.tracker"  #arbitrary name
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass      

    app.setWindowIcon(QIcon("assets/finance_mode_24dp_75FB4C_FILL0_wght400_GRAD0_opsz24.ico"))
    # app.setStyle("Fusion")

    window = MainWindow()
    window.setFixedSize(1540, 800)
    # window.setWindowIcon(QIcon("assets/finance_mode_24dp_75FB4C_FILL0_wght400_GRAD0_opsz24.ico"))  # optional: also set per window
    window.show()
    sys.exit(app.exec())