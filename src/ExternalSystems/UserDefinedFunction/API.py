import subprocess

from interface_udf_builder import UDFBuilderABC

min_max = """
Function Min(ParamArray values() As Variant) As Variant
   Dim minValue, Value As Variant
   minValue = values(0)
   For Each Value In values
       If Value < minValue Then minValue = Value
   Next
   Min = minValue
End Function

Function Max(ParamArray values() As Variant) As Variant
   Dim maxValue, Value As Variant
   maxValue = values(0)
   For Each Value In values
       If Value > maxValue Then maxValue = Value
   Next
   Max = maxValue
End Function
"""


class UDFBuilder(UDFBuilderABC):
    def __init__(self):
        self._text = 'Option Explicit\n\n'

    @property
    def text(self) -> str:
        return self._text

    def export(self, **kwargs):
        file_name = kwargs['folder_name']
        max_loop = kwargs['max_loop']
        tolerance = kwargs['tolerance']
        arguments = kwargs['arguments']
        function_name = kwargs['name']
        formulas = kwargs['formulas']
        variables = kwargs['variables']
        target_value = kwargs['target_value']
        direct_links = kwargs['direct_links']
        minimum_iteration = kwargs['minimum_iteration']

        self._declare_variables(variables, formulas)
        self._create_function(function_name, arguments, max_loop, tolerance, formulas, direct_links, target_value,
                              minimum_iteration)
        self._text += min_max
        try:
            subprocess.run("pbcopy", universal_newlines=True, input=self._text)
        except FileNotFoundError:
            subprocess.run("pbcopy", universal_newlines=True, input=self._text, shell=True)

    def _declare_variables(self, variables: tuple, formulas):
        self._text += f'Dim max_loop\n'
        self._text += f'Dim tolerance\n'
        self._text += f'Dim iteration\n'
        self._text += f'Dim target_value\n'

        self._text += '\n'
        for n, formula in enumerate(formulas):
            formula_owner = formula.split('=')[0]
            self._text += f'Dim previous_{n}_{formula_owner}\n'

        self._text += '\n'
        self._text += '\nDim delta'

        self._text += '\n'
        for n, formula in enumerate(formulas):
            formula_owner = formula.split('=')[0]
            self._text += f'Dim delta_{n}_{formula_owner}\n'

        self._text += '\n'
        for variable in variables:
            self._text += f'Dim {variable}\n'
        self._text += '\n'

    def _create_function(self, name: str, arguments: tuple, max_loop: int, tolerance: float, formulas: tuple,
                         direct_links: tuple, target_value, minimum_iteration: int):

        arguments_str = str(arguments).replace("'", '').replace('"', '')
        self._text += f'Function {name}( _\n'
        split_argument_str = arguments_str.split(',')
        text = ''
        for n, argument_str in enumerate(split_argument_str):
            if len(text) > 100:
                self._text += f'{text} _\n\t'
                text = ''
            text += f'{argument_str.replace("(", "").replace(" ", "")}, '
        self._text += f'{text.replace("),", ")")}'

        self._text += f'\n'
        self._text += f'\tmax_loop = {max_loop}\n'
        self._text += f'\ttolerance = {tolerance}\n'
        self._text += f'\n'
        self._text += f'\tFor iteration = 1 To max_loop\n'

        self._text += f'\n'
        self._text += f"\t\t' Values before calculation\n"
        for n, formula in enumerate(formulas):
            formula_owner = formula.split('=')[0]
            self._text += f'\t\tprevious_{n}_{formula_owner} = {formula_owner}\n'

        self._text += f'\n'
        self._text += f"\t\t' Calculations\n"
        for formula in formulas:
            self._text += f'\t\t{formula}\n'

        self._text += f'\n'
        for direct_link in direct_links:
            ac_from, ac_to = direct_link
            self._text += f'\t\t{ac_to}={ac_from}\n'

        self._text += f'\n'
        self._text += f"\t\t' Compare values after calculations\n"
        for n, formula in enumerate(formulas):
            formula_owner = formula.split('=')[0]
            self._text += f'\t\tdelta_{n}_{formula_owner} = Abs(previous_{n}_{formula_owner} - {formula_owner})\n'

        self._text += f'\n'
        self._text += f"\t\t' Cumulative absolute differences (deltas)\n"
        self._text += f'\t\tdelta = 0\n'
        for n, formula in enumerate(formulas):
            formula_owner = formula.split('=')[0]
            self._text += f'\t\tdelta = delta + delta_{n}_{formula_owner}\n'

        self._text += f'\n'
        self._text += f"\t\t' If cumulative differences is smaller than tolerance, then exit function.\n"
        self._text += f'\t\tIf iteration > {minimum_iteration} And delta < tolerance Then\n'
        self._text += f'\t\t\ttarget_value = {target_value}\n'
        self._text += f'\t\t\t{name} = {target_value}\n'
        self._text += f'\t\t\tExit Function\n'
        self._text += f'\t\tEnd If\n'

        self._text += f'\tNext iteration\n'

        self._text += f'End Function\n'
