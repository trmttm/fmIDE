from typing import Callable

import Utilities
from interface_fm import BoundaryInABC
from interface_view import ViewABC
from stacker import Stacker
from stacker import widgets as w

frame_number = 0


class GUI:
    def __init__(self, parent, view: ViewABC, interactor: BoundaryInABC):
        self._parent = parent
        self._view = view
        self._interactor = interactor
        self._frame_number = 0

    def add_widgets(self):
        add_widgets(self._parent, self._view, self.switch_main_frame)

    def switch_main_frame(self, increment: int, switchable_frames, names: tuple, view: ViewABC):
        if increment > 0:
            self._frame_number = min(len(switchable_frames) - 1, self._frame_number + 1)
        else:
            self._frame_number = max(0, self._frame_number - 1)

        _switch_main_frame_implementation(increment, names, switchable_frames, view, self._frame_number, self._method)

    def _method(self, data: dict):
        method_injected(self._interactor, self._view, data)


def add_widgets(parent, view: ViewABC, switch_main_frame: Callable = None):
    if switch_main_frame is None:
        switch_main_frame = _switch_main_frame

    stacker = Stacker(parent)
    switchable_frames = []

    names = 'Banks', 'SG&A', 'Other Expense', 'Other Income', 'Product'

    stacker.vstack(
        w.FrameSwitcher('frame_switcher', stacker, switchable_frames).stackers(
            stacker.vstack(
                w.Label('label_frame0').text('Frame00'),
                _number_of(names[0], stacker, view),
                _number_of(names[1], stacker, view),
                _number_of(names[2], stacker, view),
                _number_of(names[3], stacker, view),
                _number_of(names[4], stacker, view),
                stacker.hstack(
                    w.Button('button_clear').text('Clear').command(lambda: _clear_entries(names, view, )).width(15),
                    w.Spacer(),
                ),
                w.Spacer(),
            ),
            stacker.vstack(),
            stacker.vstack(),
            stacker.vstack(),
            stacker.vstack(),
        ),
        stacker.hstack(
            w.Button('Back').text('Back<').command(lambda: switch_main_frame(-1, switchable_frames, names, view)),
            w.Spacer(),
            w.Button('Next').text('>Next').command(lambda: switch_main_frame(1, switchable_frames, names, view)),
        ),
    )
    view_model = stacker.view_model
    view.add_widgets(view_model)
    view.switch_frame(switchable_frames[frame_number])


def _switch_main_frame(increment: int, switchable_frames, names: tuple, view: ViewABC):
    global frame_number
    if increment > 0:
        frame_number = min(len(switchable_frames) - 1, frame_number + 1)
    else:
        frame_number = max(0, frame_number - 1)
    _switch_main_frame_implementation(increment, names, switchable_frames, view)


def _switch_main_frame_implementation(increment, names, switchable_frames, view: ViewABC, frame_number_passed=None,
                                      method: Callable = None):
    local_frame_number = frame_number_passed if frame_number_passed is not None else frame_number
    next_frame = switchable_frames[local_frame_number]
    if increment > 0:  # Keep user inputs if Back< button is pushed
        local_view_model = None
        if local_frame_number == 1:
            local_view_model = _create_frame_1_view_model(names, local_frame_number, next_frame, view)
        elif local_frame_number == 2:
            local_view_model = _create_frame_2_view_model(names, local_frame_number, next_frame, view)
        elif local_frame_number == 3:
            local_view_model = _create_frame_3_view_model(names, next_frame, view)
        elif local_frame_number == 4:
            data_structure = create_data_structure(names, view)
            # Execute injected method here
            if method is not None:
                method(data_structure)
                return
            else:
                print(data_structure)

        if local_view_model is not None:
            view.add_widgets(local_view_model)
    view.switch_frame(next_frame)


def _number_of(name: str, stacker, view: ViewABC, default_value=0):
    dv = default_value
    args = _get_entry_id(name), view, dv
    return stacker.hstack(
        w.Label(f'label_number_of_{name}').text(f'Number of {name}'),
        w.Button(f'button_number_of_{name}').text('-').width(1).command(lambda: _increment_entry(-1, *args)),
        w.Entry(_get_entry_id(name)).default_value(default_value).width(5),
        w.Button(f'button_number_of_{name}').text('+').width(1).command(lambda: _increment_entry(1, *args)),
    )


