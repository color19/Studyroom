#!/usr/bin/env python3
"""Convert a questions CSV into bank.json (same rules as the in-app CSV import).

  python3 tools/csv2bank.py my_questions.csv -o my/bank.json [--taxonomy sample/taxonomy.json]

Columns (header row, any order, case-insensitive; Chinese aliases in brackets):
  required: subject(科目) question(题干) A B answer(答案)
  optional: source(来源) set(章节) no(题号) C D E explanation(解析) explanation_zh(中文解析) tip(易错点) kp(知识点, e.g. 85.5) mock
subject = any name (e.g. 数据结构, Networking). The 10 CFA subject ids/names are recognised; other names become new subjects.
answer  = letter A-E or 1-based number. A source whose name contains "mock" is treated as full mock exams.
"""
import argparse, csv, html, json, os, re, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = {'subject': ['subject', '科目'], 'source': ['source', '来源'], 'set': ['set', 'chapter', 'reading', '章节', '分组'], 'no': ['no', 'number', '题号'],
        'question': ['question', 'stem', '题干', '题目'], 'A': ['a', '选项a'], 'B': ['b', '选项b'], 'C': ['c', '选项c'], 'D': ['d', '选项d'], 'E': ['e', '选项e'],
        'answer': ['answer', '答案'], 'explanation': ['explanation', '解析'], 'explanation_zh': ['explanation_zh', '中文解析'], 'tip': ['tip', '易错点'], 'kp': ['kp', '知识点'], 'mock': ['mock']}

def para(t): return ''.join(f'<p>{html.escape(x)}</p>' for x in t.splitlines())

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('csv'); ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--taxonomy', help='your taxonomy.json (default: CFA taxonomy only if all subjects are CFA subjects)'); ap.add_argument('--exam', help='exam.json with name/weights/session/secPer/note'); ap.add_argument('--subjects', default=os.path.join(H, 'sample/subjects.json'))
    a = ap.parse_args()
    subjects = json.load(open(a.subjects, encoding='utf-8'))
    rows = list(csv.reader(open(a.csv, encoding='utf-8-sig', newline='')))
    head = [h.strip().lower() for h in rows[0]]
    idx = {k: next((i for i, h in enumerate(head) if h in v), -1) for k, v in COLS.items()}
    for k in ['subject', 'question', 'A', 'B', 'answer']:
        if idx[k] < 0: sys.exit(f'missing required column: {k}')
    def find_sj(v):
        v = v.strip().lower()
        for s in subjects:
            if v in (s['id'], s['zh'].lower(), s['en'].lower()): return s['id']
    sources, src_ids, readings, qs, errs, created = [], {}, {}, [], [], []
    for n, r in enumerate(rows[1:], 2):
        if not any(x.strip() for x in r): continue
        g = lambda k: r[idx[k]].strip() if 0 <= idx[k] < len(r) else ''
        sj = find_sj(g('subject'))
        if not sj and g('subject'):
            sj = f'sj{len(subjects)+1}'; subjects.append({'id': sj, 'zh': g('subject'), 'en': g('subject'), 'no': len(subjects)+1}); created.append(sj)
        if not sj: errs.append(f'line {n}: empty subject'); continue
        sname = g('source') or '我的题库'
        if sname not in src_ids:
            sid = f'u{len(sources)+1}'; src_ids[sname] = sid
            sources.append({'id': sid, 'name': sname, 'short': sname if len(sname) <= 16 else sname[:15] + '…', 'mock': bool(re.search('mock|模考', sname, re.I)) or g('mock') == '1'})
        sid = src_ids[sname]; st = g('set') or next(s['zh'] for s in subjects if s['id'] == sj)
        rid = f'{sid}::{st}::{sj}'
        readings.setdefault(rid, {'id': rid, 'title': st, 'subject': sj, 'src': sid, 'count': 0})
        opts = [g(x) for x in 'ABCDE' if g(x)]
        ans = g('answer').upper()
        ai = ord(ans) - 65 if re.fullmatch('[A-E]', ans) else (int(ans) - 1 if ans.isdigit() else -1)
        if not 0 <= ai < len(opts): errs.append(f'line {n}: answer "{g("answer")}" does not match an option'); continue
        readings[rid]['count'] += 1
        q = {'id': f'U{n-1}', 'r': rid, 'sj': sj, 'n': int(g('no')) if g('no').isdigit() else readings[rid]['count'], 's': para(g('question')), 'o': opts, 'a': ai}
        if g('explanation'): q['e'] = para(g('explanation'))
        if g('explanation_zh'): q['z'] = g('explanation_zh')
        if g('tip'): q['t'] = g('tip')
        m = re.fullmatch(r'(\d+)\.(\d+)', g('kp'))
        if m: q['k'] = [int(m[1]), int(m[2])]
        qs.append(q)
    if errs: sys.exit('\n'.join(errs[:20]) + (f'\n... {len(errs)} problems' if len(errs) > 20 else ''))
    used = {q['sj'] for q in qs}
    bank = {'format': 'studyroom/bank@1', 'subjects': [s for s in subjects if s['id'] in used], 'sources': sources, 'readings': list(readings.values()), 'q': qs, 'kp': [], 'gl': [], 'jc': {}}
    if a.exam: bank['exam'] = json.load(open(a.exam, encoding='utf-8'))
    if a.taxonomy and os.path.exists(a.taxonomy): bank['kp'] = json.load(open(a.taxonomy, encoding='utf-8'))
    elif not created:  # all subjects are the built-in CFA ones: attach the CFA taxonomy + glossary
        bank['kp'] = json.load(open(os.path.join(H, 'sample/taxonomy.json'), encoding='utf-8'))
        bank['gl'] = json.load(open(os.path.join(H, 'sample/glossary.json'), encoding='utf-8'))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(bank, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{len(qs)} questions, {len(readings)} sets, {len(sources)} sources -> {a.out}')

if __name__ == '__main__': main()
