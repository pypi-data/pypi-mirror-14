# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QComboBox, QListWidget

from catidb_ui import global_vars


class SelectorUnique(QComboBox):
    selectionChanged = pyqtSignal()

    def __init__(self, name, values):
        QComboBox.__init__(self)
        self.addItems(values)
        self.name = name

        self.currentIndexChanged[str].connect(self.selectionChanged.emit)

    def getSelection(self):
        value = str(self.currentText())
        return {self.name: value}


class SelectorMultiple(QListWidget):
    selectionChanged = pyqtSignal()

    def __init__(self, name, values):
        QListWidget.__init__(self)
        self.addItems(values)
        self.name = name

        self.itemSelectionChanged.connect(self.selectionChanged.emit)

    def getSelection(self):
        values = []
        for widget_item in self.selectedItems():
            values.append(str(widget_item.text()))
        return {self.name: values}
#==============================================================================
#
#==============================================================================


class StudySelectorUnique(SelectorUnique):
    def __init__(self):
        studies = global_vars.catidb.study_codes()
        super(StudySelectorUnique, self).__init__("study", studies)
