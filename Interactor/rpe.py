from typing import Callable
from typing import Iterable

from . import implementation_9 as impl
from ..Entities import Connections
from ..Entities import Shapes


def get_bb_rpes(connections: Connections, relay_to_original_mapper: dict, shapes: Shapes, shift: int) -> dict:
    bb_rpes = {}
    bbs = shapes.get_shapes('bb')
    relay_mapper = relay_to_original_mapper
    for bb in bbs:
        base_accounts = connections.get_connections_into(bb)
        if len(base_accounts) == 0:
            continue
        else:
            base_account = base_accounts.pop()
        bb_accounts = connections.get_connections_out_of(bb)

        for bb_account in bb_accounts:
            base_account = impl.if_relay_then_get_the_the_original_account(base_account, relay_mapper)
            bb_rpes[bb_account] = (base_account, shift, 'shift')
    return bb_rpes


def get_rpe_dictionary(bb_rpes: dict, rpes: Iterable, get_text: Callable, all_operators: Iterable) -> dict:
    def convert_operator_to_text(rpe_formula: tuple) -> tuple:
        return tuple(get_text(id_) if id_ in all_operators else id_ for id_ in rpe_formula)

    rpe_dictionary = {}
    for owner, raw_rpe in rpes:
        r = convert_operator_to_text(raw_rpe)
        if len(r) > 2:
            rpe_dictionary[owner] = r
        elif len(r) == 2:
            # 'total_Depreciation' = (1, '+') direct link.
            rpe_dictionary[owner] = (r[0],)
        else:
            # 'total_Depreciation' = ('+',) no accounts are added to total accounts.
            pass
    rpe_dictionary.update(bb_rpes)
    return rpe_dictionary
