def merge_account_order_data(account_order, account_order_data, shape_id_converter):
    if (len(account_order.data) > 0) and (not account_order.is_blank(account_order.data[-1])):
        account_order.add_blank(len(account_order.data))
    for element in account_order_data:
        if element in shape_id_converter:
            element = shape_id_converter[element]
            account_order.add_element_to_last(element)
        elif account_order.is_blank(element):
            account_order.add_blank(len(account_order.data))

    if len(account_order.data) > 0:  # Add blank at the end.
        if not account_order.is_blank(account_order.data[-1]):
            account_order.add_blank(len(account_order.data))
