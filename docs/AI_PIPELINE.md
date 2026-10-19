# 用你自己的 AI 做知识卡

这是做这个网站时实际跑过的流程：讲义 → 知识卡 → 用真题核对 → 导入。用 Claude、ChatGPT、Gemini 都可以，只要能读 PDF 或图片、能输出 JSON。

```
讲义 PDF ──(01)──> 每个科目一个 cards_*.json ──merge──> cards.json
                                                  │
                         (02 可选) 补齐讲义没讲的知识点
                                                  │
题库 bank.json ──batches──> 每张卡配 4 道真题 ──(03)──> 改动 ──apply──> cards.json
                                                  │
                                         网站「导入题库」第 2 步
```

建议在仓库里建一个 `my/` 文件夹放你的私人文件。`.gitignore` 已经排除了它，**不会被误传到 GitHub**。

## 第 0 步 · 准备

- 题库：用 CSV 或 bank.json 导入网站，同时留一份 `my/bank.json`（网站「导出题库」也能导出）。
- 讲义：每个科目一个 PDF。AI 读 PDF 效果不好的话，转成图片：
  ```bash
  bash tools/pdf_to_images.sh my/slides/固收讲义.pdf my/pages/fi
  ```
- 知识点目录：CFA 直接用 `sample/taxonomy.json`。别的考试先用 `prompts/00_taxonomy_from_syllabus.md` 让 AI 从考纲或讲义目录生成 `my/taxonomy.json`，在网站「导入题库」第 3 步导入。

## 第 1 步 · 讲义 → 知识卡（prompts/01）

```bash
python3 tools/cards_pipeline.py taxonomy fi --taxonomy my/taxonomy.json   # 打印某科的知识点编号，贴进 prompt（CFA 示例可省略 --taxonomy）
```
把 `prompts/01_cards_from_slides.md` 的 prompt 和讲义一起交给 AI，结果存成 `my/cards_fi.json`。每个科目做一次，然后合并：
```bash
python3 tools/cards_pipeline.py merge my/cards.json my/cards_*.json
```

## 第 2 步 · 补齐（可选，prompts/02）

讲义一般覆盖 80% 到 90% 的知识点。缺的那些用 `prompts/02_fill_gaps.md` 让 AI 补，会带 `bu: 1` 标记，网站上显示"AI 补充"。

## 第 3 步 · 用真题核对（prompts/03），最重要的一步

AI 第一遍写的卡，大约每 10 张就有 1 张有实质错误：符号写反、IFRS 和 US GAAP 搞混、道德准则编号张冠李戴。让 AI 凭记忆再查一遍只能查出一部分，因为它是在用同一套记忆检查自己。

更好的办法是**拿你自己的题库当标准答案**：
```bash
python3 tools/cards_pipeline.py batches --bank my/bank.json --cards my/cards.json --out my/verify
```
每张卡会配上同一知识点的 4 道题和官方答案。把每个 `in_N.json` 连同 `prompts/03_verify_with_questions.md` 交给 AI，输出存成 `out_N.json`，然后：
```bash
python3 tools/cards_pipeline.py apply --cards my/cards.json my/verify/out_*.json
```

**一定要人工看一遍 `my/cards_changelog.txt`。** 核对员也会出错。我们实际跑的时候，有两个核对员都把 IV(A) 独立执业的"书面同意"要求改错了，最后是对照 Standards of Practice Handbook 改回来的。拿不准的条目，翻原文。

顺带的好处：核对员会报告**题库里官方答案本身有问题的题**，比如答案和解析自相矛盾。把这些题记下来，做错的时候先别急着怪自己。

## 第 4 步 · 检查和导入

```bash
node tools/check_latex.mjs my/cards.json          # 公式能不能渲染（先 npm install katex@0.16.11）
python3 tools/validate_bank.py my/bank.json --cards my/cards.json
```
然后在网站「导入题库」第 2 步选 `my/cards.json`。

## 给题目加中文讲解和知识点（可选，prompts/04）

题目标上知识点 `k` 之后，做题时下面会出现对应的知识卡，"同类新题"和"考前一页纸"也能用上。题库本来没有知识点的话，用 `prompts/04_explain_questions_zh.md` 批量标。

## 用 Claude Code 这类工具批量跑

如果你会用能开多个 agent 的工具（Claude Code 之类），第 1 步可以每个科目一个 agent，第 3 步每个批次一个 agent，并行跑，几个小时就能跑完 600 多张卡。注意让每个 agent 只往自己的文件夹里写文件，不然它们的临时脚本会互相覆盖。

## 成本参考

633 个知识点、一整套 10 科讲义：第 1 步加第 3 步大约是几百万 token。用订阅版的聊天窗口分几天做也可以，不一定要用 API。
