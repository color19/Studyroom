# Prompt 01 · 讲义 → 知识卡

把下面整段复制给你的 AI（Claude、ChatGPT、Gemini 都行），同时上传一个科目的讲义 PDF，或者用 `tools/pdf_to_images.sh` 转成的页面图片。
`{TAXONOMY}` 换成 `python3 tools/cards_pipeline.py taxonomy <科目id> --taxonomy my/taxonomy.json` 的输出（CFA 示例可以省略 --taxonomy，科目 id 比如 fi）。

一次只给一个科目。讲义超过 60 页的话分几次给，最后用 `cards_pipeline.py merge` 合并。

`{EXAM}` 换成你的考试名，比如"CFA Level I"、"408 计算机考研"、"AWS Solutions Architect Associate"。

---

You are helping a Chinese-speaking candidate preparing for {EXAM} build compact review cards ("知识卡") from lecture slides they bought. You will read the slides and write cards keyed to a fixed knowledge-point taxonomy.

TAXONOMY (keys look like "M.T", e.g. "35.0"):
{TAXONOMY}

TASK
1. Read EVERY page of the attached slides, in order. Do not skip any.
2. For each page, decide which taxonomy key it belongs to. Skip title, agenda, table-of-contents and advertising pages, and pages that fit no key.
3. For every key the slides cover, write ONE card summarizing what the slides teach about it, IN YOUR OWN WORDS. Do not copy slide sentences verbatim; condense.

CARD FORMAT
{
  "core": "1-3 short sentences, Simplified Chinese, keeping key English technical terms in English. Max ~120 Chinese characters.",
  "ftex": ["key formulas as KaTeX LaTeX, e.g. \\beta_i = \\frac{\\text{Cov}(R_i,R_m)}{\\sigma_m^2}. Chinese words only inside \\text{}"],
  "pts": ["2-5 must-know points or comparisons"],
  "trap": ["0-3 classic exam traps (易错点)"],
  "srcs": [{"src": "<lecture file name>", "pg": [page numbers used]}]
}
- "ftex" may be [] for non-quantitative topics. Keep every string under ~80 characters.
- Be accurate. If a formula on a slide is hard to read, write the standard formula you are certain of; never invent.
- Never use the em dash character.
- Rules, laws or ethics standards: "core" states what the rule requires; "pts" list required and prohibited actions; "trap" lists classic traps.

OUTPUT
A single JSON object mapping key -> card, and nothing else. Example:
{"35.0": {"core": "...", "ftex": ["..."], "pts": ["..."], "trap": ["..."], "srcs": [{"src": "固收讲义.pdf", "pg": [12, 13]}]}}
