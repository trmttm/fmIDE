operator = {
    '+': '+',
    '-': '-',
    'x': '*',
    '*': '*',
    '/': '/',
    '^': '^',
    '**': '^',
    'max': 'max',
    'min': 'min',
    'average': 'average',
    'ave': 'average',
    '=': '=',
    '<': '<',
    '<=': '<=',
    '>': '>',
    '>=': '>=',
    'abs': 'abs',

}


def post_to_infix(expression: tuple) -> str:
    prec = {'+': 0, '-': 0, '*': 1, "/": 1, '%': 1, '^': 2, 'max': 2, 'min': 2,
            'ave': 2, '<=': 0, '<': 0, '>=': 0, '>': 0, '=': 0, 'abs': 2, }
    spreadsheet_functions = ['max', 'min', 'average', 'abs']
    takes_only_one_argument = ['abs']
    missing_operand_filler = {'+': ('0', '0'), '-': ('0', '0'), '*': ('1', '1'), '/': ('1', '1'), '%': ('1', '1'),
                              '^': ('1', '1'), 'min': ('0', '0'), 'max': ('0', '0')}

    stack = []
    for n, x in enumerate(expression):

        if x in spreadsheet_functions:
            try:
                two_forward = expression[n + 2]
            except IndexError:
                two_forward = None

            if x in takes_only_one_argument:
                op1 = stack.pop()
                stack.append([f'{x}({op1[0]})'])
            else:
                if len(stack) == 0:
                    if x in missing_operand_filler:
                        op2 = missing_operand_filler[x][1]
                        op1 = missing_operand_filler[x][0]
                    else:
                        return "invalid"
                elif len(stack) == 1:
                    if x in missing_operand_filler:
                        op2 = missing_operand_filler[x][1]
                        op1 = stack.pop()
                    else:
                        return "invalid"
                else:
                    op2 = stack.pop()  # pop a wrapped list out
                    op1 = stack.pop()

                if two_forward == x:
                    # Handling operator that takes more than 2 arguments: Average(a, b, c)
                    stack.append([f'{op1[0]}, {op2[0]}'])
                else:
                    stack.append([f'{x}({op1[0]}, {op2[0]})'])

        elif x in prec.keys():
            # ['+','-','*','/','%','^']:
            if len(stack) == 0:
                if x in missing_operand_filler:
                    op2 = missing_operand_filler[x][1]
                    op1 = missing_operand_filler[x][0]
                else:
                    return "invalid"
            elif len(stack) == 1:
                if x in missing_operand_filler:
                    op2 = missing_operand_filler[x][1]
                    op1 = stack.pop()
                else:
                    return "invalid"
            else:
                op2 = stack.pop()  # pop a wrapped list out
                op1 = stack.pop()

            if len(op2) > 1 and ((prec[op2[1]] < prec[x]) or (prec[op2[1]] == prec[x])):
                op2 = f'({op2[0]})'
            else:
                op2 = op2[0]

            if len(op1) > 1 and prec[op1[1]] < prec[x]:
                op1 = f'({op1[0]})'
            else:
                op1 = op1[0]

            stack.append([f'{op1}{x}{op2}', x])

        else:
            stack.append([x])
    if len(stack) != 1:
        return "invalid"
    return stack.pop()[0]


if __name__ == '__main__':
    """
    ('cash_eb', ('cash_bb', 'interest_income', '+')),
    ('base', ('cash_bb', 'cash_eb', '+', '2', '/')),
    ('interest_income', ('base', 'interest_rate', '*'))
    """
    expressions = (
        ('A1', 'B1', '+', '5', 'AB30', '-', '-'),
        ('A1', 'B1', 'max',),
        ('cash_bb', 'interest_income', '+'),
        ('cash_bb', 'cash_eb', '+', '2', '/'),
        ('base', 'interest_rate', '*'),
    )
    for exp in expressions:
        s = post_to_infix(exp)
        print(s)
