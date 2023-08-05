# -*- coding: utf-8 -*-
import os.path as osp
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import (QFrame,
                         QComboBox, QListWidget, QListWidgetItem, QPushButton,
                         QLabel, QGridLayout, QVBoxLayout, QMessageBox)
from PyQt4.uic import loadUi

from catidb_ui.api_constants import (users_route,
                                     user_login_key,
                                     groups_route,
                                     group_name_key,
                                     group_members_key,
                                     group_member_route)
from catidb_ui import global_vars


class GroupMembership(QFrame):
    """
    A widget to edit group membership.
    """

    addInGroup = pyqtSignal(str, list)
    removeFromGroup = pyqtSignal(str, list)

    def __init__(self):
        QFrame.__init__(self)
        self.group_selector = QComboBox()
        self.membersList = QListWidget()
        self.membersList.setSelectionMode(QListWidget.ExtendedSelection)
        self.nonMembersList = QListWidget()
        self.nonMembersList.setSelectionMode(QListWidget.ExtendedSelection)
        self.add_members_button = QPushButton(">")
        self.remove_members_button = QPushButton("<")

        # Signals
        self.group_selector.currentIndexChanged.connect(self.displayGroupInfo)
        self.add_members_button.clicked.connect(self.addMembers)
        self.remove_members_button.clicked.connect(self.removeMembers)

        # Layout
        main_layout = QGridLayout(self)
        main_layout.addWidget(QLabel("Group"), 0, 0)
        main_layout.addWidget(self.group_selector, 0, 1, 1, 2)
        main_layout.addWidget(QLabel("Non-members"), 1, 0)
        main_layout.addWidget(self.nonMembersList, 2, 0, 4, 1)
        main_layout.addWidget(self.add_members_button, 3, 1)
        main_layout.addWidget(self.remove_members_button, 4, 1)
        main_layout.addWidget(QLabel("Members"), 1, 2)
        main_layout.addWidget(self.membersList, 2, 2, 4, 1)

    def clear(self):
        self.membersList.clear()
        self.nonMembersList.clear()

    def setInfo(self, users, groups, group_members):
        self.users = users
        self.groups = groups
        self.group_members = group_members

        # Update UI (list of groups in group selector)
        _, current_group_index = self.getCurrentGroup()  # To restore it
        self.group_selector.clear()
        self.group_selector.addItems(groups)
        if current_group_index:
            self.group_selector.setCurrentIndex(current_group_index)

    def getCurrentGroup(self):
        index = self.group_selector.currentIndex()
        text = str(self.group_selector.currentText())
        return (text, index)

    def getCurrentSelectedUsers(self, list_view):
        selected_users = []
        for user in list_view.selectedItems():
            selected_users.append(str(user.text()))
        return selected_users

    def displayGroupInfo(self):
        current_group, _ = self.getCurrentGroup()
        if not current_group:
            self.clear()
            return
        all_users = set(self.users)
        current_group_members = set(self.group_members[current_group])
        current_group_non_members = all_users - current_group_members

        # Update UI (list of members and non-members)
        self.clear()
        for user in current_group_members:
            self.membersList.addItem(user)
        for user in current_group_non_members:
            self.nonMembersList.addItem(user)

    def addMembers(self):
        current_group, _ = self.getCurrentGroup()
        if not current_group:
            return
        users_to_add = self.getCurrentSelectedUsers(self.nonMembersList)
        if not users_to_add:
            return
        self.addInGroup.emit(current_group, users_to_add)

    def removeMembers(self):
        current_group, _ = self.getCurrentGroup()
        if not current_group:
            return
        users_to_remove = self.getCurrentSelectedUsers(self.membersList)
        if not users_to_remove:
            return
        self.removeFromGroup.emit(current_group, users_to_remove)


class GroupsPanel(QFrame):
    # An internal signal to notify that the group information has changed
    info_updated = pyqtSignal()

    def __init__(self):
        QFrame.__init__(self)
        # Widgets
        self.refresh_button = QPushButton("Refresh info")
        self.group_members_editor = GroupMembership()

        # Connect signals
        self.refresh_button.clicked.connect(self.getInfo)
        self.info_updated.connect(self.configView)
        self.group_members_editor.addInGroup.connect(self.addMembers)
        self.group_members_editor.removeFromGroup.connect(self.removeMembers)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.refresh_button, 1)
        main_layout.addWidget(self.group_members_editor, 2)
        main_layout.addStretch(1)

        # Initialize group information
        self.getInfo()

    def getInfo(self):
        db = global_vars.catidb
        # Get all information
        users = db.call_server_get(users_route)
        groups = db.call_server_get(groups_route)
        # COnstruct user list
        self.users = []
        for user in users:
            self.users.append(user[user_login_key])
        self.users.sort()
        # Construct group list & group members
        self.groups = []
        self.group_members = {}
        for group in groups:
            group_name = group[group_name_key]
            self.groups.append(group_name)
            self.group_members[group_name] = group.get(group_members_key, [])
        self.groups.sort()
        # Revert the dict
        self.user_groups = dict((i,[]) for i in self.users)
        for group, users in self.group_members.items():
            for user in users:
                self.user_groups.setdefault(user,[]).append(group)
        self.groups = sorted(self.group_members.keys())
        self.info_updated.emit()

    def configView(self):
        self.group_members_editor.setInfo(self.users, self.groups,
                                          self.group_members)

    def addMembers(self, group, users):
        db = global_vars.catidb
        route = group_member_route.format(group=group)
        params = {}
        params["users"] = users
        db.call_server_post(route, params=params)
        self.getInfo()

    def removeMembers(self, group, users):
        db = global_vars.catidb
        route = group_member_route.format(group=group)
        params = {}
        params["users"] = users
        db.call_server_delete(route, params=params)
        self.getInfo()