def _increment_entry(increment: int, entry: str, view: ViewABC, default_value=0):
    current_value = view.get_value(entry)
    if Utilities.is_number(current_value):
        current_value = int(current_value)
    else:
        current_value = default_value
    new_value = max(0, current_value + increment)
    view.set_value(entry, new_value)


def _clear_entries(names: tuple, view: ViewABC, default_value=0):
    for name in names:
        view.set_value(_get_entry_id(name), default_value)


def _get_entry_id(name) -> str:
    return f'entry_number_of_{name}'


def _get_entry_id2(name: str, n: int) -> str:
    return f'frame_1_entry_{name}_{n}'


def _frame1_each_page(stacker_, names: tuple, name: str, view: ViewABC, widget):
    w = widget
    number = int(view.get_value(_get_entry_id(name)))
    if name in (names[4],):
        return _input_product(name, number, stacker_, view, w)
    else:
        return stacker_.vstack_scrollable(*tuple(stacker_.vstack(
            stacker_.hstack(
                w.Label(f'{_lbl(name, n, "")}').text(f'{name}{n} Name').width(20),
                w.Entry(_get_entry_id2(name, n)).default_value(f'{name}{n}'),
            )
        ) for n in range(number)))


def _lbl(name, n_, post_fix):
    return f'frame_1_label_{name}_{n_}_{post_fix}'


def _get_entry_id_product_fixed_cost(name, n) -> str:
    return f'frame_1_entry_{name}_{n}_fixed_costs'


def _get_entry_id_product_variable_cost(name, n) -> str:
    return f'frame_1_entry_{name}_{n}_variable_costs'


def _get_entry_id_product_inventory_cost(name, n) -> str:
    return f'frame_1_entry_{name}_{n}_inventory_costs'


def _input_product(name, number_of_product, stacker_, view, w):
    e1 = _get_entry_id_product_fixed_cost
    e2 = _get_entry_id_product_variable_cost
    e3 = _get_entry_id_product_inventory_cost
    dv = 0
    return stacker_.vstack_scrollable(
        *tuple(
            stacker_.vstack(
                stacker_.hstack(
                    w.Label(f'{_lbl(name, n, "")}').text(f'{name}{n} Name').width(20),
                    w.Entry(_get_entry_id2(name, n)).default_value(f'{name}{n}'),
                ),
                stacker_.hstack(
                    w.Label(f'{_lbl(name, n, "fixed_costs")}').text(f'n fixed costs').width(20).align('e'),
                    w.Button(f'button_n_fixed_{name}_-_{n}').text('-').width(1).command(
                        lambda i=n: _increment_entry(-1, e1(name, i), view, dv)),
                    w.Entry(_get_entry_id_product_fixed_cost(name, n)).default_value(dv).width(5),
                    w.Button(f'button_n_fixed_{name}_+_{n}').text('+').width(1).command(
                        lambda i=n: _increment_entry(1, e1(name, i), view, dv)),
                ),
                stacker_.hstack(
                    w.Label(f'{_lbl(name, n, "variable_costs")}').text(f'n variable costs').width(20).align('e'),
                    w.Button(f'button_n_fixed_{name}_-_{n}').text('-').width(1).command(
                        lambda i=n: _increment_entry(-1, e2(name, i), view, dv)),
                    w.Entry(_get_entry_id_product_variable_cost(name, n)).default_value(dv).width(5),
                    w.Button(f'button_n_fixed_{name}_+_{n}').text('+').width(1).command(
                        lambda i=n: _increment_entry(1, e2(name, i), view, dv)),
                ),
                stacker_.hstack(
                    w.Label(f'{_lbl(name, n, "inventory_costs")}').text(f'n inventory costs').width(20).align('e'),
                    w.Button(f'button_n_fixed_{name}_-_{n}').text('-').width(1).command(
                        lambda i=n: _increment_entry(-1, e3(name, i), view, dv)),
                    w.Entry(_get_entry_id_product_inventory_cost(name, n)).default_value(dv).width(5),
                    w.Button(f'button_n_fixed_{name}_+_{n}').text('+').width(1).command(
                        lambda i=n: _increment_entry(1, e3(name, i), view, dv)),
                ),
            ) for n in range(number_of_product))
    )


