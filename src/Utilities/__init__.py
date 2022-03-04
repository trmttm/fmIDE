import os
import shutil
import sys
from typing import Tuple

import os_identifier

from . import geometry

if os_identifier.is_windows:
    folder_save_file = desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_documents = documents = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
else:
    folder_save_file = desktop = os.path.expanduser('~/Desktop/')
    folder_documents = documents = os.path.expanduser('~/Documents/')


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # for PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return f'{os.getcwd()}/{relative_path.replace(".", "")}'


cwd = resource_path('src')

path_save = desktop

lines_intersect = geometry.lines_intersect
point_in_rectangle = geometry.point_in_rectangle
line_intersect_rectangle = geometry.line_intersect_rectangle
get_nearest_points = geometry.get_nearest_points
get_rectangle_edges = geometry.get_rectangle_edges


def remove_file(file_path):
    os.remove(file_path)


def remove_file_or_directory(path):
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


def is_number(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except TypeError:
        return False
    except ValueError:
        return False


def convert_to_number_if_possible(s: str):
    if is_number(s):
        if '.' in s:
            return float(s)
        else:
            return int(s)
    elif s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        return s


def comma_separate_string_value(value, format_code: str = ''):
    value = str(value)
    if '.' in value:
        value = format(float(value), f',{format_code}')
    else:
        value = format(int(value), f',{format_code}')
    return value


def swap_tuple_data(destination: int, index_: int, data: tuple) -> tuple:
    total_datas = len(data)
    is_moving_up = destination <= index_
    mylist = list(data)

    if destination == -1:
        mylist += [mylist[index_]]
        del mylist[index_]
    elif is_moving_up:
        mylist.insert(destination, mylist[index_])
        del mylist[index_ + 1]
    else:
        if destination >= total_datas:
            mylist.insert(destination - total_datas, mylist[index_])
            del mylist[index_ + 1]
        else:
            mylist.insert(destination + 1, mylist[index_])
            del mylist[index_]
    return tuple(mylist)


def get_final_destinations_after_sorting(indexes: tuple, number_of_elements: int, shift: int) -> Tuple[tuple, tuple]:
    if (0 in indexes) and (shift < 0):  # Stop at the top
        new_destinations = indexes
    elif (number_of_elements - 1 in indexes) and (0 < shift):  # Stop at the bottom
        new_destinations = indexes
    else:
        new_destinations_list = []

        if shift > 0:
            indexes = tuple(reversed(indexes))

        for index_ in indexes:
            destination = index_ + shift
            if destination == -1:
                final_destination = number_of_elements - 1
            elif destination >= number_of_elements:
                final_destination = destination - number_of_elements
            elif destination < -1:
                final_destination = destination + 1
            else:
                final_destination = destination
            new_destinations_list.append(final_destination)

        new_destinations = tuple(new_destinations_list)
    return indexes, new_destinations


def move_tuple_element(existing_data_tuple: tuple, index_: int, destination: int) -> tuple:
    new_data_list = list(existing_data_tuple)
    if index_ < destination:
        new_data_list.insert(destination + 1, new_data_list[index_])
        del new_data_list[index_]
    elif destination < index_:
        new_data_list.insert(destination, new_data_list[index_])
        del new_data_list[index_ + 1]
    new_data = tuple(new_data_list)
    return new_data


def remove_item_from_tuple(existing_data, what_to_remove) -> tuple:
    new_data_list = []
    for a in existing_data:
        if a != what_to_remove:
            new_data_list.append(a)
    new_data = tuple(new_data_list)
    return new_data


def remove_item_from_tuple_by_index(existing_data, indexes):
    new_data_list = []
    for n, command in enumerate(existing_data):
        if n not in indexes:
            new_data_list.append(command)
    new_data = tuple(new_data_list)
    return new_data


def sort_lists(list_sorter, list_sorted) -> Tuple[list, list]:
    zipped_lists = zip(list_sorter, list_sorted)
    try:
        list_sorter_without_duplicate = [i + 0.0001 * n for (n, i) in enumerate(list_sorter)]
    except TypeError:
        list_sorter_without_duplicate = list_sorter

    try:
        sorted_pairs = sorted(zipped_lists)
    except TypeError:
        sorted_pairs = sorted(zip(list_sorter_without_duplicate, list_sorted))
    tuples = zip(*sorted_pairs)
    try:
        list_sorter, list_sorted = [list(tuple_) for tuple_ in tuples]
    except ValueError:
        list_sorter, list_sorted = [], []
    return list_sorter, list_sorted


def values_tuple_to_values_str(values, decimal: int = None):
    if values is None:
        return ''
    if decimal is not None:
        values = tuple(float(round(value, decimal)) for value in values)
    else:
        values = tuple(float(value) for value in values)
    return ','.join(str(values).split(',')).strip('(').strip(')')


def get_tuple_and_destinations_after_shifting_elements(existing_data_tuple, indexes, shift):
    number = len(existing_data_tuple)
    indexes_sorted, destinations = get_final_destinations_after_sorting(indexes, number, shift)
    new_data = existing_data_tuple
    for index_, destination in zip(indexes_sorted, destinations):
        new_data = move_tuple_element(existing_data_tuple, index_, destination)
        existing_data_tuple = new_data
    return destinations, new_data


def str_to_int(text, if_error) -> int:
    try:
        digits = int(text)
    except ValueError:
        digits = if_error
    return digits


def str_to_float(text, if_error) -> float:
    try:
        digits = float(text)
    except ValueError:
        digits = if_error
    return digits


def create_folder(path):
    try:
        os.mkdir(path)
        feedback = 'success'
    except FileExistsError:
        feedback = f'success'
    except OSError:
        feedback = f'Cannot create folder there! {path}'
    return feedback


def is_directory(path) -> bool:
    return os.path.isdir(path)
