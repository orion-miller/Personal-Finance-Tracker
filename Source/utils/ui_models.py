from PySide6.QtWidgets import (
    QStyledItemDelegate, QComboBox
)
from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex
)
import pandas as pd
from . import status

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