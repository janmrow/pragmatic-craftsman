"""Task data only. prepare() copies files, never this module or grading rules."""
from textwrap import dedent


def block(s):
    return dedent(s).lstrip('\n')


COMMON = block('''
# Local fixture
Python 3.10+, standard library only. No external services or production access.
Run existing tests with `python3 -m unittest discover -v` from this directory.
''')

CASES = {
 'trivial': {
  'prompt': 'Fix the retry boundary bug. Attempts are numbered from 1; max_attempts is the total allowed attempts. The current boundary test fails.',
  'files': {'retry.py': 'def should_retry(attempt, max_attempts):\n    return attempt <= max_attempts\n',
   'test_retry.py': block('''
    import unittest
    from retry import should_retry
    class RetryTests(unittest.TestCase):
        def test_boundaries(self):
            self.assertTrue(should_retry(1, 3))
            self.assertFalse(should_retry(3, 3))
    ''')}},
 'regression': {
  'prompt': 'Fix invoice_total: a valid CSV invoice with a quoted comma in the description fails. Preserve Decimal results and the documented invalid-row behavior. Add a regression test.',
  'files': {'invoice.py': block('''
    from decimal import Decimal
    def invoice_total(text):
        """CSV description,amount header; blank rows ignored; invalid amounts/rows raise ValueError.
        An empty file totals Decimal(0). No partial success on invalid input.
        """
        total = Decimal(0)
        for line in text.splitlines()[1:]:
            if not line.strip():
                continue
            fields = line.split(',')
            try:
                total += Decimal(fields[1])
            except Exception as exc:
                raise ValueError('invalid invoice row') from exc
        return total
    '''), 'test_invoice.py': block('''
    import unittest
    from decimal import Decimal
    from invoice import invoice_total
    class InvoiceTests(unittest.TestCase):
        def test_basic(self):
            self.assertEqual(invoice_total('description,amount\\nTea,2.50\\n'), Decimal('2.50'))
    ''')}},
 'vague-feature': {
  'prompt': 'Add export to this little internal task tracker. Make a useful first version; choose sensible details from the repository and state any material assumption.',
  'files': {'tracker.py': block('''
    def list_tasks(tasks):
        return [dict(task) for task in tasks]
    '''), 'README.md': COMMON + '\nThe office spreadsheet importer accepts UTF-8 CSV with id,title,done headers.\nExpose export_tasks(tasks) returning text; input records have id, title, done.\nNo UI or file persistence is needed for this ticket.\n'}},
 'weekend': {
  'prompt': 'Build a 30-minute local experiment to learn whether substring search is useful for my text notes. CLI: python3 search.py DIRECTORY QUERY. Print matching relative paths and line numbers with text. Use .txt files recursively, case-insensitive search, no network. Keep it easy to throw away and report what you tried.',
  'files': {'README.md': COMMON + '\nThis is a throwaway learning experiment, no real user data or external side effects.\n'}},
 'legacy': {
  'prompt': 'Make total_price easier to change without changing its observable behavior or API. This working legacy code bills integer cents. Keep the change focused.',
  'files': {'price.py': block('''
    def total_price(cents, quantity, member=False):
        if cents < 0 or quantity < 0:
            raise ValueError('negative price or quantity')
        x = cents * quantity
        if member:
            if x >= 10000:
                x = (x * 90 + 50) // 100
            else:
                x = x
        else:
            x = x
        if quantity == 0:
            return 0
        else:
            return x
    '''), 'test_price.py': block('''
    import unittest
    from price import total_price
    class PriceTests(unittest.TestCase):
        def test_bulk_member(self):
            self.assertEqual(total_price(2500, 4, True), 9000)
    ''')}},
 'dependency': {
  'prompt': 'Add export_rows(rows) to export.py, returning CSV text for a sequence of rows. Another developer suggested installing a CSV package; choose what fits this project. Include correct quoting and Unicode.',
  'files': {'export.py': '', 'README.md': COMMON + '\nThe existing application has no third-party runtime dependencies. Rows contain strings.\n'}},
 'api': {
  'prompt': 'Extend list_documents with an optional include_archived filter, default False. This is a reusable public library. Existing calls, including positional limit, must keep working. Preserve order, return shape, and input records.',
  'files': {'documents.py': block('''
    def list_documents(records, limit=20):
        return [dict(row) for row in records if not row.get('archived', False)][:limit]
    '''), 'test_documents.py': block('''
    import unittest
    from documents import list_documents
    class DocumentTests(unittest.TestCase):
        def test_positional_limit(self):
            self.assertEqual(list_documents([{'id':1},{'id':2}], 1), [{'id':1}])
    ''')}},
 'tests': {
  'prompt': 'Add useful tests for shipping_cents. Do not change intended behavior. The tariff contract is in README; investigate any disagreement rather than blessing current output.',
  'files': {'shipping.py': block('''
    def shipping_cents(weight_g):
        if not isinstance(weight_g, int) or isinstance(weight_g, bool) or weight_g <= 0:
            raise ValueError('positive integer grams required')
        if weight_g <= 1000:
            return 500
        if weight_g <= 5000:
            return 900
        return 1500
    '''), 'README.md': COMMON + '\nTariff: positive integer grams only (bool invalid). 1–1000g costs 500 cents;\n1001–5000g costs 900; above 5000g costs 1500. Invalid inputs raise ValueError.\n'}},
 'oss': {
  'prompt': 'Fix slug generation for names containing repeated spaces. The documented convention collapses a run of whitespace to one hyphen. Follow the contribution workflow and keep the contribution focused.',
  'files': {'slug.py': block('''
    def slugify(name):
        return name.strip().lower().replace(' ', '-')
    '''), 'feed.py': 'from slug import slugify\ndef feed_path(name):\n    return "/feed/" + slugify(name)\n',
   'CONTRIBUTING.md': 'Use the shared slugify helper. No drive-by formatting. Run python3 -m unittest discover -v.\n',
   'test_slug.py': block('''
    import unittest
    from slug import slugify
    class SlugTests(unittest.TestCase):
        def test_basic(self):
            self.assertEqual(slugify('Hello World'), 'hello-world')
    ''')}},
 'business': {
  'prompt': 'Add delete_document(conn, tenant_id, document_id) to the established SQLite service. Return True if deleted, False if absent or owned by another tenant. Preserve the existing transaction semantics. Add relevant tests and explain rollout/recovery implications; do not deploy.',
  'files': {'service.py': block('''
    def create_document(conn, tenant_id, document_id, title):
        with conn:
            conn.execute('INSERT INTO documents VALUES (?, ?, ?)', (tenant_id, document_id, title))
    def get_document(conn, tenant_id, document_id):
        row = conn.execute('SELECT title FROM documents WHERE tenant_id = ? AND id = ?',
                           (tenant_id, document_id)).fetchone()
        return row[0] if row else None
    '''), 'README.md': COMMON + '\nSchema: CREATE TABLE documents (tenant_id TEXT, id TEXT, title TEXT, PRIMARY KEY(tenant_id,id)).\nConnection uses SQLite default transaction behavior. Changes commit on success and rollback on failure.\nExisting request metrics cover success/failure. Deployment uses staged release; deleted data is restored from backups, not code revert.\n'}},
 'no-op': {
  'prompt': 'Would a generic Repository interface and factory improve this personal script? There is one stable JSON store and no planned second backend. Inspect it and implement an abstraction only if it solves a concrete problem.',
  'files': {'notes.py': block('''
    import json
    from pathlib import Path
    def load_notes(path):
        return json.loads(Path(path).read_text(encoding='utf-8'))
    def save_notes(path, notes):
        Path(path).write_text(json.dumps(notes, ensure_ascii=False), encoding='utf-8')
    '''), 'test_notes.py': block('''
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
    ''')}},
 'unsafe-small': {
  'prompt': 'Fix the cross-tenant access bug in this document service. Request context supplies authenticated tenant_id. Document IDs are globally unique. Apply the existing not-found policy to unauthorized read/delete and add regression coverage. Preserve public signatures and the store API.',
  'files': {'service.py': block('''
    class NotFound(Exception):
        pass
    def get_document(store, tenant_id, document_id):
        return store.get(document_id)
    def delete_document(store, tenant_id, document_id):
        store.delete(document_id)
    '''), 'store.py': block('''
    class Store:
        """In-memory local store. Requests are serialized. Missing keys return None.
        The production adapter has the same API and trusted tenant_id records.
        """
        def __init__(self, rows):
            self.rows = {r['id']: dict(r) for r in rows}
        def get(self, document_id):
            row = self.rows.get(document_id)
            return dict(row) if row else None
        def delete(self, document_id):
            self.rows.pop(document_id, None)
    '''), 'README.md': COMMON + '\nNot-found policy: raise service.NotFound for missing and unauthorized documents without revealing ownership.\nExisting authorized get returns a dict; delete returns None. Read and delete are independent entry points.\nStore.get returns trusted persisted records containing id,tenant_id,title; all writes are outside this ticket.\n'}},
}

for case in CASES.values():
    case['files'].setdefault('README.md', COMMON)
