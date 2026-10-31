import tempfile
import unittest
from pathlib import Path
from notes import load_notes, save_notes
class NotesTests(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'notes.json'
            save_notes(path, ['hello'])
            self.assertEqual(load_notes(path), ['hello'])
