import sys
import os
from pathlib import Path
import ctypes

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox,
    QStyledItemDelegate, QComboBox, QProgressBar, QGraphicsOpacityEffect,
    QStatusBar, QLabel
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

import pandas as pd
import numpy as np
import ollama

#COMPILATION CMD:
# pyside6-uic mainwindow.ui -o mainwindow.py

class Properties:
    def __init__(self):
        self.APP_VERSION = "1.0"
        self.data_folder = "D:\\!Orion_Documents\\Financial\\!OM_Finance_Tracker" # None
        self.income_types = ["-", "Job", "Investment", "Other"]
        # self.expense_types = ["-", "Bills", "Groceries","Takeout","Car","Travel","Other"]
        self.expense_types = ["Transfer", "Bills", "Groceries","Takeout","Car","Travel","Entertainment","Other"]
        self.db = {
            "2025": {
                "12": {
                    "bs": {},
                    "ie":  {},
                    "notes": ""
                }           
        }   
        }
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

        #Properties
        self.ps = Properties()
        try:
            self.ps.db = np.load(os.path.join(self.ps.data_folder,"db.npz"), allow_pickle=True)["db"].item()
        except:
            pass

        #Startup tasks
        self.setWindowTitle(f"Finance Tracker {self.ps.APP_VERSION}")

        self.ui.tabWidget.setTabText(0, "Balance Sheet")
        self.ui.tabWidget.setTabText(1, "Income + Expense")    
        self.ui.tabWidget_2.setTabText(0, "Balance Sheet")
        self.ui.tabWidget_2.setTabText(1, "Income + Expense")        

        self.ui.sheetTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.ui.comboBox_year.addItems(["2020", "2021", "2022", "2023", "2024", "2025"])        
        self.ui.comboBox_month.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        # self.ui.comboBox_month.setItemData(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)        
        self.ui.comboBox_year.setCurrentText("2025")
        self.ui.comboBox_month.setCurrentText("Dec")
        self.ui.comboBox_year_2.addItems(["2020", "2021", "2022", "2023", "2024", "2025"])        
        self.ui.comboBox_month_2.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        # self.ui.comboBox_month_2.setItemData(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)          
        self.ui.comboBox_year_2.setCurrentText("2025")
        self.ui.comboBox_month_2.setCurrentText("Dec")
        self.ui.comboBox_year_3.addItems(["2020", "2021", "2022", "2023", "2024", "2025"])        
        self.ui.comboBox_month_3.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        # self.ui.comboBox_month_3.setItemData(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)          
        self.ui.comboBox_year_3.setCurrentText("2025")
        self.ui.comboBox_month_3.setCurrentText("Dec")                
        # self.ui.statusbar.sizeGripEnabled = False
        # self.statusBar.sizeGripEnabled = False

        # Create progress bar, add it to the status bar
        self.ui.progress = QProgressBar()
        self.ui.progress.setMaximumWidth(150)      
        self.ui.progress.setTextVisible(True)     
        self.ui.progress.setVisible(False) # hide until needed 
        self.ui.progress.setRange(0, 100)
        # self.ui.statusbar().addPermanentWidget(self.ui.progress)      
        self.statusBar().addPermanentWidget(self.ui.progress)  

        # Create a permanent label inside the status bar (invisible at first)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: white; background: rgba(0,0,0,180); padding: 4px 10px; border-radius: 4px;")
        self.statusBar().addPermanentWidget(self.status_label)
        self.status_label.hide()         

        #Connections
        self.ui.actionOpen.triggered.connect(self.pick_folder)
        self.ui.actionAbout.triggered.connect(self.show_info)
        self.ui.sheetLoad.clicked.connect(self.load_csv)
        self.ui.sheetSave.clicked.connect(self.save_csv)
        self.ui.pushButton_refresh.clicked.connect(self.setup_bar_graph)        
        self.ui.pushButton_savemonth.clicked.connect(self.save_month)
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.ui.tabWidget_2.currentChanged.connect(self.on_tab_changed_2)
        # self.ui.saveMonth.clicked.connect(self.save_month)

    #----------------------------------------------------------
    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            parent=self,                                   # your MainWindow or widget
            caption="Choose a folder"                    # title bar text
        )

        if folder:                                         # user clicked OK (not Cancel)
            self.ps.data_folder = folder 
            self.statusBar().showMessage(f"Set Workspace Directory: {folder}", 5000)          
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
    def load_month(self):

        #create blank entries in database if month does not exist
        if self.ps.year_sel not in self.ps.db:
            self.db[self.ps.year_sel] = {}
       
        if self.ps.month_sel not in self.ps.db[self.ps.year_sel]:
            self.db[self.ps.year_sel][self.ps.month_sel] = {
                "bs": {},
                "ie":  {},
                "notes": ""  
                }
        else:
            pass #populate ui components with existing data
             
    #----------------------------------------------------------
    def save_month(self):

        self.ps.db[self.ps.year_sel][self.ps.month_sel]["notes"] = self.ui.textEdit.toPlainText() 

        #write out to file
        np.savez_compressed(os.path.join(self.ps.data_folder,"db.npz"), db=self.ps.db)

        msg = QMessageBox(QMessageBox.NoIcon, "Month Saved Successfully", "")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Your changes have been saved")
        msg.exec()             
    #----------------------------------------------------------
    def save_csv(self):
        self.ps.db[self.ps.year_sel][self.ps.month_sel]["ie"][self.ui.sheetDropdown.currentText()] = self.ui.sheetTable.model()._df.copy()

        self.statusBar().showMessage("Saved sheet", 5000) 
        # self.show_temporary_message("Sheet saved", 2500)  
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
        try:
            df = pd.read_csv(
                file_path, header=None, names=['Date', 'Amount', 'x', 'y','Description']
            )
            # remove unneeded columns then insert "type" column between Date and Amount
            df.drop(df.columns[[2,3]], axis=1, inplace=True)
            df.insert(2, "Type", "-")

            self.ui.progress.setVisible(True) 
         
            for i in range(len(df)):
                prog_value = 100*(i+1)/len(df)
                self.ui.progress.setValue(prog_value)
                # self.ui.progress.text = f"Reading sheet: {prog_value:.0f}%"               
                # assign initial categorizations of items using ollama
                response = ollama.chat(model='gemma3:4b', messages=[{
                    'role': 'user',
                    'content': f"Return only one category from this list that best matches the expense. Return only the category itself. List: {', '.join(self.ps.expense_types)}\n\nDescription: {df['Description'][i]}\n\nCategory:"
                }])
                response_isolated = response['message']['content'].strip() 

                if response_isolated in self.ps.expense_types:
                    df['Type'][i] = response_isolated                                   

            self.ui.progress.setVisible(False)

            # Show in table
            model = TableModel(df)
            self.ui.sheetTable.setModel(model)
            self.ui.sheetTable.resizeColumnsToContents()

            if "Type" in df.columns:
                col_idx = df.columns.get_loc("Type")
                delegate = ComboBoxDelegate(self.ps.expense_types, self.ui.sheetTable)
                self.ui.sheetTable.setItemDelegateForColumn(col_idx, delegate)     

            # Add sheet to dropdown
            self.ui.sheetDropdown.addItem(Path(file_path).stem)

        except Exception as e:
            QMessageBox.critical(self, "Error Loading CSV", str(e))  
    #----------------------------------------------------------
    def setup_bar_graph(self):
            # This is the widget you promoted in Designer!
            # plot = self.ui.findChild(pg.PlotWidget, "PlotWidget")  # or whatever ObjectName you gave it
            plot = self.ui.graphIE3         
            # If you didn't set an objectName, use: plot = self.ui.your_placeholder_widget_name

            # Optional styling
            # plot.setBackground('b')
            plot.showGrid(x=True, y=True)
            plot.setTitle("Expense Breakdown", size='14pt')
            plot.setLabel('left', 'Amount (USD)')
            plot.setLabel('bottom', 'Category')

            # Data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            values = [120, 190, 150, 230, 210, 280]

            x = np.arange(len(months))
            bars = pg.BarGraphItem(x=x, height=values, width=0.6, brush='#0066cc', pen='k')
            plot.addItem(bars)

            # Custom x-axis labels
            ax = plot.getAxis('bottom')
            ax.setTicks([[(i, month) for i, month in enumerate(months)]])

            plot.setXRange(-0.6, len(months) - 0.4) 
    #----------------------------------------------------------
    def show_temporary_message(self, text, duration=3000, fade_ms=600):
        """Show message for `duration` ms and then fade it out over `fade_ms` ms"""
        self.status_label.setText(text)
        self.status_label.adjustSize()
        self.status_label.show()

        # Cancel any running animation first
        if hasattr(self, "_fade_anim"):
            self._fade_anim.stop()

        # Fade in instantly, stay, then fade out
        self.status_label.setGraphicsEffect(None)
        opacity = QGraphicsOpacityEffect(self.status_label)
        self.status_label.setGraphicsEffect(opacity)

        self._fade_anim = QPropertyAnimation(opacity, b"opacity")
        self._fade_anim.setDuration(duration + fade_ms)
        self._fade_anim.setEasingCurve(QEasingCurve.Linear)

        # 1.0 → 1.0 (stay) → 0.0 (fade out)
        self._fade_anim.setKeyValues([(0, 1.0),
                                      (duration, 1.0),
                                      (duration + fade_ms, 0.0)])

        self._fade_anim.finished.connect(self.status_label.hide)
        self._fade_anim.start()            

    
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
    if sys.platform.startswith("win"):
        myappid = "finance.tracker"  # Change to something unique for your app
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass  # Fails gracefully on non-Windows

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("finance_mode_24dp_75FB4C_FILL0_wght400_GRAD0_opsz24.ico"))  # or "icon.ico" on Windows
    # app.setStyle("Fusion")

    window = MainWindow()
    window.setFixedSize(1540, 800)
    window.setWindowIcon(QIcon("finance_mode_24dp_75FB4C_FILL0_wght400_GRAD0_opsz24.ico"))  # optional: also set per window
    window.show()
    sys.exit(app.exec())