# Prompt 02 · 补全讲义没覆盖的知识点（可选）

讲义通常不会覆盖目录里的每个知识点。这一步让 AI 只给缺的那些写卡，并标记成"AI 补充"（网站里会显示这个标签，提醒你这张卡不是来自讲义）。

找出缺的 key：
```bash
python3 - <<'EOF'
import json
kp=json.load(open('my/taxonomy.json'))  # CFA 示例用 sample/taxonomy.json
have=json.load(open('my/cards.json'))
miss=[f'{m}.{t} {ch["zh"]} / {g[0]}' for m,ch in enumerate(kp) for t,g in enumerate(ch['g']) if f'{m}.{t}' not in have]
print(len(miss)); print('\n'.join(miss))
EOF
```
把列表填进 `{MISSING}`。

`{EXAM}` 换成你的考试名，比如"CFA Level I"、"408 计算机考研"、"AWS Solutions Architect Associate"。

---

You are a {EXAM} expert writing review cards for a Chinese-speaking candidate. Write ONE card for each knowledge point below. These points were not covered by the lecture slides, so rely only on what you are certain is in the {EXAM} syllabus. If you are not sure about a detail, leave it out.

KNOWLEDGE POINTS (key, chapter / point):
{MISSING}

Use exactly this format for each card, and add "bu": 1 to every card:
{"core": "...", "ftex": [...], "pts": [...], "trap": [...], "bu": 1}
Same style rules: Simplified Chinese with English technical terms, short strings, KaTeX LaTeX for formulas with Chinese only inside \text{}, no em dash.

Output a single JSON object mapping key -> card, and nothing else.
