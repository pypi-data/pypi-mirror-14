# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QTabWidget, QFrame, QTextEdit, QPushButton
from PyQt4.QtGui import QVBoxLayout
from catidb_ui.selector_container import SelectorContainer
from catidb_ui.selector import StudySelectorUnique

from customqtablewidget import CustomQTableWidget

from catidb_ui import global_vars


class StudiesPanel(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        #widgets
        self.viewer = StudiesPanelViewer()
        self.modifier = StudiesPanelModifier()
        #init
        self.setTabPosition(QTabWidget.East)
        self.addTab(self.viewer, 'Viewer')
        self.addTab(self.modifier, 'Modifier')


class StudiesPanelViewer(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        #widgets
        self.selector = SelectorContainer()
        study_selector = StudySelectorUnique()
        self.info = QTextEdit()
        self.info.setReadOnly(True)
        #layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.selector, 0)
        main_layout.addWidget(self.info, 1)
        main_layout.addStretch(1)
        #init
        self.selector.addSelector(study_selector, 0, 0)

        self.selector.globalSelectionChanged.connect(self.showInfo)

    def showInfo(self, info_dict):
        self.info.clear()
        study = info_dict["study"]
        self.info.clear()
        text = "<html>"
        study_info = global_vars.catidb.study_info(study)
        for info_dict in study_info:
            for study_key, study_value in sorted(info_dict.items()):
                text += "<b>" + study_key + "</b> :<br>"
                text += study_value + "<br><br>"
        text += "</html>"
        self.info.setText(text)


class StudiesPanelModifier(QFrame):
    def __init__(self):
        QFrame.__init__(self)


class ExpectedAcquisitionsPanel(QFrame):
    dataChangedSignal = pyqtSignal()
    currentStudyChangedSignal = pyqtSignal()

    def __init__(self):
        super(ExpectedAcquisitionsPanel, self).__init__()
        # Get the information
        self.getData()

        # Widgets
        self.refresh_button = QPushButton("Refresh data")
        self.selector_container = SelectorContainer()
        self.study_selector = StudySelectorUnique()
        self.selector_container.addSelector(self.study_selector, 0, 0)
        self.expected_acquisitions = CustomQTableWidget(
            columns=["timepoint", "code", "modality", "description"])

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.refresh_button, 0)
        main_layout.addLayout(self.selector_container, 1)
        main_layout.addWidget(self.expected_acquisitions, 2)
        main_layout.addStretch(1)

        # Signals
        self.selector_container.globalSelectionChanged.connect(
            self.changeCurrentStudy)
        self.refresh_button.clicked.connect(self.getData)
        self.currentStudyChangedSignal.connect(self.showInfo)
        self.dataChangedSignal.connect(self.showInfo)

    def getData(self):
        db = global_vars.catidb
        # db.timepoints fails on some studies
        # studies = db.study_codes()
        studies = ["memento", "adni"]
        self.data = dict.fromkeys(studies)
        for study in studies:
            self.data[study] = []
            study_timepoints = db.timepoints(study)
            for timepoint in study_timepoints:
                timepoint_acqs = db.expected_acquisitions(study, timepoint)
                for timepoint_acq in timepoint_acqs:
                    timepoint_acq["timepoint"] = timepoint
                self.data[study].extend(timepoint_acqs)
        self.dataChangedSignal.emit()

    def changeCurrentStudy(self, info_dict):
        """
        Called when the selected study is changed.
        """
        self.current_study = info_dict["study"]
        self.currentStudyChangedSignal.emit()

    def showInfo(self):
        """
        Called when the data to display in the table has to change (either
        because data was updated or because we have selected another study).
        """
        current_data = self.data[self.current_study]
        self.expected_acquisitions.setData(current_data)
