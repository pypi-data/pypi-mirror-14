# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QTableWidget, QTableWidgetItem


class CustomQTableWidget(QTableWidget):
    dataChangedSignal = pyqtSignal()

    def __init__(self, columns=None, hidden_columns=[], initial_data=[]):
        """
        columns: list of string or None
            The columns to use. If None, they will be inferred from the first
            data.

        hidden_columns: list of strings or None:
            The columns to not display. If None, all the columns will be
            displayed.

        initial_data: list of dict
            The initial data.
        """
        super(CustomQTableWidget, self).__init__()

        # Non Qt variables
        self.columns = columns
        self.hidden_columns = hidden_columns
        # Data contains the  internal representation of the information to
        # display (it's a list of list of QTableWidgetItem)
        try:
            self.setData(initial_data)
            self.updateContent()  # Signal is not connected yet
        except Exception as e:
            raise e

        # Init
        self.setSortingEnabled(True)

        # Signals
        self.dataChangedSignal.connect(self.updateContent)

    def _convert_data(self, data):
        """
        Check that data is a list of dict with the correct keys and convert it
        to a list of list of table items.
        """
        res = []
        for item in data:
            res.append(self._convert_item(item))
        return res

    def _convert_item(self, item):
        """
        Check that item is a dict with the correct keys and convert it to list
        of table items. Otherwise raise an exception.
        """
        if not isinstance(item, dict):
            raise ValueError("item must be dict")
        if not self._check_item_columns(item):
            msg_fmt = "item keys must be in {exp} (got {real})"
            msg = msg_fmt.format(exp=self.columns, real=item.keys())
            raise ValueError(msg)
        return [QTableWidgetItem(item[col]) for col in self.columns
                if col not in self.hidden_columns]

    def _check_item_columns(self, item, check_hidden_columns=True):
        if not self.columns:
            self._columns_from_item(item)
        if check_hidden_columns:
            hidden_cols_ok = set(item.keys()) >= set(self.hidden_columns)
        else:
            hidden_cols_ok = True
        return set(item.keys()) >= set(self.columns) and hidden_cols_ok

    def _columns_from_item(self, item, force=False):
        if not self.columns or force:
            self.columns = sorted([col for col in item.keys()
                                   if col not in self.hidden_columns])

    def updateContent(self):
        self._setTableSize()
        if self.columns:  # Otherwise there is no data and no header
            headers = [col for col in self.columns
                       if col not in self.hidden_columns]
            self.setHorizontalHeaderLabels(headers)
            # Disable sorting when inserting data (see QTableWidget help)
            self.setSortingEnabled(False)
            for i, row in enumerate(self.data):
                for j, col in enumerate(headers):
                    current_item = row[j]
                    flags = current_item.flags() ^ Qt.ItemIsEditable
                    current_item.setFlags(flags)
                    self.setItem(i, j, current_item)
            # Re-enable sorting when inserting data
            self.setSortingEnabled(True)
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.freezeSize()

    def _setTableSize(self):
        self.setRowCount(len(self.data))
        if self.columns:
            column_count = len(self.columns)
        else:
            column_count = 0
        self.setColumnCount(column_count)

    def freezeSize(self):
        width, height = self._getOptimumSize()
        self.setMaximumSize(width, height)

    def _getOptimumSize(self):
        width = self.contentsMargins().left()
        width += self.contentsMargins().right()
        width += self.verticalHeader().width()
        for column_index in range(self.columnCount()):
            width += self.columnWidth(column_index)

        height = self.contentsMargins().top()
        height += self.contentsMargins().bottom()
        height += self.horizontalHeader().height()
        for row_index in range(self.rowCount()):
            height += self.rowHeight(row_index)

        return width, height

    def setData(self, data):
        self.data = self._convert_data(data)
        self.dataChangedSignal.emit()

    def addItem(self, item):
        self.data.append(self._convert_item(item))
        self.dataChangedSignal.emit()

    def removeItem(self):
        self.dataChangedSignal.emit()

    def clearData(self):
        self.data = []
        self.dataChangedSignal.emit()
