# Markdown 课程报告转 PDF

<p align="center">
  <img src="assets/njust_logo.png" alt="南京理工大学校徽" width="96">
</p>

> 如果你在使用中遇到格式问题、构建失败、学校模板适配需求，或有更好的排版、QA、工作流建议，欢迎提交 GitHub Issue，也可以发邮件到 `huyi@njust.edu.cn`。邮件标题建议注明来意，例如 `md-course-report-to-pdf 使用反馈`、`课程报告 PDF 格式建议` 或 `Codex skill 改进建议`。

[![Smoke Test](https://github.com/Eason412/md-course-report-to-pdf/actions/workflows/smoke.yml/badge.svg)](https://github.com/Eason412/md-course-report-to-pdf/actions/workflows/smoke.yml)

<h2 align="center">📄 还在为 AI 生成的 Markdown 转 PDF 而烦恼吗？</h2>

**别再为格式反复折腾了！这是一款可以解决你大部分格式问题的 Codex Skill。✨**

**把 AI 生成的 Markdown 课程报告、课程论文或作业报告，连同图片 🖼️、表格 📊、公式 🧮 和参考文献 📚，一键转换为标准 LaTeX/PDF 文档。**

<h1 align="center">🚀 少调格式，多专注内容！🎓</h1>

## 适用场景

- 中文课程报告、结课论文、作业报告、专题综述。
- 需要封面、摘要、目录、正文、图表、公式和参考文献的 PDF。
- 希望用 Markdown 写作，但最终提交格式稳定的 PDF。
- 希望让 Codex 按固定流程完成排版、编译和 QA。

这个项目面向课程报告，不是完整学位论文提交模板。若用于正式学位论文，请以学校或学院当前正式模板为准。

## 格式来源

模板主要参照仓库中的原始 Word 文件：

```text
references/njust-thesis-format.doc
```

当前已实现的主要格式：

- A4 页面；上 30 mm、下 24 mm、左 25 mm、右 25 mm。
- 正文小四号宋体，固定 20 bp 行距；英文和数字优先使用 Times New Roman。
- 一级标题小三号加粗宋体，段前/段后 18 bp；二级标题四号加粗宋体，段前/段后 12 bp；三级标题小四号加粗宋体，段前/段后 6 bp。
- 中文摘要、英文摘要和目录置于正文前；正文页码重新从 1 开始。
- 图题在图下，表题在表上，图题/表题使用五号宋体。
- 图、表、公式按章节编号，例如 `图 2.1`、`表 2.1`、`（2.1）`。
- 参考文献另页开始，标题居中。

尚未实现或不会自动检查的学位论文格式：

- 完整学位论文封面字段：分类号、密级、UDC、学位类型、导师、学位类别、学科名称、研究方向、论文提交时间、书脊等。
- 封二、英文封二、原创性声明、学位论文使用授权声明。
- 奇偶页不同页眉、外侧页码、双面印刷、装订和封面纸张要求。
- 图表目录、注释表、脚注/文后注释系统。
- 摘要字数、关键词 3-8 个、参考文献数量和外文/近年文献比例。
- 图的自明性、分图 `a)`/`b)`、坐标轴量纲、表内空白/破折号含义等内容规范。
- 附录 A/B 编号、附录图表编号、匿名送审信息隐藏、计量单位规范。

## 功能亮点 ✨

- 生成包含课程名称、姓名、学号的封面。
- 自动抽取中文摘要、英文摘要和关键词。
- 生成目录，并区分前置页罗马页码与正文阿拉伯页码。
- 将 Markdown pipe table 转为 booktabs/longtable 风格表格。
- 为未编号展示公式生成编号。
- 清理重复数字引用，保留第一次有效正文引用。
- 输出 JSON QA，检查图片、表题、引用、公式、目录和封面字段布局。

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

如果仓库内存在 `assets/njust_logo.png`，脚本会把它作为默认 logo 使用。AI 生成的图片需要先保存到本地项目目录，并在 Markdown 中使用相对路径引用。

如果你不需要封面，使用 Codex skill 时可以直接告诉 AI「不加入封面」；命令行使用时加上 `--no-cover` 即可。

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

不要在图片说明中手写 `图 1`，否则会和自动编号重复。

### 表格

推荐使用 Markdown pipe table，并在表格后紧跟 Pandoc 表题，中间不要空行。

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

后处理脚本会把未编号展示公式转为编号公式环境。需要特殊对齐或标签时，可以显式使用 `align` 或 `equation`。

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

重点 QA 字段：

- `missing_images`：图片文件是否缺失。
- `unsafe_image_paths`：图片路径是否为绝对路径、远程路径或越出项目目录。
- `captions_with_manual_numbers`：图片说明是否手写编号。
- `missing_reference_entries`：正文引用是否缺少参考文献条目。
- `tables_without_adjacent_caption`：表格是否缺少紧邻表题。
- `remaining_unnumbered_display_math`：是否仍有未编号展示公式。
- `reference_urls`：参考文献中是否保留了不需要的 URL。
- `cover_fields_use_makebox_centering`：封面字段是否居中。

## 测试 ✅

```bash
python3 scripts/run_smoke_tests.py
python3 -m py_compile scripts/*.py
```

smoke test 会渲染仓库示例、校验 JSON QA，并在本机存在 `tectonic` 或 `xelatex` 时编译 PDF。GitHub Actions 会在干净环境中运行跨平台 smoke test 和 Python 语法检查。

## 仓库结构

```text
SKILL.md                           Codex skill 使用说明
agents/openai.yaml                 skill 展示元数据
assets/njust_logo.png              README 和默认封面 logo
assets/templates/                  Pandoc/ctexart 模板
examples/                          smoke test Markdown 输入
references/format-qa.md            详细排版和 QA 规则
references/njust-thesis-format.doc 南京理工大学学位论文格式参考文件
scripts/build_course_report.py     端到端构建封装
scripts/prepare_course_report.py   Markdown 预处理和 QA
scripts/postprocess_course_tex.py  LaTeX 后处理和 QA
scripts/run_smoke_tests.py         smoke test 运行器
```

## 常见问题 🛠️

**找不到 Pandoc 或 LaTeX 编译器**：确认 `pandoc --version` 可运行；macOS 可用 `brew install pandoc tectonic`。如果暂时没有 LaTeX 编译器，可以先用 `--skip-compile` 检查 Markdown 和 LaTeX 后处理。

**图片找不到**：从报告项目根目录运行构建命令，并保持图片路径为相对路径。默认模板会搜索 `./`、`image/`、`figures/`、`assets/`。

**表格没有编号**：确认表格后紧跟 `: 标题`，中间没有空行。

**出现重复的“图 1 图 1”**：删除 Markdown 图片说明或正文附近手写的 `图 1`，图片说明只保留纯标题。

**参考文献 URL 导致行太长**：优先删除参考文献列表中不必要的原始 URL 或 DOI URL；如果学校要求保留 URL，再考虑调整模板断行。

**中文字体不可用**：模板默认优先使用 macOS 的 `Songti SC` 和 `Times New Roman`，不可用时回退到 TeX 字体。若学校有固定字体要求，请安装对应字体或修改 `assets/templates/ctexart-course-report.tex`。

## 开源说明

代码、模板、示例和文档使用 MIT License 开源。

`assets/njust_logo.png` 用于 README 展示和默认封面 logo。南京理工大学校徽及相关标识权利归属原权利人，不属于 MIT License 授权范围。用户自行提供的 logo、校徽或其他第三方素材也不包含在本许可证范围内。
