import unittest
from unittest.mock import Mock

from service import NotFound, delete_document, get_document
from store import Store


class DocumentServiceTests(unittest.TestCase):
    def setUp(self):
        self.document = {
            "id": "global-document-id",
            "tenant_id": "tenant-a",
            "title": "Private document",
        }
        self.store = Store([self.document])

    def test_authorized_read_returns_document(self):
        self.assertEqual(
            get_document(self.store, "tenant-a", self.document["id"]),
            self.document,
        )

    def test_cross_tenant_read_raises_not_found(self):
        with self.assertRaises(NotFound) as caught:
            get_document(self.store, "tenant-b", self.document["id"])
        self.assertEqual(str(caught.exception), "")
        self.assertEqual(self.store.get(self.document["id"]), self.document)

    def test_missing_read_raises_not_found(self):
        with self.assertRaises(NotFound) as caught:
            get_document(self.store, "tenant-a", "missing-document")
        self.assertEqual(str(caught.exception), "")

    def test_authorized_delete_returns_none_and_removes_document(self):
        self.assertIsNone(
            delete_document(self.store, "tenant-a", self.document["id"])
        )
        self.assertIsNone(self.store.get(self.document["id"]))

    def test_cross_tenant_delete_raises_not_found_without_deleting(self):
        self.store.delete = Mock(wraps=self.store.delete)
        with self.assertRaises(NotFound) as caught:
            delete_document(self.store, "tenant-b", self.document["id"])
        self.assertEqual(str(caught.exception), "")
        self.store.delete.assert_not_called()
        self.assertEqual(self.store.get(self.document["id"]), self.document)

    def test_missing_delete_raises_not_found_without_deleting(self):
        self.store.delete = Mock(wraps=self.store.delete)
        with self.assertRaises(NotFound) as caught:
            delete_document(self.store, "tenant-a", "missing-document")
        self.assertEqual(str(caught.exception), "")
        self.store.delete.assert_not_called()
        self.assertEqual(self.store.get(self.document["id"]), self.document)


if __name__ == "__main__":
    unittest.main()
