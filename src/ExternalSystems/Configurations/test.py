import unittest


class MyTestCase(unittest.TestCase):
    def test_main(self):
        from ...ExternalSystems.Configurations import ConfigurationTest
        from view_tkinter import View
        from ...EntityGateway import GateWays
        from ...Main import Main

        """
        This is where you select 
            1) Configuration
            2) View
            3) GateWays
        then plug them into Main.
        """

        config = ConfigurationTest()
        view = View()
        cls_gateways = GateWays
        app = Main(config, view, cls_gateways)
        # app.run()

    def test_gui(self):
        from stacker import Stacker
        from stacker import widgets as w
        from view_tkinter import View

        view = View(width=500, height=600)
        view.set_title('Financial Model Constructor')
        stacker = Stacker()

        names = 'Banks', 'SG&A', 'Other Expense', 'Other Income', 'Product'
        switchable_frames = []

        frame_number = 0

        def switch_frame(increment: int):
            nonlocal frame_number
            if increment > 0:
                frame_number = min(len(switchable_frames) - 1, frame_number + 1)
            else:
                frame_number = max(0, frame_number - 1)

            next_frame = switchable_frames[frame_number]

            if increment > 0:  # Keep user inputs if Back< button is pushed
                local_view_model = None
                if frame_number == 1:
                    local_view_model = create_frame_1_view_model(names, frame_number, next_frame, view)
                elif frame_number == 2:
                    local_view_model = create_frame_2_view_model(names, frame_number, next_frame, view)
                elif frame_number == 3:
                    local_view_model = create_frame_3_view_model(names, frame_number, next_frame, view)
                elif frame_number == 4:
                    data_structure = create_data_structure(names, view)
                    print(data_structure)

                if local_view_model is not None:
                    view.add_widgets(local_view_model)

            view.switch_frame(next_frame)

        stacker.vstack(
            w.FrameSwitcher('frame_switcher', stacker, switchable_frames).stackers(
                stacker.vstack(
                    w.Label('label_frame0').text('Frame00'),
                    number_of(names[0], stacker, view),
                    number_of(names[1], stacker, view),
                    number_of(names[2], stacker, view),
                    number_of(names[3], stacker, view),
                    number_of(names[4], stacker, view),
                    stacker.hstack(
                        w.Button('button_clear').text('Clear').command(lambda: clear_entries(names, view, )).width(15),
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
                w.Button('Back').text('Back<').command(lambda: switch_frame(-1)),
                w.Spacer(),
                w.Button('Next').text('>Next').command(lambda: switch_frame(1)),
            ),
        )

        view_model = stacker.view_model
        view.add_widgets(view_model)
        view.switch_frame(switchable_frames[frame_number])
        view.launch_app()


def number_of(name: str, stacker, view, default_value=0):
    from stacker import widgets as w
    dv = default_value
    args = get_entry_id(name), view, dv
    return stacker.hstack(
        w.Label(f'label_number_of_{name}').text(f'Number of {name}'),
        w.Button(f'button_number_of_{name}').text('-').width(1).command(lambda: increment_entry(-1, *args)),
        w.Entry(get_entry_id(name)).default_value(default_value).width(5),
        w.Button(f'button_number_of_{name}').text('+').width(1).command(lambda: increment_entry(1, *args)),
    )


def increment_entry(increment: int, entry: str, view, default_value=0):
    import Utilities
    current_value = view.get_value(entry)
    if Utilities.is_number(current_value):
        current_value = int(current_value)
    else:
        current_value = default_value
    new_value = max(0, current_value + increment)
    view.set_value(entry, new_value)


def clear_entries(names: tuple, view, default_value=0):
    for name in names:
        view.set_value(get_entry_id(name), default_value)


def get_entry_id(name) -> str:
    return f'entry_number_of_{name}'


def get_entry_id2(name: str, n: int) -> str:
    return f'frame_1_entry_{name}_{n}'


def frame1_each_page(stacker_, names: tuple, name: str, view, widget):
    w = widget
    number = int(view.get_value(get_entry_id(name)))
    if name in (names[4],):
        return input_product(name, number, stacker_, view, w)
    else:
        return stacker_.vstack_scrollable(*tuple(stacker_.vstack(
            stacker_.hstack(
                w.Label(f'{lbl(name, n, "")}').text(f'{name}{n} Name').width(20),
                w.Entry(get_entry_id2(name, n)).default_value(f'{name}{n}'),
            )
        ) for n in range(number)))


def lbl(name, n_, post_fix):
    return f'frame_1_label_{name}_{n_}_{post_fix}'


def get_entry_id_product_fixed_cost(name, n) -> str:
    return f'frame_1_entry_{name}_{n}_fixed_costs'


def get_entry_id_product_variable_cost(name, n) -> str:
    return f'frame_1_entry_{name}_{n}_variable_costs'


def get_entry_id_product_inventory_cost(name, n) -> str:
    return f'frame_1_entry_{name}_{n}_inventory_costs'


def input_product(name, number_of_product, stacker_, view, w):
    e1 = get_entry_id_product_fixed_cost
    e2 = get_entry_id_product_variable_cost
    e3 = get_entry_id_product_inventory_cost
    dv = 0
    return stacker_.vstack_scrollable(
        *tuple(
            stacker_.vstack(
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "")}').text(f'{name}{n} Name').width(20),
                    w.Entry(get_entry_id2(name, n)).default_value(f'{name}{n}'),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "fixed_costs")}').text(f'n fixed costs').width(20).align('e'),
                    w.Button(f'button_n_fixed_{name}_-_{n}').text('-').width(1).command(
                        lambda i=n: increment_entry(-1, e1(name, i), view, dv)),
                    w.Entry(get_entry_id_product_fixed_cost(name, n)).default_value(dv).width(5),
                    w.Button(f'button_n_fixed_{name}_+_{n}').text('+').width(1).command(
                        lambda i=n: increment_entry(1, e1(name, i), view, dv)),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "variable_costs")}').text(f'n variable costs').width(20).align('e'),
                    w.Button(f'button_n_fixed_{name}_-_{n}').text('-').width(1).command(
                        lambda i=n: increment_entry(-1, e2(name, i), view, dv)),
                    w.Entry(get_entry_id_product_variable_cost(name, n)).default_value(dv).width(5),
                    w.Button(f'button_n_fixed_{name}_+_{n}').text('+').width(1).command(
                        lambda i=n: increment_entry(1, e2(name, i), view, dv)),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "inventory_costs")}').text(f'n inventory costs').width(20).align('e'),
                    w.Button(f'button_n_fixed_{name}_-_{n}').text('-').width(1).command(
                        lambda i=n: increment_entry(-1, e3(name, i), view, dv)),
                    w.Entry(get_entry_id_product_inventory_cost(name, n)).default_value(dv).width(5),
                    w.Button(f'button_n_fixed_{name}_+_{n}').text('+').width(1).command(
                        lambda i=n: increment_entry(1, e3(name, i), view, dv)),
                ),
            ) for n in range(number_of_product))
    )


