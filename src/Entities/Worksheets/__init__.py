import copy
from typing import Dict
from typing import Iterable

import Utilities

from ..Observable import Observable
from ..Observable import notify


class Worksheets(Observable):
    _sheet_data = '_sheet_data'
    _selected = 'selected'

    def __init__(self):
        Observable.__init__(self)
        self._data = {
            self._selected: '',
            self._sheet_data: {},
        }

    @property
    def data(self) -> dict:
        return self._data

    @property
    def sheet_names(self) -> tuple:
        return tuple(self._data[self._sheet_data].keys())

    @property
    def selected_sheet(self):
        try:
            return self._data[self._selected]
        except KeyError:
            return None

    @property
    def selected_sheet_contents(self) -> tuple:
        return self.get_sheet_contents(self.selected_sheet)

    @property
    def shape_id_to_sheet_name_dict(self) -> dict:
        d = {}
        for sheet_name, contents in self._data[self._sheet_data].items():
            for content in contents:
                d[content] = sheet_name
        return d

    @property
    def sheet_name_to_sheet_contents(self) -> Dict[str, set]:
        return copy.deepcopy(self._data[self._sheet_data])

    def get_sheet_name_by_index(self, index: int):
        try:
            return self.sheet_names[index]
        except IndexError:
            return None

    def get_valid_sheet_name(self, sheet_name) -> str:
        if sheet_name is None:
            n = 1
            sheet_name = f'Sheet{n}'
            while sheet_name in self._data[self._sheet_data]:
                n += 1
                sheet_name = f'Sheet{n}'
        return sheet_name

    def get_sheet_contents(self, sheet_name) -> tuple:
        try:
            return tuple(sorted(self._data[self._sheet_data][sheet_name]))
        except TypeError:
            sortables = []
            strings = []
            for content in self._data[self._sheet_data][sheet_name]:
                if Utilities.is_number(content):
                    sortables.append(content)
                else:
                    strings.append(content)
            sortables_sorted = tuple(sorted(sortables))
            strings_sorted = tuple(sorted(strings))
            return sortables_sorted + strings_sorted

    def is_empty(self, sheet_name) -> bool:
        if sheet_name in self._data[self._sheet_data]:
            return self._data[self._sheet_data][sheet_name] == set()
        return False

    def get_worksheet_of_an_account(self, shape_id):
        for sheet_name, contents in self._data[self._sheet_data].items():
            if shape_id in contents:
                return sheet_name
        return None

    @notify
    def select_sheet(self, sheet_name: str):
        self._data[self._selected] = sheet_name

    @notify
    def add_new_worksheet(self, sheet_name=None):
        sheet_name = self.get_valid_sheet_name(sheet_name)
        self._data[self._sheet_data][sheet_name] = set()
        self._data[self._selected] = sheet_name

    def delete_selected_sheet(self):
        self.delete_a_sheet(self.selected_sheet)

    @notify
    def delete_a_sheet(self, sheet_name: str):
        if len(self.sheet_names) == 1:
            return
        n = self.get_sheet_position(sheet_name)
        next_selection = self.sheet_names[n - 1]
        self.select_sheet(next_selection)
        del self._data[self._sheet_data][sheet_name]

    def get_sheet_position(self, sheet_name: str) -> int:
        if sheet_name in self.sheet_names:
            n = self.sheet_names.index(sheet_name)
            return n

    def add_sheet_contents(self, sheet_name, contents: Iterable):
        for content in contents:
            self.add_sheet_content(sheet_name, content)

    @notify
    def add_sheet_content(self, sheet_name, content):
        sheet_contents: set = self._data[self._sheet_data][sheet_name]
        sheet_contents.add(content)

    def remove_sheet_contents(self, sheet_name, contents: Iterable):
        for content in contents:
            self.remove_sheet_content(sheet_name, content)

    @notify
    def remove_sheet_content(self, sheet_name, content):
        sheet_contents: set = self._data[self._sheet_data][sheet_name]
        try:
            sheet_contents.remove(content)
        except (IndexError, KeyError):
            pass

    @notify
    def change_selected_sheet_name(self, new_sheet_name: str):
        old_sheet_name = self.selected_sheet

        self._data[self._sheet_data][new_sheet_name] = self._data[self._sheet_data][old_sheet_name]
        del self._data[self._sheet_data][old_sheet_name]

    @notify
    def add_contents_to_selected_sheet(self, contents: Iterable):
        self.add_sheet_contents(self.selected_sheet, contents)

    @notify
    def change_sheet_order(self, indexes: tuple, shift: int) -> tuple:
        current_sheet_data = self._data[self._sheet_data]
        new_sheet_data = {}
        current_sheet_names_order = tuple(current_sheet_data.keys())
        args = current_sheet_names_order, indexes, shift
        destinations, new_sheet_names_order = Utilities.get_tuple_and_destinations_after_shifting_elements(*args)
        for sheet_name in new_sheet_names_order:
            new_sheet_data[sheet_name] = set(self.get_sheet_contents(sheet_name))
        self._data[self._sheet_data] = new_sheet_data
        return destinations

    @notify
    def insert_sheets(self, sheets_to_insert: Iterable, location: int):
        new_sheet_data = {}
        for n, (sheet_name, sheet_data) in enumerate(self._data[self._sheet_data].items()):
            if n == location:
                for sheet_to_insert in sheets_to_insert:
                    new_sheet_data[sheet_to_insert] = set(self.get_sheet_contents(sheet_to_insert))
            if sheet_name not in sheets_to_insert:
                new_sheet_data[sheet_name] = sheet_data
        self._data[self._sheet_data] = new_sheet_data

    @notify
    def remove_contents_from_respective_sheets(self, contents: Iterable):
        shape_id_to_sheet_name = self.shape_id_to_sheet_name_dict
        for content in contents:
            if content in shape_id_to_sheet_name:
                self.remove_sheet_content(shape_id_to_sheet_name[content], content)

    @notify
    def merge_data(self, worksheets_data: dict, shape_id_converter: dict):
        self.select_sheet(worksheets_data[self._selected])
        sheet_data: Dict[str, set] = worksheets_data[self._sheet_data]

        for sheet_name, contents in sheet_data.items():
            if sheet_name not in self._data[self._sheet_data]:
                self._data[self._sheet_data][sheet_name] = set()
            for content in contents:
                safe_content_id = shape_id_converter[content]
                self._data[self._sheet_data][sheet_name].add(safe_content_id)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        sheet_data: Dict[str, set] = self._data[self._sheet_data]

        for sheet_name, contents in sheet_data.items():
            if old_shape_id in contents:
                self.remove_sheet_content(sheet_name, old_shape_id)
                self.add_sheet_content(sheet_name, new_shape_id)
