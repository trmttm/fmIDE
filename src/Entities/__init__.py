from typing import Iterable

from . import RPE
from .AccountOrder import AccountOrder
from .AccountOrder import Blank
from .AccountOrders import AccountOrders
from .Configurations import Configurations
from .Connection import Connections
from .ConnectionIDs import ConnectionIDs
from .Format import Format
from .InputDecimals import InputDecimals
from .InputRanges import InputRanges
from .InputValues import InputValues
from .Line import Lines
from .NumberFormat import NumberFormat
from .RectangleSelector import RectangleSelectors
from .Selection import Selection
from .Selections import Selections
from .Shape import Shapes
from .ShapeFormat import ShapeFormat
from .UnitOfMeasure import UnitOfMeasure
from .VerticalAccounts import VerticalAccounts
from .WorkSheetRelationship import WorksheetRelationship
from .Worksheets import Worksheets
from .commands import Commands
from .copied_commands import CopiedCommands


class Entities:
    def __init__(self):
        self._connections = Connections()
        self._selection = Selection()
        self._shapes = Shapes()
        self._rectangle_selector = RectangleSelectors()
        self._line = Lines()
        self._account_order = AccountOrder()
        self._account_orders = AccountOrders()
        self._selections = Selections()
        self._worksheets = Worksheets()
        self._configurations = Configurations()
        self._input_values = InputValues()
        self._input_ranges = InputRanges()
        self._input_decimals = InputDecimals()
        self._connection_ids = ConnectionIDs()
        self._format = Format()
        self._number_format = NumberFormat()
        self._vertical_accounts = VerticalAccounts()
        self._commands = Commands()
        self._copied_commands = CopiedCommands()
        self._shape_format = ShapeFormat()
        self._worksheet_relationship = WorksheetRelationship()

        self._unit_of_measure = UnitOfMeasure()
        self._blank = Blank()

    @property
    def connections(self) -> Connections:
        return self._connections

    @property
    def shapes(self) -> Shapes:
        return self._shapes

    @property
    def rectangle_selector(self) -> RectangleSelectors:
        return self._rectangle_selector

    @property
    def lines(self) -> Lines:
        return self._line

    @property
    def account_order(self) -> AccountOrder:
        return self._account_orders.data[self._worksheets.selected_sheet]

    @property
    def selection(self) -> Selection:
        return self._selections.data[self._worksheets.selected_sheet]

    @property
    def worksheets(self) -> Worksheets:
        return self._worksheets

    @property
    def account_orders(self) -> AccountOrders:
        return self._account_orders

    @property
    def selections(self) -> Selections:
        return self._selections

    @property
    def configurations(self) -> Configurations:
        return self._configurations

    @property
    def input_values(self) -> InputValues:
        return self._input_values

    @property
    def input_ranges(self) -> InputRanges:
        return self._input_ranges

    @property
    def input_decimals(self) -> InputDecimals:
        return self._input_decimals

    @property
    def connection_ids(self) -> ConnectionIDs:
        return self._connection_ids

    @property
    def format(self) -> Format:
        return self._format

    @property
    def number_format(self) -> NumberFormat:
        return self._number_format

    @property
    def vertical_accounts(self) -> VerticalAccounts:
        return self._vertical_accounts

    @property
    def commands(self) -> Commands:
        return self._commands

    @property
    def copied_commands(self) -> CopiedCommands:
        return self._copied_commands

    @property
    def shape_format(self) -> ShapeFormat:
        return self._shape_format

    @property
    def worksheet_relationship(self) -> WorksheetRelationship:
        return self._worksheet_relationship

    @property
    def unit_of_measure(self) -> UnitOfMeasure:
        return self._unit_of_measure

    @property
    def blank(self) -> Blank:
        return self._blank

    @property
    def rpe(self) -> RPE:
        return RPE

    def add_new_worksheet(self, sheet_name: str):
        sheet_name = self._worksheets.get_valid_sheet_name(sheet_name)
        self._account_orders.create_new_account_order(sheet_name, AccountOrder())
        self._selections.create_new_selection(sheet_name, Selection())
        self._worksheets.add_new_worksheet(sheet_name)

    def change_selected_sheet_name(self, sheet_name: str):
        if sheet_name in self._worksheets.sheet_names:
            return
        self._selections.change_sheet_name(self._worksheets.selected_sheet, sheet_name)
        self._account_orders.change_sheet_name(self._worksheets.selected_sheet, sheet_name)
        self._worksheets.change_selected_sheet_name(sheet_name)

    def add_sheet_content(self, sheet_name, content, account_order_negative_list: Iterable):
        self.add_sheet_contents(sheet_name, (content,), account_order_negative_list)

    def add_sheet_contents(self, sheet_name, contents: Iterable, account_order_negative_list: Iterable):
        self._worksheets.add_sheet_contents(sheet_name, contents)

        account_order = self._account_orders.get_account_order(sheet_name)
        contents_to_add_to_account_order = tuple(c for c in contents if c not in account_order_negative_list)
        account_order.add_elements_to_last(contents_to_add_to_account_order)

        selection = self._selections.get_selection(sheet_name)
        selection.select_shapes(tuple({'shape_id': shape_id} for shape_id in contents))

    def remove_sheet_content(self, sheet_name, content):
        self.remove_sheet_contents(sheet_name, (content,))

    def remove_sheet_contents(self, sheet_name, contents: Iterable):
        self._worksheets.remove_sheet_contents(sheet_name, contents)

        account_order = self._account_orders.get_account_order(sheet_name)
        account_order.remove_accounts(contents)

        selection = self._selections.get_selection(sheet_name)
        selection.unselect_shapes(tuple({'shape_id': shape_id} for shape_id in contents))

    def delete_selected_sheet(self):
        selected_sheet = self._worksheets.selected_sheet
        self._account_orders.delete_account_order(selected_sheet)
        self._selections.delete_selection(selected_sheet)
        self._worksheets.delete_selected_sheet()

    def delete_a_sheet(self, sheet_name: str):
        self._account_orders.delete_account_order(sheet_name)
        self._selections.delete_selection(sheet_name)
        self._worksheets.delete_a_sheet(sheet_name)