def get_entry_id_inventory_cost_name(product_name, n) -> str:
    return f'frame2_entry_{product_name}_{n}_inventory_cost'


def get_entry_id_fixed_cost_name(product_name, n) -> str:
    return f'Fixed Cost Name{n} {product_name}'


def get_entry_id_variable_cost_name(product_name, n) -> str:
    return f'Variable Cost Name{n} {product_name}'


def frame2_each_page(stacker_, name, product_name: str, product_number: int, view, widget):
    w = widget
    frame_names = 'Fixed Cost', 'Variable Cost', 'Inventory'
    number_of_fixed_cost = int(view.get_value(get_entry_id_product_fixed_cost(name, product_number)))
    number_of_variable_cost = int(view.get_value(get_entry_id_product_variable_cost(name, product_number)))
    number_of_inventory_cost = int(view.get_value(get_entry_id_product_inventory_cost(name, product_number)))
    return stacker_.vstack(
        w.Label(f'frame_2_lable_{product_name}').text(product_name).padding(25, 0),
        w.NoteBook(f'notebook_frame_2_{product_name}', stacker_).frame_names(frame_names).stackers(
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_fixed_cost').text(f'Fixed Cost Name{n}'),
                        w.Entry(get_entry_id_fixed_cost_name(product_name, n)).default_value(
                            f'Fixed Cost Name{n} {product_name}'),
                        w.Spacer().adjust(-1),
                    ) for n in range(number_of_fixed_cost)),
                w.Spacer(),
            ),
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_variable_cost').text(f'Variable Cost Name{n}'),
                        w.Entry(get_entry_id_variable_cost_name(product_name, n)).default_value(
                            f'Variable Cost Name{n} {product_name}'),
                        w.Spacer().adjust(-1),
                    ) for n in range(number_of_variable_cost)),
                w.Spacer(),
            ),
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_inventory_cost').text(f'Inventory Cost Name{n}'),
                        w.Entry(get_entry_id_inventory_cost_name(product_name, n)).default_value(
                            f'Inventory Cost Name{n} {product_name}'),
                        w.Spacer().adjust(-1),
                    ) for n in range(number_of_inventory_cost)),
                w.Spacer(),
            ),
        ),
        w.Spacer().adjust(-1),
    )


