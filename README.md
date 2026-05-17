# Markdown 课程报告转 PDF

把中文 Markdown 课程报告、课程论文或作业报告转换成排版完整的 LaTeX/PDF 文档。

这个仓库既可以作为 Codex skill 使用，也可以直接在命令行运行脚本。流程会先预处理 Markdown，抽取中英文摘要，再通过 `ctexart` Pandoc 模板生成 LaTeX，随后处理引用、表格和公式，最后编译 PDF 并输出 JSON QA 报告。

## 功能

- 生成包含课程名称、姓名、学号的封面。
- 自动抽取中文摘要、英文摘要和关键词。
- 按中文课程报告习惯生成目录。
- 图、表、公式按章节编号。
- Markdown pipe table 渲染为 booktabs/longtable 风格表格。
- 清理重复数字引用，并支持简洁的 GB/T 7714 风格参考文献。
- 输出 JSON QA，用于检查缺失图片、不安全路径、错误表题、引用不匹配、参考文献 URL、未编号公式、目录格式和封面字段布局。

## 环境要求

- Python 3.10 或更新版本。
- `PATH` 中可用的 Pandoc。
- `PATH` 中可用的 LaTeX 编译器：优先使用 `tectonic`，也支持 `xelatex`。
- 如果学校模板要求指定中文字体，请在本机安装对应字体。默认模板在 macOS 字体不可用时会回退到常见 TeX 字体。

## 使用方法

在任意报告项目目录中运行：

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

## Markdown 写法约定

- 第一个 `#` 标题会作为报告标题。
- 正文从 `##` 及更低级标题开始。
- 中英文摘要写在源 Markdown 中，预处理脚本会把它们移动到前置页。
- 图片路径保持为相对报告项目根目录的路径。
- 图片说明只写标题，例如 `![方法流程图](image/figure_01.png)`。
- 表格使用 Markdown pipe table，并在表格后紧跟 Pandoc 表题：

```markdown
| 路线 | 优势 | 约束 |
|---|---|---|
| 绿色甲醇 | 便于储运 | 依赖绿氢成本 |
: 绿色甲醇路线比较
```

不要在图片或表格说明中手写 `图 1`、`表 1` 这类编号，模板会自动编号。

## 测试

发布或修改脚本前运行 smoke test：

```bash
python3 scripts/run_smoke_tests.py
```

测试会渲染仓库内置示例，校验 JSON QA 输出，并在本机存在 `tectonic` 或 `xelatex` 时编译 PDF。如果没有 LaTeX 编译器，测试仍会覆盖预处理、Pandoc 转换和后处理流程。

## 仓库结构

```text
SKILL.md                          Codex skill 使用说明
agents/openai.yaml                skill 展示元数据
assets/templates/                 Pandoc/ctexart 模板
examples/                         smoke test Markdown 输入
references/format-qa.md           详细排版和 QA 规则
scripts/build_course_report.py    端到端构建封装
scripts/prepare_course_report.py  Markdown 预处理和 QA
scripts/postprocess_course_tex.py LaTeX 后处理和 QA
scripts/run_smoke_tests.py        smoke test 运行器
```

## 许可证

代码、模板、示例和文档使用 MIT License 开源。用户自行提供的 logo 或其他第三方素材不包含在本许可证范围内。
