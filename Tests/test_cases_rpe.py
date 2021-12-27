def get_rpe_test_cases():
    revenue = (None,
               {(3, 0), (1, 3), (2, 3)},
               {0: 'Revenue', 1: 'Volume', 2: 'Unit Price', 3: 'x'},
               {0: 80.0, 1: 11, 2: 149, 3: 105.0},
               (3,),

               (
                   ('Revenue', ('Volume', 'Unit Price', 'x')),
               ),)
    is_ = ((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19),
           {(16, 17), (12, 2), (6, 16), (1, 12), (17, 10), (8, 15), (4, 15), (10, 19), (0, 12), (5, 14),
            (9, 16), (18, 19), (14, 8), (15, 9), (7, 17), (2, 14), (19, 11), (3, 14)},
           {0: 'Revenue', 1: 'COGS', 2: 'Gross Profit', 3: 'SG&A', 4: 'D+A', 5: 'Others',
            6: 'Interest Income', 7: 'Interest Expense', 8: 'EBITDA', 9: 'EBIT', 10: 'EBT',
            11: 'Net Income',
            12: '-', 14: '-', 15: '-', 16: '+', 17: '-', 18: 'Tax Expense', 19: '-'},
           {0: 42, 1: 112, 2: 42, 3: 112, 4: 112, 5: 112, 6: 112, 7: 112, 8: 42, 9: 42, 10: 42, 11: 42,
            12: 17.0, 14: 17.0, 15: 17.0, 16: 17.0, 17: 17.0, 18: 111, 19: 17.0
            },
           (12, 14, 15, 16, 17, 19),
           (('Gross Profit', ('Revenue', 'COGS', '-')),
            ('EBITDA', ('Gross Profit', 'SG&A', '-', 'Others', '-')),
            ('EBIT', ('EBITDA', 'D+A', '-')),
            ('EBT', ('EBIT', 'Interest Income', '+', 'Interest Expense', '-')),
            ('Net Income', ('EBT', 'Tax Expense', '-'))),
           )
    bs = ((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
          {(8, 14), (12, 15), (15, 13), (7, 14), (2, 6), (4, 5), (6, 0), (10, 15), (1, 6), (11, 15), (14, 9),
           (5, 2), (3, 5)},
          {0: 'Total Asset', 1: 'Non Current Asset', 2: 'Current Asset', 3: 'Cash', 4: 'Non Cash', 5: '+',
           6: '+',
           7: 'Current Liability', 8: 'Non Current Liability', 9: 'Total Liability', 10: 'Retained Earnings',
           11: 'Paid in Capital', 12: 'Other Equity', 13: 'Total Equity', 14: '+', 15: '+'},
          {0: 17.0, 1: 17.0, 2: 17.0, 3: 17.0, 4: 17.0, 5: 137.0, 6: 192.0, 7: 339.0, 8: 339.0, 9: 284.0,
           10: 339.0, 11: 339.0, 12: 339.0, 13: 284.0, 14: 259.0, 15: 259.0},
          (5, 6, 14, 15),
          (('Current Asset', ('Cash', 'Non Cash', '+')),
           ('Total Asset', ('Non Current Asset', 'Current Asset', '+')),
           ('Total Liability', ('Current Liability', 'Non Current Liability', '+')),
           ('Total Equity', ('Retained Earnings', 'Paid in Capital', '+', 'Other Equity', '+'))),
          )
    cf = ((0, 1, 2, 3, 4, 5, 6, 8, 7),
          {(6, 7), (1, 4), (3, 8), (7, 5), (4, 3), (0, 4), (8, 6), (2, 4), (5, 8)},
          {0: 'Cash Flow from Operation', 1: 'Cash Flow from Investings', 2: 'Cash Flow from Financing',
           3: 'Total Cash Flow', 4: '+', 5: 'Cash BB', 6: 'Cash EB', 8: '+', 7: 'BB'},
          {0: 90, 1: 90, 2: 90, 3: 90, 4: 310.0, 5: 90, 6: 90, 8: 370.0, 7: 14},
          (4, 8),
          (('Total Cash Flow',
            ('Cash Flow from Operation', 'Cash Flow from Investings', '+', 'Cash Flow from Financing', '+')),
           ('Cash EB', ('Total Cash Flow', 'Cash BB', '+'))),
          )
    dcf = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15),
        {(3, 12), (7, 15), (1, 12), (9, 15), (13, 14), (2, 11), (5, 13), (14, 7), (4, 13), (0, 11), (11, 1),
         (12, 4), (15, 8), (6, 14)},
        {0: 'EBIT', 1: 'NOPAT', 2: 'Cash Taxes', 3: 'D&A', 4: 'EBITDA', 5: 'Capex', 6: 'Change in WC',
         7: 'Unlevered FCF', 8: 'Unlevered FCF - PV', 9: 'Discount Factor', 11: '-', 12: '+', 13: '-', 14: '-',
         15: 'x'},
        {0: 115.0, 1: 115.0, 2: 115.0, 3: 115.0, 4: 115.0, 5: 115.0, 6: 115.0, 7: 115.0, 8: 115.0, 9: 115.0,
         11: 18, 12: 18, 13: 18, 14: 18, 15: 18},
        (11, 12, 13, 14, 15),
        (('NOPAT', ('EBIT', 'Cash Taxes', '-')),
         ('EBITDA', ('NOPAT', 'D&A', '+')),
         ('Unlevered FCF', ('EBITDA', 'Capex', '-', 'Change in WC', '-')),
         ('Unlevered FCF - PV', ('Unlevered FCF', 'Discount Factor', 'x'))),

    )
    discount_factor = (
        (0, 1, 2, 3, 4, 5, 6, 8),
        {(6, 8), (4, 6), (2, 8), (1, 6), (5, 0), (8, 5), (3, 5)},
        {0: 'Discount Factor', 1: 'Discount Rate', 2: 'Discount Period', 3: '1', 4: '1', 5: '/', 6: '+', 8: '^'},
        {0: 52.0, 1: 251, 2: 251.0, 3: 16, 4: 172.76646999999997, 5: 94.49000000000001, 6: 172.76646999999997,
         8: 172.98000000000002},
        (5, 6, 8),
        (('Discount Factor', ('1', '1', 'Discount Rate', '+', 'Discount Period', '^', '/')),),
    )

    interest = (
        (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 13, 16, 17, 18, 19, 22, 23, 24, 25, 26),
        {(2, 22), (1, 6), (24, 22), (16, 17), (18, 23), (4, 19), (8, 10), (25, 26), (23, 25), (6, 0), (9, 10),
         (10, 1), (2, 17), (7, 9), (17, 18), (22, 25), (13, 23), (19, 5), (0, 9), (26, 19)},
        {0: 'Debt BB', 1: 'Debt EB', 2: 'Weight BB', 4: 'Interest Rate', 5: 'Interest', 6: 'BB', 7: 'Increase',
         8: 'Decrease', 9: '+', 10: '-', 13: 'Debt EB', 16: '1', 17: '-', 18: 'Weight EB', 19: 'x', 22: 'x',
         23: 'x', 24: 'Debt BB', 25: '+', 26: 'Base'},
        {0: 103, 1: 103, 2: 105, 4: 497, 5: 435.3555, 6: 223, 7: 103, 8: 103, 9: 19, 10: 19, 13: 105,
         16: 34.24199999999999, 17: 34.24199999999999, 18: 105, 19: 462.8555, 22: 238, 23: 238, 24: 105,
         25: 306.053325, 26: 373.711},
        (9, 10, 17, 19, 22, 23, 25),
        (('Debt EB', ('Debt BB', 'Increase', '+', 'Decrease', '-')),
         ('Weight EB', ('1', 'Weight BB', '-')),
         ('Interest', ('Base', 'Interest Rate', 'x')),
         ('Base', ('Weight BB', 'Debt BB', 'x', 'Debt EB', 'Weight EB', 'x', '+'))),

    )
    dividend = (
        (1, 2, 3, 4, 5, 6),
        {(2, 6), (4, 5), (3, 6), (5, 1), (6, 5)},
        {1: 'Dividend Payout', 2: 'Net Income', 3: 'Payout Ratio', 4: 'Payout Cap', 5: 'max', 6: 'x'},
        {1: 153.52051999999998, 2: 196, 3: 15, 4: 234, 5: 185.970168, 6: 138.288},
        (5, 6),
        (('Dividend Payout', ('Payout Ratio', 'Net Income', 'x', 'Payout Cap', 'max')),),
    )
    re = (
        (2, 3, 4, 5, 6, 8, 0),
        {(8, 3), (2, 6), (6, 8), (4, 8), (5, 6), (3, 0), (0, 2)},
        {2: 'Retained Earnings BB', 3: 'Retained Earnings EB', 4: 'Dividend Payout', 5: 'Net Income', 6: '+',
         8: '-', 0: 'BB'},
        {2: 95, 3: 95, 4: 95, 5: 95, 6: 14, 8: 14, 0: 280},
        (6, 8),
        (('Retained Earnings EB', ('Retained Earnings BB', 'Net Income', '+', 'Dividend Payout', '-')),),
    )
    plug = (
        (17, 18, 50, 51, 52, 53, 54, 55, 0, 1, 2, 5, 7, 8, 9, 10),
        {(10, 8), (18, 54), (5, 10), (54, 55), (53, 55), (52, 0), (55, 52), (1, 5), (8, 9), (17, 54), (52, 5),
         (1, 0), (50, 53), (7, 8), (0, 2), (51, 53)},
        {17: 'Total Liability', 18: 'Total Equity', 50: 'Non Cash', 51: 'Non Current Asset', 52: 'Net Plug',
         53: '+', 54: '+', 55: '-', 0: 'max', 1: '0', 2: 'Excess Cash', 5: 'min', 7: '-1', 8: 'x', 9: 'Revolver',
         10: 'Cash Deficit'},
        {17: 389, 18: 389, 50: 12, 51: 12, 52: 215.0, 53: 179, 54: 321, 55: 250.0, 0: 190.0, 1: 250.0, 2: 168,
         5: 309.5, 7: 375, 8: 310.0, 9: 287.5, 10: 287.5},
        (53, 54, 55, 0, 5, 8),
        (('Net Plug', ('Non Cash', 'Non Current Asset', '+', 'Total Liability', 'Total Equity', '+', '-')),
         ('Excess Cash', ('Net Plug', '0', 'max')),
         ('Cash Deficit', ('Net Plug', '0', 'min')),
         ('Revolver', ('Cash Deficit', '-1', 'x'))),
    )
    test_cases = revenue, is_, bs, cf, dcf, discount_factor, interest, dividend, re, plug
    return test_cases
