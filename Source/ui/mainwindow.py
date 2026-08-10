# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMdiArea, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QTabWidget, QTableView, QTextEdit,
    QToolBar, QVBoxLayout, QWidget)

from pyqtgraph.dockarea import DockArea

class Ui_OrionsApp(object):
    def setupUi(self, OrionsApp):
        if not OrionsApp.objectName():
            OrionsApp.setObjectName(u"OrionsApp")
        OrionsApp.resize(1595, 826)
        OrionsApp.setMinimumSize(QSize(1535, 826))
        OrionsApp.setTabShape(QTabWidget.TabShape.Triangular)
        self.actionOpen = QAction(OrionsApp)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(OrionsApp)
        self.actionSave.setObjectName(u"actionSave")
        self.actionScreenshot = QAction(OrionsApp)
        self.actionScreenshot.setObjectName(u"actionScreenshot")
        self.actionAbout = QAction(OrionsApp)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(OrionsApp)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_6 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 184))
        self.groupBox.setMaximumSize(QSize(437, 184))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_year = QComboBox(self.groupBox)
        self.comboBox_year.setObjectName(u"comboBox_year")
        self.comboBox_year.setMaxVisibleItems(12)

        self.horizontalLayout.addWidget(self.comboBox_year)

        self.comboBox_month = QComboBox(self.groupBox)
        self.comboBox_month.setObjectName(u"comboBox_month")
        self.comboBox_month.setMaxVisibleItems(12)

        self.horizontalLayout.addWidget(self.comboBox_month)

        self.spinBox_month = QSpinBox(self.groupBox)
        self.spinBox_month.setObjectName(u"spinBox_month")
        self.spinBox_month.setMaximumSize(QSize(34, 16777215))
        self.spinBox_month.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBox_month.setMinimum(-11)
        self.spinBox_month.setMaximum(11)

        self.horizontalLayout.addWidget(self.spinBox_month)

        self.pushButton_loadmonth = QPushButton(self.groupBox)
        self.pushButton_loadmonth.setObjectName(u"pushButton_loadmonth")

        self.horizontalLayout.addWidget(self.pushButton_loadmonth)

        self.pushButton_savemonth = QPushButton(self.groupBox)
        self.pushButton_savemonth.setObjectName(u"pushButton_savemonth")

        self.horizontalLayout.addWidget(self.pushButton_savemonth)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.verticalLayout.setStretch(2, 1)

        self.verticalLayout_5.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QSize(437, 94))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.comboBox_year_2 = QComboBox(self.groupBox_2)
        self.comboBox_year_2.setObjectName(u"comboBox_year_2")
        self.comboBox_year_2.setMaxVisibleItems(12)

        self.horizontalLayout_2.addWidget(self.comboBox_year_2)

        self.comboBox_month_2 = QComboBox(self.groupBox_2)
        self.comboBox_month_2.setObjectName(u"comboBox_month_2")
        self.comboBox_month_2.setMaxVisibleItems(12)

        self.horizontalLayout_2.addWidget(self.comboBox_month_2)

        self.pushButton_refresh = QPushButton(self.groupBox_2)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pushButton_refresh)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.comboBox_year_3 = QComboBox(self.groupBox_2)
        self.comboBox_year_3.setObjectName(u"comboBox_year_3")
        self.comboBox_year_3.setMaxVisibleItems(12)

        self.horizontalLayout_3.addWidget(self.comboBox_year_3)

        self.comboBox_month_3 = QComboBox(self.groupBox_2)
        self.comboBox_month_3.setObjectName(u"comboBox_month_3")
        self.comboBox_month_3.setMaxVisibleItems(12)

        self.horizontalLayout_3.addWidget(self.comboBox_month_3)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")
        self.mdiArea.setMinimumSize(QSize(0, 450))
        self.mdiArea.setMaximumSize(QSize(437, 16777215))
        self.mdiArea.setViewMode(QMdiArea.ViewMode.TabbedView)
        self.mdiArea.setTabPosition(QTabWidget.TabPosition.South)
        self.BS_panel = QWidget()
        self.BS_panel.setObjectName(u"BS_panel")
        self.verticalLayout_4 = QVBoxLayout(self.BS_panel)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_copy_previous = QPushButton(self.BS_panel)
        self.pushButton_copy_previous.setObjectName(u"pushButton_copy_previous")
        font = QFont()
        font.setPointSize(8)
        self.pushButton_copy_previous.setFont(font)
        self.pushButton_copy_previous.setToolTipDuration(-1)

        self.horizontalLayout_4.addWidget(self.pushButton_copy_previous)

        self.pushButton_add_row = QPushButton(self.BS_panel)
        self.pushButton_add_row.setObjectName(u"pushButton_add_row")

        self.horizontalLayout_4.addWidget(self.pushButton_add_row)

        self.pushButton_del_row = QPushButton(self.BS_panel)
        self.pushButton_del_row.setObjectName(u"pushButton_del_row")

        self.horizontalLayout_4.addWidget(self.pushButton_del_row)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.tableBS = QTableView(self.BS_panel)
        self.tableBS.setObjectName(u"tableBS")

        self.verticalLayout_4.addWidget(self.tableBS)

        self.verticalLayout_4.setStretch(1, 1)
        self.mdiArea.addSubWindow(self.BS_panel)
        self.IE_panel = QWidget()
        self.IE_panel.setObjectName(u"IE_panel")
        self.verticalLayout_3 = QVBoxLayout(self.IE_panel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.sheetDropdown = QComboBox(self.IE_panel)
        self.sheetDropdown.setObjectName(u"sheetDropdown")
        self.sheetDropdown.setMinimumSize(QSize(220, 0))

        self.horizontalLayout_5.addWidget(self.sheetDropdown)

        self.sheetLoad = QPushButton(self.IE_panel)
        self.sheetLoad.setObjectName(u"sheetLoad")

        self.horizontalLayout_5.addWidget(self.sheetLoad)

        self.sheetDelete = QPushButton(self.IE_panel)
        self.sheetDelete.setObjectName(u"sheetDelete")

        self.horizontalLayout_5.addWidget(self.sheetDelete)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.sheetTable = QTableView(self.IE_panel)
        self.sheetTable.setObjectName(u"sheetTable")

        self.verticalLayout_3.addWidget(self.sheetTable)

        self.verticalLayout_3.setStretch(1, 1)
        self.mdiArea.addSubWindow(self.IE_panel)

        self.verticalLayout_5.addWidget(self.mdiArea)

        self.verticalLayout_5.setStretch(2, 1)

        self.horizontalLayout_6.addLayout(self.verticalLayout_5)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(1150, 0))
        self.BS_area = DockArea()
        self.BS_area.setObjectName(u"BS_area")
        self.stackedWidget.addWidget(self.BS_area)
        self.IE_area = DockArea()
        self.IE_area.setObjectName(u"IE_area")
        self.stackedWidget.addWidget(self.IE_area)

        self.horizontalLayout_6.addWidget(self.stackedWidget)

        self.horizontalLayout_6.setStretch(1, 1)
        OrionsApp.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(OrionsApp)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 1595, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        OrionsApp.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(OrionsApp)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        self.statusbar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.statusbar.setAutoFillBackground(False)
        OrionsApp.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(OrionsApp)
        self.toolBar.setObjectName(u"toolBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy1)
        self.toolBar.setIconSize(QSize(22, 22))
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        OrionsApp.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(OrionsApp)

        QMetaObject.connectSlotsByName(OrionsApp)
    # setupUi

    def retranslateUi(self, OrionsApp):
        OrionsApp.setWindowTitle(QCoreApplication.translate("OrionsApp", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("OrionsApp", u"Set Workspace Directory", None))
        self.actionSave.setText(QCoreApplication.translate("OrionsApp", u"Save", None))
        self.actionScreenshot.setText(QCoreApplication.translate("OrionsApp", u"Screenshot", None))
        self.actionAbout.setText(QCoreApplication.translate("OrionsApp", u"About", None))
        self.groupBox.setTitle(QCoreApplication.translate("OrionsApp", u"Month", None))
        self.comboBox_year.setPlaceholderText(QCoreApplication.translate("OrionsApp", u"Year", None))
        self.comboBox_month.setPlaceholderText(QCoreApplication.translate("OrionsApp", u"Month", None))
        self.pushButton_loadmonth.setText(QCoreApplication.translate("OrionsApp", u"Load", None))
        self.pushButton_savemonth.setText(QCoreApplication.translate("OrionsApp", u"Save", None))
        self.label_2.setText(QCoreApplication.translate("OrionsApp", u"Notes", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("OrionsApp", u"Plotting Range", None))
        self.label_3.setText(QCoreApplication.translate("OrionsApp", u"From", None))
        self.comboBox_year_2.setPlaceholderText(QCoreApplication.translate("OrionsApp", u"Year", None))
        self.comboBox_month_2.setPlaceholderText(QCoreApplication.translate("OrionsApp", u"Month", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("OrionsApp", u"Refresh", None))
        self.label_4.setText(QCoreApplication.translate("OrionsApp", u"To", None))
        self.comboBox_year_3.setPlaceholderText(QCoreApplication.translate("OrionsApp", u"Year", None))
        self.comboBox_month_3.setPlaceholderText(QCoreApplication.translate("OrionsApp", u"Month", None))
        self.BS_panel.setWindowTitle(QCoreApplication.translate("OrionsApp", u"Balance Sheet", None))
#if QT_CONFIG(tooltip)
        self.pushButton_copy_previous.setToolTip(QCoreApplication.translate("OrionsApp", u"Copy data from the previous month as a starting point", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_copy_previous.setText(QCoreApplication.translate("OrionsApp", u"Copy Previous", None))
        self.pushButton_add_row.setText(QCoreApplication.translate("OrionsApp", u"Add Row", None))
        self.pushButton_del_row.setText(QCoreApplication.translate("OrionsApp", u"Delete Row", None))
        self.IE_panel.setWindowTitle(QCoreApplication.translate("OrionsApp", u"Income + Expense", None))
        self.sheetLoad.setText(QCoreApplication.translate("OrionsApp", u"Load", None))
        self.sheetDelete.setText(QCoreApplication.translate("OrionsApp", u"Delete", None))
        self.menuFile.setTitle(QCoreApplication.translate("OrionsApp", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("OrionsApp", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("OrionsApp", u"toolBar", None))
    # retranslateUi

