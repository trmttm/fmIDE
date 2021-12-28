import os
from os import listdir
from os.path import isfile
from os.path import join


def get_file_names_in_a_folder(path, exceptions: tuple = ()):
    only_files = sorted(f for f in listdir(path) if isfile(join(path, f)) if f not in exceptions)
    return list(only_files)


class FileSystemIO:
    def __init__(self):
        self._root_path = os.getcwd()

    @staticmethod
    def get_file_names(folder_path, negative_list=()) -> list:
        return get_file_names_in_a_folder(folder_path, negative_list)
