from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from core.file_system import FileSystem
from utils.helpers import get_file_info

class FileTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Name", "Size", "Type"])
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setAlternatingRowColors(True)
        self.current_path = ""
        self.ignore_patterns = []
        self.file_types = []
        
        self.itemChanged.connect(self.on_item_changed)
        self.itemExpanded.connect(self.on_item_expanded)
        self.ignore_item_changed = False

    def load_project(self, path, ignore_patterns, file_types):
        self.current_path = path
        self.ignore_patterns = ignore_patterns
        self.file_types = file_types
        self.clear()
        self._populate_tree(path, self.invisibleRootItem())

    def _populate_tree(self, path, parent):
        for entry in FileSystem.get_directory_contents(path, self.ignore_patterns):
            if self.file_types and entry['type'] == 'file':
                if not any(entry['name'].lower().endswith(f".{ft.lower()}") for ft in self.file_types):
                    continue

            item = QTreeWidgetItem(parent)
            item.setText(0, entry['name'])
            item.setData(0, Qt.ItemDataRole.UserRole, entry['full_path'])
            
            if entry['type'] == 'directory':
                item.setCheckState(0, Qt.CheckState.Unchecked)
                # Add dummy item to show expansion arrow
                QTreeWidgetItem(item)
            else:
                item.setCheckState(0, Qt.CheckState.Unchecked)
                file_info = get_file_info(entry['full_path'])
                item.setText(1, file_info['size'])
                item.setText(2, FileSystem.get_file_type(entry['full_path']))

    def on_item_changed(self, item, column):
        if self.ignore_item_changed or column != 0:
            return

        self.ignore_item_changed = True
        self.update_children(item)
        self.update_parents(item)
        self.ignore_item_changed = False

    def on_item_expanded(self, item):
        if item.childCount() == 1 and item.child(0).text(0) == "":
            self.load_children(item)

    def load_children(self, item):
        item.takeChild(0)  # Remove dummy item
        path = item.data(0, Qt.ItemDataRole.UserRole)
        self._populate_tree(path, item)

    def update_children(self, item):
        if item.childCount() == 1 and item.child(0).text(0) == "":
            self.load_children(item)
        
        check_state = item.checkState(0)
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, check_state)

    def update_parents(self, item):
        parent = item.parent()
        while parent and parent != self.invisibleRootItem():
            child_states = [parent.child(i).checkState(0) for i in range(parent.childCount())]
            if all(state == Qt.CheckState.Checked for state in child_states):
                parent.setCheckState(0, Qt.CheckState.Checked)
            elif all(state == Qt.CheckState.Unchecked for state in child_states):
                parent.setCheckState(0, Qt.CheckState.Unchecked)
            else:
                parent.setCheckState(0, Qt.CheckState.PartiallyChecked)
            parent = parent.parent()

    def get_selected_files(self):
        return self._get_checked_files(self.invisibleRootItem())

    def _get_checked_files(self, parent):
        checked_files = []
        for i in range(parent.childCount()):
            item = parent.child(i)
            if item.checkState(0) in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked):
                if item.childCount() == 0:  # It's a file
                    checked_files.append(item.data(0, Qt.ItemDataRole.UserRole))
                else:  # It's a directory
                    checked_files.extend(self._get_checked_files(item))
        return checked_files