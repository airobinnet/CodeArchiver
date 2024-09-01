import fnmatch
import os

class Filters:
    @staticmethod
    def apply_file_type_filter(file_list, file_types):
        if not file_types:
            return file_list
        return [file for file in file_list if any(file.lower().endswith(f".{ft.lower()}") for ft in file_types)]

    @staticmethod
    def apply_ignore_patterns(file_list, ignore_patterns, root_path):
        if not ignore_patterns:
            return file_list
        
        filtered_list = []
        for file_path in file_list:
            relative_path = os.path.relpath(file_path, root_path)
            if not any(fnmatch.fnmatch(relative_path, pattern) for pattern in ignore_patterns):
                filtered_list.append(file_path)
        return filtered_list

    @staticmethod
    def apply_search_filter(file_list, search_term):
        if not search_term:
            return file_list
        return [file for file in file_list if search_term.lower() in os.path.basename(file).lower()]

    @staticmethod
    def apply_all_filters(file_list, file_types, ignore_patterns, search_term, root_path):
        filtered_list = Filters.apply_file_type_filter(file_list, file_types)
        filtered_list = Filters.apply_ignore_patterns(filtered_list, ignore_patterns, root_path)
        filtered_list = Filters.apply_search_filter(filtered_list, search_term)
        return filtered_list