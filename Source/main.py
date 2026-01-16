#Built in modules
import sys
import os
from pathlib import Path
import ctypes

#Installed modules
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
from PySide6.QtGui import QIcon, QAction
from ui.mainwindow import Ui_OrionsApp
import PySide6
import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock
import pandas as pd
import numpy as np
import ollama 

#Project modules, functions
from utils.ui_models import TableModel, ComboBoxDelegate
from utils import plotting, status, calc_metrics

#COMPILATION CMD:
# pyside6-uic mainwindow.ui -o mainwindow.py

class Properties:
    def __init__(self):
        self.APP_NAME = "Finance Tracker"          
        self.APP_VERSION = "1.0"   
        self.root_dir = "" #root directory of repo or installed location
        self.working_dir = "C:\\" #directory for user data
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
        self.year_list = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"] #make editable through ui later
        self.month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] #make editable through ui later
        self.year_sel = "2025"
        self.month_sel = "12"
        self.year_p1 = "2024"
        self.month_p1 = "12"
        self.year_p2 = "2025"
        self.month_p2 = "12"
        self.active_plot = ""    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_OrionsApp()
        self.ui.setupUi(self)        

        #-------------------STARTUP TASKS-------------------

        #Import properties
        self.ps = Properties()

        #set root directory
        if getattr(sys, 'frozen', False): #if running EXE, find installed directory
            self.ps.root_dir = os.path.dirname(sys.executable)
        else: #if running source, find repo directory
            self.ps.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        #set working directory to program directory
        os.chdir(self.ps.root_dir)  

        #initialize database with blank template
        MainWindow.db_init(self)

        try: 
            #load working dir from settings file if present
            self.ps.working_dir = np.load(os.path.join(self.ps.root_dir,"resources\\settings.npz"), allow_pickle=True)["working_dir"].item() 
            #load db file from working directory if present, to overwrite blank template
            self.ps.db = np.load(os.path.join(self.ps.working_dir,"db.npz"), allow_pickle=True)["db"].item()
        except:
            QMessageBox.warning(
                self,
                "Database Warning",
                f'Could not find the database file "db.npz" in the working directory: {self.ps.working_dir} \n\Initialized a new blank database. If you have an existing database, please set the working directory to its location and restart the program.'
            )

        #Set initial component properties
        self.setWindowTitle(f"{self.ps.APP_NAME} {self.ps.APP_VERSION}")

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
        self.ui.spinBox_month.setValue(-1*self.ui.comboBox_month.currentIndex()) #needs to match the index (*-1) of the combo box above       
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
        # self.ui.tableBS.setShowGrid(False)        
        # self.ui.sheetTable.setShowGrid(False)     

        self.ui.actionOpen.setIcon(QIcon(os.path.join(self.ps.root_dir,"assets\\folder_managed_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg")))
        self.ui.actionAbout.setIcon(QIcon(os.path.join(self.ps.root_dir,"assets\\info_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg")))

        #toolbar setup
        self.ui.toolBar.setMovable(False)
        self.ui.toolBar.setFloatable(False)
        self.ui.toolBar.setIconSize(PySide6.QtCore.QSize(22, 22))

        # self.ui.toolBar.addSeparator()
        self.add_toolbar_space(405)

        self.ui.act_data_cursor = QAction(QIcon(os.path.join(self.ps.root_dir,"assets\\add_2_24dp_B7B7B7_FILL0_wght400_GRAD0_opsz24.svg")), "Data Cursor (Ctrl+D)", self)
        self.ui.act_data_cursor.setShortcut("Ctrl+D")
        self.ui.act_data_cursor.setCheckable(True)
        self.ui.act_data_cursor.setChecked(False)
        self.ui.toolBar.addAction(self.ui.act_data_cursor)
        self.ui.act_data_cursor.toggled.connect(self.data_cursor_switch)

        #Add figure docks
        self.ui.dock_BS1 = Dock("Balances vs. Time", autoOrientation=False)
        self.ui.dock_BS2 = Dock("Totals vs. Time", autoOrientation=False)
        self.ui.dock_BS3 = Dock("Asset Breakdown", autoOrientation=False)        

        self.ui.graphBS1 = pg.PlotWidget()
        self.ui.graphBS2 = pg.PlotWidget()
        self.ui.graphBS3 = pg.PlotWidget() 

        self.ui.graphBS1.setXLink(self.ui.graphBS2) 

        self.ui.dock_BS1.addWidget(self.ui.graphBS1) 
        self.ui.dock_BS2.addWidget(self.ui.graphBS2)
        self.ui.dock_BS3.addWidget(self.ui.graphBS3)        

        self.ui.BS_area.addDock(self.ui.dock_BS1, 'top')
        self.ui.BS_area.addDock(self.ui.dock_BS2, 'bottom')
        self.ui.BS_area.addDock(self.ui.dock_BS3, 'right')  

        self.ui.dock_IE1 = Dock("Income and Expense vs. Time", autoOrientation=False)
        self.ui.dock_IE2 = Dock("Totals vs. Time", autoOrientation=False)
        self.ui.dock_IE3 = Dock("Expense Breakdown", autoOrientation=False)  

        self.ui.graphIE1 = pg.PlotWidget()
        self.ui.graphIE2 = pg.PlotWidget()
        self.ui.graphIE3 = pg.PlotWidget()  

        self.ui.graphIE1.setXLink(self.ui.graphIE2)         

        self.ui.dock_IE1.addWidget(self.ui.graphIE1) 
        self.ui.dock_IE2.addWidget(self.ui.graphIE2)
        self.ui.dock_IE3.addWidget(self.ui.graphIE3)               

        self.ui.IE_area.addDock(self.ui.dock_IE1, 'top')
        self.ui.IE_area.addDock(self.ui.dock_IE2, 'bottom')
        self.ui.IE_area.addDock(self.ui.dock_IE3, 'right')   

        pg.setConfigOptions(
            antialias=True,
            useOpenGL=False,
            )  
        
        plotting.init(self)             

        #all this plot logic following should be put in a subfunction and called for each plot to not duplicate

        #label for data cursor
        self.ui.graphBS1_label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )      
        self.ui.graphBS2_label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )  
        self.ui.graphBS3_label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )  
        self.ui.graphIE1_label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )   
        self.ui.graphIE2_label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )    
        self.ui.graphIE3_label = pg.TextItem(
            text="",
            color=(255, 255, 255),
            anchor=(0, 1),          # top-left corner of text
            border=pg.mkPen('yellow', width=1),
            fill=(0, 0, 0, 180)     # semi-transparent black background
        )  
        self.ui.graphBS1.addItem(self.ui.graphBS1_label, ignoreBounds=True)
        self.ui.graphBS2.addItem(self.ui.graphBS2_label, ignoreBounds=True)
        self.ui.graphBS3.addItem(self.ui.graphBS3_label, ignoreBounds=True)
        self.ui.graphIE1.addItem(self.ui.graphIE1_label, ignoreBounds=True)
        self.ui.graphIE2.addItem(self.ui.graphIE2_label, ignoreBounds=True)
        self.ui.graphIE3.addItem(self.ui.graphIE3_label, ignoreBounds=True)

        # === Plot Mouse tracking ===
        self.proxyBS1 = pg.SignalProxy(
            self.ui.graphBS1.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=lambda evt: self.data_cursor_moved(evt, self.ui.graphBS1, self.ui.graphBS1_label)
        )  
        self.proxyBS2 = pg.SignalProxy(
            self.ui.graphBS2.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=lambda evt: self.data_cursor_moved(evt, self.ui.graphBS2, self.ui.graphBS2_label)
        )    
        self.proxyBS3 = pg.SignalProxy(
            self.ui.graphBS3.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=lambda evt: self.data_cursor_moved(evt, self.ui.graphBS3, self.ui.graphBS3_label)
        ) 
        self.proxyIE1 = pg.SignalProxy(
            self.ui.graphIE1.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=lambda evt: self.data_cursor_moved(evt, self.ui.graphIE1, self.ui.graphIE1_label)
        )   
        self.proxyIE2 = pg.SignalProxy(
            self.ui.graphIE2.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=lambda evt: self.data_cursor_moved(evt, self.ui.graphIE2, self.ui.graphIE2_label)
        )   
        self.proxyIE3 = pg.SignalProxy(
            self.ui.graphIE3.scene().sigMouseMoved,
            rateLimit=60,           # max 60 updates/sec — smooth but not CPU killer
            slot=lambda evt: self.data_cursor_moved(evt, self.ui.graphIE3, self.ui.graphIE3_label)
        )      

        #Callbacks
        MainWindow.data_cursor_switch(self)
        MainWindow.year_changed(self)
        MainWindow.month_changed(self)       

        #Connections
        self.ui.actionOpen.triggered.connect(self.pick_folder)
        self.ui.actionAbout.triggered.connect(self.show_info)
        self.ui.sheetLoad.clicked.connect(self.load_csv)
        self.ui.sheetDelete.clicked.connect(self.delete_csv)   
        self.ui.sheetDropdown.currentIndexChanged.connect(self.changed_csv)     
        self.ui.pushButton_refresh.clicked.connect(self.refresh_plots)    
        self.ui.pushButton_loadmonth.clicked.connect(self.load_month)            
        self.ui.pushButton_savemonth.clicked.connect(self.save_month)
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.ui.tabWidget_2.currentChanged.connect(self.on_tab_changed_2)
        self.ui.comboBox_month.currentIndexChanged.connect(self.month_changed)
        self.ui.spinBox_month.valueChanged.connect(self.month_spinbox_changed)        
        self.ui.comboBox_month_2.currentIndexChanged.connect(self.month_changed)    
        self.ui.comboBox_month_3.currentIndexChanged.connect(self.month_changed)
        self.ui.comboBox_year.currentIndexChanged.connect(self.year_changed)
        self.ui.comboBox_year_2.currentIndexChanged.connect(self.year_changed)      
        self.ui.comboBox_year_3.currentIndexChanged.connect(self.year_changed)
        self.ui.pushButton_add_row.clicked.connect(self.add_bs_row)
        self.ui.pushButton_del_row.clicked.connect(self.delete_bs_row)        
        self.ui.pushButton_copy_previous.clicked.connect(self.bs_copy_previous)        

    #----------------------------------------------------------
    def pick_folder(self):
        #open file dialog to select working directory

        try:
            folder = QFileDialog.getExistingDirectory(
                parent=self,                                   
                caption="Choose a folder",                     
                dir=self.ps.working_dir                                      
            )
        except: #fall back on C drive root if dir not valid
            folder = QFileDialog.getExistingDirectory(
                parent=self,                                   
                caption="Choose a folder",                     
                dir="C:\\"                                      
            )

        if folder: # user clicked OK (not Cancel)
            self.ps.working_dir = folder 

            #write out to settings file
            np.savez_compressed(os.path.join(self.ps.root_dir,"resources\\settings.npz"), working_dir=self.ps.working_dir)

            status.msg.show(self, f"Workspace directory set: {folder}")                           
    #----------------------------------------------------------
    def show_info(self):
        QMessageBox.information(
            self,
            "About",
            f"Finance Tracker\nVersion: {self.ps.APP_VERSION}\n\nContact: orion.miller@outlook.com"
        )
    #----------------------------------------------------------
    def add_toolbar_space(self, width: int):
        spacer = QWidget()
        spacer.setFixedWidth(width)
        self.ui.toolBar.addWidget(spacer)
    #----------------------------------------------------------
    def data_cursor_switch(self):
        if self.ui.act_data_cursor.isChecked():
            self.ui.BS_area.setCursor(Qt.CursorShape.CrossCursor)   
            self.ui.IE_area.setCursor(Qt.CursorShape.CrossCursor) 
        else:
            self.ui.BS_area.setCursor(Qt.CursorShape.ArrowCursor)   
            self.ui.IE_area.setCursor(Qt.CursorShape.ArrowCursor) 
            self.ui.graphBS1_label.hide()
            self.ui.graphBS2_label.hide()
            self.ui.graphBS3_label.hide()
            self.ui.graphIE1_label.hide()
            self.ui.graphIE2_label.hide()
            self.ui.graphIE3_label.hide()            
    #----------------------------------------------------------
    def data_cursor_moved(self, event, fig, label):

        if not self.ui.act_data_cursor.isChecked():
            return  # Exit if data cursor is not active

        pos = event[0]  # position in scene coordinates

        if str(fig) != self.ps.active_plot: #check if active plot has changed since last call            
            #hide all labels and then show only for active plot
            self.ui.graphBS1_label.hide()
            self.ui.graphBS2_label.hide()
            self.ui.graphBS3_label.hide()
            self.ui.graphIE1_label.hide()
            self.ui.graphIE2_label.hide()
            self.ui.graphIE3_label.hide()
            label.show()

            self.ps.active_plot = str(fig)                 

        # Check if mouse is inside plot area
        if fig.sceneBoundingRect().contains(pos):
            mouse_point = fig.plotItem.vb.mapSceneToView(pos)
            x, y = mouse_point.x(), mouse_point.y()

            # Update coordinate label (positioned slightly above & right of cursor)
            label.setText(f"y: {y:.2f}")
            # label.setText(f"x: {x:.2f}\ny: {y:.3f}")            
            label.setPos(x, y)  # small offset — adjust as needed
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

        #balance sheet setup - copied from load_month
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

        status.msg.show(self, "Previous month copied") 
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
            status.msg.show(self, "Error adding balance sheet row - ensure to load a month first", "yellow")
    #----------------------------------------------------------
    def delete_bs_row(self):  
        #delete row from balance sheet table - supports multiselect
        row = []
        try:
            for i, item in enumerate(self.ui.tableBS.selectionModel().selectedIndexes()):
                row.append(item.row())

            row = np.unique(row)  #get unique row indices only

            #drop rows from bs dataframe
            self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"] = self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"].drop(index=row).reset_index(drop=True)

            # Show bs table - duplicated in load month below
            model = TableModel(self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"])
            self.ui.tableBS.setModel(model)
            self.ui.tableBS.resizeColumnsToContents()   

            # Set column widths
            BSheader = self.ui.tableBS.horizontalHeader()
            BSheader.setSectionResizeMode(0, QHeaderView.Stretch)  #"item" column stretches 
            self.ui.tableBS.setColumnWidth(1, 140)                 #fixed width                  

            status.msg.show(self, "Balance sheet row(s) deleted")
        except:
            status.msg.show(self, "Error deleting balance sheet row(s) - ensure a table cell is selected", "yellow")                    
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
                    calc_metrics(self, year, str(iM+1))        
             
    #----------------------------------------------------------
    def load_month(self):
        #load all data for selected year and month from database and sync to UI components

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

        #set ui elements with existing data
        #notes setup
        try:           
            self.ui.textEdit.setPlainText(self.ps.db[self.ps.year_sel][self.ps.month_sel]["notes"])  
        except:
            #clear notes
            self.ui.textEdit.setPlainText("")

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
            #clear table
            self.ui.sheetTable.setModel(TableModel(pd.DataFrame()))
            #clear dropdown
            self.ui.sheetDropdown.clear()
             
        status.msg.show(self, f"{self.ui.comboBox_month.currentText()} {self.ps.year_sel} data loaded") 
    #----------------------------------------------------------
    def save_month(self):
        #save all data for the month to the database
        #need to remember not to change between sheets without saving in order to capture table changes

        #save notes
        self.ps.db[self.ps.year_sel][self.ps.month_sel]["notes"] = self.ui.textEdit.toPlainText() 

        #save balance sheet
        self.ps.db[self.ps.year_sel][self.ps.month_sel]["bs"] = self.ui.tableBS.model()._df.copy()

        #save income + expense sheet
        if self.ui.sheetDropdown.count() > 0:
            sheet_name = self.ui.sheetDropdown.currentText()        
            self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"][sheet_name] = self.ui.sheetTable.model()._df.copy()          

        #calculate metrics
        calc_metrics(self, self.ps.year_sel, self.ps.month_sel)

        #write out to file
        np.savez_compressed(os.path.join(self.ps.working_dir,"db.npz"), db=self.ps.db)

        status.msg.show(self, f"{self.ui.comboBox_month.currentText()} {self.ps.year_sel} data saved")  
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

        self.ui.spinBox_month.setValue(-1*self.ui.comboBox_month.currentIndex()) #needs to match the index (*-1) of the combo box above 
    #----------------------------------------------------------
    def month_spinbox_changed(self):
        self.ui.comboBox_month.setCurrentIndex(-1*self.ui.spinBox_month.value())

        self.ps.month_sel = str(self.ui.comboBox_month.currentIndex() + 1)        
    #----------------------------------------------------------    
    def changed_csv(self):
        if self.ui.sheetDropdown.count() > 0:
            sheet = self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"][self.ui.sheetDropdown.currentText()]
            self.ui.sheetTable.setModel(TableModel(sheet))                                 
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
            self.ps.working_dir,
            "CSV Files (*.csv)"
        )

        if not file_path:
            return  # User cancelled
        
        try:
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
            self.save_month()

        except Exception as e:
            QMessageBox.critical(self, "Error Loading CSV", str(e))  
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

    #import items from subfolders - if running from source need to go up one dir 
    if getattr(sys, 'frozen', False): #if running EXE
        app.setWindowIcon(QIcon("assets/finance_mode_24dp_75FB4C_FILL0_wght400_GRAD0_opsz24.svg"))
        #import stylesheet and apply
        with open("resources/mainstyle.qss", "r") as f:
            _style = f.read()
    else: #if running source
        app.setWindowIcon(QIcon("../assets/finance_mode_24dp_75FB4C_FILL0_wght400_GRAD0_opsz24.svg"))
        #import stylesheet and apply
        with open("../resources/mainstyle.qss", "r") as f:
            _style = f.read()

    app.setStyleSheet(_style)    
    app.setStyle("windows11")

    window = MainWindow() 
    window.setFixedSize(window.width(), window.height())        
    window.show()
    sys.exit(app.exec())