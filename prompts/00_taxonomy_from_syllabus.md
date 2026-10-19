# Prompt 00 · 考纲 / 讲义目录 → 知识点目录（别的考试先做这一步）

知识点目录 (`taxonomy.json`) 是知识卡、"同类新题"、"考前一页纸"的骨架：每张卡挂在一个知识点上，每道题也标到一个知识点。
示例自带的是 CFA 一级的目录。考别的（408、软考、AWS、教资、法考……）先用这个 prompt 生成自己的目录。

把考试大纲，或者讲义的目录页，连同下面的 prompt 交给 AI。结果存成 `my/taxonomy.json`，在网站「导入题库」第 3 步导入。

科目 id 要和你题库 CSV 里的 `subject` 对得上：CSV 里写"数据结构"，导入后网站会自动给它一个 id。最省事的做法是先导入题库，再到「导入题库」页面导出 bank.json，看看每个科目的 id，填进下面的 `{SUBJECTS}`。

---

You are building a knowledge-point taxonomy for exam preparation.

EXAM: {EXAM NAME, e.g. 全国硕士研究生招生考试 计算机学科专业基础 (408)}
SUBJECTS (id: name): {SUBJECTS, e.g. sj1: 数据结构, sj2: 计算机组成原理, sj3: 操作系统, sj4: 计算机网络}

From the attached syllabus or table of contents, produce a JSON array of chapters. Each chapter:
{"t": "chapter title (original language)", "zh": "中文章节名", "sj": "<subject id>", "g": [["中文知识点名", "English name"], ...]}

Rules:
- Follow the order of the syllabus. One chapter per syllabus chapter or learning module.
- 4 to 8 knowledge points per chapter. Each point should be small enough that one review card (3 sentences + a few bullets) can cover it, and big enough that several exam questions could test it.
- Knowledge point names: short (2 to 10 Chinese characters), concrete, no numbering.
- Only include what the syllabus actually covers.
- No em dash.

Output the JSON array only.
