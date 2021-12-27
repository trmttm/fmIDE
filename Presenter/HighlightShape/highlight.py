import copy

key_method = 'method'
key_highlight_datas = 'highlight_datas'

fill = 'fill'
border_color = 'border_color'
border_width = 'border_width'
text_color = 'text_color'
key_shape_id = 'shape_id'

key_base = 'base'
key_account = 'account'
key_operator = 'operator'
key_constant = 'constant'
key_core_account = 'core_account'
key_bb = 'bb'
key_relay = 'relay'
key_bar = 'graph_bar'
key_slider = 'slider'
key_slider_handle = 'slider_handle'
key_slider_min = 'slider_min'
key_slider_max = 'slider_max'
key_selected = 'selected'
key_input_account = 'input_or_relay'

key_is_input_account = 'key_is_input_account'
key_is_depended_by_external_sheet = 'key_is_depended_by_external_sheet'
key_depending_on_external_sheet = 'key_depending_on_external_sheet'
key_is_heading = 'key_is_heading'
key_is_total = 'key_is_total'

key_height = 'key_height'
key_bar_positive = 'key_bar_positive'
key_bar_negative = 'key_bar_negative'

key_specified_fill = 'specified_fill'

key_arrows_in = 'arrows_in'
key_arrows_out = 'arrows_out'
key_canvas_tag = 'canvas_tag'
key_tag_type = 'tag_type'
key_shape_data = 'shape_data'

key_auto = 0
key_manual = 1

HIGHLIGHT_TYPE = {
    key_base: {text_color: 'black', border_width: 1, border_color: 'black', },
    key_account: {fill: 'white', },
    key_operator: {fill: 'pink', },
    key_constant: {fill: 'light green', },
    key_core_account: {fill: 'light grey', },
    key_bb: {fill: 'light green', },
    key_relay: {fill: 'light yellow', },
    key_slider: {fill: None, },
    key_slider_handle: {fill: 'light yellow', },
    key_slider_max: {fill: 'light green', },
    key_slider_min: {fill: 'light green', },
    None: {fill: 'light gray', },

    key_selected: {border_width: 3, },
    key_input_account: {fill: 'light blue', },
    key_is_depended_by_external_sheet: {fill: 'light grey', },
    key_depending_on_external_sheet: {border_color: 'red', },
    key_is_heading: {fill: 'orange'},
    key_is_total: {fill: 'yellow'},

    key_bar_positive: {fill: 'light green'},
    key_bar_negative: {fill: 'pink'},
}


def get_highlight_configuration_auto(highlight_data: dict) -> dict:
    tag_type: str = highlight_data[key_tag_type]
    is_selected: bool = highlight_data[key_selected]
    canvas_tag: set = highlight_data[key_canvas_tag]
    shape_id = highlight_data[key_shape_id]

    is_input_account = highlight_data[key_is_input_account]
    is_depending_on_external_worksheets = highlight_data[key_depending_on_external_sheet]
    is_depended_by_external_worksheets = highlight_data[key_is_depended_by_external_sheet]
    is_heading = highlight_data[key_is_heading] if key_is_heading in highlight_data else False
    is_total = highlight_data[key_is_total] if key_is_total in highlight_data else False
    fill_specified_by_user = highlight_data[key_specified_fill] if key_specified_fill in highlight_data else None

    highlight_configuration = copy.deepcopy(HIGHLIGHT_TYPE[key_base])
    if tag_type == key_account:
        highlight_configuration.update(HIGHLIGHT_TYPE[key_input_account if is_input_account else key_account])
    elif tag_type not in HIGHLIGHT_TYPE:
        highlight_configuration.update(HIGHLIGHT_TYPE[None])
    else:
        highlight_configuration.update(HIGHLIGHT_TYPE[tag_type])
    if is_selected:
        highlight_configuration.update(HIGHLIGHT_TYPE[key_selected])
    if is_depended_by_external_worksheets:
        highlight_configuration.update(HIGHLIGHT_TYPE[key_is_depended_by_external_sheet])
    if is_depending_on_external_worksheets:
        highlight_configuration.update(HIGHLIGHT_TYPE[key_depending_on_external_sheet])
    if is_heading:
        highlight_configuration.update(HIGHLIGHT_TYPE[key_is_heading])
    if is_total:
        highlight_configuration.update(HIGHLIGHT_TYPE[key_is_total])
    if tag_type == key_bar:
        height = 0 if key_height not in highlight_data else highlight_data[key_height]
        if height >= 0:
            highlight_configuration.update(HIGHLIGHT_TYPE[key_bar_positive])
        else:
            highlight_configuration.update(HIGHLIGHT_TYPE[key_bar_negative])
    if fill_specified_by_user is not None:
        highlight_configuration.update({'fill':fill_specified_by_user})
    return highlight_configuration


def get_highlight_configuration_manual(highlight_data: dict) -> dict:
    shape_data = highlight_data[key_shape_data]
    highlight_configuration = {
        text_color: shape_data['text_color'],
        border_width: shape_data['border_width'],
        border_color: shape_data['border_color'],
        fill: shape_data['fill'],
    }
    return highlight_configuration


configuration_method = {
    key_auto: get_highlight_configuration_auto,
    key_manual: get_highlight_configuration_manual,
}


def configure_as_per_each_highlight_data(response_model) -> dict:
    highlight_datas = response_model[key_highlight_datas]
    auto_or_manual = response_model[key_method]
    method = configuration_method[auto_or_manual]

    view_model = {}
    for highlight_data in highlight_datas:
        tag = highlight_data[key_canvas_tag]
        shape_id = highlight_data[key_shape_id]

        highlight_configuration = method(highlight_data)

        highlight_configuration.update({key_shape_id: shape_id})
        view_model.update({tag: copy.deepcopy(highlight_configuration)})
    return view_model
