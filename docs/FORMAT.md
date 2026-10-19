# 数据格式

网站只认三种文件。都是 UTF-8。

| 文件 | 内容 | 怎么导入 |
|---|---|---|
| 题目 CSV 或 `bank.json` | 题目、选项、答案、解析 | 网站「导入题库」第 1 步，或 `tools/csv2bank.py` |
| `cards.json` | 知识卡 | 「导入题库」第 2 步 |
| `taxonomy.json` | 知识点目录 | 「导入题库」第 3 步（默认已内置 CFA 一级 2026） |

## 1. 题目 CSV（最简单）

第一行是表头，列的顺序随意，大小写不限，中文列名也认。

| 列 | 必需 | 说明 |
|---|---|---|
| `subject` / 科目 | ✓ | `quant` `econ` `corp` `fsa` `equity` `fi` `deriv` `alt` `pm` `ethics`，或中文名（数量分析、固定收益……） |
| `question` / 题干 | ✓ | 题干，可以换行（用引号包起来） |
| `A` `B` | ✓ | 选项，`C` `D` `E` 可选 |
| `answer` / 答案 | ✓ | `A` / `B` / `C`，或者 `1` / `2` / `3` |
| `source` / 来源 | | 题库名，比如"我的笔记题"。名字里带 `mock` 的来源会被当成整套模拟卷 |
| `set` / 章节 | | 章节或分组名，比如 "Rates and Returns" |
| `no` / 题号 | | 数字 |
| `explanation` / 解析 | | 原解析 |
| `explanation_zh` / 中文解析 | | 中文讲解 |
| `tip` / 易错点 | | 一句话 |
| `kp` / 知识点 | | 知识点编号，比如 `85.5`。见下面第 3 节 |

模板可以在网站「导入题库」里下载。Excel 另存为「CSV UTF-8」就行。

## 2. bank.json（完整格式）

```jsonc
{
  "format": "shuati-room/bank@1",
  "title": "我的题库",                       // 可选
  "subjects": [{"id": "quant", "zh": "数量分析", "en": "Quantitative Methods", "no": 1}, ...],   // 可选，默认 CFA 一级 10 科
  "sources":  [{"id": "s1", "name": "我的题库", "short": "我的", "mock": false}],               // 可选，没有会自动生成
  "readings": [{"id": "s1-r1", "title": "Rates and Returns", "subject": "quant", "src": "s1", "num": "1"}],
  "q": [{
    "id": "s1-1",          // 唯一
    "r": "s1-r1",          // 属于哪个 reading
    "sj": "quant",         // 科目 id
    "n": 1,                // 题号
    "s": "<p>题干，HTML</p>",
    "o": ["选项 A", "选项 B", "选项 C"],
    "a": 1,                // 正确答案的序号，从 0 开始
    "e": "<p>原解析，HTML，可选</p>",
    "z": "中文讲解，可选",
    "t": "易错提醒，可选",
    "f": "答案存疑说明，可选",
    "k": [85, 5]           // 知识点 [章节序号, 知识点序号]，可选
  }],
  "kp": [ ...taxonomy... ],     // 可选，导入时没有就沿用当前的
  "gl": [ ...glossary... ],     // 可选，重点词高亮用
  "jc": { ...cards... }         // 可选，知识卡
}
```

题干和解析里可以放 `<img src="data:image/png;base64,...">` 图片。

## 3. taxonomy.json（知识点目录）

一个数组，每个元素是一个章节（对应一个 Learning Module），`g` 是这个章节下的知识点：

```json
[
  {"t": "Rates and Returns", "zh": "利率与收益率", "sj": "quant",
   "g": [["持有期收益率", "Holding period return"], ["连续复利收益", "Continuous compounding"]]}
]
```

知识点的编号就是 `章节序号.知识点序号`，从 0 开始。上面的"连续复利收益"是 `0.1`。
仓库自带的 `sample/taxonomy.json` 是 CFA 一级 2026 的 102 个章节、633 个知识点，`python3 tools/cards_pipeline.py taxonomy quant` 可以按科目打印出来。

## 4. cards.json（知识卡）

键是知识点编号，值是一张卡：

```json
{
  "85.5": {
    "core": "一到三句话讲清楚这个知识点",
    "ftex": ["\\text{EAR} = \\left(1 + \\frac{r}{m}\\right)^{m} - 1"],
    "pts": ["要点 1", "要点 2"],
    "trap": ["易错点"],
    "srcs": [{"src": "数量讲义.pdf", "pg": [12, 13]}],
    "bu": 1
  }
}
```

- `ftex`：KaTeX 能渲染的 LaTeX。中文要放在 `\text{}` 里。可以用 `node tools/check_latex.mjs cards.json` 检查。
- `srcs`：讲义出处，网站上会显示"讲义 · 第几页"。
- `bu: 1`：这张卡是 AI 补充的，不是来自讲义，网站会标出来。
- 网站内部格式 `{"c","f","p","t","s","b"}` 也能直接导入。

你在网站上手动编辑过的卡会单独保存，重新导入不会覆盖你的修改。
