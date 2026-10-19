#!/usr/bin/env python3
"""Check a bank.json (and optionally a cards.json) before importing.

  python3 tools/validate_bank.py my/bank.json [--cards my/cards.json]
"""
import argparse, json, re, sys

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('bank'); ap.add_argument('--cards'); a = ap.parse_args()
    b = json.load(open(a.bank, encoding='utf-8')); errs, warns = [], []
    subj = {s['id'] for s in b.get('subjects', [])} or {'quant', 'econ', 'corp', 'fsa', 'equity', 'fi', 'deriv', 'alt', 'pm', 'ethics'}
    reads = {r['id']: r for r in b.get('readings', [])}; kp = b.get('kp', []); ids = set()
    for i, q in enumerate(b.get('q', [])):
        at = f"q[{i}] {q.get('id', '')}"
        if q.get('id') in ids: errs.append(at + ': duplicate id')
        ids.add(q.get('id'))
        if q.get('sj') not in subj: errs.append(at + f": unknown subject {q.get('sj')}")
        if not str(q.get('s', '')).strip(): errs.append(at + ': empty stem s')
        o = q.get('o')
        if not isinstance(o, list) or len(o) < 2: errs.append(at + ': needs >= 2 options in o')
        elif not (isinstance(q.get('a'), int) and 0 <= q['a'] < len(o)): errs.append(at + ': answer a must be a 0-based option index')
        if q.get('r') and q['r'] not in reads: warns.append(at + f": reading {q['r']} not listed (it will be created)")
        k = q.get('k')
        if k and not (isinstance(k, list) and len(k) == 2 and k[0] < len(kp) and k[1] < len(kp[k[0]]['g'])): warns.append(at + f': kp {k} not in taxonomy')
    if not b.get('q'): errs.append('no questions in q')
    cards = json.load(open(a.cards, encoding='utf-8')) if a.cards else b.get('jc', {})
    for key, c in cards.items():
        if not re.fullmatch(r'\d+\.\d+', key): errs.append(f'card {key}: key must look like "12.3"'); continue
        m, t = map(int, key.split('.'))
        if not (m < len(kp) and t < len(kp[m]['g'])): warns.append(f'card {key}: not in taxonomy, will not show')
        txt = json.dumps(c, ensure_ascii=False)
        if '\u2014' in txt: warns.append(f'card {key}: contains an em dash')
    print(f"questions {len(b.get('q', []))}, readings {len(reads)}, taxonomy chapters {len(kp)}, cards {len(cards)}")
    for w in warns[:30]: print('WARN', w)
    if len(warns) > 30: print(f'... {len(warns)} warnings')
    for e in errs[:30]: print('ERROR', e)
    sys.exit(1 if errs else 0)

if __name__ == '__main__': main()
