import unittest

from src.Entities import RPE
from src.Tests import test_cases_rpe


class TestRPE(unittest.TestCase):

    def test_rpe_algorithm(self):
        unit_price = 0
        volume = 1
        revenue = 2
        operator = 3

        positions = {unit_price: 10, volume: 0, revenue: 5, }
        operators = (operator,)
        connections = ((unit_price, operator), (volume, operator), (operator, revenue))

        expectation = (
            (revenue, (volume, unit_price, operator)),
        )
        rpes = RPE.get_rpes(connections, positions, operators)
        self.assertEqual(rpes, expectation)

        texts = {
            unit_price: 'Unit Price',
            volume: 'Volume',
            revenue: 'Revenue',
            operator: 'x',
        }
        expectation = (
            (texts[revenue], (texts[volume], texts[unit_price], texts[operator])),
        )
        self.assertEqual(RPE.get_rpe_readable(rpes, texts), expectation)

    def test_rpes(self):
        test_cases = test_cases_rpe.get_rpe_test_cases()
        for n, test_case in enumerate(test_cases):
            shape_ids, connections, texts, positions, operators, expectation = test_case
            rpes = RPE.get_rpes(tuple(connections), positions, operators)
            self.assertEqual(RPE.get_rpe_readable(rpes, texts), expectation)


if __name__ == '__main__':
    unittest.main()
