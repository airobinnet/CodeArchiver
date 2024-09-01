import os
from datetime import datetime

def get_relative_path(file_path, root_path):
    return os.path.relpath(file_path, root_path)

def format_file_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

def get_file_info(file_path):
    stat = os.stat(file_path)
    return {
        'size': format_file_size(stat.st_size),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    }

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)