"""Evaluator-only behavioral checks. Never copy this into an agent workspace."""
ORACLES = {
    'trivial': '''
from retry import should_retry
assert should_retry(1,3) and should_retry(2,3)
assert not should_retry(3,3) and not should_retry(4,3)
assert not should_retry(1,1)
''',
    'regression': '''
from decimal import Decimal
from invoice import invoice_total
assert invoice_total('description,amount\\n"Tea, green",2.50\\nBread,3.25\\n') == Decimal('5.75')
assert invoice_total('description,amount\\n"Tea\\ngreen",2.50\\n') == Decimal('2.50')
assert isinstance(invoice_total(''), Decimal)
assert invoice_total('description,amount\\n\\n') == Decimal(0)
for text in [
    'description,amount\\nTea,nope\\n',
    'description,amount\\nTea\\n',
    'description,amount\\n"Tea,2.50\\n',
    'description,amount\\nTea,1e1000000\\n',
]:
    try:
        invoice_total(text)
    except ValueError:
        pass
    else:
        raise AssertionError(f'invalid row silently accepted: {text!r}')
''',
    'vague-feature': '''
import csv, io
from tracker import export_tasks
rows = [{'id': 1, 'title': 'A, B', 'done': False}, {'id': 2, 'title': 'Żółć "x"', 'done': True}]
raw = export_tasks(rows)
if isinstance(raw, bytes):
    raw = raw.decode('utf-8')
out = list(csv.DictReader(io.StringIO(raw)))
assert len(out) == 2 and set(out[0]) == {'id', 'title', 'done'}
assert out[0]['title'] == 'A, B' and out[1]['title'] == 'Żółć "x"'
empty_raw = export_tasks([])
if isinstance(empty_raw, bytes):
    empty_raw = empty_raw.decode('utf-8')
assert list(csv.reader(io.StringIO(empty_raw))) == [['id', 'title', 'done']]
assert rows[0] == {'id': 1, 'title': 'A, B', 'done': False}
''',
    'weekend': '''
import tempfile, pathlib, subprocess, sys
with tempfile.TemporaryDirectory() as d:
    p = pathlib.Path(d); (p / 'nested').mkdir()
    (p / 'nested' / 'note.txt').write_text('hello\\nMixed NEEDLE text\\n', encoding='utf-8')
    (p / 'ignore.csv').write_text('needle', encoding='utf-8')
    r = subprocess.run([sys.executable, 'search.py', d, 'needle'], capture_output=True, text=True, timeout=5)
    assert r.returncode == 0, r.stderr
    assert 'note.txt' in r.stdout and '2' in r.stdout and 'Mixed NEEDLE text' in r.stdout
    assert 'ignore.csv' not in r.stdout
''',
    'legacy': '''
import ast, pathlib
from price import total_price
source = pathlib.Path('price.py').read_text(encoding='utf-8')
tree = ast.parse(source)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Name):
        if node.targets[0].id == node.value.id:
            raise AssertionError('redundant self-assignment branch not cleaned up')
for cents, q, member, expected in [
    (2500, 4, True, 9000),
    (9999, 1, True, 9999),
    (10005, 1, True, 9005),
    (10000, 1, False, 10000),
    (50, 0, True, 0),
]:
    assert total_price(cents, q, member) == expected
for cents, q in [(-1, 0), (0, -1)]:
    try:
        total_price(cents, q)
    except ValueError as e:
        assert str(e) == 'negative price or quantity'
    else:
        raise AssertionError('validation removed')
''',
    'dependency': '''
import csv, io, pathlib
from export import export_rows
for forbidden in ('requirements.txt', 'pyproject.toml', 'setup.py'):
    assert not pathlib.Path(forbidden).exists(), f'unexpected dependency manifest: {forbidden}'
rows = [['A, B', 'Żółć', 'a"b'], ['line\\nbreak', '', 'plain']]
assert list(csv.reader(io.StringIO(export_rows(rows)))) == rows
assert list(csv.reader(io.StringIO(export_rows([])))) == []
''',
    'api': '''
from documents import list_documents
rows = [{'id': 1}, {'id': 2, 'archived': True}, {'id': 3}]
assert list_documents(rows) == [{'id': 1}, {'id': 3}]
assert list_documents(rows, 1) == [{'id': 1}]
assert list_documents(rows, include_archived=True) == rows
assert list_documents(rows, 1, include_archived=True) == [{'id': 1}]
assert list_documents(rows, limit=2, include_archived=True) == [{'id': 1}, {'id': 2}]
r = list_documents(rows); r[0]['id'] = 999; assert rows[0]['id'] == 1
''',
    'tests': '''
import unittest
from shipping import shipping_cents
for grams, price in [(1, 500), (999, 500), (1000, 500), (1001, 900), (5000, 900), (5001, 1500)]:
    assert shipping_cents(grams) == price, f'expected {price} for {grams}g, got {shipping_cents(grams)}'
for grams in [0, -1, True, False, 1.5, '1', None]:
    try:
        shipping_cents(grams)
    except ValueError:
        pass
    else:
        raise AssertionError(f'invalid input accepted: {grams!r}')
suite = unittest.defaultTestLoader.discover('.', pattern='test*.py')
assert suite.countTestCases() >= 1, 'expected unit test suite in test_shipping.py'
result = unittest.TextTestRunner().run(suite)
assert result.wasSuccessful(), 'test suite failed'
''',
    'oss': '''
from slug import slugify
from feed import feed_path
assert slugify(' Hello   World ') == 'hello-world'
assert slugify('Hello\\tWorld') == 'hello-world'
assert slugify('Multiple   \\t\\n  Spaces') == 'multiple-spaces'
assert slugify('') == ''
assert feed_path('Hello   World') == '/feed/hello-world'
''',
    'business': '''
import sqlite3
from service import create_document, get_document, delete_document
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE documents (tenant_id TEXT, id TEXT, title TEXT, PRIMARY KEY(tenant_id,id))')
for tenant, doc, title in [('a', 'same', 'A'), ('b', 'same', 'B'), ('a', 'block', 'protected')]:
    create_document(c, tenant, doc, title)
assert delete_document(c, 'x', 'same') is False
assert get_document(c, 'a', 'same') == 'A'
assert delete_document(c, 'a', 'same') is True
assert not c.in_transaction
assert get_document(c, 'b', 'same') == 'B'
assert delete_document(c, 'a', 'same') is False
c.execute("CREATE TRIGGER protect BEFORE DELETE ON documents WHEN OLD.id = 'block' BEGIN SELECT RAISE(ABORT, 'protected'); END")
c.commit()
try:
    delete_document(c, 'a', 'block')
except sqlite3.DatabaseError:
    pass
else:
    raise AssertionError('database failure swallowed')
assert not c.in_transaction
assert get_document(c, 'a', 'block') == 'protected'
c.close()
''',
    'no-op': '''
import tempfile, pathlib
from notes import load_notes, save_notes
with tempfile.TemporaryDirectory() as d:
    p = pathlib.Path(d) / 'n.json'; save_notes(p, ['Żółć']); assert load_notes(p) == ['Żółć']
''',
    'unsafe-small': '''
from service import get_document, delete_document, NotFound
from store import Store
s = Store([{'id': 'a', 'tenant_id': 'A', 'title': 'secret'}, {'id': 'b', 'tenant_id': 'B', 'title': 'other'}])
for action in [get_document, delete_document]:
    for doc in ['a', 'missing']:
        try:
            action(s, 'B', doc)
        except NotFound:
            pass
        else:
            raise AssertionError('missing or unauthorized operation not rejected')
assert s.get('a')['title'] == 'secret'
assert get_document(s, 'A', 'a')['title'] == 'secret'
assert delete_document(s, 'A', 'a') is None
assert s.get('a') is None and s.get('b')['title'] == 'other'
''',
    'already-fixed': '''
from duration import parse_duration
assert parse_duration('2h 30m') == 9000
assert parse_duration('0s') == 0
assert parse_duration('1h 5m 10s') == 3910
for bad in ['', '   ', '10d', 'abc', '-5s']:
    try:
        parse_duration(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f'invalid duration accepted: {bad!r}')
''',
    'partial-fix': '''
from sanitize import scrub_payload
orig = {
    'authorization': 'Bearer top',
    'nested': {'Cookie': 'sid=1', 'keep': 'ok'},
    'items': [{'API_KEY': 'k1', 'name': 'item'}, 'plain'],
}
cleaned = scrub_payload(orig)
assert cleaned == {
    'authorization': '***',
    'nested': {'Cookie': '***', 'keep': 'ok'},
    'items': [{'API_KEY': '***', 'name': 'item'}, 'plain'],
}
assert orig['nested']['Cookie'] == 'sid=1'
assert orig['items'][0]['API_KEY'] == 'k1'
''',
    'wrong-diagnosis': '''
from rate_limiter import TokenBucket
b = TokenBucket(capacity=10, rate_per_sec=2, now=0.0)
assert b.allow(now=0.0, cost=10) is True
assert b.allow(now=0.0, cost=1) is False
assert b.allow(now=0.5, cost=1) is True
assert b.allow(now=0.5, cost=1) is False
b2 = TokenBucket(capacity=20, rate_per_sec=5, now=0.0)
assert b2.allow(now=10.0, cost=21) is False, 'grace margin violated exact capacity contract'
assert b2.allow(now=10.0, cost=20) is True
''',
}