def _get_entry_id_inventory_cost_name(product_name, n) -> str:
    return f'frame2_entry_{product_name}_{n}_inventory_cost'


def _get_entry_id_fixed_cost_name(product_name, n) -> str:
    return f'frame2_entry_{product_name}_{n}_fixed_cost'


def _get_entry_id_variable_cost_name(product_name, n) -> str:
    return f'frame2_entry_{product_name}_{n}_variable_cost'


def _frame2_each_page(stacker_, name, product_name: str, product_number: int, view: ViewABC, widget):
    w = widget
    frame_names = 'Fixed Cost', 'Variable Cost', 'Inventory'
    number_of_fixed_cost = int(view.get_value(_get_entry_id_product_fixed_cost(name, product_number)))
    number_of_variable_cost = int(view.get_value(_get_entry_id_product_variable_cost(name, product_number)))
    number_of_inventory_cost = int(view.get_value(_get_entry_id_product_inventory_cost(name, product_number)))
    return stacker_.vstack(
        w.Label(f'frame_2_lable_{product_name}').text(product_name).padding(25, 0),
        w.NoteBook(f'notebook_frame_2_{product_name}', stacker_).frame_names(frame_names).stackers(
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_fixed_cost').text(f'Fixed Cost Name{n}'),
                        w.Entry(_get_entry_id_fixed_cost_name(product_name, n)).default_value(
                            f'Fixed Cost Name{n} {product_name}'),
                        w.Spacer().adjust(-1),
                    ) for n in range(number_of_fixed_cost)),
                w.Spacer(),
            ),
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_variable_cost').text(f'Variable Cost Name{n}'),
                        w.Entry(_get_entry_id_variable_cost_name(product_name, n)).default_value(
                            f'Variable Cost Name{n} {product_name}'),
                        w.Spacer().adjust(-1),
                    ) for n in range(number_of_variable_cost)),
                w.Spacer(),
            ),
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_inventory_cost').text(f'Inventory Cost Name{n}'),
                        w.Entry(_get_entry_id_inventory_cost_name(product_name, n)).default_value(
                            f'Inventory Cost Name{n} {product_name}'),
                        w.Spacer().adjust(-1),
                    ) for n in range(number_of_inventory_cost)),
                w.Spacer(),
            ),
        ),
        w.Spacer().adjust(-1),
    )


def _switch_frames1(n_: int, frame_names, view: ViewABC):
    next_frame = frame_names[n_]
    view.switch_frame(next_frame)


def _create_frame_1_view_model(names, frame_number, next_frame, view: ViewABC) -> list:
    frame1_frames = []
    args = frame1_frames, view
    view.clear_frame(next_frame)
    local_stacker = Stacker(next_frame)
    local_stacker.hstack(
        local_stacker.vstack(
            # Buttons
            *tuple(
                w.Button(f'frame{frame_number}_button_{n}').text(name).command(
                    lambda i=n: _switch_frames1(i, *args))
                for (n, name) in enumerate(names)
            ) + (w.Spacer(),)
        ),
        w.FrameSwitcher(f'frame{frame_number}_frame_switcher', local_stacker, frame1_frames).stackers(
            *tuple(
                _frame1_each_page(local_stacker, names, name, view, w)
                for (i, name) in enumerate(names)
            ),
        ),
        w.Spacer().adjust(-1),
    )
    local_view_model = local_stacker.view_model
    return local_view_model


def _create_frame_2_view_model(names, frame_number, frame, view: ViewABC) -> list:
    frame2_frames = []
    name = names[4]
    number_of_products = int(view.get_value(_get_entry_id(name)))
    product_names = tuple(view.get_value(f'frame_1_entry_{name}_{n}') for n in range(number_of_products))
    local_stacker = Stacker(frame)
    args = frame2_frames, view

    local_stacker.hstack(
        # 1) Buttons
        local_stacker.vstack(
            *tuple(
                w.Button(f'frame_{frame_number}_{n}').text(product_name).command(lambda i=n: _switch_frames(i, *args))
                for (n, product_name) in enumerate(product_names)
            ) + (w.Spacer(),)
        ),
        # 2) Notebooks
        w.FrameSwitcher(f'frame{frame_number}_frame_switcher', local_stacker, frame2_frames).stackers(
            *tuple(
                _frame2_each_page(local_stacker, name, product_name, i, view, w)
                for (i, product_name) in enumerate(product_names)
            ),
        ),
        w.Spacer().adjust(-1),
    )
    local_view_model = local_stacker.view_model
    return local_view_model


