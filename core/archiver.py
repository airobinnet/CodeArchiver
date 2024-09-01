from core.file_system import FileSystem
from utils.helpers import get_relative_path

class Archiver:
    def __init__(self):
        self.project_path = ""

    def set_project_path(self, path):
        self.project_path = path

    def generate_content(self, selected_files):
        content = []
        for file_path in selected_files:
            relative_path = get_relative_path(file_path, self.project_path)
            content.append(f"--- {relative_path} ---\n")
            if not FileSystem.is_binary_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content.append(f.read())
                except Exception as e:
                    content.append(f"Error reading file: {str(e)}")
            else:
                content.append("[Binary file content not shown]")
            content.append("\n\n")
        return "".join(content)