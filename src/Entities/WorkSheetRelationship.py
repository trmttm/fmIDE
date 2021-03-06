from typing import Dict
from typing import List
from typing import Tuple

from .Observable import Observable
from .Observable import notify


class WorksheetRelationship(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[str, List[str]] = {}

    @property
    def data(self) -> dict:
        return self._data

    @notify
    def add_worksheet_parent_child_relationship(self, parent_sheet_name: str, child_sheet_name: str):
        if parent_sheet_name in self._data:
            self._data[parent_sheet_name].append(child_sheet_name)
        else:
            self._data[parent_sheet_name] = [child_sheet_name]

    @notify
    def remove_parent_worksheet(self, child_worksheet_name: str):
        parent_worksheet = self.get_parent_worksheet(child_worksheet_name)
        if parent_worksheet is not None:
            if child_worksheet_name in self._data[parent_worksheet]:
                self._data[parent_worksheet].remove(child_worksheet_name)
            if not self.get_children_sheet_names(parent_worksheet):
                del self._data[parent_worksheet]

    @property
    def sheet_name_to_parent(self) -> dict:
        child_to_parent = {}
        for parent_sheet_name, children_sheet_names in self._data.items():
            d = dict(zip(children_sheet_names, tuple(parent_sheet_name for _ in children_sheet_names)))
            child_to_parent.update(d)
        return child_to_parent

    @notify
    def clean_data(self):
        for parent_sheet_name in tuple(self._data.keys()):
            if self.get_children_sheet_names(parent_sheet_name) == ():
                self.remove_data(parent_sheet_name)

    def remove_data(self, sheet_name: str):
        if sheet_name in self._data:
            del self._data[sheet_name]
        self.remove_parent_worksheet(sheet_name)

    def get_children_sheet_names(self, parent_sheet_name: str) -> Tuple[str]:
        return tuple(self._data.get(parent_sheet_name, ()))

    def get_parent_worksheet(self, child_worksheet_name: str) -> str:
        return self.sheet_name_to_parent.get(child_worksheet_name, None)

    @property
    def all_parent_sheets(self) -> tuple:
        return tuple(self._data.keys())

    def has_a_parent(self, child_sheet_name: str) -> bool:
        return child_sheet_name in self.sheet_name_to_parent

    def is_a_parent(self, sheet_name: str) -> bool:
        if sheet_name not in self._data:
            return False
        if len(self._data.get(sheet_name, ())) == 0:
            return False
        return True

    @property
    def has_data(self) -> bool:
        return self._data != {}

    @notify
    def change_sheet_name(self, from_: str, to_: str):
        for parent_sheet_name in tuple(self._data.keys()):
            child_sheet_names = list(self.get_children_sheet_names(parent_sheet_name))
            if from_ == parent_sheet_name:
                self._data[to_] = child_sheet_names
                self.remove_data(parent_sheet_name)
            elif from_ in child_sheet_names:
                child_sheet_names.remove(from_)
                child_sheet_names.append(to_)
                self._data[parent_sheet_name] = child_sheet_names

    @notify
    def merge_data(self, data: dict, *_, **__):
        self._data.update(data)