def _switch_frames(i: int, frame2_frames, view: ViewABC):
    next_frame = frame2_frames[i]
    view.switch_frame(next_frame)


def _create_frame_3_view_model(names, frame, view: ViewABC) -> list:
    inventory_names = _extract_all_inventory_cost_names(names, view)
    product_names = _extract_all_product_names(names, view)

    local_stacker = Stacker(frame)

    local_stacker.vstack(
        w.Label(f'label_frame_3').text('Intercompany Sales'),
        local_stacker.hstack(
            w.ComboBox(_get_combobox_id_product()).values(product_names).padding(10, 10),
            w.Spacer(),
            w.Label(f'label_frame_3_arrow').text('->').padding(10, 10),
            w.Spacer(),
            w.ComboBox(_get_combobox_id_inventory()).values(inventory_names).padding(10, 10),
        ),
        local_stacker.hstack(
            w.Spacer(),
            w.Button('button_frame_3_add').text('+').command(lambda: _add_intercompany_sales(view)),
            w.Button('button_frame_3_subtract').text('-').command(lambda: _remove_intercompany_sales(view)),
            w.Spacer(),
        ),
        local_stacker.vstack(
            w.TreeView(f'tree_frame_3').padding(10, 10),
        ),
        w.Spacer().adjust(-1),
    )

    view.switch_tree(_get_tree_id())
    local_view_model = local_stacker.view_model
    return local_view_model


def _extract_all_product_names(names, view: ViewABC):
    name_product = names[4]
    number_of_products = int(view.get_value(_get_entry_id(name_product)))
    product_names = tuple(view.get_value(_get_entry_id2(name_product, n)) for n in range(number_of_products))
    return product_names


def _extract_all_inventory_cost_names(names, view: ViewABC):
    name_product = names[4]
    number_of_products = int(view.get_value(_get_entry_id(name_product)))
    inventory_names = []
    for n in range(number_of_products):
        product_name_id = _get_entry_id2(name_product, n)
        product_name = view.get_value(product_name_id)
        number_of_inventory_costs = int(view.get_value(_get_entry_id_product_inventory_cost(name_product, n)))
        for i in range(number_of_inventory_costs):
            inventory_name_id = _get_entry_id_inventory_cost_name(product_name, i)
            inventory_cost_name = view.get_value(inventory_name_id)
            inventory_names.append(inventory_cost_name)
    inventory_names = tuple(inventory_names)
    return inventory_names


def _get_combobox_id_product() -> str:
    return f'combobox_frame_3_1'


def _get_combobox_id_inventory() -> str:
    return f'combobox_frame_3_2'


def _get_tree_id() -> str:
    return f'tree_frame_3'


def _add_intercompany_sales(view: ViewABC):
    new_product_name = view.get_value(_get_combobox_id_product())
    new_inventory_name = view.get_value(_get_combobox_id_inventory())
    if new_inventory_name != '' and new_inventory_name != '':
        tree_values = view.get_all_tree_values(_get_tree_id())
        existing_product_names = list(v[1] for v in tree_values)
        existing_inventory_names = list(v[2] for v in tree_values)
        product_names = existing_product_names + [new_product_name]
        inventory_names = existing_inventory_names + [new_inventory_name]

        headings = 'No', 'Product Name', 'Inventory Cost'
        widths = 50, 200, 200
        tree_datas = tuple(Utilities.create_tree_data('', n, '', (n, p, v), (), False)
                           for (n, (p, v)) in enumerate(zip(product_names, inventory_names)))
        stretches = False, True, True
        scroll_v = True
        scroll_h = False
        view_model = Utilities.create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
        view.update_tree(view_model)