def switch_frames1(n_: int, frame_names, view):
    next_frame = frame_names[n_]
    view.switch_frame(next_frame)


def create_frame_1_view_model(names, frame_number, next_frame, view) -> list:
    from stacker import Stacker
    from stacker import widgets as w
    frame1_frames = []
    args = frame1_frames, view
    view.clear_frame(next_frame)
    local_stacker = Stacker(next_frame)
    local_stacker.hstack(
        local_stacker.vstack(
            # Buttons
            *tuple(
                w.Button(f'frame{frame_number}_button_{n}').text(name).command(
                    lambda i=n: switch_frames1(i, *args))
                for (n, name) in enumerate(names)
            ) + (w.Spacer(),)
        ),
        w.FrameSwitcher(f'frame{frame_number}_frame_switcher', local_stacker, frame1_frames).stackers(
            *tuple(
                frame1_each_page(local_stacker, names, name, view, w)
                for (i, name) in enumerate(names)
            ),
        ),
        w.Spacer().adjust(-1),
    )
    local_view_model = local_stacker.view_model
    return local_view_model


def create_frame_2_view_model(names, frame_number, frame, view) -> list:
    from stacker import Stacker
    from stacker import widgets as w

    frame2_frames = []
    name = names[4]
    number_of_products = int(view.get_value(get_entry_id(name)))
    product_names = tuple(view.get_value(f'frame_1_entry_{name}_{n}') for n in range(number_of_products))
    local_stacker = Stacker(frame)

    def switch_frames(i: int):
        next_frame = frame2_frames[i]
        view.switch_frame(next_frame)

    local_stacker.hstack(
        # 1) Buttons
        local_stacker.vstack(
            *tuple(
                w.Button(f'frame_{frame_number}_{n}').text(product_name).command(lambda i=n: switch_frames(i))
                for (n, product_name) in enumerate(product_names)
            ) + (w.Spacer(),)
        ),
        # 2) Notebooks
        w.FrameSwitcher(f'frame{frame_number}_frame_switcher', local_stacker, frame2_frames).stackers(
            *tuple(
                frame2_each_page(local_stacker, name, product_name, i, view, w)
                for (i, product_name) in enumerate(product_names)
            ),
        ),
        w.Spacer().adjust(-1),
    )
    local_view_model = local_stacker.view_model
    return local_view_model


def create_frame_3_view_model(names, frame_number, frame, view) -> list:
    from stacker import Stacker
    from stacker import widgets as w

    inventory_names = extract_all_inventory_cost_names(names, view)
    product_names = extract_all_product_names(names, view)

    local_stacker = Stacker(frame)

    local_stacker.vstack(
        w.Label(f'label_frame_3').text('Intercompany Sales'),
        local_stacker.hstack(
            w.ComboBox(get_combobox_id_product()).values(product_names).padding(10, 10),
            w.Spacer(),
            w.Label(f'label_frame_3_arrow').text('->').padding(10, 10),
            w.Spacer(),
            w.ComboBox(get_combobox_id_inventory()).values(inventory_names).padding(10, 10),
        ),
        local_stacker.hstack(
            w.Spacer(),
            w.Button('button_frame_3_add').text('+').command(lambda: add_intercompany_sales(view)),
            w.Button('button_frame_3_subtract').text('-').command(lambda: remove_intercompany_sales(view)),
            w.Spacer(),
        ),
        local_stacker.vstack(
            w.TreeView(f'tree_frame_3').padding(10, 10),
        ),
        w.Spacer().adjust(-1),
    )

    view.switch_tree(get_tree_id())
    local_view_model = local_stacker.view_model
    return local_view_model


def extract_all_product_names(names, view):
    name_product = names[4]
    number_of_products = int(view.get_value(get_entry_id(name_product)))
    product_names = tuple(view.get_value(get_entry_id2(name_product, n)) for n in range(number_of_products))
    return product_names


