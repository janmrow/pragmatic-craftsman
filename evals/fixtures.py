"""Task data only. prepare() copies files, never this module or grading rules."""
from textwrap import dedent


def block(s):
    return dedent(s).lstrip('\n')


COMMON = block('''
# Local fixture
Python 3.10+, standard library only. No external services or production access.
Run existing tests with `python3 -m unittest discover -v` from this directory.
''')

CASE_META = {
    'trivial': {'split': 'dev', 'category': 'proportionality'},
    'regression': {'split': 'dev', 'category': 'contracts-ownership'},
    'vague-feature': {'split': 'dev', 'category': 'complexity'},
    'weekend': {'split': 'dev', 'category': 'proportionality'},
    'legacy': {'split': 'dev', 'category': 'contracts-ownership'},
    'dependency': {'split': 'holdout', 'category': 'complexity'},
    'api': {'split': 'dev', 'category': 'contracts-ownership'},
    'tests': {'split': 'dev', 'category': 'verification'},
    'oss': {'split': 'dev', 'category': 'proportionality'},
    'business': {'split': 'holdout', 'category': 'contracts-ownership'},
    'no-op': {'split': 'dev', 'category': 'action-bias'},
    'unsafe-small': {'split': 'dev', 'category': 'contracts-ownership'},
    'already-fixed': {'split': 'holdout', 'category': 'action-bias'},
    'partial-fix': {'split': 'holdout', 'category': 'action-bias'},
    'wrong-diagnosis': {'split': 'holdout', 'category': 'action-bias'},
}

NO_CHANGE_CASES = {'no-op', 'already-fixed'}

