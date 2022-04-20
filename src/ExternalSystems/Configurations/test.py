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
        stacker = Stacker()

        names = 'Banks', 'SG&A', 'Other Expense', 'Other Income', 'Product', 'Product with ICS'
        switchable_frames = []

        frame_number = 0

        def switch_frame(increment: int):
            nonlocal frame_number
            if increment > 0:
                frame_number = min(len(switchable_frames) - 1, frame_number + 1)
            else:
                frame_number = max(0, frame_number - 1)

            next_frame = switchable_frames[frame_number]

            local_view_model = None
            if frame_number == 1:
                local_view_model = create_frame_1_view_model(names, frame_number, next_frame, view)
            elif frame_number == 2:
                local_view_model = create_frame_2_view_model(names, frame_number, next_frame, view)

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
                    number_of(names[5], stacker, view),
                    stacker.hstack(
                        w.Button('button_clear').text('Clear').command(lambda: clear_entries(names, view, )).width(15),
                        w.Spacer(),
                    ),
                    w.Spacer(),
                ),
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
    return stacker.hstack(
        w.Label(f'label_number_of_{name}').text(f'Number of {name}'),
        w.Button(f'button_number_of_{name}').text('-').width(1).command(lambda: increment_entry(name, -1, view, dv)),
        w.Entry(get_entry_id(name)).default_value(default_value).width(5),
        w.Button(f'button_number_of_{name}').text('+').width(1).command(lambda: increment_entry(name, 1, view, dv)),
    )


def increment_entry(name: str, increment: int, view, default_value=0):
    import Utilities
    entry = get_entry_id(name)
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
    if name == names[4]:
        return input_product(name, number, stacker_, w)
    elif name == names[5]:
        return input_product_intercompany_sales(name, number, stacker_, w)
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


def input_product(name, number_of_product, stacker_, w):
    return stacker_.vstack_scrollable(
        *tuple(
            stacker_.vstack(
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "")}').text(f'{name}{n} Name').width(20),
                    w.Entry(get_entry_id2(name, n)).default_value(f'{name}{n}'),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "fixed_costs")}').text(f'n fixed costs').width(20).align('e'),
                    w.Entry(get_entry_id_product_fixed_cost(name, n)).default_value(1),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "variable_costs")}').text(f'n variable costs').width(20).align('e'),
                    w.Entry(get_entry_id_product_variable_cost(name, n)).default_value(1),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "inventory_costs")}').text(f'n inventory costs').width(20).align('e'),
                    w.Entry(get_entry_id_product_inventory_cost(name, n)).default_value(1),
                ),
            ) for n in range(number_of_product))
    )


def input_product_intercompany_sales(name, number, stacker_, w):
    return stacker_.vstack_scrollable(
        *tuple(
            stacker_.vstack(
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "")}').text(f'{name}{n} Name').width(20),
                    w.Entry(get_entry_id2(name, n)).default_value(f'{name}{n}'),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "target_inventory_cost")}').text(f'Target Inventory Name').width(20),
                    w.Entry(get_entry_id2(name, n)).default_value(f'Target Inventory {n}'),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "fixed_costs")}').text(f'n fixed costs').width(20).align('e'),
                    w.Entry(f'frame_1_entry_{name}_{n}_fixed_costs').default_value(1),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "variable_costs")}').text(f'n variable costs').width(20).align('e'),
                    w.Entry(f'frame_1_entry_{name}_{n}_variable_costs').default_value(1),
                ),
                stacker_.hstack(
                    w.Label(f'{lbl(name, n, "inventory_costs")}').text(f'n inventory costs').width(20).align('e'),
                    w.Entry(f'frame_1_entry_{name}_{n}_inventory_costs').default_value(1),
                ),
            ) for n in range(number))
    )


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
                        w.Entry(f'frame2_entry_{product_name}_{n}_fixed_cost').default_value(f'Fixed Cost Name{n}'),
                    ) for n in range(number_of_fixed_cost)),
                w.Spacer(),
            ),
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_variable_cost').text(f'Variable Cost Name{n}'),
                        w.Entry(f'frame2_entry_{product_name}_{n}_variable_cost').default_value(
                            f'Variable Cost Name{n}'),
                    ) for n in range(number_of_variable_cost)),
                w.Spacer(),
            ),
            stacker_.vstack(
                *tuple(
                    stacker_.hstack(
                        w.Label(f'frame2_label_{product_name}_{n}_inventory_cost').text(f'Inventory Cost Name{n}'),
                        w.Entry(f'frame2_entry_{product_name}_{n}_inventory_cost').default_value(
                            f'Inventory Cost Name{n}'),
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


def create_frame_2_view_model(names, frame_number, next_frame, view) -> list:
    from stacker import Stacker
    from stacker import widgets as w

    frame2_frames = []
    name = names[4]
    number_of_products = int(view.get_value(get_entry_id(name)))
    product_names = tuple(view.get_value(f'frame_1_entry_{name}_{n}') for n in range(number_of_products))
    local_stacker = Stacker(next_frame)
    local_stacker.hstack(
        # 1) Buttons
        local_stacker.vstack(
            *tuple(
                w.Button(f'frame_{frame_number}_{n}').text(product_name)
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


if __name__ == '__main__':
    unittest.main()
