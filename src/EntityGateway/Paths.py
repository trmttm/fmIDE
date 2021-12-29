import os
import sys


def get_path(directory, file_name: str):
    try:
        path = directory / file_name
    except TypeError:
        path = f'{directory}{file_name}'
    return path


def get_proper_path_depending_on_development_or_distribution(relative_path):
    possible_overlap = relative_path.split('/')[0]
    folder_path = os.path.join(sys.path[0], relative_path)
    folder_path = remove_overlap(folder_path, possible_overlap)
    if not (os.path.exists(folder_path)):
        folder_path = f'{os.getcwd()}/{relative_path}'
    folder_path = remove_overlap(folder_path, possible_overlap)
    return folder_path


def remove_overlap(folder_path, possible_overlap):
    return folder_path.replace(f'{possible_overlap}/{possible_overlap}', possible_overlap)
