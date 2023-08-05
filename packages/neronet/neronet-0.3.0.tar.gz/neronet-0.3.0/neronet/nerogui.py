import sys
import webbrowser
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QVariant
from PyQt4.QtGui import QApplication, QTableWidget, QTableWidgetItem
import design
import neronet.neroman
import os.path

class MyTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if ( isinstance(other, QTableWidgetItem) ):
            my_value, my_ok = self.data(Qt.EditRole).toInt()
            other_value, other_ok = other.data(Qt.EditRole).toInt()

            if ( my_ok and other_ok ):
                return my_value < other_value

        return super(MyTableWidgetItem, self).__lt__(other)


class Nerogui(QtGui.QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Nerogui, self).__init__(parent)
        self.allLabels = set()
        self.filteredLabels = set()
        self.actions = {}
        self.setupUi(self)
        self.nero = neronet.neroman.Neroman()
        self.menu = QtGui.QMenu(self)
        self.init_clusters()
        self.init_labels()
        self.init_menu()
        self.add_to_param_table()
        # bind signals and slots
        self.cluster_add_btn.clicked.connect(self.add_cluster)
        self.clusters.itemSelectionChanged.connect(self.update_cluster_fields)
        self.paramTable.itemSelectionChanged.connect(self.show_one_experiment)
        self.paramTable.verticalHeader().sectionDoubleClicked.connect(self.open_config)
        self.paramTable.doubleClicked.connect(self.open_config)
        self.exp_add_btn.clicked.connect(self.add_file)
        self.submit_btn.clicked.connect(self.submit_exp)
        self.refresh_btn.clicked.connect(self.fetch_exp)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)


    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
             e.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path =  url.toLocalFile().toLocal8Bit().data()
                self.nero.specify_experiments(path)
            self.init_labels()
            self.init_menu()
            self.add_to_param_table()
        else:
            event.ignore()

    def init_menu(self):
        self.menu = QtGui.QMenu(self)
        self.filteredLabels = set()
        for name in self.allLabels:
            self.menu.addAction(name)
        for action in self.menu.actions():
            action.setCheckable(True)

    
    @QtCore.pyqtSlot(QtCore.QPoint)
    def openMenu(self, pos):
        self.filteredLabels = set()
        self.menu.popup(self.mapToGlobal(pos))
        selectedAction = self.menu.exec_(self.mapToGlobal(pos))
        if selectedAction is None:
            return
        selectedAction.setChecked(selectedAction.isChecked())
        for action in self.menu.actions():
            if not action.isChecked():
                self.filteredLabels |= set(
                    [str(action.text()),])        
        self.add_to_param_table()

    def init_labels(self):
        self.allLabels = set() #prepare label list
        for exp in self.nero.database.keys():
            self.allLabels |= set(
                self.nero.database[exp]._fields["parameters"].keys())        

    def init_clusters(self):
        """add each cluster to view"""
        self.clusters.clear()
        for cluster in self.nero.clusters["clusters"]:
            self.clusters.addItem(cluster)

    def add_cluster(self):
        """add cluster to neroman configs"""
        addr = str(self.cluster_address_field.text())
        nm = str(self.cluster_name_field.text())
        type = str(self.cluster_type_combo.currentText())
        self.nero.specify_cluster(nm, type, addr)
        self.init_clusters()

    def update_cluster_fields(self):
        """add clusters view"""
        cluster = str(self.clusters.currentItem().text())
        self.cluster_name_field.setText(cluster)
        self.cluster_address_field.setText(
            self.nero.clusters["clusters"][cluster].ssh_address)

    def add_file(self):
        """add folder to neroman database"""
        file_path = str(
            QtGui.QFileDialog.getExistingDirectory(
                self,
                "Select Directory"))
        self.nero.specify_experiments(file_path)
        self.init_labels()
        self.init_menu()
	self.add_to_param_table()
        

    def submit_exp(self):
        """submit button functionality"""
        cluster = str(self.clusters.currentItem().text())
        if cluster is NoneType:
            return
        for exp in self.paramTable.selectionModel().selectedRows():
            name = str(self.paramTable.item(exp.row(), 0).text())
            self.nero.submit(name, cluster)

    def add_to_param_table(self):
        """inserts values from database to comparison table"""
        expNames = self.nero.database.keys()
        insertedLabels = set()
        if len(self.filteredLabels) == len(self.allLabels):
            insertedLabels = self.allLabels
        else:
            insertedLabels = self.allLabels - self.filteredLabels
        self.paramTable.setRowCount(0)
        self.paramTable.setColumnCount(0)
        self.paramTable.setRowCount(len(expNames))
        self.paramTable.setColumnCount(len(insertedLabels)+1)
        self.paramTable.setColumnWidth(0,200)
        self.paramTable.setHorizontalHeaderLabels(tuple(["Name",] + list(insertedLabels)))
	for yAxis, name in enumerate(expNames):
	    self.paramTable.setItem(
	        yAxis,
	        0,
	        MyTableWidgetItem(
	           QtCore.QString("%1").arg(name)))
	    for xAxis, param in enumerate(insertedLabels):
	        try:
	            value = self.nero.database[
	                name]._fields["parameters"][param]
	            self.paramTable.setItem(
	                yAxis,
	                xAxis+1,
	                MyTableWidgetItem(
	                    QtCore.QString("%1").arg(value)))
	        except KeyError:
	            pass

    def show_one_experiment(self):
        """prints detailed info of one experiment"""
        self.experiment_log.clear()
        row = self.paramTable.currentRow()
        if self.paramTable.item(row, 0) is None:
            return
	name = str(self.paramTable.item(row, 0).text())
        for line in self.nero.status_gen(name):
            self.experiment_log.insertPlainText(line)

    def open_config(self):
        """double clicking opens config file"""
        row = self.paramTable.currentRow()
	name = str(self.paramTable.item(row, 0).text())
        path = self.nero.database[name]._fields["path"]
        webbrowser.open(path)

    def fetch_exp(self):
        """fetches experiments statuses"""
        self.nero.fetch()


def main():
    app = QtGui.QApplication(sys.argv)
    form = Nerogui()
    form.show()
    app.exec_()