class UsersPanel(QFrame):
    '''
    Panel to modify users credentials.
    '''

    def __init__(self):
        QFrame.__init__(self)
        dir = osp.dirname(__file__)
        loadUi(osp.join(dir, 'security_users_panel.ui'), self)
        self.modification = {}
        self.bbxModified.setVisible(False)
        self.lstUsers.itemClicked.connect(self.select_user)
        self.lstGroups.itemSelectionChanged.connect(self.set_groups)
        self.bbxModified.button(self.bbxModified.Apply).clicked.connect(self.apply_changes)
        self.bbxModified.button(self.bbxModified.Cancel).clicked.connect(self.cancel_changes)
        self.refresh()

    def refresh(self):
        db = global_vars.catidb
        users = db.call_server_get(users_route)
        self.users = dict((user[user_login_key],set()) for user in users)
        # Construct group list & group members
        groups = db.call_server_get(groups_route)
        self.groups = set()
        for group in groups:
            group_name = group[group_name_key]
            members = set(group.get(group_members_key, []))
            self.groups.add(group_name)
            for m in members:
                self.users.setdefault(m,set()).add(group_name)
        
        self.lstGroups.itemSelectionChanged.disconnect(self.set_groups)
        try:
            self.lstUsers.clear()
            for u in sorted(self.users):
                self.lstUsers.addItem(u)
        finally:
            self.lstGroups.itemSelectionChanged.connect(self.set_groups)

    def select_user(self):
        self.lstGroups.itemSelectionChanged.disconnect(self.set_groups)
        try:
            self.lstGroups.clear()
            user = self.lstUsers.currentItem().text()
            groups = self.users[user]
            added_groups, deleted_groups = self.modification.get(user,(set(), set()))
            selected_groups = groups.difference(deleted_groups).union(added_groups)
            for u in sorted(selected_groups):
                item = QListWidgetItem(u)
                self.lstGroups.addItem(item)
                item.setSelected(True)
            for g in sorted(self.groups):
                if g not in selected_groups:
                    self.lstGroups.addItem(g)
        finally:
            self.lstGroups.itemSelectionChanged.connect(self.set_groups)

    def set_groups(self):
        user = self.lstUsers.currentItem().text()
        groups = self.users[user]
        new_groups = set(item.text() for item in self.lstGroups.selectedItems())
        
        added_groups = new_groups.difference(groups)
        deleted_groups = groups.difference(new_groups)
        
        if added_groups or deleted_groups:
            self.modification[user] = (added_groups, deleted_groups)
        else:
            self.modification.pop(user, None)
        self.bbxModified.setVisible(bool(self.modification))

    def apply_changes(self):
        # Build modification per group instead of per user
        groups_modif = {}
        for user, added_deleted in self.modification.iteritems():
            added_groups, deleted_groups = added_deleted
            for g in added_groups:
                groups_modif.setdefault(g, ([],[]))[0].append(user)
            for g in deleted_groups:
                groups_modif.setdefault(g, ([],[]))[1].append(user)
        
        # Build a message to summarize modifications
        message = ['The following actions are going to be performed:']
        for group, added_deleted in groups_modif.iteritems():
            added_users, deleted_users = added_deleted
            message.append('Group {0}'.format(group))
            if added_users:
                message.append('  add users: {0}'.format(', '.join(added_users)))
            if deleted_users:
                message.append('  remove users: {0}'.format(', '.join(deleted_users)))
        message = '\n'.join(message)
        
        # Display a dialog box to the user and wait for confirmation
        answer = QMessageBox.question(self, 'Please confirm', message, QMessageBox.Ok | QMessageBox.Cancel)
        if answer == QMessageBox.Ok:
            # Apply group modification
            db = global_vars.catidb
            for group, added_deleted in groups_modif.iteritems():
                added_users, deleted_users = added_deleted
                if added_users:
                    db.call_server_post(group_member_route.format(group=group), params=dict(users=added_users))
                if deleted_users:
                    db.call_server_delete(group_member_route.format(group=group), params=dict(users=deleted_users))
            
            # Update groups per user
            for user, added_deleted in self.modification.iteritems():
                self.users[user].difference_update(deleted_groups)
                self.users[user].update(added_groups)
                
            # Reset modifications
            self.modification = {}
            
            # Update GUI
            self.bbxModified.setVisible(False)
            self.select_user()
    
    def cancel_changes(self):
        self.modification = {}
        self.bbxModified.setVisible(False)
        self.select_user()
