import os
import fnmatch

class FileSystem:
    DEFAULT_IGNORE_PATTERNS = [
        '.git', '.venv', 'venv', 'node_modules', '__pycache__',
        '*.pyc', '*.pyo', '*.pyd', '*.db', '*.sqlite3', '*.log', '*.tmp',
        '.DS_Store', 'Thumbs.db'
    ]

    @staticmethod
    def get_directory_contents(path, additional_ignore_patterns=None):
        ignore_patterns = FileSystem.DEFAULT_IGNORE_PATTERNS.copy()
        if additional_ignore_patterns:
            ignore_patterns.extend(additional_ignore_patterns)

        contents = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if any(fnmatch.fnmatch(entry.name, pattern) for pattern in ignore_patterns):
                        continue
                    
                    entry_type = 'directory' if entry.is_dir() else 'file'
                    contents.append({
                        'name': entry.name,
                        'full_path': entry.path,
                        'type': entry_type
                    })
        except PermissionError:
            print(f"Permission denied: {path}")
        except Exception as e:
            print(f"Error accessing {path}: {str(e)}")

        return sorted(contents, key=lambda x: (x['type'] == 'file', x['name'].lower()))

    @staticmethod
    def get_file_type(file_path):
        _, extension = os.path.splitext(file_path)
        return extension.lstrip('.') or 'No Extension'

    @staticmethod
    def is_binary_file(file_path):
        try:
            with open(file_path, 'tr') as check_file:
                check_file.read(1024)
                return False
        except:
            return True