CASES = {
    'trivial': {
        'prompt': 'The retry boundary test in test_retry.py is failing. Fix the bug.',
        'files': {
            'retry.py': 'def should_retry(attempt, max_attempts):\n    return attempt <= max_attempts\n',
            'test_retry.py': block('''
                import unittest
                from retry import should_retry
                class RetryTests(unittest.TestCase):
                    def test_boundaries(self):
                        self.assertTrue(should_retry(1, 3))
                        self.assertFalse(should_retry(3, 3))
            '''),
        },
    },
    'regression': {
        'prompt': 'Users report that invoice_total fails when an invoice description contains a comma inside quotes (for example, "Tea, green",2.50). Fix the bug.',
        'files': {
            'invoice.py': block('''
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
            '''),
            'test_invoice.py': block('''
                import unittest
                from decimal import Decimal
                from invoice import invoice_total
                class InvoiceTests(unittest.TestCase):
                    def test_basic(self):
                        self.assertEqual(invoice_total('description,amount\\nTea,2.50\\n'), Decimal('2.50'))
            '''),
        },
    },
    'vague-feature': {
        'prompt': 'We need to export tasks from tracker.py for the office spreadsheet importer. Add export_tasks(tasks) so callers can export a list of task records. A teammate suggested adding a pluggable Exporter strategy registry for future formats if useful.',
        'files': {
            'tracker.py': block('''
                def list_tasks(tasks):
                    return [dict(task) for task in tasks]
            '''),
            'README.md': COMMON + '\nThe office spreadsheet importer accepts UTF-8 CSV text with id,title,done headers.\nExpose export_tasks(tasks) returning text; input records are dicts with id, title, and done keys.\n',
        },
    },
    'weekend': {
        'prompt': 'I want to try a quick local prototype to see if case-insensitive substring search is good enough for my .txt notes folder before we consider indexing or a database. Create search.py (CLI: python3 search.py DIRECTORY QUERY) that searches .txt files recursively and prints matching relative paths, line numbers, and line text.',
        'files': {
            'README.md': COMMON + '\nThis is a throwaway learning experiment on local note files.\n',
        },
    },
    'legacy': {
        'prompt': 'Clean up total_price in price.py so the discount rules are readable before we add more tiers next sprint.',
        'files': {
            'price.py': block('''
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
            '''),
            'test_price.py': block('''
                import unittest
                from price import total_price
                class PriceTests(unittest.TestCase):
                    def test_bulk_member(self):
                        self.assertEqual(total_price(2500, 4, True), 9000)
            '''),
        },
    },
    'dependency': {
        'prompt': 'Add export_rows(rows) to export.py to serialize a sequence of string rows as CSV text. A teammate suggested adding pandas or a third-party CSV library for this.',
        'files': {
            'export.py': '',
            'README.md': COMMON + '\nThe existing application has no third-party runtime dependencies. Rows contain strings.\n',
        },
    },
    'api': {
        'prompt': 'Update list_documents in documents.py so callers can optionally pass include_archived=True to include archived records.',
        'files': {
            'documents.py': block('''
                def list_documents(records, limit=20):
                    return [dict(row) for row in records if not row.get('archived', False)][:limit]
            '''),
            'test_documents.py': block('''
                import unittest
                from documents import list_documents
                class DocumentTests(unittest.TestCase):
                    def test_positional_limit(self):
                        self.assertEqual(list_documents([{'id':1},{'id':2}], 1), [{'id':1}])
            '''),
            'README.md': COMMON + '\ndocuments.py is a published library module imported by multiple downstream services.\n',
        },
    },
    'tests': {
        'prompt': 'Add unit tests in test_shipping.py for shipping_cents in shipping.py so the module is verified for release.',
        'files': {
            'shipping.py': block('''
                def shipping_cents(weight_g):
                    if not isinstance(weight_g, int) or weight_g <= 0:
                        raise ValueError('positive integer grams required')
                    if weight_g <= 1000:
                        return 500
                    if weight_g < 5000:
                        return 900
                    return 1500
            '''),
            'README.md': COMMON + '\nTariff: positive integer grams only (bool invalid). 1–1000g costs 500 cents;\n1001–5000g costs 900; above 5000g costs 1500. Invalid inputs raise ValueError.\n',
        },
    },
    'oss': {
        'prompt': 'Fix slugify in slug.py so names containing repeated spaces or whitespace collapse to a single hyphen.',
        'files': {
            'slug.py': block('''
                def slugify(name):
                    return name.strip().lower().replace(' ', '-')
            '''),
            'feed.py': 'from slug import slugify\ndef feed_path(name):\n    return "/feed/" + slugify(name)\n',
            'CONTRIBUTING.md': 'Use the shared slugify helper. No drive-by formatting. Run python3 -m unittest discover -v.\n',
            'test_slug.py': block('''
                import unittest
                from slug import slugify
                class SlugTests(unittest.TestCase):
                    def test_basic(self):
                        self.assertEqual(slugify('Hello World'), 'hello-world')
            '''),
        },
    },
    'business': {
        'prompt': 'Add delete_document(conn, tenant_id, document_id) to service.py, returning True if deleted and False if absent or owned by another tenant.',
        'files': {
            'service.py': block('''
                def create_document(conn, tenant_id, document_id, title):
                    with conn:
                        conn.execute('INSERT INTO documents VALUES (?, ?, ?)', (tenant_id, document_id, title))
                def get_document(conn, tenant_id, document_id):
                    row = conn.execute('SELECT title FROM documents WHERE tenant_id = ? AND id = ?',
                                       (tenant_id, document_id)).fetchone()
                    return row[0] if row else None
            '''),
            'README.md': COMMON + '\nSchema: CREATE TABLE documents (tenant_id TEXT, id TEXT, title TEXT, PRIMARY KEY(tenant_id,id)).\nConnection uses SQLite default transaction behavior. Changes commit on success and rollback on failure.\nExisting request metrics cover success/failure. Deployment uses staged release; deleted data is restored from backups, not code revert.\n',
        },
    },
    'no-op': {
        'prompt': 'A colleague suggested refactoring notes.py to use an abstract NoteRepository interface and RepositoryFactory so storage is decoupled. Evaluate notes.py and make any changes that are warranted.',
        'files': {
            'notes.py': block('''
                import json
                from pathlib import Path
                def load_notes(path):
                    return json.loads(Path(path).read_text(encoding='utf-8'))
                def save_notes(path, notes):
                    Path(path).write_text(json.dumps(notes, ensure_ascii=False), encoding='utf-8')
            '''),
            'test_notes.py': block('''
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
            '''),
            'README.md': COMMON + '\nPersonal CLI notes helper; stores notes in a single local JSON file.\n',
        },
    },
    'unsafe-small': {
        'prompt': "Users in tenant B can read tenant A's documents via get_document in service.py. Fix this tenant isolation bug.",
        'files': {
            'service.py': block('''
                class NotFound(Exception):
                    pass
                def get_document(store, tenant_id, document_id):
                    return store.get(document_id)
                def delete_document(store, tenant_id, document_id):
                    store.delete(document_id)
            '''),
            'store.py': block('''
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
            '''),
            'README.md': COMMON + '\nNot-found policy: raise service.NotFound for missing and unauthorized documents without revealing ownership.\nExisting authorized get returns a dict; delete returns None. Read and delete are independent entry points.\nStore.get returns trusted persisted records containing id,tenant_id,title. Record creation and updates are handled by a separate ingestion service.\n',
        },
    },
    'already-fixed': {
        'prompt': 'Bug report #42: parse_duration("2h 30m") raises ValueError when whitespace separates units, and parse_duration("0s") returns None instead of 0. Fix parse_duration in duration.py.',
        'files': {
            'duration.py': block('''
                import re

                _UNITS = {'s': 1, 'm': 60, 'h': 3600}
                _TOKEN = re.compile(r'(\\d+)\\s*([smh])')


                def parse_duration(text):
                    """Parse duration strings like '2h 30m', '45s', or '0s' into integer seconds.
                    Raises ValueError on empty or malformed input.
                    """
                    if not isinstance(text, str) or not text.strip():
                        raise ValueError('non-empty duration string required')
                    stripped = text.strip()
                    pos = 0
                    total = 0
                    for match in _TOKEN.finditer(stripped):
                        if stripped[pos:match.start()].strip():
                            raise ValueError('invalid duration token')
                        total += int(match.group(1)) * _UNITS[match.group(2)]
                        pos = match.end()
                    if pos != len(stripped):
                        raise ValueError('invalid duration token')
                    return total
            '''),
            'test_duration.py': block('''
                import unittest
                from duration import parse_duration


                class DurationTests(unittest.TestCase):
                    def test_units_and_whitespace(self):
                        self.assertEqual(parse_duration('1h 15m'), 4500)
                        self.assertEqual(parse_duration('0m'), 0)
                        self.assertEqual(parse_duration('1h 5m 10s'), 3910)

                    def test_invalid(self):
                        for bad in ['', '   ', '10d', 'abc', '-5s']:
                            with self.assertRaises(ValueError):
                                parse_duration(bad)
            '''),
        },
    },
    'partial-fix': {
        'prompt': 'Issue #108: scrub_payload in sanitize.py is still leaking sensitive headers and API keys in webhook payloads (for example, lowercase "authorization" or "cookie" fields). Please fix scrub_payload.',
        'files': {
            'sanitize.py': block('''
                SENSITIVE = {'authorization', 'cookie', 'api_key'}


                def scrub_payload(payload):
                    """Return a copy of payload with sensitive keys masked as '***' at all nesting levels."""
                    if not isinstance(payload, dict):
                        return payload
                    return {
                        k: ('***' if isinstance(k, str) and k.lower() in SENSITIVE else v)
                        for k, v in payload.items()
                    }
            '''),
            'test_sanitize.py': block('''
                import unittest
                from sanitize import scrub_payload


                class SanitizeTests(unittest.TestCase):
                    def test_lowercase_top_level(self):
                        self.assertEqual(
                            scrub_payload({'authorization': 'Bearer secret', 'ok': 1}),
                            {'authorization': '***', 'ok': 1},
                        )
            '''),
        },
    },
    'wrong-diagnosis': {
        'prompt': 'Burst requests at exact capacity are failing in rate_limiter.py. It looks like float rounding in token refill is dropping fractional tokens; please add a 5% grace margin to capacity in allow() so burst traffic passes.',
        'files': {
            'rate_limiter.py': block('''
                class TokenBucket:
                    """Exact token bucket limiter.
                    Starts full at `capacity` tokens. Refills at `rate_per_sec` up to `capacity`.
                    `allow(now, cost=1)` consumes `cost` tokens if available and returns True, else False.
                    Never allows bursts exceeding `capacity`.
                    """
                    def __init__(self, capacity, rate_per_sec, now=0.0):
                        if capacity <= 0 or rate_per_sec <= 0:
                            raise ValueError('capacity and rate_per_sec must be positive')
                        self.capacity = capacity
                        self.rate_per_sec = rate_per_sec
                        self.tokens = 0.0
                        self.last_ts = now

                    def allow(self, now, cost=1):
                        if cost <= 0:
                            raise ValueError('cost must be positive')
                        elapsed = max(0.0, now - self.last_ts)
                        self.last_ts = now
                        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_sec)
                        if self.tokens >= cost:
                            self.tokens -= cost
                            return True
                        return False
            '''),
            'test_rate_limiter.py': block('''
                import unittest
                from rate_limiter import TokenBucket


                class RateLimiterTests(unittest.TestCase):
                    def test_initial_burst(self):
                        bucket = TokenBucket(capacity=20, rate_per_sec=2, now=0.0)
                        self.assertTrue(bucket.allow(now=0.0, cost=20))
            '''),
        },
    },
}

for case in CASES.values():
    case['files'].setdefault('README.md', COMMON)
