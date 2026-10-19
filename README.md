# 刷题室 · Study Room

一个单文件的刷题网站，**任何选择题考试都能用**：CFA、408 计算机考研、软考、AWS 认证、教资、法考……
你带来自己的题库和讲义，用自己的 AI 把讲义做成知识卡，然后在浏览器里刷题、复习、模考。

不用装任何东西，不用后端，数据只存在你自己的浏览器里。

> 这个项目**只是工具，不含任何真题和讲义**。自带的 20 道 CFA 示例题是原创的演示题。题库和讲义请用你自己合法拥有的材料，**只能自用，不要传播**。

## 能做什么

- **首页持仓报告**：把各科当成一个投资组合，考纲权重是目标仓位，做过的题是实际仓位，哪科低配一眼就看到。
- **章节练习**：按来源、科目、章节选题，10 / 20 / 全部，随机或顺序。
- **模拟考试**：整套模考原卷计时，或者按各科权重随机组卷。交卷后出成绩单和逐题解析。
- **错题本 + 间隔复习**：做错自动进错题本，按 1 / 2 / 4 / 7 / 15 天复习。设了考试日期，会把复习节奏压缩到考前两天全部完成。
- **错因标签**：概念不会、计算错、审题错、粗心，按错因筛选错题。
- **同类新题**：错题旁边推同一知识点、还没做过的新题。
- **知识卡**：每个知识点一张卡，含 LaTeX 公式、要点和易错点。做题时自动显示在解析下面，可以直接在网页上改。
- **考前一页纸**：自动挑出你最弱的知识点和对应的卡，可以打印。
- **暂停 / 断点续做**、做题记录、学习报告、按章节分组的笔记、重点术语高亮。

## 三分钟开始

1. 下载这个仓库（绿色 Code 按钮 → Download ZIP），双击打开 `index.html`。
   或者直接打开 GitHub Pages 地址：`https://color19.github.io/studyroom/`
2. 先用示例题点一点，看看功能。
3. 点左边「导入题库」，导入你的题目 CSV。科目随便写（"数据结构"、"Networking" 都行），模板在页面里能下载，格式见 [docs/FORMAT.md](docs/FORMAT.md)。
4. 想要知识卡：按 [docs/AI_PIPELINE.md](docs/AI_PIPELINE.md) 用你的 AI 把讲义做成 `cards.json`，再导入。

换电脑：「导入题库」页面底部可以导出题库和学习记录，到新电脑再导入。

## 题库和讲义要什么格式

### 题库：Excel 表格就行（另存为「CSV UTF-8」）

一行一道题，第一行是表头：

| 科目 | 来源 | 章节 | 题干 | A | B | C | D | 答案 | 中文解析 |
|---|---|---|---|---|---|---|---|---|---|
| 数据结构 | 408真题 | 线性表 | 顺序表随机访问的时间复杂度是 | O(1) | O(n) | O(log n) | O(n²) | A | 按下标直接定位 |

- 必填只有 **科目、题干、A、B、答案**，其他列可以空着。
- 科目名随便写，选项最多 5 个，答案填字母。
- 来源名里带"模考"或"mock"的，会被当成整套模拟卷。
- 网站「导入题库」页面能下载现成的模板。完整字段见 [docs/FORMAT.md](docs/FORMAT.md)。

**题库是 PDF 或 Word？** 把文件丢给 Claude 或 ChatGPT，附上这句话：

> 把这份题目整理成 CSV，列为：科目,来源,章节,题干,A,B,C,D,答案,中文解析。答案只写字母。题干里有逗号或换行的用英文双引号包起来。逐题提取，不要省略，不要改题目内容。

题目多就分几次给，每次几十页，最后把几个 CSV 拼起来。

### 讲义：PDF 就行

- 一个科目一个 PDF 最好。PPT 或 Word 先导出成 PDF。
- 能选中文字的 PDF 效果最好；扫描版也能用，只是 AI 读得慢一点。
- 讲义不用导入网站，它只是喂给 AI 生成知识卡，生成的 `cards.json` 才导进网站。
- 没有讲义也行：只导题库，刷题、错题本、复习、模考照样都能用。

