import json
import sys

import Utilities
from Utilities.Memento import Memento
from fmIDE import instantiate_app
from src.Entities.AccountOrder import AccountOrder
from src.Entities.AccountOrder import Blank
from src.Entities.Selection import Selection

json_str = sys.stdin.readline()
data = json.loads(json_str)


def clean_account_order_data(data):
    return tuple(ao if str(ao).lower() != "blank" else Blank() for ao in data)


def create_worksheet_to_account_order(worksheets_to_account_order_data):
    worksheet_to_account_order = {}
    for sheet_name, account_order_data in worksheets_to_account_order_data.items():
        new_account_order = AccountOrder()
        new_account_order.set_data(clean_account_order_data(account_order_data))
        worksheet_to_account_order[sheet_name] = new_account_order
    return worksheet_to_account_order


def create_worksheet_to_selections(worksheets_to_selection_data):
    worksheet_to_selection = {}
    for sheet_name, selection_data in worksheets_to_selection_data.items():
        new_selection = Selection()
        new_selection.set_data(set(selection_data))
        worksheet_to_selection[sheet_name] = new_selection
    return worksheet_to_selection


# Data passed from JavaScript
connections_passed = data.get("connections", [])
selection_passed = data.get("selection", [])


def convert_key_to_int(dict_data):
    shapes_keys = tuple(int(key) if Utilities.is_number(key) else key for key in dict_data.keys())
    shapes_values = tuple(v for v in dict_data.values())
    return dict(zip(shapes_keys, shapes_values))


def convert_key_str_null_to_none(dict_data):
    shapes_keys = tuple(None if str(key) in ['null', 'None'] else key for key in dict_data.keys())
    shapes_values = tuple(v for v in dict_data.values())
    return dict(zip(shapes_keys, shapes_values))


shapes_passed = convert_key_to_int(data.get("shapes", {}))

account_order_passed = data.get("account_order", [])
worksheets_to_account_order_passed = data.get("worksheets_to_account_order", {})
worksheets_passed = tuple(worksheets_to_account_order_passed.keys())
worksheets_to_selections_passed = data.get("worksheets_to_selection", {})
worksheets_data_passed = data.get("worksheets_data", {})
configuration_passed = data.get("configuration", {})
input_values_passed = convert_key_to_int(data.get("input_values", {}))
input_ranges_passed = convert_key_to_int(data.get("input_ranges", {}))
connection_ids_passed = {
    '_key_connection_ids': convert_key_to_int(data.get("connection_ids", {})),
    '_key_partner_plugs': convert_key_to_int(data.get("plugs", {})),
    '_key_partner_sockets': convert_key_to_int(data.get("sockets", {})),
}
format_passed = convert_key_str_null_to_none(convert_key_to_int(data.get("formats", {})))
number_format_passed = convert_key_str_null_to_none(data.get("number_format", {}))
uom_passed = convert_key_to_int(data.get("uom", {}))
input_decimals_passed = convert_key_to_int(data.get("decimals", {}))

state = [
    set(tuple(c) for c in connections_passed),
    set(selection_passed),
    shapes_passed,
    {},
    {},
    clean_account_order_data(account_order_passed),
    create_worksheet_to_account_order(worksheets_to_account_order_passed),
    create_worksheet_to_selections(worksheets_to_selections_passed),
    worksheets_data_passed,
    configuration_passed,
    input_values_passed,
    input_ranges_passed,
    connection_ids_passed,
    format_passed,
    number_format_passed,
    {},
    (),
    (),
    input_decimals_passed,
    {'fill': {}},
    uom_passed,
    {},
    set()
]

app = instantiate_app()
memento = Memento(state)
app.interactor.load_memento(memento)
app.interactor.export_excel('spreadsheet from JS.xlsx', "/Users/yamaka/Desktop/")
print("/Users/yamaka/Desktop/spreadsheet from JS.xlsx")
