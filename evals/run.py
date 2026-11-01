#!/usr/bin/env python3
"""Prepare isolated fixture repos; validate package & manifest; score runs with independent checks."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time

from fixtures import CASES, CASE_META, NO_CHANGE_CASES
from oracles import ORACLES

ROOT = Path(__file__).resolve().parent.parent
DIMENSIONS = [
    'correctness', 'scope_discipline', 'simplicity', 'completeness',
    'verification_quality', 'test_value', 'semantic_quality', 'reviewability',
    'maintainability', 'efficiency',
]

HOST_LOCATIONS = {
    'codex': '.agents/skills',
    'claude': '.claude/skills',
    'opencode': '.opencode/skills',
    'gemini': '.gemini/skills',
}

HOST_EXPLICIT_PREFIX = {
    'codex': 'Use $pragmatic-craftsman.',
    'claude': 'Use /pragmatic-craftsman.',
    'opencode': 'Use @pragmatic-craftsman.',
    'gemini': 'Activate the pragmatic-craftsman skill.',
}

IGNORED_DIRS = {
    '.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.agents', '.claude', '.opencode', '.gemini',
}


def command(args, cwd, timeout=20):
    start = time.monotonic()
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return {
            'command': args,
            'exit_code': r.returncode,
            'stdout': r.stdout,
            'stderr': r.stderr,
            'seconds': round(time.monotonic() - start, 3),
        }
    except subprocess.TimeoutExpired as e:
        def dec(v):
            return v.decode(errors='replace') if isinstance(v, bytes) else v or ''
        return {
            'command': args,
            'exit_code': None,
            'timeout': True,
            'stdout': dec(e.stdout),
            'stderr': dec(e.stderr),
            'seconds': round(time.monotonic() - start, 3),
        }


def git(repo, *args):
    r = command(['git', *args], repo)
    if r['exit_code'] != 0:
        raise RuntimeError(r)
    return r['stdout']


def hashes(root, ignore_relpaths=()):
    ignored = {Path(p) for p in ignore_relpaths if p}
    out = {}
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if any(rel == ig or ig in rel.parents for ig in ignored):
            continue
        out[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def stage_skill(args, dest):
    if args.arm == 'off':
        return None, 'none'
    if args.skill:
        src = Path(args.skill).resolve()
        version = f'{args.arm[1:]}.0' if args.arm in ('v0.1', 'v0.2', 'v0.3') else 'custom'
        return src, version
    if args.arm in ('v0.1', 'v0.2'):
        archive_file = (
            ROOT / 'evals' / 'results' / ('v0.2-skill.json' if args.arm == 'v0.2' else 'iteration-1-skill.json')
        )
        data = json.loads(archive_file.read_text(encoding='utf-8'))
        skill_dir = dest / '.skill' / 'pragmatic-craftsman'
        for rel, content in data.items():
            if rel == 'version':
                continue
            target = skill_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        return skill_dir, f'{args.arm[1:]}.0'
    return (ROOT / 'pragmatic-craftsman').resolve(), '0.3.0'


def prepare(args):
    dest = Path(args.dest).resolve()
    if dest.exists() and any(dest.iterdir()):
        raise ValueError('Destination must be empty or new')
    repo = dest / 'repo'
    repo.mkdir(parents=True)
    for name, content in CASES[args.case]['files'].items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
    (repo / '.gitignore').write_text(
        '__pycache__/\n*.pyc\n.pytest_cache/\n.mypy_cache/\n.ruff_cache/\n',
        encoding='utf-8',
    )
    git(repo, 'init', '-q')
    exclude_file = repo / '.git' / 'info' / 'exclude'
    exclude_file.parent.mkdir(parents=True, exist_ok=True)
    with exclude_file.open('a', encoding='utf-8') as f:
        f.write('\n/.agents/\n/.claude/\n/.opencode/\n/.gemini/\n')
    git(repo, 'add', '.')
    git(repo, '-c', 'user.name=Local Eval', '-c', 'user.email=eval@example.invalid', 'commit', '-qm', 'Fixture baseline')
    baseline_commit = git(repo, 'rev-parse', 'HEAD').strip()

    prompt = CASES[args.case]['prompt']
    skill_hashes = {}
    installed_rel = None
    external_skill_read = False
    native_host = getattr(args, 'native_host', None)
    invocation_mode = getattr(args, 'invocation', None)
    skill_dir, skill_version = stage_skill(args, dest)

    if args.arm != 'off':
        if not skill_dir or not (skill_dir / 'SKILL.md').is_file():
            raise ValueError('Missing SKILL.md')
        skill_hashes = hashes(skill_dir)
        if not invocation_mode:
            invocation_mode = 'explicit' if native_host else 'file'
        if native_host:
            rel_root = HOST_LOCATIONS[native_host]
            installed_rel = f'{rel_root}/pragmatic-craftsman'
            installed = repo / installed_rel
            shutil.copytree(skill_dir, installed)
            if invocation_mode == 'explicit':
                prompt = HOST_EXPLICIT_PREFIX[native_host] + '\n\n' + prompt
            elif invocation_mode == 'file':
                prompt = f'Read and apply the skill at {installed_rel}/SKILL.md.\n\n' + prompt
        else:
            if invocation_mode == 'implicit':
                raise ValueError('--invocation implicit requires --native-host')
            local_skill = dest / '.skill' / 'pragmatic-craftsman'
            if skill_dir != local_skill:
                shutil.copytree(skill_dir, local_skill, dirs_exist_ok=True)
            prompt = f'Read and apply the skill at {local_skill}/SKILL.md.\n\n' + prompt
            external_skill_read = True
    else:
        invocation_mode = 'off'

    trailer = '\n\nWork only in this repository'
    if external_skill_read:
        trailer += ', except reading the skill file above'
    trailer += '. Do not inspect parent or sibling directories.'
    prompt += trailer
    (dest / 'prompt.txt').write_text(prompt + '\n', encoding='utf-8')
    ignore_rels = (installed_rel, installed_rel.split('/')[0]) if installed_rel else ()
    meta = {
        'case': args.case,
        'split': CASE_META[args.case]['split'],
        'category': CASE_META[args.case]['category'],
        'arm': args.arm,
        'skill_version': skill_version,
        'created_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'repo': str(repo),
        'baseline_commit': baseline_commit,
        'baseline_files': hashes(repo, ignore_rels),
        'skill_files': skill_hashes,
        'installed_skill_relpath': installed_rel,
        'native_host': native_host,
        'invocation': f'{native_host}:{invocation_mode}' if native_host and args.arm != 'off' else invocation_mode,
        'runtime': {
            'python': sys.version.split()[0],
            'agent': 'record manually',
            'model': 'record manually',
            'effort': 'record manually',
            'instruction_isolation': 'record manually',
        },
    }
    save(dest / 'run.json', meta)
    save(dest / 'rubric.json', {d: {'score': None, 'evidence': ''} for d in DIMENSIONS})
    print(json.dumps({'run': str(dest), 'repo': str(repo), 'prompt': str(dest / 'prompt.txt'), 'arm': args.arm, 'skill_version': skill_version}))


def own_tests(repo):
    r = command([sys.executable, '-m', 'unittest', 'discover', '-v'], repo)
    count = re.search(r'Ran (\d+) tests?', r['stderr'])
    r['test_count'] = int(count.group(1)) if count else None
    r['status'] = 'none' if r['test_count'] == 0 else 'passed' if r['exit_code'] == 0 else 'failed'
    return r


def replace_function(source, func_name, new_def_src, class_name=None):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    scope = tree.body
    indent = ''
    if class_name:
        cls = next(
            (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name),
            None,
        )
        if not cls:
            return None
        scope = cls.body
        indent = '    '
    fn = next(
        (n for n in scope if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func_name),
        None,
    )
    if not fn:
        return None
    start_line = fn.decorator_list[0].lineno if fn.decorator_list else fn.lineno
    lines = source.splitlines(keepends=True)
    replacement = textwrap.indent(textwrap.dedent(new_def_src).strip('\n') + '\n', indent)
    lines[start_line - 1 : fn.end_lineno] = [replacement]
    return ''.join(lines)


# Each probe is (label, filename, func_name, replacement_src, optional_class_name)
MUTATION_PROBES = {
    'trivial': [
        ('boundary-le', 'retry.py', 'should_retry', '''
            def should_retry(attempt, max_attempts):
                return attempt <= max_attempts
        ''', None),
    ],
    'regression': [
        ('quoted-csv-split', 'invoice.py', 'invoice_total', '''
            def invoice_total(text):
                total = Decimal(0)
                for line in text.splitlines()[1:]:
                    if not line.strip():
                        continue
                    fields = line.split(',')
                    if len(fields) != 2:
                        raise ValueError('invalid invoice row')
                    try:
                        total += Decimal(fields[1])
                    except Exception as exc:
                        raise ValueError('invalid invoice row') from exc
                return total
        ''', None),
    ],
    'vague-feature': [
        ('headerless-unquoted-csv', 'tracker.py', 'export_tasks', '''
            def export_tasks(tasks):
                return '\\n'.join(f"{t['id']},{t['title']},{t['done']}" for t in tasks) + '\\n'
        ''', None),
    ],
    'legacy': [
        ('truncating-discount', 'price.py', 'total_price', '''
            def total_price(cents, quantity, member=False):
                if cents < 0 or quantity < 0:
                    raise ValueError('negative price or quantity')
                x = cents * quantity
                if member and x >= 10000:
                    return (x * 90) // 100
                return 0 if quantity == 0 else x
        ''', None),
        ('negative-input-accepted', 'price.py', 'total_price', '''
            def total_price(cents, quantity, member=False):
                x = cents * quantity
                if member and x >= 10000:
                    return (x * 90 + 50) // 100
                return 0 if quantity == 0 else x
        ''', None),
    ],
    'dependency': [
        ('unquoted-join', 'export.py', 'export_rows', '''
            def export_rows(rows):
                return '\\n'.join(','.join(r) for r in rows)
        ''', None),
    ],
    'api': [
        ('broken-positional-limit', 'documents.py', 'list_documents', '''
            def list_documents(records, include_archived=False, limit=20):
                return [dict(row) for row in records if include_archived or not row.get('archived', False)][:limit]
        ''', None),
        ('ignored-include-archived', 'documents.py', 'list_documents', '''
            def list_documents(records, limit=20, include_archived=False):
                return [dict(row) for row in records if not row.get('archived', False)][:limit]
        ''', None),
    ],
    'tests': [
        ('threshold-1000', 'shipping.py', 'shipping_cents', '''
            def shipping_cents(weight_g):
                if not isinstance(weight_g, int) or isinstance(weight_g, bool) or weight_g <= 0:
                    raise ValueError('positive integer grams required')
                if weight_g < 1000:
                    return 500
                if weight_g <= 5000:
                    return 900
                return 1500
        ''', None),
        ('threshold-5000', 'shipping.py', 'shipping_cents', '''
            def shipping_cents(weight_g):
                if not isinstance(weight_g, int) or isinstance(weight_g, bool) or weight_g <= 0:
                    raise ValueError('positive integer grams required')
                if weight_g <= 1000:
                    return 500
                if weight_g < 5000:
                    return 900
                return 1500
        ''', None),
        ('bool-accepted', 'shipping.py', 'shipping_cents', '''
            def shipping_cents(weight_g):
                if not isinstance(weight_g, int) or weight_g <= 0:
                    raise ValueError('positive integer grams required')
                if weight_g <= 1000:
                    return 500
                if weight_g <= 5000:
                    return 900
                return 1500
        ''', None),
    ],
    'oss': [
        ('single-space-replace', 'slug.py', 'slugify', '''
            def slugify(name):
                return name.strip().lower().replace(' ', '-')
        ''', None),
    ],
    'business': [
        ('unscoped-tenant-delete', 'service.py', 'delete_document', '''
            def delete_document(conn, tenant_id, document_id):
                with conn:
                    cur = conn.execute('DELETE FROM documents WHERE id = ?', (document_id,))
                    return cur.rowcount > 0
        ''', None),
    ],
    'unsafe-small': [
        ('cross-tenant-read', 'service.py', 'get_document', '''
            def get_document(store, tenant_id, document_id):
                row = store.get(document_id)
                if not row:
                    raise NotFound(document_id)
                return row
        ''', None),
        ('cross-tenant-delete', 'service.py', 'delete_document', '''
            def delete_document(store, tenant_id, document_id):
                if not store.get(document_id):
                    raise NotFound(document_id)
                store.delete(document_id)
        ''', None),
    ],
    'partial-fix': [
        ('top-level-only', 'sanitize.py', 'scrub_payload', '''
            def scrub_payload(payload):
                if not isinstance(payload, dict):
                    return payload
                return {
                    k: ('***' if isinstance(k, str) and k.lower() in SENSITIVE else v)
                    for k, v in payload.items()
                }
        ''', None),
    ],
    'wrong-diagnosis': [
        ('grace-margin-leak', 'rate_limiter.py', 'allow', '''
            def allow(self, now, cost=1):
                if cost <= 0:
                    raise ValueError('cost must be positive')
                elapsed = max(0.0, now - self.last_ts)
                self.last_ts = now
                margin = max(1.0, 0.05 * self.capacity)
                self.tokens = min(self.capacity + margin, self.tokens + elapsed * self.rate_per_sec)
                if self.tokens + margin >= cost:
                    self.tokens = max(0.0, self.tokens - cost)
                    return True
                return False
        ''', 'TokenBucket'),
    ],
}


def mutate(repo, case):
    """Run targeted AST-level fault probes against the agent's test suite."""
    if case not in MUTATION_PROBES:
        return {'status': 'not_applicable'}
    probes = []
    for label, filename, func_name, replacement_src, class_name in MUTATION_PROBES[case]:
        with tempfile.TemporaryDirectory(prefix='pc-mutant-') as d:
            target = Path(d)
            shutil.copytree(repo, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            p = target / filename
            if not p.is_file():
                probes.append({'mutation': label, 'status': 'missing_target'})
                continue
            mutated = replace_function(p.read_text(encoding='utf-8'), func_name, replacement_src, class_name)
            if not mutated:
                probes.append({'mutation': label, 'status': 'transform_failed'})
                continue
            p.write_text(mutated, encoding='utf-8')
            result = own_tests(target)
            tested = bool(result['test_count'] and result['test_count'] > 0)
            status = (
                'killed'
                if tested and result['exit_code'] not in (0, None)
                else 'survived'
                if tested
                else 'no_tests'
            )
            probes.append({'mutation': label, 'status': status, 'exit_code': result['exit_code'], 'test_count': result['test_count']})
    if not probes:
        return {'status': 'not_applicable'}
    if any(p['status'] == 'no_tests' for p in probes):
        overall = 'no_tests'
    elif any(p['status'] in ('missing_target', 'transform_failed') for p in probes):
        overall = 'transform_failed'
    elif all(p['status'] == 'killed' for p in probes):
        overall = 'killed'
    else:
        overall = 'survived'
    return {
        'mutation': ','.join(p['mutation'] for p in probes),
        'status': overall,
        'killed_count': sum(1 for p in probes if p['status'] == 'killed'),
        'total_probes': len(probes),
        'probes': probes,
    }


def compute_numstat(repo, baseline_commit, untracked):
    tracked = git(repo, 'diff', '--numstat', baseline_commit, '--')
    lines = [line for line in tracked.splitlines() if line.strip()]
    for f in untracked:
        p = repo / f
        if not p.is_file() or p.is_symlink():
            continue
        try:
            count = len(p.read_text(encoding='utf-8').splitlines())
            lines.append(f'{count}\t0\t{f}')
        except UnicodeError:
            lines.append(f'-\t-\t{f}')
    return ('\n'.join(lines) + '\n') if lines else ''


def score(args):
    dest = Path(args.run).resolve()
    meta = json.loads((dest / 'run.json').read_text(encoding='utf-8'))
    repo = dest / 'repo'
    case = meta['case']
    baseline_commit = meta['baseline_commit']
    installed_rel = meta.get('installed_skill_relpath')
    ignore_rels = (installed_rel, installed_rel.split('/')[0]) if installed_rel else ()

    env_code = 'import sys; sys.path.insert(0, ".")\n' + ORACLES[case]
    oracle = command([sys.executable, '-c', env_code], repo)
    tests = own_tests(repo)
    current = hashes(repo, ignore_rels)
    changed = sorted(
        k for k in set(current) | set(meta['baseline_files'])
        if current.get(k) != meta['baseline_files'].get(k)
    )
    diff = git(repo, 'diff', baseline_commit, '--')
    raw_untracked = git(repo, 'ls-files', '--others', '--exclude-standard').splitlines()
    ignored_prefixes = {Path(p) for p in ignore_rels if p}
    untracked = [
        f for f in raw_untracked
        if f
        and not any(part in IGNORED_DIRS for part in Path(f).parts)
        and not any(Path(f) == ig or ig in Path(f).parents for ig in ignored_prefixes)
    ]
    for f in untracked:
        p = repo / f
        diff += '\nUntracked: ' + f + '\n'
        if not p.is_file() or p.is_symlink():
            diff += '[non-regular file]\n'
        elif p.stat().st_size < 100000:
            try:
                diff += p.read_text(encoding='utf-8') + '\n'
            except UnicodeError:
                diff += '[binary]\n'
        else:
            diff += '[file over 100 KB; inspect separately]\n'
    (dest / 'diff.txt').write_text(diff, encoding='utf-8')
    numstat = compute_numstat(repo, baseline_commit, untracked)
    no_change_gate = (len(changed) == 0) if case in NO_CHANGE_CASES else None
    oracle_pass = oracle['exit_code'] == 0
    task_pass = oracle_pass and (no_change_gate is not False)
    mutation = (
        mutate(repo, case)
        if tests['status'] == 'passed'
        else {'status': 'no_tests' if tests['status'] == 'none' else 'tests_not_green'}
    )
    result = {
        'case': case,
        'split': meta.get('split', CASE_META.get(case, {}).get('split')),
        'category': meta.get('category', CASE_META.get(case, {}).get('category')),
        'arm': meta['arm'],
        'skill_version': meta.get('skill_version'),
        'task_pass': task_pass,
        'behavior_oracle': oracle,
        'own_tests': tests,
        'changed_files': changed,
        'git_numstat': numstat,
        'untracked_files': untracked,
        'no_change_gate': no_change_gate,
        'mutation': mutation,
        'notes': 'Subjective dimensions require rubric review; test pass alone is not full correctness.',
    }
    save(dest / 'checks.json', result)
    print(json.dumps({
        'case': case,
        'arm': meta['arm'],
        'skill_version': meta.get('skill_version'),
        'task_pass': task_pass,
        'oracle_pass': oracle_pass,
        'own_tests_status': tests['status'],
        'changed_files': changed,
        'mutation': mutation['status'],
        'no_change_gate': no_change_gate,
    }))


def parse_frontmatter(text):
    norm = text.replace('\r\n', '\n')
    if not norm.startswith('---\n'):
        raise ValueError('SKILL.md must start with YAML frontmatter (---)')
    end = norm.find('\n---\n', 4)
    if end == -1:
        raise ValueError('SKILL.md frontmatter closing --- not found')
    header = norm[4:end]
    body = norm[end + 5 :]
    fields = {}
    for line in header.splitlines():
        if not line.strip() or line.strip().startswith('#'):
            continue
        if ':' not in line:
            raise ValueError(f'Invalid frontmatter line: {line!r}')
        k, v = line.split(':', 1)
        fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, body


def file_metrics(path, is_skill_md=False):
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    metrics = {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'bytes': len(raw),
        'words_whitespace': len(text.split()),
        'lines': len(text.splitlines()),
    }
    if is_skill_md:
        _, body = parse_frontmatter(text)
        metrics['words_markdown_body'] = len(body.split())
    return metrics


def validate(args):
    errors = []
    skill_dir = ROOT / 'pragmatic-craftsman'
    skill_md = skill_dir / 'SKILL.md'
    openai_yaml = skill_dir / 'agents' / 'openai.yaml'
    manifest_path = ROOT / 'MANIFEST.json'
    triggers_path = ROOT / 'evals' / 'triggers.json'

    if not skill_md.is_file():
        errors.append('Missing pragmatic-craftsman/SKILL.md')
    else:
        text = skill_md.read_text(encoding='utf-8')
        try:
            fm, body = parse_frontmatter(text)
            name = fm.get('name', '')
            desc = fm.get('description', '')
            lic = fm.get('license', '')
            if name != 'pragmatic-craftsman' or not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
                errors.append(f'Invalid frontmatter name: {name!r}')
            if not (1 <= len(desc) <= 1024):
                errors.append(f'Invalid description length: {len(desc)}')
            if lic != 'MIT':
                errors.append(f'Expected frontmatter license: MIT, got {lic!r}')
            body_words = len(body.split())
            if body_words > 450:
                errors.append(f'Expected compact SKILL.md body (<= 450 words), got {body_words}')
        except Exception as exc:
            errors.append(str(exc))

    if not openai_yaml.is_file():
        errors.append('Missing pragmatic-craftsman/agents/openai.yaml')
    else:
        ytext = openai_yaml.read_text(encoding='utf-8')
        for required_key in ('display_name:', 'short_description:', 'default_prompt:', 'allow_implicit_invocation:'):
            if required_key not in ytext:
                errors.append(f'Missing {required_key} in agents/openai.yaml')

    actual_package_files = set(hashes(skill_dir).keys())
    if actual_package_files != {'SKILL.md', 'agents/openai.yaml'}:
        errors.append(f'Unexpected files in pragmatic-craftsman/: {sorted(actual_package_files)}')

    if not manifest_path.is_file():
        errors.append('Missing MANIFEST.json')
    else:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        expected_skill = file_metrics(skill_md, is_skill_md=True) if skill_md.is_file() else {}
        expected_yaml = file_metrics(openai_yaml, is_skill_md=False) if openai_yaml.is_file() else {}
        recorded_skill = manifest.get('skill_files', {}).get('SKILL.md', {})
        recorded_yaml = manifest.get('skill_files', {}).get('agents/openai.yaml', {})
        for k, v in expected_skill.items():
            if recorded_skill.get(k) != v:
                errors.append(f'MANIFEST.json SKILL.md {k} mismatch: recorded={recorded_skill.get(k)} actual={v}')
        for k, v in expected_yaml.items():
            if recorded_yaml.get(k) != v:
                errors.append(f'MANIFEST.json agents/openai.yaml {k} mismatch: recorded={recorded_yaml.get(k)} actual={v}')
        for ver, snap_rel in manifest.get('archived_snapshots', {}).items():
            if not (ROOT / snap_rel).is_file():
                errors.append(f'Missing archived snapshot for {ver}: {snap_rel}')

    if not triggers_path.is_file():
        errors.append('Missing evals/triggers.json')
    else:
        trig = json.loads(triggers_path.read_text(encoding='utf-8'))
        explicit = trig.get('explicit', [])
        implicit = trig.get('implicit_candidates', [])
        pos = [x for x in implicit if x.get('activate') is True]
        neg = [x for x in implicit if x.get('activate') is False]
        if len(explicit) < 4 or len(pos) < 12 or len(neg) < 12:
            errors.append(f'triggers.json coverage too small: explicit={len(explicit)}, pos={len(pos)}, neg={len(neg)}')

    if set(CASES) != set(ORACLES) or set(CASES) != set(CASE_META):
        errors.append('Mismatch between CASES, ORACLES, and CASE_META keys')

    out = {'valid': len(errors) == 0, 'errors': errors}
    print(json.dumps(out))
    if errors:
        sys.exit(1)
    return out


def selftest(args):
    # Only genuine no-action baselines should pass the behavior oracle without edits.
    should_pass = set(NO_CHANGE_CASES)
    baseline_passing_test_cases = {'regression', 'legacy', 'api', 'oss', 'partial-fix'}
    results = []
    baseline_mutation_survived = {}
    with tempfile.TemporaryDirectory(prefix='pc-harness-') as d:
        for case in CASES:
            dest = Path(d) / case
            prepare(argparse.Namespace(dest=str(dest), arm='off', skill=None, case=case, native_host=None, invocation=None))
            code = 'import sys; sys.path.insert(0,".")\n' + ORACLES[case]
            r = command([sys.executable, '-c', code], dest / 'repo')
            ok = (r['exit_code'] == 0) == (case in should_pass)
            if case in baseline_passing_test_cases:
                m = mutate(dest / 'repo', case)
                baseline_mutation_survived[case] = (m['status'] == 'survived')
            results.append({
                'case': case,
                'split': CASE_META[case]['split'],
                'category': CASE_META[case]['category'],
                'oracle_exit': r['exit_code'],
                'expectation_met': ok,
            })

        # Verify harness repairs: native-host git exclusion, committed-change diffing, untracked numstat, and multi-arm.
        probe_dir = Path(d) / '_harness_probe'
        prepare(argparse.Namespace(
            dest=str(probe_dir), arm='v0.3', skill=None, case='trivial',
            native_host='gemini', invocation='explicit',
        ))
        probe_repo = probe_dir / 'repo'
        (probe_repo / 'retry.py').write_text('def should_retry(attempt, max_attempts):\n    return attempt < max_attempts\n', encoding='utf-8')
        git(probe_repo, 'add', 'retry.py')
        git(probe_repo, '-c', 'user.name=Agent', '-c', 'user.email=agent@example.invalid', 'commit', '-qm', 'Agent commit')
        (probe_repo / 'notes_extra.txt').write_text('line1\nline2\n', encoding='utf-8')
        (probe_repo / '.pytest_cache').mkdir()
        (probe_repo / '.pytest_cache' / 'README.md').write_text('cache\n', encoding='utf-8')
        score(argparse.Namespace(run=str(probe_dir)))
        scored = json.loads((probe_dir / 'checks.json').read_text(encoding='utf-8'))
        diff_txt = (probe_dir / 'diff.txt').read_text(encoding='utf-8')
        harness_checks = {
            'committed_diff_captured': 'attempt < max_attempts' in diff_txt,
            'untracked_numstat_captured': '2\t0\tnotes_extra.txt' in scored['git_numstat'],
            'native_skill_excluded_from_changes': all(not f.startswith('.gemini') for f in scored['changed_files']),
            'tool_cache_excluded_from_changes': all(not f.startswith('.pytest_cache') for f in scored['changed_files']),
            'mutant_killed_on_fixed_trivial': scored['mutation']['status'] == 'killed',
            'baseline_tests_do_not_kill_mutants': all(baseline_mutation_survived.values()),
        }
        for arm_ver in ('v0.1', 'v0.2'):
            arm_dir = Path(d) / f'_arm_{arm_ver}'
            prepare(argparse.Namespace(dest=str(arm_dir), arm=arm_ver, skill=None, case='no-op', native_host='opencode', invocation='implicit'))
            arm_meta = json.loads((arm_dir / 'run.json').read_text(encoding='utf-8'))
            harness_checks[f'archived_{arm_ver}_materialized'] = bool(arm_meta['skill_files'])

    all_ok = all(r['expectation_met'] for r in results) and all(harness_checks.values())
    save(Path(__file__).parent / 'harness-selftest.json', {'cases': results, 'harness_checks': harness_checks})
    print(json.dumps({'selftest_pass': all_ok, 'harness_checks': harness_checks, 'cases': results}))
    if not all_ok:
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)
    l_parser = sub.add_parser('list')
    l_parser.add_argument('--split', choices=['all', 'dev', 'holdout'], default='all')
    q = sub.add_parser('prepare')
    q.add_argument('--case', choices=CASES, required=True)
    q.add_argument('--arm', choices=['on', 'off', 'v0.3', 'v0.2', 'v0.1'], required=True)
    q.add_argument('--dest', required=True)
    q.add_argument('--skill')
    q.add_argument('--native-host', choices=['codex', 'claude', 'opencode', 'gemini'])
    q.add_argument('--invocation', choices=['explicit', 'implicit', 'file'])
    s = sub.add_parser('score')
    s.add_argument('--run', required=True)
    sub.add_parser('validate')
    sub.add_parser('selftest')
    a = p.parse_args()
    if a.cmd == 'list':
        for name in CASES:
            if a.split == 'all' or CASE_META[name]['split'] == a.split:
                print(f"{name}\t{CASE_META[name]['split']}\t{CASE_META[name]['category']}")
    elif a.cmd == 'prepare':
        prepare(a)
    elif a.cmd == 'score':
        score(a)
    elif a.cmd == 'validate':
        validate(a)
    else:
        selftest(a)


if __name__ == '__main__':
    main()
