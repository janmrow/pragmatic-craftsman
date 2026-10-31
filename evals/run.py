#!/usr/bin/env python3
"""Prepare isolated fixture repos; inspect artifacts with independent checks. No model API required."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

from fixtures import CASES
from oracles import ORACLES

DIMENSIONS = ['correctness','scope_discipline','simplicity','completeness',
              'verification_quality','test_value','semantic_quality','reviewability',
              'maintainability','efficiency']


def command(args, cwd, timeout=20):
    start=time.monotonic()
    try:
        r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=timeout)
        return {'command':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,
                'seconds':round(time.monotonic()-start,3)}
    except subprocess.TimeoutExpired as e:
        def dec(v): return v.decode(errors='replace') if isinstance(v,bytes) else v or ''
        return {'command':args,'exit_code':None,'timeout':True,'stdout':dec(e.stdout),
                'stderr':dec(e.stderr),'seconds':round(time.monotonic()-start,3)}


def git(repo,*args):
    r=command(['git',*args],repo)
    if r['exit_code']!=0: raise RuntimeError(r)
    return r['stdout']


def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts
            and '__pycache__' not in p.parts}


def save(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')


def prepare(args):
    dest=Path(args.dest).resolve()
    if dest.exists() and any(dest.iterdir()): raise ValueError('Destination must be empty or new')
    if args.arm=='on' and not args.skill: raise ValueError('--skill is required for on')
    repo=dest/'repo'; repo.mkdir(parents=True)
    for name,content in CASES[args.case]['files'].items():
        p=repo/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content)
    (repo/'.gitignore').write_text('__pycache__/\n*.pyc\n')
    git(repo,'init','-q')
    git(repo,'add','.')
    git(repo,'-c','user.name=Local Eval','-c','user.email=eval@example.invalid','commit','-qm','Fixture baseline')
    prompt=CASES[args.case]['prompt']
    skill_hashes={}
    if args.arm=='on':
        skill=Path(args.skill).resolve()
        if not (skill/'SKILL.md').is_file():raise ValueError('Missing SKILL.md')
        skill_hashes=hashes(skill)
        native_host=getattr(args,'native_host',None)
        if native_host:
            locations={'codex':'.agents/skills','claude':'.claude/skills','opencode':'.opencode/skills'}
            installed=repo/locations[native_host]/'pragmatic-craftsman'
            shutil.copytree(skill,installed)
            git(repo,'add','.')
            git(repo,'-c','user.name=Local Eval','-c','user.email=eval@example.invalid',
                'commit','-qm','Install skill fixture')
            prefix='Use $pragmatic-craftsman.' if native_host=='codex' else 'Use the pragmatic-craftsman skill.'
            prompt=prefix+'\n\n'+prompt
        else:
            prompt=f'Use $pragmatic-craftsman. Read the skill at {skill}/SKILL.md.\n\n'+prompt
    prompt+='\n\nWork only in this repository, except reading the named skill if supplied. Do not inspect sibling runs or evaluator files. Complete the task and report the decisive evidence.'
    (dest/'prompt.txt').write_text(prompt+'\n')
    meta={'case':args.case,'arm':args.arm,'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
          'repo':str(repo),'baseline_commit':git(repo,'rev-parse','HEAD').strip(),
          'baseline_files':hashes(repo),'skill_files':skill_hashes,
          'invocation':(getattr(args,'native_host',None) or 'file') if args.arm=='on' else 'off',
          'runtime':{'python':sys.version.split()[0],'agent':'record manually','model':'record manually',
                     'effort':'record manually','instruction_isolation':'record manually'}}
    save(dest/'run.json',meta)
    save(dest/'rubric.json',{d:{'score':None,'evidence':''} for d in DIMENSIONS})
    print(json.dumps({'run':str(dest),'repo':str(repo),'prompt':str(dest/'prompt.txt')}))


def own_tests(repo):
    r=command([sys.executable,'-m','unittest','discover','-v'],repo)
    count=re.search(r'Ran (\d+) tests?',r['stderr'])
    r['test_count']=int(count.group(1)) if count else None
    r['status']='none' if r['test_count']==0 else 'passed' if r['exit_code']==0 else 'failed'
    return r


def mutate(repo,case):
    """Targeted wrong versions; a kill is useful evidence, not a full mutation score."""
    files={
      'trivial':('retry.py','boundary'),
      'regression':('invoice.py','quoted-csv'),
      'tests':('shipping.py','threshold'),
      'unsafe-small':('service.py','cross-tenant-read'),
    }
    if case not in files:return {'status':'not_implemented'}
    with tempfile.TemporaryDirectory(prefix='pc-mutant-') as d:
        target=Path(d)
        shutil.copytree(repo,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','__pycache__'))
        name,label=files[case]; p=target/name
        if case in ('trivial','regression'):
            p.write_text(CASES[case]['files'][name])
        elif case=='tests':
            p.write_text(p.read_text().replace('<= 1000','< 1000'))
        else:
            text=p.read_text(); tree=ast.parse(text)
            fn=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=='get_document')
            lines=text.splitlines(keepends=True)
            lines[fn.lineno-1:fn.end_lineno]=['def get_document(store, tenant_id, document_id):\n    return store.get(document_id)\n']
            p.write_text(''.join(lines))
        result=own_tests(target)
        count=re.search(r'Ran (\d+) tests?',result['stderr'])
        tested=bool(count and int(count.group(1))>0)
        return {'mutation':label,'status':'killed' if tested and result['exit_code'] not in (0,None) else 'survived' if tested else 'no_tests',
                'result':result}


def score(args):
    dest=Path(args.run).resolve(); meta=json.loads((dest/'run.json').read_text())
    repo=dest/'repo'; case=meta['case']
    # -c keeps evaluator source out of the repository and leaves normal imports visible.
    env_code='import sys; sys.path.insert(0, ".")\n'+ORACLES[case]
    oracle=command([sys.executable,'-c',env_code],repo)
    tests=own_tests(repo)
    current=hashes(repo)
    changed=sorted(k for k in set(current)|set(meta['baseline_files']) if current.get(k)!=meta['baseline_files'].get(k))
    diff=git(repo,'diff','HEAD','--')
    untracked=git(repo,'ls-files','--others','--exclude-standard').splitlines()
    for f in untracked:
        p=repo/f
        diff+='\nUntracked: '+f+'\n'
        if p.stat().st_size<100000:
            try:diff+=p.read_text()+'\n'
            except UnicodeError:diff+='[binary]\n'
        else:diff+='[file over 100 KB; inspect separately]\n'
    (dest/'diff.txt').write_text(diff)
    result={'case':case,'arm':meta['arm'],'behavior_oracle':oracle,'own_tests':tests,
            'changed_files':changed,'git_numstat':git(repo,'diff','--numstat','HEAD'),
            'untracked_files':untracked,
            'no_change_gate':len(changed)==0 if case=='no-op' else None,
            'mutation':mutate(repo,case) if tests['status']=='passed' else {'status':'no_tests' if tests['status']=='none' else 'tests_not_green'},
            'notes':'Subjective dimensions require rubric review; test pass alone is not full correctness.'}
    save(dest/'checks.json',result)
    print(json.dumps({'case':case,'arm':meta['arm'],'oracle_pass':oracle['exit_code']==0,
                      'own_tests_status':tests['status'],'changed_files':changed,
                      'mutation':result['mutation']['status'],'no_change_gate':result['no_change_gate']}))


def selftest(args):
    # Known broken baselines must fail; already-working/no-code-change baselines must pass.
    should_pass={'legacy','tests','no-op'}
    results=[]
    with tempfile.TemporaryDirectory(prefix='pc-harness-') as d:
        for case in CASES:
            dest=Path(d)/case
            prepare(argparse.Namespace(dest=str(dest),arm='off',skill=None,case=case))
            code='import sys; sys.path.insert(0,".")\n'+ORACLES[case]
            r=command([sys.executable,'-c',code],dest/'repo')
            ok=(r['exit_code']==0)==(case in should_pass)
            results.append({'case':case,'oracle_exit':r['exit_code'],'expectation_met':ok})
    save(Path(__file__).parent/'harness-selftest.json',results)
    print(json.dumps({'selftest_pass':all(r['expectation_met'] for r in results),'cases':results}))
    if not all(r['expectation_met'] for r in results):sys.exit(1)


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('list')
    q=sub.add_parser('prepare');q.add_argument('--case',choices=CASES,required=True);q.add_argument('--arm',choices=['on','off'],required=True);q.add_argument('--dest',required=True);q.add_argument('--skill');q.add_argument('--native-host',choices=['codex','claude','opencode'])
    q=sub.add_parser('score');q.add_argument('--run',required=True)
    sub.add_parser('selftest')
    a=p.parse_args()
    if a.cmd=='list': print('\n'.join(CASES))
    elif a.cmd=='prepare':prepare(a)
    elif a.cmd=='score':score(a)
    else:selftest(a)

if __name__=='__main__':main()
