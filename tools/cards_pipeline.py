#!/usr/bin/env python3
"""Helpers for the AI knowledge-card pipeline (see docs/AI_PIPELINE.md).

  taxonomy  SUBJECT                 print the taxonomy keys for one subject (paste into prompt 01)
  merge     OUT.json IN1.json ...   merge card files from several AI runs into one cards.json
  batches   --bank B --cards C --out DIR [--size 46]
                                    split cards into verification batches, each card paired with
                                    up to 4 real questions from your own bank (input for prompt 03)
  apply     --cards C DIR/out_*.json
                                    apply verification fixes back into cards.json, write changelog
  attach    --bank B --cards C -o OUT
                                    put cards into a bank.json (same as importing cards in the app)
"""
import argparse, glob, json, os, random, re, shutil, sys, collections
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda p: json.load(open(p, encoding='utf-8'))
def save(p, o): os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True); json.dump(o, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
strip = lambda h: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h or '')).strip()

def cmd_taxonomy(a):
    kp = load(a.taxonomy)
    for m, ch in enumerate(kp):
        if ch.get('sj') == a.subject:
            print(f"# {m} {ch.get('zh', '')} / {ch['t']}")
            for t, g in enumerate(ch['g']): print(f'  {m}.{t}  {g[0]} ({g[1]})')

def cmd_merge(a):
    out = {}
    for f in a.inputs:
        for k, c in load(f).items():
            if k not in out: out[k] = c; continue
            o = out[k]
            if len(c.get('core', '')) > len(o.get('core', '')): o['core'] = c['core']
            for fld in ('f', 'ftex', 'pts', 'trap'):
                for x in c.get(fld, []) or []:
                    if x not in o.setdefault(fld, []): o[fld].append(x)
            o['srcs'] = (o.get('srcs') or []) + (c.get('srcs') or [])
    save(a.out, out); print(f'{len(out)} cards -> {a.out}')

def cmd_batches(a):
    random.seed(5); b = load(a.bank); cards = load(a.cards); kp = b.get('kp', [])
    byk = collections.defaultdict(list)
    for q in b['q']:
        if q.get('k'): byk[f"{q['k'][0]}.{q['k'][1]}"].append(q)
    items = {}
    for k, c in cards.items():
        m, t = map(int, k.split('.'))
        qs = sorted(byk.get(k, []), key=lambda q: -len(q.get('z') or q.get('e') or ''))[:12]; random.shuffle(qs)
        ex = [{'q': strip(q['s'])[:420], 'answer': strip(q['o'][q['a']])[:160], 'why': (q.get('z') or strip(q.get('e', '')))[:320]} for q in qs[:4]]
        name = f"{kp[m].get('zh', '')} / {kp[m]['g'][t][0]}" if m < len(kp) and t < len(kp[m]['g']) else k
        items[k] = {'_kp': name, 'core': c.get('core', ''), 'formulas_latex': c.get('ftex') or c.get('f') or [], 'pts': c.get('pts', []), 'trap': c.get('trap', []), '_questions': ex}
    keys = list(items); n = max(1, -(-len(keys) // a.size))
    for i in range(n): save(os.path.join(a.out, f'in_{i}.json'), {k: items[k] for k in keys[i*a.size:(i+1)*a.size]})
    print(f'{len(keys)} cards in {n} batches -> {a.out}/in_*.json')

def cmd_apply(a):
    cards = load(a.cards); bak = a.cards + '.bak'
    if not os.path.exists(bak): shutil.copy(a.cards, bak)
    log = []
    for f in a.outputs:
        for k, ch in load(f).items():
            if k not in cards: log.append(f'?? {k} not in cards'); continue
            c = cards[k]; changed = False
            for src, dst in (('core', 'core'), ('pts', 'pts'), ('trap', 'trap'), ('formulas_latex', 'ftex')):
                if src in ch and ch[src] != c.get(dst): c[dst] = ch[src]; changed = True
            if changed: log.append(f"{k} [{ch.get('_conf', '')}] {ch.get('_why', '')}")
    save(a.cards, cards); open(os.path.splitext(a.cards)[0] + '_changelog.txt', 'w', encoding='utf-8').write('\n'.join(log))
    print(f'{sum(1 for l in log if not l.startswith("??"))} cards changed (backup: {bak})'); print('\n'.join(log))

def cmd_attach(a):
    b = load(a.bank); jc = b.setdefault('jc', {})
    for k, c in load(a.cards).items():
        o = {'c': c.get('core', c.get('c', '')), 'f': c.get('ftex') or c.get('f', []), 'p': c.get('pts', c.get('p', [])), 't': c.get('trap', c.get('t', []))}
        if c.get('bu') or c.get('b'): o['b'] = 1
        elif c.get('srcs'): o['s'] = [[s.get('src', ''), ', '.join(map(str, s.get('pg', [])))] for s in c['srcs']]
        jc[k] = o
    save(a.out, b); print(f'{len(jc)} cards in bank -> {a.out}')

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest='cmd', required=True)
p = sp.add_parser('taxonomy'); p.add_argument('subject'); p.add_argument('--taxonomy', default=os.path.join(H, 'sample/taxonomy.json')); p.set_defaults(fn=cmd_taxonomy)
p = sp.add_parser('merge'); p.add_argument('out'); p.add_argument('inputs', nargs='+'); p.set_defaults(fn=cmd_merge)
p = sp.add_parser('batches'); p.add_argument('--bank', required=True); p.add_argument('--cards', required=True); p.add_argument('--out', required=True); p.add_argument('--size', type=int, default=46); p.set_defaults(fn=cmd_batches)
p = sp.add_parser('apply'); p.add_argument('--cards', required=True); p.add_argument('outputs', nargs='+'); p.set_defaults(fn=cmd_apply)
p = sp.add_parser('attach'); p.add_argument('--bank', required=True); p.add_argument('--cards', required=True); p.add_argument('-o', '--out', required=True); p.set_defaults(fn=cmd_attach)
a = ap.parse_args(); a.fn(a)
