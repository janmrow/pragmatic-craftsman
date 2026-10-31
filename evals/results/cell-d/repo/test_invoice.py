import unittest
from decimal import Decimal
from invoice import invoice_total
class InvoiceTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(invoice_total('description,amount\nTea,2.50\n'), Decimal('2.50'))

    def test_quoted_comma_in_description(self):
        total = invoice_total('description,amount\n"Tea, loose leaf",2.50\nCake,0.10\n')
        self.assertIsInstance(total, Decimal)
        self.assertEqual(total, Decimal('2.60'))

    def test_empty_and_blank_rows(self):
        self.assertEqual(invoice_total(''), Decimal(0))
        self.assertEqual(invoice_total('description,amount\n\n  \nTea,2.50\n'), Decimal('2.50'))

    def test_invalid_rows_raise_value_error(self):
        for row in ('Tea', 'Tea,2.50,extra', 'Tea,invalid', 'Tea,', '"Tea,2.50'):
            with self.subTest(row=row):
                with self.assertRaises(ValueError):
                    invoice_total('description,amount\nCake,1.00\n' + row + '\n')
