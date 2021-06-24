import os
import ntpath
from typing import Pattern


def change_rel_path(old_path, new_path, rel_file_path):
    """
    Return changed relative path of a rel_file_path from old_path
    to new_path.
    """
    assert isinstance(old_path, str)
    assert isinstance(new_path, str)
    assert isinstance(rel_file_path, str)

    old_dir = os.path.dirname(old_path)
    full_path = os.path.normpath(os.path.join(old_dir, rel_file_path))

    full_path = os.path.relpath(full_path, new_path)
    return full_path


def get_files(directory, pattern=None, exclude=None, relative_path=False):
    """
    Return list of files in a given directory that meet up given
    regex pattern. By default it does not include files in subdirectories.
    If subdirectories should also be included, those that are listed
    in exclude list, will be ommited.
    """
    assert isinstance(directory, str)
    if pattern is not None:
        assert isinstance(pattern, Pattern)

    result = []
    for root, dirs, files in os.walk(directory, topdown=True):
        if exclude is not None:
            dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if pattern is not None:
                match = pattern.match(file)
                if match is None:
                    continue
            abs_path = os.path.join(root, file)
            if relative_path:
                result.append(os.path.relpath(abs_path, directory))
            else:
                result.append(abs_path)
    return result


def path_leaf(path):
    """
    Return extracted file/dir name from path.
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
