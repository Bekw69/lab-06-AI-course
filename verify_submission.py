"""Check evidence consistency; this cannot certify legal accuracy or fairness."""
import ast
import hashlib
import json
from pathlib import Path

import nbformat
from lab06_core import ControlEntry, Harness, RECORD_KEYS, check_register, parse_decision
from lab06_data import Profile, Pair, check_pair_invariants, divergence_table, render_profile

ROOT=Path(__file__).resolve().parent
PENCILS={'lab06-11':'PREDICTION_0','lab06-15':'PREDICTION_1','lab06-20':'OBSERVATION_1',
         'lab06-22':'BLIND_WHY','lab06-32':'PREDICTION_3','lab06-35':'OBSERVATION_3',
         'lab06-37':'PREDICTION_4','lab06-40':'OBSERVATION_4'}


def main():
    n=nbformat.read(ROOT/'lab06_harness_says_no.ipynb',as_version=4)
    nbformat.validate(n)
    cells={c.id:c for c in n.cells}
    for cid,fn in [('lab06-01','lab06_data.py'),('lab06-02','lab06_core.py')]:
        assert cells[cid].source.strip()==(ROOT/fn).read_text(encoding='utf-8').strip(),fn
    for c in n.cells:
        if c.cell_type=='code':
            ast.parse(c.source)
            assert c.execution_count is not None, f'Unexecuted {c.id}'
            assert not any(o.output_type=='error' for o in c.outputs),f'Error output {c.id}'
    for cid,name in PENCILS.items():
        assignments=[node for node in ast.parse(cells[cid].source).body if isinstance(node,ast.Assign)]
        found=next(node for node in assignments if any(isinstance(t,ast.Name) and t.id==name for t in node.targets))
        assert isinstance(ast.literal_eval(found.value),str) and ast.literal_eval(found.value).strip(),name
    for name in ('REPORT.md','JUSTIFICATION.md'):
        text=(ROOT/name).read_text(encoding='utf-8')
        assert '<!-- STUDENT: replace -->' not in text and len(text.split())>200,name
    assert '## AI-use declaration' in (ROOT/'JUSTIFICATION.md').read_text(encoding='utf-8')
    evidence=json.loads((ROOT/'results/measurements.json').read_text(encoding='utf-8'))
    env=evidence['environment']
    assert env['model_id']=='Qwen/Qwen2.5-3B-Instruct' and env['greedy'] and env['model_revision']
    assert env['device']=='cuda' and env['dtype']=='torch.float16'
    pairs=[Pair(**{**p,'a':Profile(**p['a']),'b':Profile(**p['b']),'differs':tuple(p['differs'])}) for p in evidence['pairs']]
    assert len(pairs)==200 and evidence['n_pairs']==40
    for p in pairs:check_pair_invariants(p)
    for key in ('BASE','AFTER'):
        run=evidence['runs'][key]
        assert len(run['verdicts_a'])==len(run['verdicts_b'])==200,key
        assert run['calls']==400,key
        a=[(v['outcome'],v['score']) for v in run['verdicts_a']]
        b=[(v['outcome'],v['score']) for v in run['verdicts_b']]
        expected=evidence['BASE_TABLE' if key=='BASE' else 'AFTER_TABLE']
        actual=divergence_table(pairs,a,b)
        assert json.loads(json.dumps(actual))==expected,key
    rows=[json.loads(s) for s in (ROOT/'decisions.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    assert len(rows)==406,len(rows)
    assert len({r['record_id'] for r in rows})==406
    for row in rows:assert set(row)==set(RECORD_KEYS)
    after=evidence['runs']['AFTER']
    for i,p in enumerate(pairs):
        for offset,profile,side in [(0,p.a,'a'),(1,p.b,'b')]:
            row=rows[2*i+offset];v=after['verdicts_'+side][i]
            assert row['record_id']==v['record_id'] and row['pid']==profile.pid
            assert row['outcome']==v['outcome'] and row['score']==v['score']
            assert row['input_sha256']==hashlib.sha256(render_profile(profile,hide=row['harness']['blind']).encode('utf-8')).hexdigest()
            assert {'name','university'}<=set(row['fields_withheld'])
            assert 'name' not in row['fields_shown'] and 'university' not in row['fields_shown']
            parsed=parse_decision(row['raw_output'])
            assert parsed.parse_ok or row['reason_code']=='unparseable'
            if parsed.parse_ok:assert parsed.score==row['score'] and parsed.decision==row['decision']
    for row in rows[-5:]:assert row['outcome']=='refuse' and row['raw_output'].startswith('[no model call]')
    assert {r['reason_code'] for r in rows[-5:]}=={'purpose_not_allowed','minor','no_consent','invalid_input','instruction_in_profile'}
    register=json.loads((ROOT/'control_register.json').read_text(encoding='utf-8'))
    h=Harness(**rows[0]['harness'])
    assert not register['format_problems']
    assert not check_register([ControlEntry(**e) for e in register['entries']],h)
    queue=[json.loads(s) for s in (ROOT/'review_queue.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    assert {r['record_id'] for r in queue}=={r['record_id'] for r in rows if r['escalated_to_human']}
    print('Verified: original toolbox cells, all code executions, eight answers, 200 pair invariants,')
    print('baseline/after statistics, 406 real log records, five refusal reasons, register and review queue.')
    print('Legal meaning, actual eligibility, production privacy and completed human review are not certified.')


if __name__=='__main__':main()