> 题库和讲义只能自己用，别发到群里或网上。网站的数据只存在你自己的浏览器里，不会上传到任何地方。

## 换成你自己的考试

| 你要准备的 | 怎么来 |
|---|---|
| 题库 | 整理成 CSV：科目、题干、选项、答案、解析。Excel 就能做 |
| 知识点目录 | `prompts/00`：把考纲或讲义目录给 AI，生成 `taxonomy.json` |
| 知识卡 | `prompts/01`：把讲义给 AI，每个知识点生成一张卡 |
| 核对 | `prompts/03`：每张卡配 4 道你自己题库里的题，和官方答案对不上就改 |
| 考试设置（可选） | 在 bank.json 里加 `exam`：考试名、各科权重、每场题数、每题秒数，见 FORMAT.md |

只导入题库也能用：刷题、错题本、复习、模考都不依赖知识卡。知识卡和知识点目录是加分项。

## 用你自己的 AI 做知识卡

`prompts/` 里是实际用过的提示词，配合 `tools/` 里的脚本：

| 步骤 | 提示词 | 做什么 |
|---|---|---|
| 0 | `00_taxonomy_from_syllabus.md` | 考纲 → 知识点目录（CFA 已内置，可跳过） |
| 1 | `01_cards_from_slides.md` | 讲义 → 每个知识点一张卡 |
| 2 | `02_fill_gaps.md` | 讲义没覆盖的知识点让 AI 补（标记为"AI 补充"） |
| 3 | `03_verify_with_questions.md` | **用你自己的题库核对卡片**：每张卡配 4 道真题，和官方答案矛盾就改 |
| 4 | `04_explain_questions_zh.md` | 给题目写中文讲解、标知识点 |

第 3 步是关键。在 CFA 上实测，AI 第一版写的 633 张卡里有 105 张有实质错误；第二轮拿真题官方答案逐张对，又揪出 55 张。拿真题对答案，比让 AI 凭记忆再查一遍有效得多。改动清单一定要自己看一遍。

## 仓库结构

```
index.html          打开就能用（构建产物，已提交）
src/app.html        网站源码
build.py            构建 index.html；--bank 可以把你的题库打包进一个私人文件
sample/             示例题库（原创）、CFA 一级知识点目录、术语表
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

- 商业题库、官方真题、培训机构讲义一般都受版权保护。这个仓库不包含、也不接受任何这类内容的 PR。
- 请把你的私人文件放在 `my/` 或 `dist/` 里，这两个文件夹已经被 `.gitignore` 排除。
- 截图分享时注意遮住题目原文。
- CFA® 和 Chartered Financial Analyst® 是 CFA Institute 的注册商标。本项目与 CFA Institute 以及任何考试机构都没有关联，也未经其认可。

## 关于这个项目

作者是金融专业的学生，这个网站是在备考 CFA 一级的过程中和 Claude 一起 vibecoding 出来的。朋友问能不能用在别的领域刷题，于是把它改成了通用版开源出来。

欢迎提 issue 和 PR：功能、bug都可以。

## License

代码：[MIT](LICENSE)。KaTeX：MIT，见 `vendor/KATEX_LICENSE`。

---

## English

**Study Room** (刷题室, "practice room") is a single-file practice app for **any multiple-choice exam**. Import your own question bank (CSV or JSON), build a knowledge-point taxonomy and review cards from your own lecture notes with your own AI using the prompts in `prompts/`, then practice, review with spaced repetition, and sit timed mocks in the browser. No server, no install: everything stays in your browser.

This repo ships **no third-party questions or course material**. The 20 sample questions (CFA Level I flavoured) are original. Use materials you have legally obtained, for personal study only.

Quick start: open `index.html`, try the sample, then go to 「导入题库」(Import) and load your CSV. Subjects can be any names. See `docs/FORMAT.md` for the data format and `docs/AI_PIPELINE.md` for the card pipeline.

CFA® and Chartered Financial Analyst® are registered trademarks owned by CFA Institute. This project is not affiliated with or endorsed by CFA Institute or any exam body.
