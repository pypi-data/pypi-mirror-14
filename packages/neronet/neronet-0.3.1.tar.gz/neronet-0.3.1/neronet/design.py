# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'neronetgui.ui'
#
# Created: Wed Mar 16 14:25:32 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1117, 595)
        MainWindow.setMinimumSize(QtCore.QSize(1117, 595))
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(352, 285))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.clusters = QtGui.QListWidget(self.tab)
        self.clusters.setGeometry(QtCore.QRect(0, 20, 171, 151))
        self.clusters.setObjectName(_fromUtf8("clusters"))
        self.cluster_name_field = QtGui.QLineEdit(self.tab)
        self.cluster_name_field.setGeometry(QtCore.QRect(230, 20, 113, 27))
        self.cluster_name_field.setObjectName(_fromUtf8("cluster_name_field"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(230, 0, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.terminate_btn = QtGui.QPushButton(self.tab)
        self.terminate_btn.setGeometry(QtCore.QRect(230, 180, 111, 27))
        self.terminate_btn.setObjectName(_fromUtf8("terminate_btn"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(230, 50, 101, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.submit_btn = QtGui.QPushButton(self.tab)
        self.submit_btn.setGeometry(QtCore.QRect(230, 140, 111, 27))
        self.submit_btn.setObjectName(_fromUtf8("submit_btn"))
        self.cluster_add_btn = QtGui.QPushButton(self.tab)
        self.cluster_add_btn.setGeometry(QtCore.QRect(230, 100, 111, 27))
        self.cluster_add_btn.setObjectName(_fromUtf8("cluster_add_btn"))
        self.cluster_address_field = QtGui.QLineEdit(self.tab)
        self.cluster_address_field.setGeometry(QtCore.QRect(230, 70, 113, 27))
        self.cluster_address_field.setObjectName(_fromUtf8("cluster_address_field"))
        self.refresh_btn = QtGui.QPushButton(self.tab)
        self.refresh_btn.setGeometry(QtCore.QRect(120, 180, 111, 27))
        self.refresh_btn.setObjectName(_fromUtf8("refresh_btn"))
        self.exp_add_btn = QtGui.QPushButton(self.tab)
        self.exp_add_btn.setGeometry(QtCore.QRect(10, 180, 111, 27))
        self.exp_add_btn.setObjectName(_fromUtf8("exp_add_btn"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 64, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cluster_type_combo = QtGui.QComboBox(self.tab)
        self.cluster_type_combo.setEnabled(True)
        self.cluster_type_combo.setGeometry(QtCore.QRect(10, 250, 16, 16))
        self.cluster_type_combo.setObjectName(_fromUtf8("cluster_type_combo"))
        self.cluster_type_combo.addItem(_fromUtf8(""))
        self.cluster_type_combo.addItem(_fromUtf8(""))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 1)
        self.experiment_log = QtGui.QPlainTextEdit(self.centralwidget)
        self.experiment_log.setMaximumSize(QtCore.QSize(352, 286))
        self.experiment_log.setObjectName(_fromUtf8("experiment_log"))
        self.gridLayout.addWidget(self.experiment_log, 0, 1, 1, 1)
        self.paramTable = QtGui.QTableWidget(self.centralwidget)
        self.paramTable.setMinimumSize(QtCore.QSize(741, 561))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.paramTable.setFont(font)
        self.paramTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.paramTable.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed)
        self.paramTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.paramTable.setObjectName(_fromUtf8("paramTable"))
        self.paramTable.setColumnCount(0)
        self.paramTable.setRowCount(0)
        self.paramTable.verticalHeader().setDefaultSectionSize(22)
        self.paramTable.verticalHeader().setMinimumSectionSize(22)
        self.gridLayout.addWidget(self.paramTable, 0, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "NeroGUI", None))
        self.label.setText(_translate("MainWindow", "cluster name", None))
        self.terminate_btn.setText(_translate("MainWindow", "Terminate", None))
        self.label_2.setText(_translate("MainWindow", "cluster address", None))
        self.submit_btn.setText(_translate("MainWindow", "Submit", None))
        self.cluster_add_btn.setText(_translate("MainWindow", "Add cluster", None))
        self.refresh_btn.setText(_translate("MainWindow", "Refresh", None))
        self.exp_add_btn.setText(_translate("MainWindow", "Add experiment", None))
        self.label_3.setText(_translate("MainWindow", "Clusters", None))
        self.cluster_type_combo.setItemText(0, _translate("MainWindow", "unmanaged", None))
        self.cluster_type_combo.setItemText(1, _translate("MainWindow", "slurm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.paramTable.setSortingEnabled(True)

