# Prompt 04 · 给题目写中文讲解、标知识点（可选）

如果你的题库只有英文原解析，可以让 AI 给每道题加一段中文讲解 (`z`)、一条易错提醒 (`t`)，并标上知识点 (`k`)。标了知识点，"同类新题"、"考前一页纸"和题目下面的知识卡才会生效。

每次给 AI 30 到 50 道题，格式：`[{"id","sj","s","o","a","e"}, ...]`（直接从 bank.json 的 q 里截取）。`{TAXONOMY}` 用 `python3 tools/cards_pipeline.py taxonomy <科目id> --taxonomy my/taxonomy.json` 的输出。

把 AI 返回的结果合并回 bank.json：
```bash
python3 - <<'EOF'
import json,glob
b=json.load(open('my/bank.json')); Q={q['id']:q for q in b['q']}
for f in glob.glob('my/explain/out_*.json'):
    for i,x in json.load(open(f)).items():
        if i in Q:
            Q[i].update({k:v for k,v in x.items() if k in ('z','t','k')})
            if x.get('flag'): Q[i]['f']=x['flag']   # shows as 答案存疑 in the app
json.dump(b,open('my/bank.json','w'),ensure_ascii=False)
EOF
```

`{EXAM}` 换成你的考试名，比如"CFA Level I"、"408 计算机考研"、"AWS Solutions Architect Associate"。

---

You are a {EXAM} tutor writing Chinese explanations for practice questions.

TAXONOMY for tagging (keys "M.T"):
{TAXONOMY}

For each question in the INPUT: "s" is the stem (HTML), "o" the options, "a" the 0-based index of the official answer, "e" the original explanation.

Return one JSON object mapping question id -> {
  "z": "Simplified Chinese explanation, 1-4 sentences, show the key calculation, keep English technical terms",
  "t": "one short exam trap, or empty string",
  "k": [M, T]   // the single best taxonomy key, as two integers
}
Follow the official answer. If you believe the official answer is wrong, still explain it, and add "flag": "one line why" to that item.
No em dash. Output the JSON only.

INPUT:
{PASTE QUESTIONS HERE}
