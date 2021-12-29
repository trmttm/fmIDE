import distutils.errors
import os
import pickle
import subprocess
import sys
from distutils.dir_util import copy_tree

import os_identifier
from interface_gateway_fm import GateWayABC

from src.Utilities import Memento
from .CommandState import CommandState
from .FilesSystemIO import FileSystemIO
from .Paths import get_path
from .StatesIOFiles import StateIOFile
from .StatesIOMemory import StatesIOMemory
from .SystemState import SystemState
from .. import Utilities
from ..Entities import Entities


class GateWays(GateWayABC):
    negative_list = ('.DS_Store', 'pickle_for_unit_test', '__init__.py', '__pycache__')
    _relative_path_to_pickles = 'src/Pickles'
    _relative_path_to_commands = 'src/PicklesCommands'
    _templates_directory = 'Templates'
    _commands_directory = 'Macros'
    _canvas_image_directory = 'canvas_images'

    def __init__(self, entities: Entities):
        GateWayABC.__init__(self, entities)

        self._package_pickles = 'src.Pickles'
        self._package_pickles_commands = 'src.PicklesCommands'

        self._system_state = system_state = SystemState(entities)
        caretaker = Utilities.Memento.Caretaker(system_state)
        caretaker_command = Utilities.Memento.Caretaker(CommandState(entities))

        self._entities = entities
        self._states_io_memory = StatesIOMemory(caretaker)
        self._states_io_file_system = StateIOFile(caretaker)
        self._command_io_file_system = StateIOFile(caretaker_command)
        self._file_system_io = FileSystemIO()

        self._project_folder = None
        self._test_path_pickles = None

    def embed_resources_to_project_folder(self, directory_to):
        path_pickles = get_proper_path_depending_on_development_or_distribution(self._relative_path_to_pickles)
        path_commands = get_proper_path_depending_on_development_or_distribution(self._relative_path_to_commands)
        try:
            copy_tree(path_pickles, os.path.join(directory_to, self._templates_directory))
            copy_tree(path_commands, os.path.join(directory_to, self._commands_directory))
        except distutils.errors.DistutilsFileError:
            return
        for item in self.negative_list:
            Utilities.remove_file_or_directory(os.path.join(directory_to, self._templates_directory, item))
            Utilities.remove_file_or_directory(os.path.join(directory_to, self._commands_directory, item))

    def get_resource(self, file_name, package):
        return self._states_io_file_system.get_resource(file_name, package)

    def get_resource_pickle_load_by_package(self, file_name, package):
        return self._states_io_file_system.get_resource_pickle_load_by_package(package, file_name)

    def get_resource_pickle_load_by_abs_path(self, abs_path):
        loaded_pickle = self._states_io_file_system.get_resource_pickle_load_by_file_path(abs_path)
        return loaded_pickle

    @property
    def embedded_templates(self):
        folder_path = get_proper_path_depending_on_development_or_distribution(self._relative_path_to_pickles)
        return self._file_system_io.get_file_names(folder_path, self.negative_list)

    @property
    def embedded_macros(self):
        folder_path = get_proper_path_depending_on_development_or_distribution(self._relative_path_to_commands)
        return self._file_system_io.get_file_names(folder_path)

    def set_project_folder(self, directory):
        self._project_folder = directory

    @property
    def project_folder(self):
        return self._project_folder

    @property
    def path_pickles(self):
        return f'{self.project_folder}/{self._templates_directory}/'

    @property
    def path_commands_pickles(self):
        return f'{self.project_folder}/{self._commands_directory}/'

    def change_path_pickles(self, directory: str):
        self._package_pickles = 'src.Tests.pickles'
        if directory[-1] != '/':
            directory += '/'
        self._test_path_pickles = directory

    def change_path_command_pickles(self, directory: str):
        if directory[-1] != '/':
            directory += '/'

    @property
    def entities(self) -> Entities:
        return self._entities

    def undo(self):
        self._states_io_memory.undo()

    def redo(self):
        self._states_io_memory.redo()

    def save_state(self, name: str) -> bool:
        if self.state_changed():
            self._states_io_memory.save_state(name)
            return True
        else:
            return False

    def load_state(self, memento):
        self._states_io_memory.load_state(memento)

    @property
    def save_result(self) -> str:
        return self._states_io_memory.save_result

    @property
    def save_file_result(self) -> str:
        return self._states_io_file_system.save_result

    def save_file(self, file_name: str):
        file_path = get_path(self.path_pickles, file_name)
        feedback = self._states_io_file_system.save_state(file_path)
        return feedback

    def save_commands_to_file(self, file_name: str):
        file_path = get_path(self.path_commands_pickles, file_name)
        feedback = self._command_io_file_system.save_state(file_path)
        return feedback

    def load_file(self, file_name: str):
        if self._test_path_pickles is not None:
            file_path = get_path(self._test_path_pickles, file_name)
            self._states_io_file_system.load_state_from_file_system(file_path)
            return

        try:
            relative_path = os.path.join(self._relative_path_to_pickles, file_name)
            file_path = get_proper_path_depending_on_development_or_distribution(relative_path)
            self._states_io_file_system.load_state_from_file_system(file_path)
        except AttributeError:
            self._states_io_file_system.load_state(file_name, self._package_pickles)

    def load_pickle(self, package, file_name):
        return self._states_io_file_system.load_state(file_name, package)

    def load_macro_file(self, file_name: str):
        self._command_io_file_system.load_state(file_name, self._package_pickles_commands)

    def merge_file(self, file_name: str):
        if self._test_path_pickles is not None:
            file_path = get_path(self._test_path_pickles, file_name)
            self._states_io_file_system.merge_state_from_file_system(file_path)
            return
        if self._project_folder is None:
            self._states_io_file_system.merge_state(file_name, self._package_pickles)
            return
        try:
            file_path = get_path(self.path_pickles, file_name)
            self._states_io_file_system.merge_state_from_file_system(file_path)
        except AttributeError:
            self._states_io_file_system.merge_state(file_name, self._package_pickles)

    def merge_macro_file(self, file_name: str):
        try:
            file_path = get_path(self.path_commands_pickles, file_name)
            self._command_io_file_system.merge_state_from_file_system(file_path)
        except AttributeError:
            self._command_io_file_system.merge_state(file_name, self._package_pickles_commands)

    def remove_template(self, file_name) -> str:
        return self._remove_pickle(self.path_pickles, file_name)

    def remove_macro(self, file_name) -> str:
        return self._remove_pickle(self.path_commands_pickles, file_name)

    def _remove_pickle(self, directory, file_name):
        if self._project_folder is not None:
            file_path = get_path(directory, file_name)
            Utilities.remove_file(file_path)
            feedback = 'success'
        else:
            feedback = "Can't delete non-project files."
        return feedback

    @property
    def pickle_file_names(self) -> list:
        try:
            user_files = self._file_system_io.get_file_names(self.path_pickles)
            return user_files
        except FileNotFoundError:
            return self.embedded_templates

    @property
    def pickle_macro_file_names(self) -> list:
        try:
            user_files = self._file_system_io.get_file_names(self.path_commands_pickles)
            return user_files
        except FileNotFoundError:
            user_files = None

        if user_files is not None:
            return user_files

        try:
            user_files = self.embedded_macros
        except FileNotFoundError:
            user_files = []
        return user_files

    def restore_state(self, entities: Entities, pickle_name: str):
        system_state = SystemState(entities)
        if self._project_folder is None:
            memento = self._states_io_file_system.get_memento(pickle_name, self._package_pickles)
            if memento is None:
                relative_path = os.path.join(self._relative_path_to_pickles, pickle_name)
                file_path = get_proper_path_depending_on_development_or_distribution(relative_path)
                memento = self._states_io_file_system.get_memento_from_file_system(file_path)
            if memento is not None:
                system_state.restore(memento)
            return

        file_path = get_path(self.path_pickles, pickle_name)
        memento = self._states_io_file_system.get_memento_from_file_system(file_path)
        try:
            system_state.restore(memento)
        except AttributeError:
            memento = self._states_io_file_system.get_memento(pickle_name, self._package_pickles)
            system_state.restore(memento)

    def save_all_sates_to_file(self, file_name='all states'):
        file_path = get_path(self.path_pickles, file_name)
        self._states_io_file_system.save_all_sates(file_path)

    def restore_all_states_from_file(self, file_name='all states'):
        self._states_io_file_system.restore_all_states(file_name, self._package_pickles)

    def reset(self, entities: Entities):
        project_folder = self.project_folder
        self.__init__(entities)
        self.set_project_folder(project_folder)

    def state_changed(self) -> bool:
        return self._system_state.state_changed()

    @property
    def current_state(self):
        return self._system_state.state

    def states_are_different(self, state_one, state_two) -> bool:
        return self._system_state.states_are_different(state_one, state_two)

    @staticmethod
    def open_file(file_path: str):
        if os_identifier.is_windows:
            subprocess.Popen(['start', file_path], shell=True)
        else:
            subprocess.call(('open', file_path))

    def save_object_as_pickle(self, file_name_abs_path, data):
        path = file_name_abs_path
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def create_project_folder(self, path) -> str:
        feedback = Utilities.create_folder(os.path.join(path, self._templates_directory))
        if feedback != 'success':
            return feedback
        feedback = Utilities.create_folder(os.path.join(path, self._commands_directory))
        if feedback != 'success':
            return feedback
        feedback = Utilities.create_folder(os.path.join(path, self._canvas_image_directory))
        if feedback != 'success':
            return feedback
        return 'success'

    @staticmethod
    def create_load_config_folder(folder_name, folder_key_word):
        folders = {'Documents': Utilities.folder_documents}
        new_folder_path = os.path.join(folders[folder_key_word], folder_name)
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)


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
