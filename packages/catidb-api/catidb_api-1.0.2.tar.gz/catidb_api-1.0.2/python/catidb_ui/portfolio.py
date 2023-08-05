# -*- coding: utf-8 -*-
from PyQt4.QtGui import QGridLayout, QFormLayout
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QComboBox, QPlainTextEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import Qt
from catidb_ui import global_vars
from catidb_ui.customqtablewidget import CustomQTableWidget


class PortfolioAcquisitions(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #no qt variables
        self.existing_codes = []
        #Widgets
        form_title = QLabel("New acquisition in CATI portfolio")
        self.code = QLineEdit()
        self.modality = QComboBox()
        self.short_description = QLineEdit()
        self.description = QPlainTextEdit()
        self.commit_button = QPushButton("Commit")
        self.dialog_label = QLabel()
        #Layout
        form_layout = QFormLayout()
        form_layout.addRow(form_title)
        form_layout.addRow("code :", self.code)
        form_layout.addRow("modality :", self.modality)
        form_layout.addRow("short description :", self.short_description)
        form_layout.addRow("description :", self.description)
        form_layout.addRow(self.commit_button)
        form_layout.addRow(self.dialog_label)
        main_layout = QGridLayout(self)
        main_layout.setColumnStretch(0, 1)
        main_layout.setRowStretch(0, 1)
        main_layout.addLayout(form_layout, 1, 1)
        main_layout.setColumnStretch(2, 1)
        main_layout.setRowStretch(2, 1)
        #init
        form_title.setAlignment(Qt.AlignCenter)
        self._updateExistingCodes()
        self.completeModality()
        #signals
        self.commit_button.clicked.connect(self.commit)
        self.code.textChanged["QString"].connect(self._checkCode)

    def completeModality(self):
        #TODO : Get it from db
        modalities = ["T1", "T2", "PET"]
        self.modality.addItems(modalities)

    def commit(self):
        if self._checkEntries():
            code = str(self.code.text())
            modality = str(self.modality.currentText())
            short_description = str(self.short_description.text())
            description = str(self.description.toPlainText())
            try:
                global_vars.catidb.add_acquisition_description(code,
                                                              modality,
                                                              short_description,
                                                              description)
                self._printSucces()
            except Exception, e:
                self._printError(e)

            self._updateExistingCodes()
            self._checkCode(code)
        else:
            pass

    def _checkEntries(self):
        entries_good = True
        self.dialog_label.clear()
        self.dialog_label.setStyleSheet("QLabel { color : red; }")
        output_text = ''
        if self.code.text().isEmpty():
            output_text += '<b>code</b> is required<br>'
            entries_good = False
        else:
            pass
        if self.short_description.text().isEmpty():
            output_text += '<b>short description</b> is required<br>'
            entries_good = False
        else:
            pass
        if self.description.toPlainText().isEmpty():
            output_text += '<b>description</b> is required<br>'
            entries_good = False
        else:
            pass
        self.dialog_label.setText(output_text)
        return entries_good

    def _printSucces(self):
        self.dialog_label.clear()
        self.dialog_label.setStyleSheet("QLabel { color : green; }")
        self.dialog_label.setText("commit successful")

    def _printError(self, e):
        self.dialog_label.clear()
        self.dialog_label.setStyleSheet("QLabel { color : red; }")
        self.dialog_label.setText("commit failed<br>%s" % e)

    def _checkCode(self, code):
        if str(code).lower() in self.existing_codes:
            self.code.setStyleSheet("QLineEdit { color : red; }")
            self.code.setToolTip("This code already exists<br>\
                                  please choose another")
            self.commit_button.setEnabled(False)
        else:
            self.code.setStyleSheet("QLineEdit { color : black; }")
            self.code.setToolTip("This code is correct")
            self.commit_button.setEnabled(True)

    def _updateExistingCodes(self):
        codes = []
        for code_dict in global_vars.catidb.acquisition_descriptions(_fields=["code"]):
            codes.append(code_dict["code"].lower())
        self.existing_codes = codes


class PortfolioAcquisitionsViewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #no qt variables
        self.data = self.getAcqusitionsDescriptions()
        #Widgets
        self.table = CustomQTableWidget(hidden_columns=["uuid"],
                                        initial_data=self.data)
        #Layout
        main_layout = QGridLayout(self)
        main_layout.addWidget(self.table, 1, 1)
        #init

    def getAcqusitionsDescriptions(self):
        return global_vars.catidb.acquisition_descriptions()
