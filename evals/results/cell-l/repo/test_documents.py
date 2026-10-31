import unittest
from documents import list_documents


class DocumentTests(unittest.TestCase):
    def test_positional_limit(self):
        self.assertEqual(list_documents([{'id':1},{'id':2}], 1), [{'id':1}])

    def test_archived_records_excluded_before_limit(self):
        records = [
            {'id': 1, 'archived': True},
            {'id': 2},
            {'id': 3, 'archived': False},
        ]
        self.assertEqual(list_documents(records, 1), [{'id': 2}])
        self.assertEqual(list_documents(records), records[1:])
        self.assertEqual(list_documents(records, include_archived=False), records[1:])

    def test_include_archived_preserves_order_and_limit(self):
        records = [
            {'id': 1, 'archived': True},
            {'id': 2},
            {'id': 3, 'archived': False},
        ]
        self.assertEqual(list_documents(records, include_archived=True), records)
        self.assertEqual(list_documents(records, 2, include_archived=True), records[:2])
        self.assertEqual(list_documents(records, limit=1, include_archived=True), records[:1])

    def test_results_are_copies_and_inputs_are_unchanged(self):
        for include_archived in (False, True):
            with self.subTest(include_archived=include_archived):
                records = [{'id': 1}, {'id': 2, 'archived': True}]
                original = [dict(row) for row in records]
                result = list_documents(records, include_archived=include_archived)
                self.assertIsInstance(result, list)
                self.assertEqual(records, original)
                for row, source in zip(result, records):
                    self.assertIsInstance(row, dict)
                    self.assertIsNot(row, source)
                    row['id'] = 'changed'
                self.assertEqual(records, original)
