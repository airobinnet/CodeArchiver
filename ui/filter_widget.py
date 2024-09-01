from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QListWidget, QPushButton, QHBoxLayout)
from PyQt6.QtCore import pyqtSignal

class FilterWidget(QWidget):
    filter_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("File Types (comma-separated):"))
        self.file_types_input = QLineEdit()
        self.file_types_input.textChanged.connect(self.filter_changed.emit)
        layout.addWidget(self.file_types_input)

        layout.addWidget(QLabel("Ignore Patterns:"))
        self.ignore_list = QListWidget()
        layout.addWidget(self.ignore_list)

        input_layout = QHBoxLayout()
        self.add_ignore_input = QLineEdit()
        input_layout.addWidget(self.add_ignore_input)

        self.add_ignore_button = QPushButton("Add")
        self.add_ignore_button.clicked.connect(self.add_ignore_pattern)
        input_layout.addWidget(self.add_ignore_button)

        layout.addLayout(input_layout)

        self.remove_ignore_button = QPushButton("Remove Selected Pattern")
        self.remove_ignore_button.clicked.connect(self.remove_ignore_pattern)
        layout.addWidget(self.remove_ignore_button)

        # Add some default ignore patterns
        default_ignores = ['.git', '__pycache__', '*.pyc', '*.pyo', '*.pyd', 'build', 'dist']
        for pattern in default_ignores:
            self.ignore_list.addItem(pattern)

    def add_ignore_pattern(self):
        pattern = self.add_ignore_input.text().strip()
        if pattern:
            self.ignore_list.addItem(pattern)
            self.add_ignore_input.clear()
            self.filter_changed.emit()

    def remove_ignore_pattern(self):
        for item in self.ignore_list.selectedItems():
            self.ignore_list.takeItem(self.ignore_list.row(item))
        self.filter_changed.emit()

    def get_file_types(self):
        return [ft.strip() for ft in self.file_types_input.text().split(',') if ft.strip()]

    def get_ignore_patterns(self):
        return [self.ignore_list.item(i).text() for i in range(self.ignore_list.count())]