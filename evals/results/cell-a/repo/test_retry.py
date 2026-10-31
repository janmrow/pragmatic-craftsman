import unittest
from retry import should_retry
class RetryTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertTrue(should_retry(1, 3))
        self.assertFalse(should_retry(3, 3))
