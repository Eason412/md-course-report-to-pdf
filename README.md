# Markdown 课程报告转 PDF

[![Smoke Test](https://github.com/Eason412/md-course-report-to-pdf/actions/workflows/smoke.yml/badge.svg)](https://github.com/Eason412/md-course-report-to-pdf/actions/workflows/smoke.yml)

把中文 Markdown 课程报告、课程论文或作业报告转换成排版完整的 LaTeX/PDF 文档。

这个仓库既可以作为 Codex skill 使用，也可以作为普通命令行工具直接运行。它会完成 Markdown 预处理、摘要抽取、Pandoc 转 LaTeX、LaTeX 后处理、PDF 编译和 JSON QA 检查，适合需要稳定输出中文课程报告 PDF 的场景。

## 格式来源

当前模板的页面尺寸、页边距、正文字号、行距、标题层级、图表位置、图表编号、公式编号、摘要/目录/正文分页等，主要参照仓库中的原始 Word 文件：

```text
references/njust-thesis-format.doc
```

该文件来自“南京理工大学博士、硕士学位论文撰写格式”示例文档。这个项目只抽取其中适合课程报告的排版规则，并没有实现完整学位论文提交模板。完整学位论文仍应以学院或学校当前正式模板为准。

## 适用场景

- 中文课程报告、课程论文、结课作业、专题综述。
- 需要封面、摘要、目录、正文和参考文献的 PDF。
- 报告中包含图片、Markdown 表格、公式和数字引用。
- 希望用 Markdown 写作，但最终提交 PDF。
- 希望让 Codex 按固定流程处理报告排版和 QA。

这个项目不是通用论文排版框架。它默认面向中文课程报告，优先保证封面、目录、图表编号、公式编号、引用清理和 PDF QA 的稳定性。

## 功能

- 生成包含课程名称、姓名、学号的封面。
- 自动抽取中文摘要、英文摘要和关键词。
- 前置页使用罗马页码，正文从阿拉伯数字第 1 页开始。
- 按中文课程报告习惯生成目录。
- 图、表、公式按章节编号，例如 `图 2.1`、`表 2.1`、`（2.1）`。
- Markdown pipe table 渲染为 booktabs/longtable 风格表格。
- 长表格支持重复表头、续表标记和底线检查。
- 清理重复数字引用，保留第一次有效正文引用。
- 支持简洁的 GB/T 7714 风格参考文献。
- 输出 JSON QA，用于检查缺失图片、不安全路径、错误表题、引用不匹配、参考文献 URL、未编号公式、目录格式和封面字段布局。

## 已参照实现的格式

- A4 页面；上 30 mm、下 24 mm、左 25 mm、右 25 mm 的页边距。
- 正文使用小四号宋体，固定 20 bp 行距；英文和数字优先使用 Times New Roman。
- 一级标题小三号加粗宋体，段前/段后 18 bp；二级标题四号加粗宋体，段前/段后 12 bp；三级标题小四号加粗宋体，段前/段后 6 bp。
- 中文摘要、英文摘要和目录置于正文前，正文页码重新从 1 开始。
- 图题置于图下，表题置于表上，图题/表题使用五号宋体。
- 图、表、公式按章节编号。
- 参考文献另页开始，标题居中。

## 原格式中尚未实现或未自动处理的部分

以下要求存在于 `references/njust-thesis-format.doc`，但当前工具没有写入模板或不会自动检查。需要严格按学位论文模板提交时，应手工处理或扩展模板。

- **装订和印刷**：封面卡纸颜色/克重、成册尺寸、封二/声明单页印刷、摘要以后双面印刷等实体装订要求没有实现。
- **完整学位论文封面**：分类号、密级、UDC、博士/硕士/专业学位类型、导师、学位类别、学科名称、研究方向、论文提交时间、书脊等字段没有实现。当前封面只面向课程报告，包含课程名称、姓名和学号。
- **封二和声明页**：中文封二、英文封二、原创性声明、学位论文使用授权声明没有生成。
- **页眉和页码位置**：原格式要求奇偶页页眉不同、页码位于外侧；当前模板默认无页眉，页脚页码居中。
- **目录字体差异**：原格式中目录一级标题、致谢、参考文献、附录等使用四号加粗宋体，其余为小四号；当前模板为课程报告可读性做了简化，目录各级使用统一小四号宋体，通过缩进体现层级。
- **目录收录层级**：原格式目次页主要由一、二、三级标题及致谢、参考文献、附录等组成；当前模板默认 `tocdepth=4`，可能收录到四级标题。
- **图表目录**：原格式在图表较多时可列图表清单；当前工具不自动生成图目录或表目录。
- **注释表和注释系统**：符号、缩略词、计量单位、术语注释表，以及文后注释/脚注示例没有自动生成。
- **摘要长度约束**：原格式要求硕士中文摘要约 400-600 字、博士中文摘要约 800-1000 字；当前工具只抽取摘要，不自动统计或限制摘要字数。
- **关键词数量**：原格式通常为 3-8 个关键词；当前课程报告默认按最多 5 个关键词进行提醒。
- **正文结构要求**：引言、结论、致谢、附录等章节的内容要求不会自动生成，只能由源 Markdown 自行写入。
- **参考文献数量和比例**：博士不少于 80 篇、硕士不少于 40 篇、外文文献和近年文献比例等学位论文要求不会检查。课程报告只检查正文引用和参考文献编号是否匹配。
- **图表内容规范**：图的自明性、分图 `a)`/`b)` 标注、坐标轴量纲、表内空白/破折号含义、表内不用“同上”等规范不会自动判断。
- **公式和引用写法**：原格式要求公式编号不用 `*` 等符号，引用公式时写“式（2.3）”；文献引用可写“文献[4]”或右上角标注。当前工具只负责公式编号和数字引用清理，不判断这些行文写法。
- **附录编号和装订**：附录 A、附录 B、图 B1、表 B1 等附录专用编号规则没有实现；附录单独装订、单独编页码或与正文连续编页码也不会自动处理。
- **匿名送审**：隐藏作者、导师、致谢等身份信息的匿名送审要求不会自动处理。
- **计量单位**：国际单位制和单位符号规范不会自动检查。

## 环境要求

- Python 3.10 或更新版本。
- `PATH` 中可用的 Pandoc。
- `PATH` 中可用的 LaTeX 编译器：优先使用 `tectonic`，也支持 `xelatex`。
- 如果学校模板要求指定中文字体，请在本机安装对应字体。默认模板在 macOS 字体不可用时会回退到常见 TeX 字体。

macOS 可以用 Homebrew 安装基础依赖：

```bash
brew install pandoc tectonic
```

如果使用 `xelatex`，请安装完整 TeX 发行版，例如 MacTeX 或 TeX Live。

## 安装方式

### 方式一：作为 Codex skill 使用

把仓库克隆到 Codex skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Eason412/md-course-report-to-pdf.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/md-course-report-to-pdf"
```

之后在 Codex 中触发 `md-course-report-to-pdf` skill 即可。

### 方式二：作为普通命令行工具使用

克隆到任意目录：

```bash
git clone https://github.com/Eason412/md-course-report-to-pdf.git
cd md-course-report-to-pdf
python3 scripts/run_smoke_tests.py
```

在其他报告项目中使用时，把 `SKILL_DIR` 指向这个仓库路径：

```bash
SKILL_DIR="/path/to/md-course-report-to-pdf"
```

## 快速开始

假设报告项目中有 `input.md`：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/md-course-report-to-pdf"
python3 "$SKILL_DIR/scripts/build_course_report.py" input.md \
  --course "课程名称" \
  --student-name "姓名" \
  --student-id "学号" \
  --output-pdf "course_report.pdf"
```

如果需要指定校徽或其他封面 logo：

```bash
python3 "$SKILL_DIR/scripts/build_course_report.py" input.md \
  --course "课程名称" \
  --student-name "姓名" \
  --student-id "学号" \
  --logo "assets/school_logo.png" \
  --output-pdf "course_report.pdf"
```

如果本地存在 `assets/njust_logo.png`，封装脚本可以把它作为默认 logo 使用。该文件被 `.gitignore` 排除，因为学校 logo 和商标类素材通常需要单独授权，不应默认随开源代码分发。

## 输入 Markdown 约定

### 标题和章节

- 第一个 `#` 标题会作为报告标题。
- 正文从 `##` 及更低级标题开始。
- 建议不要在标题里手写 `1.`、`2.1` 等编号，LaTeX 模板会自动编号。
- 一级正文标题会从新页开始。

示例：

```markdown
# 可再生合成燃料与碳中和简报

## 摘要

这里是中文摘要。

关键词：可再生燃料；绿氢；碳中和

## Abstract

This is the English abstract.

Keywords: renewable fuel; green hydrogen; carbon neutrality

## 技术路线

正文内容。
```

### 摘要和关键词

预处理脚本会从源 Markdown 中抽取：

- `摘要`
- `关键词`
- `Abstract`
- `Keywords`

抽取后，这些内容会进入模板前置页，不会重复出现在正文中。

默认关键词最多 5 个。如果学校要求不同数量，请先调整源 Markdown 或模板规则。

### 图片

- 图片路径应相对报告项目根目录。
- 不建议使用绝对路径、远程 URL 或跳出项目目录的路径。
- 图片说明只写标题，例如：

```markdown
![方法流程图](image/figure_01.png)
```

不要写成：

```markdown
![图 1 方法流程图](image/figure_01.png)
```

模板会自动生成 `图 2.1` 这类编号，手写编号会造成重复。

### 表格

推荐使用 Markdown pipe table，并在表格后紧跟 Pandoc 表题：

```markdown
| 路线 | 优势 | 约束 |
|---|---|---|
| 绿色甲醇 | 便于储运 | 依赖绿氢成本 |
: 绿色甲醇路线比较
```

注意：

- 表题必须紧贴表格，中间不要空行。
- 表题使用 `: 标题`，不要使用 `表: 标题`。
- 不要在表题中手写 `表 1`。
- 表头尽量短，例如 `路线`、`主要原料`、`优势`、`约束`。

### 公式

普通展示公式可以使用 Markdown/LaTeX 的展示公式写法：

```markdown
$$
E = mc^2
$$
```

后处理脚本会把未编号展示公式转为编号公式环境。需要特殊对齐或标签时，可以在 Markdown 中显式使用 `align` 或 `equation`。

### 引用和参考文献

正文中使用数字引用：

```markdown
可再生合成燃料可用于难以直接电气化的交通场景[1]。
```

参考文献使用简洁数字列表：

```markdown
## 参考文献

[1] International Energy Agency. The role of e-fuels in decarbonising transport[R]. Paris: IEA, 2023.
```

建议：

- 新增参考文献前先查官方来源、出版商页面或可靠数据库。
- 不要编造作者、年份、DOI、URL 或期刊信息。
- 同一条参考文献通常只保留第一次有意义的正文引用。
- 参考文献列表中尽量隐藏原始 URL 和 DOI URL，除非学校模板明确要求。

## 构建输出

默认构建会在源 Markdown 所在目录生成：

```text
course_report.pdf              默认 PDF 输出
course_report.tex              生成的 LaTeX 文件
latex/report_body.md           预处理后的正文
latex/metadata.yaml            模板元数据
latex/prepare_report.json      Markdown 预处理 QA
latex/postprocess_qa.json      LaTeX 后处理 QA
```

如果传入 `--output-pdf`，最终 PDF 会额外复制到指定路径。

如果不想保留 LaTeX 编译中间文件，默认构建会清理 `.aux`、`.log`、`.toc` 等文件。需要保留时传入：

```bash
--keep-intermediates
```

如果只想检查预处理、Pandoc 转换和后处理，不编译 PDF：

```bash
--skip-compile
```

`--skip-compile` 不能和 `--output-pdf` 同时使用，因为跳过编译时不会产生最终 PDF。

## QA 检查

构建完成后，建议先看命令输出中的 JSON summary，再检查：

```bash
cat latex/prepare_report.json
cat latex/postprocess_qa.json
```

重点字段包括：

- `missing_images`：图片文件是否缺失。
- `unsafe_image_paths`：图片路径是否为绝对路径、远程路径或越出项目目录。
- `captions_with_manual_numbers`：图片说明是否手写编号。
- `missing_reference_entries`：正文引用是否缺少参考文献条目。
- `tables_without_adjacent_caption`：表格是否缺少紧邻表题。
- `invalid_table_captions`：是否使用了不支持的表题语法。
- `remaining_raw_citations_before_references`：参考文献前是否还残留原始引用标记。
- `remaining_unnumbered_display_math`：是否仍有未编号展示公式。
- `reference_urls`：参考文献中是否保留了不需要的 URL。
- `longtables_missing_endfoot`：长表格是否缺少续页底线。
- `toc_entry_font_sizes`：目录字体是否符合模板规则。
- `cover_fields_use_makebox_centering`：封面字段是否居中。

## 测试

发布或修改脚本前运行 smoke test：

```bash
python3 scripts/run_smoke_tests.py
```

测试会渲染仓库内置示例，校验 JSON QA 输出，并在本机存在 `tectonic` 或 `xelatex` 时编译 PDF。如果没有 LaTeX 编译器，测试仍会覆盖预处理、Pandoc 转换和后处理流程。

GitHub Actions 会运行跨平台 smoke test 和 Python 语法检查，用于确认公开仓库在干净环境中至少能完成 Markdown 到 LaTeX 的主要流程。

也可以做 Python 语法检查：

```bash
python3 -m py_compile scripts/*.py
```

## 仓库结构

```text
SKILL.md                          Codex skill 使用说明
agents/openai.yaml                skill 展示元数据
assets/templates/                 Pandoc/ctexart 模板
examples/                         smoke test Markdown 输入
references/format-qa.md           详细排版和 QA 规则
references/njust-thesis-format.doc 南京理工大学学位论文格式参考文件
scripts/build_course_report.py    端到端构建封装
scripts/prepare_course_report.py  Markdown 预处理和 QA
scripts/postprocess_course_tex.py LaTeX 后处理和 QA
scripts/run_smoke_tests.py        smoke test 运行器
```

## 常见问题

### 找不到 Pandoc

确认 `pandoc` 在 `PATH` 中：

```bash
pandoc --version
```

macOS 可以用：

```bash
brew install pandoc
```

### 找不到 LaTeX 编译器

优先安装 `tectonic`：

```bash
brew install tectonic
```

也可以使用 `xelatex`。如果只想先检查 Markdown 和 LaTeX 后处理，可以临时传入 `--skip-compile`。

### 图片找不到

从报告项目根目录运行构建命令，并保持图片路径为相对路径。默认模板会搜索：

```text
./
image/
figures/
assets/
```

### 表格没有编号

确认表格后紧跟 `: 标题`，中间没有空行：

```markdown
| A | B |
|---|---|
| 1 | 2 |
: 示例表格
```

### 出现重复的“图 1 图 1”

删除 Markdown 图片说明或正文附近手写的 `图 1`。图片说明只保留纯标题。

### 参考文献 URL 导致行太长

优先删除参考文献列表中不必要的原始 URL 或 DOI URL。如果学校要求保留 URL，再考虑调整模板断行。

### 中文字体不可用

模板默认优先使用 macOS 的 `Songti SC` 和 `Times New Roman`，不可用时回退到 TeX 字体。若学校有固定字体要求，请安装对应字体或修改 `assets/templates/ctexart-course-report.tex`。

## 开源说明

代码、模板、示例和文档使用 MIT License 开源。用户自行提供的 logo、校徽或其他第三方素材不包含在本许可证范围内。

仓库不会跟踪 `assets/njust_logo.png`。如果你需要使用学校 logo，请在本地自行放置有授权的图片，或通过 `--logo` 指定路径。