def extract_all_inventory_cost_names(names, view):
    name_product = names[4]
    number_of_products = int(view.get_value(get_entry_id(name_product)))
    inventory_names = []
    for n in range(number_of_products):
        product_name_id = get_entry_id2(name_product, n)
        product_name = view.get_value(product_name_id)
        number_of_inventory_costs = int(view.get_value(get_entry_id_product_inventory_cost(name_product, n)))
        for i in range(number_of_inventory_costs):
            inventory_name_id = get_entry_id_inventory_cost_name(product_name, i)
            inventory_cost_name = view.get_value(inventory_name_id)
            inventory_names.append(inventory_cost_name)
    inventory_names = tuple(inventory_names)
    return inventory_names


def get_combobox_id_product() -> str:
    return f'combobox_frame_3_1'


def get_combobox_id_inventory() -> str:
    return f'combobox_frame_3_2'


def get_tree_id() -> str:
    return f'tree_frame_3'


def add_intercompany_sales(view):
    new_product_name = view.get_value(get_combobox_id_product())
    new_inventory_name = view.get_value(get_combobox_id_inventory())
    if new_inventory_name != '' and new_inventory_name != '':
        tree_values = view.get_all_tree_values(get_tree_id())
        existing_product_names = list(v[1] for v in tree_values)
        existing_inventory_names = list(v[2] for v in tree_values)
        product_names = existing_product_names + [new_product_name]
        inventory_names = existing_inventory_names + [new_inventory_name]

        import Utilities
        headings = 'No', 'Product Name', 'Inventory Cost'
        widths = 50, 200, 200
        tree_datas = tuple(Utilities.create_tree_data('', n, '', (n, p, v), (), False)
                           for (n, (p, v)) in enumerate(zip(product_names, inventory_names)))
        stretches = False, True, True
        scroll_v = True
        scroll_h = False
        view_model = Utilities.create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
        view.update_tree(view_model)


def remove_intercompany_sales(view):
    selected_values = view.tree_selected_values(get_tree_id())
    combinations_of_selected_product_inventory = tuple((v[1], v[2]) for v in selected_values)
    tree_values = view.get_all_tree_values(get_tree_id())

    product_names = []
    inventory_names = []
    for _, product, inventory in tree_values:
        if (product, inventory) not in combinations_of_selected_product_inventory:
            product_names.append(product)
            inventory_names.append(inventory)

    import Utilities
    headings = 'No', 'Product Name', 'Inventory Cost'
    widths = 50, 200, 200
    tree_datas = tuple(Utilities.create_tree_data('', n, '', (n, p, v), (), False)
                       for (n, (p, v)) in enumerate(zip(product_names, inventory_names)))
    stretches = False, True, True
    scroll_v = True
    scroll_h = False
    view_model = Utilities.create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    view.update_tree(view_model)


def create_data_structure(names: tuple, view):
    data = {}
    products = {}
    intercompany_sales = []
    # set number
    for name in names:
        entry_id = get_entry_id(name)
        number = int(view.get_value(entry_id))
        data[name] = {'number': number, 'text': {}}

    # set name
    for name in names:
        for n in range(data[name]['number']):
            entry_id = get_entry_id2(name, n)
            text = view.get_value(entry_id)
            data[name]['text'][n] = text

            if name == names[4]:  # Handle Product
                products[text] = {'variable costs': [], 'fixed costs': [], 'inventory costs': [], }
                number_of_fixed_cost = int(view.get_value(get_entry_id_product_fixed_cost(name, n)))
                number_of_variable_cost = int(view.get_value(get_entry_id_product_variable_cost(name, n)))
                number_of_inventory_cost = int(view.get_value(get_entry_id_product_inventory_cost(name, n)))

                for i in range(number_of_fixed_cost):
                    fixed_cost_name = get_entry_id_fixed_cost_name(text, i)
                    products[text]['fixed costs'].append(fixed_cost_name)

                for i in range(number_of_variable_cost):
                    variable_cost_name = get_entry_id_variable_cost_name(text, i)
                    products[text]['variable costs'].append(variable_cost_name)

                for i in range(number_of_inventory_cost):
                    inventory_cost_name = get_entry_id_inventory_cost_name(text, i)
                    products[text]['inventory costs'].append(inventory_cost_name)

    all_tree_values = view.get_all_tree_values(get_tree_id())
    for n, product_name, inventory_cost_name in all_tree_values:
        intercompany_sales.append((product_name, inventory_cost_name))

    data['products'] = products
    data['intercompany_sales'] = intercompany_sales

    return data


if __name__ == '__main__':
    unittest.main()
