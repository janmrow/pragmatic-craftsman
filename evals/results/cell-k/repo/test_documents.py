import unittest
from documents import list_documents


class DocumentTests(unittest.TestCase):
    def test_positional_limit(self):
        self.assertEqual(list_documents([{'id':1},{'id':2}], 1), [{'id':1}])

    def test_archived_records_are_excluded_by_default(self):
        records = [
            {'id': 1, 'archived': True},
            {'id': 2},
            {'id': 3, 'archived': False},
            {'id': 4, 'archived': 'yes'},
        ]
        self.assertEqual(list_documents(records), [records[1], records[2]])
        self.assertEqual(
            list_documents(records, include_archived=False),
            [records[1], records[2]],
        )

    def test_include_archived_preserves_order_and_positional_limit(self):
        records = [
            {'id': 1, 'archived': True},
            {'id': 2},
            {'id': 3, 'archived': False},
        ]
        self.assertEqual(
            list_documents(records, 2, include_archived=True),
            records[:2],
        )
        self.assertEqual(list_documents(records, include_archived=True), records)

    def test_limit_is_applied_after_filtering(self):
        records = [{'id': 1, 'archived': True}, {'id': 2}, {'id': 3}]
        self.assertEqual(list_documents(records, limit=1), [records[1]])
        self.assertEqual(list_documents(records, 0, include_archived=True), [])

    def test_returns_new_dictionaries_without_changing_input(self):
        records = [{'id': 1, 'archived': True}, {'id': 2}]
        original = [dict(row) for row in records]
        for include_archived in (False, True):
            with self.subTest(include_archived=include_archived):
                result = list_documents(records, include_archived=include_archived)
                self.assertIsInstance(result, list)
                for row in result:
                    self.assertIsInstance(row, dict)
                    self.assertTrue(all(row is not source for source in records))
                    row['id'] = 'changed'
                self.assertEqual(records, original)

    def test_default_limit_remains_twenty(self):
        records = [{'id': index} for index in range(25)]
        self.assertEqual(list_documents(records), records[:20])
        self.assertEqual(
            list_documents(records, include_archived=True), records[:20]
        )
