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

#other modules
import pandas as pd
import numpy as np
import ollama 

#external fcns
import plotting
import utils
import status
from win_tb import WinTB

#COMPILATION CMD:
# pyside6-uic mainwindow.ui -o mainwindow.py

class Properties:
    def __init__(self):
        self.APP_VERSION = "1.0"
        self.data_folder = "D:\\!Orion_Documents\\Financial\\!OM_Finance_Tracker" # None
        self.income_types = ["Work", "Investment", "Sales", "Rewards"]
        self.expense_types = ["Transfer", "Bills", "Groceries","Takeout","Car","Travel","Entertainment","Other"]
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
        self.year_list = ["2020", "2021", "2022", "2023", "2024", "2025"]
        self.month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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

        plotting.init(self)

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
        self.ui.pushButton_saveBS.clicked.connect(self.save_bs_month)

    #----------------------------------------------------------
    def config_status_prog(self, action: str):
        #configures status bar to show progress bar and message

        if action == 'construct':
            # Create progress bar, add it to the status bar
            self.ui.progress = QProgressBar()
            self.ui.progress.setMaximumWidth(75)  
            self.ui.progress.setAlignment(Qt.AlignCenter)    
            self.ui.progress.setRange(0, 100)         
            self.ui.statusbar.addWidget(self.ui.progress)  

            # Create a permanent label inside the status bar (invisible at first)
            self.ui.status_label = QLabel("")
            self.ui.status_label.setMinimumWidth(400)   
            self.ui.statusbar.addWidget(self.ui.status_label)                   

            #extra spacer to push prior items to left
            self.ui.status_spacer = QWidget()    
            self.ui.statusbar.addWidget(self.ui.status_spacer, stretch=1) 

        elif action == 'destruct':
            # Remove progress bar and label from status bar
            self.ui.statusbar.removeWidget(self.ui.progress)
            self.ui.statusbar.removeWidget(self.ui.status_label)
            self.ui.statusbar.removeWidget(self.ui.status_spacer)

            # Delete references
            # del self.ui.progress
            # del self.ui.status_label
            # del self.ui.status_spacer

    #----------------------------------------------------------
    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            parent=self,                                   # your MainWindow or widget
            caption="Choose a folder",                     # title bar text
            dir=self.ps.data_folder                                      
        )

        if folder:                                         # user clicked OK (not Cancel)
            self.ps.data_folder = folder 
            self.show_fading_message(f"Workspace directory set: {folder}")                           
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

            self.show_fading_message("Balance sheet row added") 
        except:
            self.show_fading_message("Error adding balance sheet row - ensure to load a month first")
    #----------------------------------------------------------
    def save_bs_month(self):  
        #save bs table data for month
       
        self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"] = self.ui.tableBS.model()._df.copy()

        self.show_fading_message("Balance sheet table saved")     
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
                delegate = ComboBoxDelegate(self.ps.expense_types, self.ui.sheetTable)
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

        self.show_fading_message(f"{self.ps.month_sel} {self.ps.year_sel} data loaded")             

    #----------------------------------------------------------
    def save_month(self):

        self.ps.db[self.ps.year_sel][self.ps.month_sel]["notes"] = self.ui.textEdit.toPlainText() 

        #calculate metrics
        utils.calc_metrics(self, self.ps.year_sel, self.ps.month_sel)

        #write out to file
        np.savez_compressed(os.path.join(self.ps.data_folder,"db.npz"), db=self.ps.db)

        self.show_fading_message(f"{self.ps.month_sel} {self.ps.year_sel} data saved")  

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

            self.show_fading_message("Sheet saved: {sheet_name}")  
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

            self.show_fading_message("Sheet deleted: {sheet_name}")               
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

        self.config_status_prog('construct') #create progress elements in status bar
        tb = WinTB(self.winId())              
        WinTB.set_state(tb, "normal")
        
        for i in range(len(df)):
            prog_value = int(100*(i+1)/len(df))
            self.ui.progress.setValue(prog_value)
            self.ui.status_label.setText("Processing expenses")  
            WinTB.set_val(tb, prog_value) 

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

        self.config_status_prog('destruct') #remove progress elements in status bar
        WinTB.set_state(tb, "normal")        

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
        if (self.ui.comboBox_year_3.currentIndex() > self.ui.comboBox_year_2.currentIndex()):
            self.show_fading_message("Specified time range for plotting is invalid")    
            #should add to this to account for months within the same year being misaligned         
        else:
            plotting.refresh(self)      
            self.show_fading_message("Plots refreshed")           
    #----------------------------------------------------------
    def show_fading_message(self, text, duration=4000):
        """Show message and then fade it out"""

        # Cancel any running animation first
        if hasattr(self, "_fade_anim"):
            self._fade_anim.stop()
            self.clear_fading_components()

        #Create components
        # Create a label inside the status bar
        self.ui.status_label = QLabel("")
        self.ui.status_label.setMinimumWidth(400)   
        self.ui.statusbar.addWidget(self.ui.status_label)                   

        #extra spacer to push prior items to left
        self.ui.status_spacer = QWidget()    
        self.ui.statusbar.addWidget(self.ui.status_spacer, stretch=1)             

        # Fade in instantly, stay, then fade out
        self.effect = QGraphicsOpacityEffect()     
        self.ui.status_label.setGraphicsEffect(self.effect)

        self._fade_anim = QPropertyAnimation(self.ui.status_label.graphicsEffect(), b"opacity")
        self._fade_anim.setDuration(duration)
        self._fade_anim.setEasingCurve(QEasingCurve.InCubic)        
        self._fade_anim.setStartValue(1)          
        self._fade_anim.setEndValue(0)        

        #Create fading text
        self.ui.status_label.setText(text)        
        self._fade_anim.start()    

        self._fade_anim.finished.connect(lambda: self.clear_fading_components())

    def clear_fading_components(self):
        # Remove progress bar and label from status bar
        self.ui.statusbar.removeWidget(self.ui.status_label)
        self.ui.statusbar.removeWidget(self.ui.status_spacer)

        # Delete references
        # del self.ui.status_label
        # del self.ui.status_spacer

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
                    # MainWindow.show_fading_message("Invalid amount entered in cell, set to 0.00 instead")                  
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