#!/usr/bin/env python3
"""Build the single-file app.

  python3 build.py                      -> index.html (sample bank only, safe to publish)
  python3 build.py --bank my/bank.json  -> dist/personal.html (your bank inlined; PRIVATE, git-ignored)

index.html works offline: open it in a browser, or serve the folder (GitHub Pages works).
"""
import argparse, json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(H, p), encoding='utf-8').read()

ap = argparse.ArgumentParser()
ap.add_argument('--bank', help='inline this bank.json (output goes to dist/personal.html, never commit it)')
a = ap.parse_args()

page = rd('src/app.html')
marker = '<script>\n(function(){'
assert page.count(marker) == 1, 'app.html boot marker not found'
css = rd('vendor/katex.inline.css')
js = rd('vendor/katex.min.js').replace('</script', '<\\/script')
sample = rd('sample/bank.sample.json').replace('</', '<\\/')
inject = (f'<style>{css}</style>\n<script>{js}</script>\n'
          f'<script id="sample" type="application/json">{sample}</script>\n')
if a.bank:
    bank = json.load(open(a.bank, encoding='utf-8'))
    inject += '<script id="bank" type="application/json">' + json.dumps(bank, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
page = page.replace(marker, inject + marker)
doc = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
       '<style>:root{color-scheme:light dark}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
       '</head><body>' + page + '</body></html>')
out = os.path.join(H, 'dist/personal.html') if a.bank else os.path.join(H, 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(doc)
print(f'wrote {os.path.relpath(out, H)} ({os.path.getsize(out)/1e6:.2f} MB)')
