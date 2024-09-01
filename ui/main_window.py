import os
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QWidget, QFileDialog, QLabel, QTextEdit, QSplitter,
                             QApplication)
from PyQt6.QtCore import Qt
from .file_tree_widget import FileTreeWidget
from .filter_widget import FilterWidget
from core.archiver import Archiver

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeArchiver")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Top section
        top_layout = QHBoxLayout()
        self.select_folder_button = QPushButton("Select Project Folder")
        self.select_folder_button.clicked.connect(self.select_folder)
        top_layout.addWidget(self.select_folder_button)

        self.status_label = QLabel("No project selected")
        self.status_label.setObjectName("status_label")
        top_layout.addWidget(self.status_label, 1)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setFixedHeight(100)
        self.layout.addWidget(top_widget)

        # Main content
        main_content = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: File tree and Filter widget
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.file_tree = FileTreeWidget()
        left_layout.addWidget(self.file_tree)
        
        self.filter_widget = FilterWidget()
        self.filter_widget.filter_changed.connect(self.apply_filters)
        left_layout.addWidget(self.filter_widget)
        
        main_content.addWidget(left_widget)
        
        # Output and buttons on the right
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setObjectName("output_text")
        right_layout.addWidget(self.output_text)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate Output")
        self.generate_button.clicked.connect(self.generate_output)
        button_layout.addWidget(self.generate_button)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)

        self.export_button = QPushButton("Export to File")
        self.export_button.clicked.connect(self.export_to_file)
        button_layout.addWidget(self.export_button)

        right_layout.addLayout(button_layout)
        
        main_content.addWidget(right_widget)

        # Set the initial sizes of the splitter
        main_content.setSizes([int(self.width() * 0.4), int(self.width() * 0.6)])

        self.layout.addWidget(main_content)

        self.archiver = Archiver()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.archiver.set_project_path(folder)
            self.status_label.setText(f"Project: {folder}")
            self.apply_filters()

    def apply_filters(self):
        if not self.archiver.project_path:
            return

        file_types = self.filter_widget.get_file_types()
        ignore_patterns = self.filter_widget.get_ignore_patterns()
        
        self.file_tree.load_project(self.archiver.project_path, ignore_patterns, file_types)
        self.status_label.setText(f"Filters applied. Ignore patterns: {len(ignore_patterns)}, File types: {len(file_types)}")

    def generate_output(self):
        selected_files = self.file_tree.get_selected_files()
        if not selected_files:
            self.status_label.setText("No files selected.")
            return

        content = self.archiver.generate_content(selected_files)
        self.output_text.setPlainText(content)
        self.status_label.setText("Output generated.")

    def copy_to_clipboard(self):
        content = self.output_text.toPlainText()
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            self.status_label.setText("Content copied to clipboard.")
        else:
            self.status_label.setText("No content to copy.")

    def export_to_file(self):
        content = self.output_text.toPlainText()
        if not content:
            self.status_label.setText("No content to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Archived Content", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.status_label.setText(f"Content saved to {file_path}")
        else:
            self.status_label.setText("Export cancelled.")