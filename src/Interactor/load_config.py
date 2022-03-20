import os

import Utilities


class LoadConfiguration:
    name = 'load_config_data'
    folder_name = 'fmIDE'
    _path = os.path.join(Utilities.folder_documents, folder_name, name)
    _recent_project_paths = '_recent_project_paths'
    _last_states = '_last_states'
    _quick_save_state = '_quick_save_state'
    _opened_project = '_opened_project'

    def __init__(self):
        self._data = {
            self._recent_project_paths: [],
            self._last_states: {},
            self._quick_save_state: {},
            self._opened_project: None,
        }

    def set_opening_project(self, project_path):
        self._data[self._opened_project] = project_path
        self.add_to_recent_project_paths(project_path)

    @property
    def config_file_path(self):
        return self._path

    @property
    def opening_project(self):
        return self._data.get(self._opened_project, None)

    @property
    def last_project_path(self):
        paths = self.recent_project_paths
        return paths[0] if len(paths) > 0 else None

    @property
    def recent_project_paths(self) -> list:
        return self._data[self._recent_project_paths]

    def add_to_recent_project_paths(self, project_path):
        try:
            self.recent_project_paths.remove(project_path)
        except ValueError:
            pass
        self.recent_project_paths.insert(0, project_path)

    @property
    def last_state(self):
        project = self.opening_project
        return self._data[self._last_states].get(project, None)

    def save_last_state(self, memento):
        project = self.opening_project
        self._data[self._last_states][project] = memento

    def quick_save(self, memento):
        project = self.opening_project
        self._data[self._quick_save_state][project] = memento

    def quick_save_state(self, memento):
        project = self.opening_project
        self._data[self._quick_save_state][project] = memento

    @property
    def load_config_data(self):
        return self._data

    def restore(self, data):
        self._data = data

        recent_paths = tuple(p for p in data[self._recent_project_paths])
        last_states = tuple(data[self._last_states].keys())
        quick_save_states = tuple(data[self._quick_save_state].keys())
        opened_project = (data[self._opened_project]),
        all_paths_in_data = set(recent_paths + last_states + quick_save_states + opened_project)
        try:
            all_paths_in_data.remove(None)
        except KeyError:
            pass
        for path in all_paths_in_data:
            if not os.path.exists(path):
                self.remove_project(path)

    def clear(self):
        self.__init__()

    def remove_project(self, project_path):
        try:
            self._data[self._recent_project_paths].remove(project_path)
        except ValueError:
            pass

        try:
            del self._data[self._last_states][project_path]
        except KeyError:
            pass

        try:
            del self._data[self._quick_save_state][project_path]
        except KeyError:
            pass
