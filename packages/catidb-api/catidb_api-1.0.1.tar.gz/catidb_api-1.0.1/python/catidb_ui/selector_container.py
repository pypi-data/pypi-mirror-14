# -*- coding: utf-8 -*-
from PyQt4.QtGui import QGridLayout
from PyQt4.QtCore import pyqtSignal


class SelectorContainer(QGridLayout):
    globalSelectionChanged = pyqtSignal(dict)

    def __init__(self):
        QGridLayout.__init__(self)
        #no qt variable
        self.selection_widget_list = []

    def addSelector(self, selector, row, column):
        self.addWidget(selector, row, column)
        self.selection_widget_list.append(selector)
        selector.selectionChanged.connect(self.returnGlobalSelection)

    def returnGlobalSelection(self):
        output_dict = {}
        for selector in self.selection_widget_list:
            output_dict.update(selector.getSelection())
        self.globalSelectionChanged.emit(output_dict)