def _remove_intercompany_sales(view: ViewABC):
    selected_values = view.tree_selected_values(_get_tree_id())
    combinations_of_selected_product_inventory = tuple((v[1], v[2]) for v in selected_values)
    tree_values = view.get_all_tree_values(_get_tree_id())

    product_names = []
    inventory_names = []
    for _, product, inventory in tree_values:
        if (product, inventory) not in combinations_of_selected_product_inventory:
            product_names.append(product)
            inventory_names.append(inventory)

    headings = 'No', 'Product Name', 'Inventory Cost'
    widths = 50, 200, 200
    tree_datas = tuple(Utilities.create_tree_data('', n, '', (n, p, v), (), False)
                       for (n, (p, v)) in enumerate(zip(product_names, inventory_names)))
    stretches = False, True, True
    scroll_v = True
    scroll_h = False
    view_model = Utilities.create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    view.update_tree(view_model)


def create_data_structure(names: tuple, view: ViewABC) -> dict:
    data = {}
    products = {}
    intercompany_sales = []
    # set number
    for name in names:
        entry_id = _get_entry_id(name)
        number = int(view.get_value(entry_id))
        data[name] = {'number': number, 'text': {}}

    # set name
    for name in names:
        for n in range(data[name]['number']):
            entry_id = _get_entry_id2(name, n)
            text = view.get_value(entry_id)
            data[name]['text'][n] = text

            if name == names[4]:  # Handle Product
                products[text] = {'variable costs': [], 'fixed costs': [], 'inventory costs': [], }
                number_of_fixed_cost = int(view.get_value(_get_entry_id_product_fixed_cost(name, n)))
                number_of_variable_cost = int(view.get_value(_get_entry_id_product_variable_cost(name, n)))
                number_of_inventory_cost = int(view.get_value(_get_entry_id_product_inventory_cost(name, n)))

                for i in range(number_of_fixed_cost):
                    fixed_cost_name = view.get_value(_get_entry_id_fixed_cost_name(text, i))
                    products[text]['fixed costs'].append(fixed_cost_name)

                for i in range(number_of_variable_cost):
                    variable_cost_name = view.get_value(_get_entry_id_variable_cost_name(text, i))
                    products[text]['variable costs'].append(variable_cost_name)

                for i in range(number_of_inventory_cost):
                    inventory_cost_name = view.get_value(_get_entry_id_inventory_cost_name(text, i))
                    products[text]['inventory costs'].append(inventory_cost_name)

    all_tree_values = view.get_all_tree_values(_get_tree_id())
    for n, product_name, inventory_cost_name in all_tree_values:
        intercompany_sales.append((product_name, inventory_cost_name))

    data['products'] = products
    data['intercompany_sales'] = intercompany_sales
    return data


