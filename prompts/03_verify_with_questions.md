# Prompt 03 · 用你自己的题库核对知识卡

AI 写的卡片一定会有错。最有效的核对方法不是再让 AI 凭记忆检查一遍，而是**拿真题对答案**：每张卡配上同一知识点的 3 到 4 道题和官方答案，卡片和官方答案矛盾就是错。

先生成批次文件（每批约 46 张卡）：
```bash
python3 tools/cards_pipeline.py batches --bank my/bank.json --cards my/cards.json --out my/verify
```
然后对每个 `my/verify/in_N.json`，把文件内容和下面的 prompt 一起交给 AI，把 AI 的输出存成 `my/verify/out_N.json`。最后：
```bash
python3 tools/cards_pipeline.py apply --cards my/cards.json my/verify/out_*.json
```
会生成备份 `cards.json.bak` 和改动清单 `cards_changelog.txt`。**改动清单一定要自己看一遍**：AI 核对员也会改错，特别是条文、法规类的细节，拿不准的去翻原始资料。

如果你用 Claude Code 这类能跑多个 agent 的工具，可以让每个 agent 处理一个批次，并行跑。

`{EXAM}` 换成你的考试名，比如"CFA Level I"、"408 计算机考研"、"AWS Solutions Architect Associate"。

---

You are a strict {EXAM} fact-checker reviewing review cards ("知识卡") for a Chinese-speaking candidate. A wrong card costs points, so be rigorous. A pointless rewrite of a correct card is also bad, so change only what is actually wrong.

INPUT (JSON below) maps key -> {
  "_kp": knowledge point name,
  "core", "formulas_latex", "pts", "trap": the card,
  "_questions": up to 4 real exam-style questions on this same knowledge point, each with the official correct "answer" and explanation "why"
}

For EVERY card:
1. Cross-check the card against its _questions. If the card's formula, conclusion, direction, definition or trap contradicts the official answer or explanation, the card is wrong: fix it. If a question looks like it belongs to a different topic, or its official answer contradicts its own explanation, ignore that question and mention it.
2. Independently check against the {EXAM} syllabus: wrong facts, formulas, signs or directions, confused definitions or rule numbers, misleading oversimplifications, garbled text.
3. Check every formulas_latex string: the math must be correct and agree with core and pts.
4. No em dash character anywhere.

OUTPUT: ONLY the cards you changed, as one JSON object:
{ "key": { "core": "...(include only fields you changed, with the full new value)", "formulas_latex": [...], "pts": [...], "trap": [...], "_why": "one line: what was wrong", "_conf": "high|medium" } }
Keep the style: Simplified Chinese with English technical terms, short strings. Output {} if nothing needs changing.
After the JSON, list questions whose official answer looks wrong (key + one line).

INPUT:
{PASTE in_N.json HERE}
