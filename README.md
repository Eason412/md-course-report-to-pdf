# Markdown 课程报告转 PDF

<p align="center">
  <img src="assets/njust_logo.png" alt="南京理工大学校徽" width="96">
</p>

> 如果你在使用中遇到格式问题、构建失败、学校模板适配需求，或有更好的排版、QA、工作流建议，欢迎提交 GitHub Issue，也可以发邮件到 `huyi@njust.edu.cn`。邮件标题建议注明来意，例如 `md-course-report-to-pdf 使用反馈`、`课程报告 PDF 格式建议` 或 `Codex skill 改进建议`。
>
> 本项目为个人维护的开源工具，不是南京理工大学官方模板或官方支持渠道；正式提交前请以学校、学院或任课教师的当前要求为准。

[![Smoke Test](https://github.com/Eason412/md-course-report-to-pdf/actions/workflows/smoke.yml/badge.svg)](https://github.com/Eason412/md-course-report-to-pdf/actions/workflows/smoke.yml)

<h2 align="center">📄 还在为 AI 生成的 Markdown 转 PDF 而烦恼吗？</h2>

**别再为格式反复折腾了！这是一款可以解决你大部分格式问题的 Codex Skill。✨**

**把 AI 生成的 Markdown 课程报告、课程论文或作业报告，连同图片 🖼️、表格 📊、公式 🧮 和参考文献 📚，一键转换为标准 LaTeX/PDF 文档。**

<h1 align="center">🚀 少调格式，多专注内容！🎓</h1>

## ❌❌ 错误排查 ❌❌

### 最容易出错的 4 个点

1. **缺少中文摘要、英文摘要和关键词**
   - 检查是否有 `## 摘要`
   - 检查是否有 `关键词：...`
   - 检查是否有 `## Abstract`
   - 检查是否有 `Keywords: ...`

2. **正文没有按报告章节组织**
   - 建议使用 `## 引言`
   - 建议使用 `## 正文分析`
   - 建议使用 `## 讨论`
   - 建议使用 `## 结论`

3. **图片、表格、公式写法不标准**
   - 图片使用 `![图题](image/xxx.png)`
   - 表格使用 Markdown pipe table
   - 表题紧跟表格下一行：`: 表题`
   - 公式使用 LaTeX 数学语法

4. **参考文献和正文引用没有对应**
   - 正文引用使用 `[1]`
   - 文末条目使用 `[1] 作者. 题名[J]. 期刊, 年份.`
   - 有正文引用时，需要有 `## 参考文献`

### 标准 Markdown 要求

转换前请先参考 [examples/标准课程报告模板.md](examples/标准课程报告模板.md)，并对照下方 `## Markdown 写法 📝` 检查源文件。标准课程报告通常应包含：

- 题目
- 中文摘要和关键词
- 英文摘要和 Keywords
- 按章节组织的正文，不需要手写章节编号
- 标准 Markdown 图片、表格和公式
- 有正文引用时，提供与引用编号对应的参考文献；无引用短作业可以省略参考文献区

## 适用场景

- 中文课程报告、结课论文、作业报告、专题综述。
- 需要封面、摘要、目录、正文、图表、公式和参考文献的 PDF。
- 希望用 Markdown 写作，但最终提交格式稳定的 PDF。
- 希望让 Codex 按固定流程完成排版、编译和 QA。

这个项目面向课程报告，不是完整学位论文提交模板。若用于正式学位论文，请以学校或学院当前正式模板为准。

## 格式来源

模板参照南京理工大学学位论文官方格式规范。仓库内同时提供二进制原件和转换后的可读文本版，便于查阅与逐条比对：

```text
references/njust-thesis-format.doc   官方格式原始 Word 文件
references/njust-thesis-format.md    转换后的可读文本版（章节对照用）
```

`references/format-qa.md` 中的「NJUST Source Format Mapping And Deviations」一节，记录了本项目逐条照搬了官方哪些规则、又在哪些地方为适配课程报告而有意偏离。

当前已实现的主要格式：

- A4 页面；上 30 mm、下 24 mm、左 25 mm、右 25 mm。
- 正文小四号宋体，固定 20 bp 行距；英文和数字优先使用 Times New Roman。
- 一级标题小三号加粗宋体，段前/段后 18 bp；二级标题四号加粗宋体，段前/段后 12 bp；三级标题小四号加粗宋体，段前/段后 6 bp。
- 中文摘要、英文摘要和目录置于正文前；正文页码重新从 1 开始。
- 目录：标题三号加粗居中；一级条目（章、致谢、参考文献、附录）四号加粗宋体，子级小四号宋体，对齐官方规范 §2.5。
- 图题在图下，表题在表上，图题/表题使用五号宋体。
- 图、表、公式按章节编号，例如 `图 2.1`、`表 2.1`、`（2.1）`。
- 参考文献另页开始，标题居中。
- 可选地通过 Markdown 顶部 front-matter 生成学位论文封面（官方附件 2.1 版式），含分类号、密级、UDC、学位类型、题名/副题名、作者、指导教师及职称、学位类别、学科/专业名称、研究方向、论文提交时间等字段；使用 `cover: thesis` 或下文列出的核心触发字段时切换，其他情况保持课程报告封面。

尚未实现或不会自动检查的学位论文格式：

- 书脊（封面侧边题名与单位）、封面纸张与颜色等装订要求。
- 封二、英文封二、原创性声明、学位论文使用授权声明。
- 奇偶页不同页眉、外侧页码、双面印刷。
- 图表目录、注释表、脚注/文后注释系统。
- 摘要字数、关键词 3-8 个、参考文献数量和外文/近年文献比例。
- 图的自明性、分图 `a)`/`b)`、坐标轴量纲、表内空白/破折号含义等内容规范。
- 附录 A/B 编号、附录图表编号、匿名送审信息隐藏、计量单位规范。

## 功能亮点 ✨

- 生成包含课程名称、姓名、学号的封面；支持通过 front-matter 生成学位论文封面（可选）。
- 自动抽取中文摘要、英文摘要和关键词。
- 生成目录，并区分前置页罗马页码与正文阿拉伯页码。
- 将 Markdown pipe table 转为 booktabs/longtable 风格表格。
- 通过 Pandoc 语义树为普通展示公式生成编号，并把正文数字引用转为上标；代码、链接、图片标签和原始 LaTeX 不会被正则误改。
- 清理重复数字引用，保留第一次有效正文引用，并拒绝 `[1-3-5]` 等非法编号格式。
- 输出 JSON QA，检查图片、表题、引用、公式、目录和封面字段布局。
- 隔离编译临时文件，串行化同目录并发构建，并以原子替换方式写入成功的 PDF。

## 环境要求

- Python 3.10 或更新版本。
- Pandoc。
- LaTeX 编译器：优先使用 `tectonic`，也支持 `xelatex`。

macOS 可以用 Homebrew 安装基础依赖：

```bash
brew install pandoc tectonic
```

如果使用 `xelatex`，请安装完整 TeX 发行版，例如 MacTeX 或 TeX Live。

## 安装

作为 Codex skill 使用：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Eason412/md-course-report-to-pdf.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/md-course-report-to-pdf"
```

作为普通命令行工具使用：

```bash
git clone https://github.com/Eason412/md-course-report-to-pdf.git
cd md-course-report-to-pdf
python3 scripts/run_smoke_tests.py
```

## 快速开始

在报告项目目录中运行：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/md-course-report-to-pdf"
python3 "$SKILL_DIR/scripts/build_course_report.py" input.md \
  --course "课程名称" \
  --student-name "姓名" \
  --student-id "学号" \
  --output-pdf "course_report.pdf"
```

如果需要指定封面 logo：

```bash
python3 "$SKILL_DIR/scripts/build_course_report.py" input.md \
  --course "课程名称" \
  --student-name "姓名" \
  --student-id "学号" \
  --logo "assets/school_logo.png" \
  --output-pdf "course_report.pdf"
```

如果仓库内存在 `assets/njust_logo.png`，脚本会把它作为默认 logo 使用。通过 `build_course_report.py` 指定 `--logo` 时可以使用绝对路径，脚本会复制到项目内生成目录；AI 生成的正文图片需要先保存到本地项目目录，并在 Markdown 中使用相对路径引用。

如果你不需要封面，使用 Codex skill 时可以直接告诉 AI「不加入封面」；命令行使用时加上 `--no-cover` 即可。

## 学位论文封面

复制 `examples/学位论文模板.md`，在文件顶部填写 YAML front-matter 字段，然后直接运行构建——**无需传入 `--course`、`--student-name`、`--student-id` 等课程报告参数**：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/md-course-report-to-pdf"
python3 "$SKILL_DIR/scripts/build_course_report.py" 学位论文.md \
  --output-pdf "thesis.pdf"
```

front-matter 写在 Markdown 文件最顶部，格式如下：

```yaml
---
cover: thesis
classification: TP391
secrecy: 公开
udc: 004.8
degree_type: 硕士学位论文
title: 基于深度学习的图像识别方法研究
subtitle: 以遥感图像为例
author: 张三
advisor: 李四
advisor_title: 教授
degree_category: 工学硕士
discipline: 计算机科学与技术
research_field: 计算机视觉
submit_date: 2025 年 6 月
---
```

支持的 front-matter 字段：

| 字段 | 含义 | 示例 |
|---|---|---|
| `cover` | 封面类型，填 `thesis` 强制使用学位论文封面；未填写时，`degree_type`、`advisor`、`degree_category`、`discipline`、`research_field` 中任一非空也会自动切换 | `thesis` |
| `classification` / `分类号` | 分类号 | `TP391` |
| `secrecy` / `密级` | 密级 | `公开` |
| `udc` / `UDC` | UDC 号 | `004.8` |
| `degree_type` / `学位类型` | 学位类型行文字 | `硕士学位论文` |
| `title` / `题目` | 题名（也可用正文首个 `#`） | `基于深度学习的…` |
| `subtitle` / `副标题` | 副题名（可选） | `以遥感图像为例` |
| `author` / `作者` | 作者姓名 | `张三` |
| `advisor` / `指导教师` | 指导教师姓名 | `李四` |
| `advisor_title` / `职称` | 指导教师职称 | `教授` |
| `degree_category` / `学位类别` | 学位类别 | `工学硕士` |
| `discipline` / `学科名称` | 学科或专业名称 | `计算机科学与技术` |
| `discipline_label` | 标签文字，默认「学科名称」，需要时改为「专业名称」 | `专业名称` |
| `research_field` / `研究方向` | 研究方向 | `计算机视觉` |
| `submit_date` / `论文提交时间` | 论文提交时间 | `2025 年 6 月` |

留空的字段在封面上显示为空下划线。命令行参数（如 `--course`、`--student-name`）若同时提供，会覆盖 front-matter 中对应的值。只有 `cover: thesis` 或上述 5 个核心触发字段会自动切换封面；`classification`、`secrecy`、`udc`、`author`、`advisor_title`、`submit_date` 是学位封面的补充字段，单独填写不会触发切换。未触发时自动回退到课程报告封面，行为与之前完全一致。

> 学位论文封面样式参照官方「附件 2.1」版式。正式提交前请以学校或学院当前要求为准。

## Markdown 写法 📝

### 标题、摘要和关键词

第一个 `#` 会作为报告标题；正文从 `##` 及更低级标题开始。建议不要手写 `1.`、`2.1` 等章节编号，模板会自动编号。

```markdown
# 课程报告题目

## 摘要

这里写中文摘要。

关键词：关键词一；关键词二；关键词三

## Abstract

This is the English abstract.

Keywords: keyword one; keyword two; keyword three

## 研究背景

这里写正文。
```

### 图片

图片路径应相对报告项目根目录。不要使用绝对路径、远程 URL 或跳出项目目录的路径。

```markdown
![方法流程图](image/figure_01.png)
```

标准 Markdown 图片标题和片段也可以使用，例如 `![方法流程图](image/figure_01.png#preview "可选标题")`；QA 只把真正的文件路径用于存在性检查。

不要在图片说明中手写 `图 1`，否则会和自动编号重复。

### 表格

推荐使用 Markdown pipe table，并在表格后紧跟 Pandoc 表题，中间不要空行。Markdown 源文件里表题写在表格后面，最终 PDF 会把表题渲染到表格上方。

```markdown
| 方案 | 优势 | 约束 |
|---|---|---|
| 方案 A | 易于实现 | 依赖输入质量 |
| 方案 B | 效果稳定 | 成本较高 |
: 方案对比
```

表题使用 `: 标题`，不要写 `表: 标题` 或手写 `表 1`。

### 公式

普通展示公式可以直接写：

```markdown
$$
E = mc^2
$$
```

Pandoc Lua 过滤器会把语义化的未编号展示公式转为编号公式环境。需要特殊对齐或标签时，可以显式使用 `align` 或 `equation`；代码块和原始 LaTeX 块会原样保留。

### 引用和参考文献

正文中使用数字引用：

```markdown
该方法适合用于报告排版自动化场景[1]。
```

参考文献使用简洁数字列表：

```markdown
## 参考文献

[1] 作者. 文献题名[J]. 期刊名, 年份, 卷(期): 页码.
```

新增参考文献前应核对官方来源、出版商页面或可靠数据库；不要编造作者、年份、DOI、URL 或期刊信息。

## 构建输出和 QA

默认构建会在源 Markdown 所在目录生成：

```text
course_report.pdf              默认 PDF 输出
course_report.tex              生成的 LaTeX 文件
latex/report_body.md           预处理后的正文
latex/metadata.yaml            模板元数据
latex/prepare_report.json      Markdown 预处理 QA
latex/postprocess_qa.json      LaTeX 后处理 QA
```

常用参数：

- `--output-pdf PATH`：额外复制最终 PDF 到指定路径。
- `--keep-intermediates`：保留 `.aux`、`.log`、`.toc` 等 LaTeX 中间文件。
- `--skip-compile`：只检查预处理、Pandoc 转换和后处理，不编译 PDF。该参数不能和 `--output-pdf` 同时使用。
- `--allow-slide-draft`：强制转换逐页讲稿或幻灯片内容稿。默认会拦截这类输入，因为它通常缺少摘要、正式章节和参考文献，直接转换不像课程报告。
- `--command-timeout SECONDS`：设置每个 Pandoc/LaTeX 子进程的最长运行时间，默认 180 秒。超时或编译失败时会保留命令退出信息和编译器诊断。

同一 Markdown 目录下的构建会自动串行化，避免并发任务覆盖 `latex/report_body.md` 等固定中间文件。LaTeX 在隔离临时目录中编译；只有生成并验证了有效 PDF 后，脚本才会原子替换 `--pdf`，再按需复制到 `--output-pdf`。

重点 QA 字段：

- `missing_images`：图片文件是否缺失。
- `unsafe_image_paths`：图片路径是否为绝对路径、远程路径或越出项目目录。
- `captions_with_manual_numbers`：图片说明是否手写编号。
- `missing_reference_entries`：正文引用是否缺少参考文献条目。
- `invalid_citation_markers`：是否存在无法安全解释的数字引用格式。
- `tables_without_adjacent_caption`：表格是否缺少紧邻表题。
- `remaining_unnumbered_display_math`：是否仍有未编号展示公式。
- `reference_urls`：参考文献中是否保留了不需要的 URL。
- `cover_fields_use_makebox_centering`：封面字段是否居中。
- `longtables_missing_endfoot` / `longtables_missing_endlastfoot`：跨页长表的非末页/末页底线是否完整。
- `longtable_cells_centered` / `longtable_columns_vertical_centered`：长表单元格是否水平、垂直居中。

## 测试 ✅

```bash
python3 scripts/run_smoke_tests.py
python3 -m unittest -v tests.test_regressions
python3 -m py_compile scripts/*.py tests/*.py
```

回归测试固定内容保护、路径碰撞、超时、图片解析、引用、公式和长表后处理等历史缺陷。smoke test 会渲染仓库示例和一个真实跨页长表，校验 JSON QA，并在本机存在 `tectonic` 或 `xelatex` 时编译 PDF；若同时存在 Poppler/qpdf，还会独立检查 PDF 头、页数、A4 纵向尺寸、嵌入字体、图片对象、续表文字和文件结构。GitHub Actions 会安装这些工具并强制覆盖真实 PDF 编译路径。

## 仓库结构

```text
SKILL.md                           Codex skill 使用说明
agents/openai.yaml                 skill 展示元数据
assets/njust_logo.png              README 和默认封面 logo
assets/templates/                  Pandoc/ctexart 模板
examples/标准课程报告模板.md       可复制的标准 Markdown 模板
examples/学位论文模板.md           学位论文封面 + 正文模板（front-matter 驱动）
examples/                          smoke test Markdown 输入
references/format-qa.md            详细排版和 QA 规则，含官方规范对照与偏离说明
references/njust-thesis-format.doc 南京理工大学学位论文格式参考文件（二进制原件）
references/njust-thesis-format.md  学位论文格式规范的可读文本版
THIRD_PARTY_NOTICES.md             非 MIT 资产、来源与校验信息
scripts/build_course_report.py     端到端构建封装
scripts/prepare_course_report.py   Markdown 预处理和 QA
scripts/postprocess_course_tex.py  LaTeX 后处理和 QA
scripts/run_smoke_tests.py         smoke test 运行器
tests/test_regressions.py          内容安全与构建可靠性回归测试
```

## 常见问题 🛠️

**找不到 Pandoc 或 LaTeX 编译器**：确认 `pandoc --version` 可运行；macOS 可用 `brew install pandoc tectonic`。如果暂时没有 LaTeX 编译器，可以先用 `--skip-compile` 检查 Markdown 和 LaTeX 后处理。

**图片找不到**：从报告项目根目录运行构建命令，并在 Markdown 中写真实的项目内相对路径，例如 `image/figure_01.png` 或 `figures/result.png`。LaTeX 模板配置了 `./`、`image/`、`figures/`、`assets/` 作为编译搜索路径，但 QA 不会替你猜测文件夹，Markdown 里的路径必须能直接定位到文件。

**表格没有编号**：确认表格后紧跟 `: 标题`，中间没有空行。

**出现重复的“图 1 图 1”**：删除 Markdown 图片说明或正文附近手写的 `图 1`，图片说明只保留纯标题。

**参考文献 URL 导致行太长**：优先删除参考文献列表中不必要的原始 URL 或 DOI URL；如果学校要求保留 URL，再考虑调整模板断行。

**中文字体不可用**：模板默认优先使用 macOS 的 `Songti SC` 和 `Times New Roman`；英文字体不可用时回退到 `Liberation Serif` 或 `DejaVu Serif`，中文字体不可用时优先回退到 Noto CJK 字体。若学校有固定字体要求，请安装对应字体或修改 `assets/templates/ctexart-course-report.tex`。

## 开源说明

代码、脚本、示例 Markdown 和原创仓库文档使用 MIT License 开源。

`assets/njust_logo.png`、官方格式原件及其可读转写件不属于 MIT License 授权范围；来源、文件哈希和已知限制见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本项目不是南京理工大学官方项目，也不表示学校背书。用户自行提供的 logo、校徽或其他第三方素材同样不包含在本许可证范围内。