def method_injected(interactor, view: ViewABC, data: dict):
    names = 'Banks', 'SG&A', 'Other Expense', 'Other Income', 'Product'

    f = interactor.add_command_always
    bank_names = data[names[0]]['text'].values()
    sga_names = data[names[1]]['text'].values()
    other_expense_names = data[names[2]]['text'].values()
    other_income_names = data[names[3]]['text'].values()
    product_names = data[names[4]]['text'].values()
    interactor.clear_commands()

    f('merge_macro', ('99_00_first_step',), {})
    f('merge_macro', ('99_01_add_financial_statements',), {})
    f('merge_macro', ('99_Add_Audit_BS_and_Audit_BS_vs_CF',), {})
    f('merge_macro', ('99_Add_Audit_BS_and_Audit_BS_vs_CFWF',), {})
    f('merge_macro', ('99_Add_Audit_BS_and_Audit_CF_vs_CFWF',), {})
    f('merge_macro_with_magic', ('7_merge_file', 'file_name', 'Retained Earnings',), {})
    f('merge_macro_with_magic', ('7_merge_file', 'file_name', 'Tr Income Tax',), {})
    f('merge_macro_with_magic', ('7_merge_file', 'file_name', 'CFWF1',), {})
    f('merge_macro_with_magic', ('7_add_new_worksheet_with_MagicArg', 'MagicArg', 'CFWF',), {})
    f('merge_macro_with_magic', ('7_add_new_worksheet_with_MagicArg', 'MagicArg', 'Debt',), {})
    f('merge_macro_with_magic', ('7_add_new_worksheet_with_MagicArg', 'MagicArg', 'FS',), {})
    f('merge_macro_with_magic', ('7_add_new_worksheet_with_MagicArg', 'MagicArg', 'Accounts',), {})
    f('merge_macro_with_magic', ('7_add_new_worksheet_with_MagicArg', 'MagicArg', 'Audit',), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('CFWF', 'CFWF1'),), {})

    for bank_name in bank_names:
        f('merge_macro_with_magic', ('7_add_debt_model_with_cfwf2', 'expense_name', bank_name,), {})
    f('merge_macro', ('7_add_pic_with_cfwf_payout',), {})
    f('merge_macro', ('7_add_cfwf_plug',), {})

    for sga_name in sga_names:
        f(
            'merge_macro_with_multiple_magic_args',
            ('7_add_sga_then_set_parent_worksheet', ('sheet_name', 'cost_name'), ('Sheet1', sga_name),),
            {})

    for oth_ex in other_expense_names:
        f(
            'merge_macro_with_multiple_magic_args',
            ('7_add_other_expense_then_set_parent_worksheet', ('sheet_name', 'cost_name'), ('Sheet1', oth_ex),),
            {})

    for oth_in in other_income_names:
        f(
            'merge_macro_with_multiple_magic_args',
            ('7_add_other_income_then_set_parent_worksheet', ('sheet_name', 'income_name'), ('Sheet1', oth_in),),
            {})

    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Audit', 'Audit BS'),), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Audit', 'Audit BS vs CF')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Audit', 'Audit BS vs CFWF')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Audit', 'Audit CF vs CFWF')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('FS', 'IS')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('FS', 'BS')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('FS', 'CF')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Accounts', 'IS Accounts')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Accounts', 'BS Accounts')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Accounts', 'CF Accounts')), {})
    f('merge_macro_with_multiple_magic_args',
      ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('Accounts', 'RE')), {})
    f('delete_commands_up_to', (), {})
    interactor.run_macro()
    interactor.run_macro()
    interactor.clear_commands()

    for product_name in product_names:
        fixed_cost_names = data['products'][product_name]['fixed costs']
        variable_cost_names = data['products'][product_name]['variable costs']
        inventory_cost_names = data['products'][product_name]['inventory costs']

        f('set_magic_arg', ('product_name', product_name), {})
        f('set_magic_arg_by_magic_arg', ('sheet_name', 'product_name'), {})
        f('merge_macro_with_magic', ('7_add_new_worksheet_with_MagicArg', 'MagicArg', 'sheet_name'), {})

        for inventory_name in inventory_cost_names:
            f('merge_macro_with_magic',
              ('7_inventory_material_then_set_parent_worksheet', 'material_name', inventory_name), {})

        for variable_cost_name in variable_cost_names:
            f('merge_macro_with_magic',
              ('7_variable_cost_then_set_parent_worksheet', 'cost_name', variable_cost_name), {})

        for fixed_cost_name in fixed_cost_names:
            f('merge_macro_with_magic',
              ('7_fixed_cost_then_set_parent_worksheet', 'cost_name', fixed_cost_name), {})

        f('merge_macro', ('7_opex_inventory_cogs',), {})
        f('merge_macro_with_multiple_magic_args',
          ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('sheet_name', f'OPEX {product_name}'),), {})
        f('merge_macro_with_multiple_magic_args',
          ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('sheet_name', f'Inventory FG {product_name}'),),
          {})
        f('merge_macro_with_multiple_magic_args',
          ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('sheet_name', f'COGS {product_name}'),), {})
        f('merge_macro_with_magic', ('7_add_revenue_with_MagicArg', 'account_name', product_name,), {})
        f('merge_macro_with_multiple_magic_args',
          ('8_Worksheet_Add_Parent', ('Parent Sheet', 'Child Sheet'), ('sheet_name', f'Revenue {product_name}'),), {})
        f('merge_macro', ('8 Auto Connect and Inter Sheets Relays',), {})
        f('delete_commands_up_to', (), {})

        interactor.run_macro()
        interactor.run_macro()
        interactor.clear_commands()

    view.close('gui_model_top_level')
    interactor.change_active_keymap('Design')
