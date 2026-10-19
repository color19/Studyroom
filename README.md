# 刷题室 · for CFA® Level I candidates

一个单文件的刷题网站：导入你自己的题库和讲义，用你自己的 AI 生成知识卡，在浏览器里刷题、复习、模考。

不用装任何东西，不用后端，数据只存在你自己的浏览器里。

> 这个项目**只是工具，不含任何题目和讲义**。自带的 20 道示例题是原创的演示题。题库和讲义请用你自己合法购买的材料，**只能自用，不要传播**。

## 能做什么

- **章节练习**：按来源、科目、章节选题，10 / 20 / 全部，随机或顺序。
- **模拟考试**：整套 Mock 原卷计时，或者按 2026 年考纲各科权重随机组卷。交卷后出成绩单和逐题解析。
- **错题本 + 间隔复习**：做错自动进错题本，按 1 / 2 / 4 / 7 / 15 天复习。设了考试日期，会把复习节奏压缩到考前两天全部完成。
- **错因标签**：概念不会、计算错、审题错、粗心，按错因筛选错题。
- **同类新题**：错题旁边推同一知识点、还没做过的新题。
- **知识卡**：每个知识点一张卡，含 LaTeX 公式、要点和易错点。做题时自动显示在解析下面，可以直接在网页上改。
- **考前一页纸**：自动挑出你最弱的知识点和对应的卡，可以打印。
- **暂停 / 断点续做**、做题记录、学习报告、按章节分组的笔记、重点术语高亮。

## 三分钟开始

1. 下载这个仓库（绿色 Code 按钮 → Download ZIP），双击打开 `index.html`。
   或者直接打开 GitHub Pages 地址：`https://color19.github.io/shuati-room/`
2. 先用示例题点一点，看看功能。
3. 点左边「导入题库」，导入你的题目 CSV。模板在页面里可以下载，格式见 [docs/FORMAT.md](docs/FORMAT.md)。
4. 想要知识卡：按 [docs/AI_PIPELINE.md](docs/AI_PIPELINE.md) 用你的 AI 把讲义做成 `cards.json`，再导入。

换电脑：「导入题库」页面底部可以导出题库和学习记录，到新电脑再导入。

## 用你自己的 AI 做知识卡

`prompts/` 里是实际用过的提示词，配合 `tools/` 里的脚本：

| 步骤 | 提示词 | 做什么 |
|---|---|---|
| 1 | `01_cards_from_slides.md` | 讲义 → 每个知识点一张卡 |
| 2 | `02_fill_gaps.md` | 讲义没覆盖的知识点让 AI 补（标记为"AI 补充"） |
| 3 | `03_verify_with_questions.md` | **用你自己的题库核对卡片**：每张卡配 4 道真题，和官方答案矛盾就改 |
| 4 | `04_explain_questions_zh.md` | 给题目写中文讲解、标知识点 |

第 3 步是关键。AI 第一遍写的卡大约每 10 张有 1 张有实质错误，拿真题对答案比让 AI 自己再查一遍有效得多。改动清单一定要自己看一遍。

## 仓库结构

```
index.html          打开就能用（构建产物，已提交）
src/app.html        网站源码
build.py            构建 index.html；--bank 可以把你的题库打包进一个私人文件
sample/             示例题库（原创）、CFA 一级 2026 知识点目录、术语表
prompts/            AI 提示词
tools/              CSV 转换、校验、知识卡流水线、LaTeX 检查
docs/               数据格式、AI 流程说明
vendor/             KaTeX 0.16.11（MIT）
```

改了 `src/app.html` 之后运行 `python3 build.py` 重新生成 `index.html`。

想要一个打包好题库、发到手机上也能用的私人文件：
```bash
python3 build.py --bank my/bank.json     # 生成 dist/personal.html，已被 .gitignore 排除
```

## 版权和合规

- 题库（Kaplan Schweser、CFA Institute 等）和培训机构的讲义都受版权保护。这个仓库不包含、也不接受任何这类内容的 PR。
- 请把你的私人文件放在 `my/` 或 `dist/` 里，这两个文件夹已经被 `.gitignore` 排除。
- 截图分享时注意遮住题目原文。
- CFA® 和 Chartered Financial Analyst® 是 CFA Institute 的注册商标。本项目与 CFA Institute 没有任何关联，也未经其认可。

## 关于这个项目

作者是金融专业的学生，不会写代码，这个网站是在备考 CFA 一级的过程中和 Claude 一起聊出来的。开源出来，是希望别的考生也能用自己的材料搭一个顺手的刷题室。

欢迎提 issue 和 PR（功能、bug、别的证书的知识点目录都可以，但请不要提交任何受版权保护的题目或讲义）。

## License

代码：[MIT](LICENSE)。KaTeX：MIT，见 `vendor/KATEX_LICENSE`。

---

## English

**Shuati Room** is a single-file practice app for CFA® Level I candidates. Import your own question bank (CSV or JSON) and your own lecture notes, generate knowledge cards with your own AI using the prompts in `prompts/`, then practice, review with spaced repetition, and sit timed mocks in the browser. No server, no install: everything stays in your browser's local storage.

This repo ships **no third-party questions or lecture material**. The 20 sample questions are original. Use materials you have legally obtained, for personal study only.

Quick start: open `index.html`, try the sample, then go to 「导入题库」(Import) and load your CSV. See `docs/FORMAT.md` for the data format and `docs/AI_PIPELINE.md` for the card pipeline.

CFA® and Chartered Financial Analyst® are registered trademarks owned by CFA Institute. This project is not affiliated with or endorsed by CFA Institute.
