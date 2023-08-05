# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'neronetgui.ui'
#
# Created: Fri Mar  4 15:39:14 2016
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
        MainWindow.resize(1119, 594)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.submit_btn = QtGui.QPushButton(self.centralwidget)
        self.submit_btn.setGeometry(QtCore.QRect(1000, 550, 111, 27))
        self.submit_btn.setObjectName(_fromUtf8("submit_btn"))
        self.cluster_name_field = QtGui.QLineEdit(self.centralwidget)
        self.cluster_name_field.setGeometry(QtCore.QRect(980, 360, 113, 27))
        self.cluster_name_field.setObjectName(_fromUtf8("cluster_name_field"))
        self.cluster_address_field = QtGui.QLineEdit(self.centralwidget)
        self.cluster_address_field.setGeometry(QtCore.QRect(980, 410, 113, 27))
        self.cluster_address_field.setObjectName(_fromUtf8("cluster_address_field"))
        self.cluster_add_btn = QtGui.QPushButton(self.centralwidget)
        self.cluster_add_btn.setGeometry(QtCore.QRect(980, 500, 111, 27))
        self.cluster_add_btn.setObjectName(_fromUtf8("cluster_add_btn"))
        self.cluster_type_combo = QtGui.QComboBox(self.centralwidget)
        self.cluster_type_combo.setGeometry(QtCore.QRect(980, 450, 111, 31))
        self.cluster_type_combo.setObjectName(_fromUtf8("cluster_type_combo"))
        self.cluster_type_combo.addItem(_fromUtf8(""))
        self.cluster_type_combo.addItem(_fromUtf8(""))
        self.clusters = QtGui.QListWidget(self.centralwidget)
        self.clusters.setGeometry(QtCore.QRect(770, 350, 171, 191))
        self.clusters.setObjectName(_fromUtf8("clusters"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(980, 340, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(980, 390, 101, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.experiment_log = QtGui.QPlainTextEdit(self.centralwidget)
        self.experiment_log.setGeometry(QtCore.QRect(770, 10, 341, 321))
        self.experiment_log.setObjectName(_fromUtf8("experiment_log"))
        self.exp_add_btn = QtGui.QPushButton(self.centralwidget)
        self.exp_add_btn.setGeometry(QtCore.QRect(760, 550, 111, 27))
        self.exp_add_btn.setObjectName(_fromUtf8("exp_add_btn"))
        self.refresh_btn = QtGui.QPushButton(self.centralwidget)
        self.refresh_btn.setGeometry(QtCore.QRect(880, 550, 111, 27))
        self.refresh_btn.setObjectName(_fromUtf8("refresh_btn"))
        self.paramTable = QtGui.QTableWidget(self.centralwidget)
        self.paramTable.setGeometry(QtCore.QRect(10, 10, 741, 561))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.paramTable.setFont(font)
        self.paramTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.paramTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.paramTable.setObjectName(_fromUtf8("paramTable"))
        self.paramTable.setColumnCount(0)
        self.paramTable.setRowCount(0)
        self.paramTable.verticalHeader().setDefaultSectionSize(22)
        self.paramTable.verticalHeader().setMinimumSectionSize(22)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(770, 330, 64, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "NeroGUI", None))
        self.submit_btn.setText(_translate("MainWindow", "Submit", None))
        self.cluster_add_btn.setText(_translate("MainWindow", "Add cluster", None))
        self.cluster_type_combo.setItemText(0, _translate("MainWindow", "unmanaged", None))
        self.cluster_type_combo.setItemText(1, _translate("MainWindow", "slurm", None))
        self.label.setText(_translate("MainWindow", "cluster name", None))
        self.label_2.setText(_translate("MainWindow", "cluster address", None))
        self.exp_add_btn.setText(_translate("MainWindow", "Add experiment", None))
        self.refresh_btn.setText(_translate("MainWindow", "refresh", None))
        self.paramTable.setSortingEnabled(True)
        self.label_3.setText(_translate("MainWindow", "Clusters", None))

