import unittest

from service import NotFound, delete_document, get_document
from store import Store


class DocumentServiceTests(unittest.TestCase):
    def setUp(self):
        self.document = {"id": "document-1", "tenant_id": "owner", "title": "Private"}
        self.store = Store([self.document])

    def test_owner_can_read_document(self):
        self.assertEqual(get_document(self.store, "owner", "document-1"), self.document)

    def test_owner_can_delete_document(self):
        self.assertIsNone(delete_document(self.store, "owner", "document-1"))
        self.assertIsNone(self.store.get("document-1"))

    def test_other_tenant_cannot_read_document(self):
        with self.assertRaises(NotFound) as error:
            get_document(self.store, "other", "document-1")
        self.assertEqual(error.exception.args, ())
        self.assertEqual(self.store.get("document-1"), self.document)

    def test_other_tenant_cannot_delete_document(self):
        with self.assertRaises(NotFound) as error:
            delete_document(self.store, "other", "document-1")
        self.assertEqual(error.exception.args, ())
        self.assertEqual(get_document(self.store, "owner", "document-1"), self.document)

    def test_missing_document_read_raises_not_found(self):
        with self.assertRaises(NotFound) as error:
            get_document(self.store, "owner", "missing")
        self.assertEqual(error.exception.args, ())

    def test_missing_document_delete_raises_not_found(self):
        with self.assertRaises(NotFound) as error:
            delete_document(self.store, "owner", "missing")
        self.assertEqual(error.exception.args, ())
        self.assertEqual(self.store.get("document-1"), self.document)


if __name__ == "__main__":
    unittest.main()
