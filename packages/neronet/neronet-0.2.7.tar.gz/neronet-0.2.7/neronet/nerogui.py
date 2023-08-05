import sys
import webbrowser
from PyQt4 import QtGui
from PyQt4 import QtCore
import design
import neronet.neroman
import os.path


class Nerogui(QtGui.QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Nerogui, self).__init__(parent)
        self.setupUi(self)
        self.nero = neronet.neroman.Neroman()
        self.init_clusters()
        self.init_experiments()
        # bind signals and slots
        self.cluster_add_btn.clicked.connect(self.add_cluster)
        self.clusters.itemSelectionChanged.connect(self.update_cluster_fields)
        self.experiments.itemSelectionChanged.connect(self.show_one_experiment)
        self.experiments.itemSelectionChanged.connect(self.add_to_param_table)
        self.experiments.doubleClicked.connect(self.open_config)
        self.exp_add_btn.clicked.connect(self.add_file)
        self.submit_btn.clicked.connect(self.submit_exp)
        self.refresh_btn.clicked.connect(self.fetch_exp)

    def init_clusters(self):
        """add each cluster to view"""
        self.clusters.clear()
        for cluster in self.nero.clusters["clusters"]:
            self.clusters.addItem(cluster)

    def init_experiments(self):
        """add each experiment to view"""
        self.experiments.clear()
        for exp_name in self.nero.database.keys():
            self.experiments.addItem(exp_name)

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
        self.init_experiments()

    def submit_exp(self):
        """submit button functionality"""
        cluster = str(self.clusters.currentItem().text())
        if cluster is None:
            return
        for exp in self.experiments.selectedItems():
            self.nero.submit(str(exp.text()), cluster)

    def add_to_param_table(self):
        """inserts values from database to comparison table"""
        labels = set()
        names = []
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        for exp in self.experiments.selectedItems():
            labels |= set(
                self.nero.database[str(exp.text())]._fields["parameters"].keys())
            names.append(str(exp.text()))
        self.tableWidget.setRowCount(len(names))
        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(tuple(labels))
        self.tableWidget.setVerticalHeaderLabels(names)

        for idx1, name in enumerate(names):
            for idx2, param in enumerate(labels):
                try:
                    value = self.nero.database[
                        name]._fields["parameters"][param]
                    self.tableWidget.setItem(
                        idx1,
                        idx2,
                        QtGui.QTableWidgetItem(
                            QtCore.QString("%1").arg(value)))
                except KeyError:
                    pass

    def show_one_experiment(self):
        """prints detailed info of one experiment"""
        self.experiment_log.clear()
        name = str(self.experiments.currentItem().text())
        for line in self.nero.status_gen(name):
            self.experiment_log.insertPlainText(line)

    def open_config(self):
        """double clicking opens config file"""
        name = str(self.experiments.currentItem().text())
        path = self.nero.database[name]._fields["path"]
        webbrowser.open(path + "/config.yaml")

    def fetch_exp(self):
        """fetches experiments statuses"""
        self.nero.fetch()


def main():
    app = QtGui.QApplication(sys.argv)
    form = Nerogui()
    form.show()
    app.exec_()
