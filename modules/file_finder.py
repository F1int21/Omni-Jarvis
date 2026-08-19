# modules/file_finder.py
import os
import re

def find_files_by_name(root_dirs: list, pattern: str, max_results: int = 10) -> list:
    found = []
    regex = re.compile(re.escape(pattern), re.IGNORECASE)
    for root in root_dirs:
        if not os.path.exists(root):
            continue
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                if len(found) >= max_results:
                    break
                for fname in filenames:
                    if regex.search(fname):
                        full_path = os.path.join(dirpath, fname)
                        found.append(full_path)
                        if len(found) >= max_results:
                            break
        except PermissionError:
            continue
    return found