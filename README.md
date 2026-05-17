# Markdown Course Report to PDF

Convert Chinese Markdown course reports, class papers, and homework reports into polished LaTeX/PDF deliverables.

This repository is packaged as a Codex skill, but the scripts can also be run directly from a shell. The workflow preprocesses Markdown, extracts Chinese and English abstracts, renders through a `ctexart` Pandoc template, postprocesses citations/tables/math, compiles the PDF, and writes JSON QA reports.

## Features

- Cover page with course name, student name, and student ID fields.
- Chinese and English abstract extraction.
- Table of contents with Chinese academic report styling.
- Section-scoped figure, table, and equation numbering.
- Markdown pipe tables rendered as booktabs/longtable tables.
- Numeric citation cleanup and GB/T 7714-style reference-list support.
- JSON QA for missing images, unsafe paths, malformed table captions, citation mismatches, raw URLs, display math, TOC layout, and cover-field layout.

## Requirements

- Python 3.10 or newer.
- Pandoc on `PATH`.
- A LaTeX compiler on `PATH`: `tectonic` is preferred, `xelatex` also works.
- For best Chinese rendering, install the fonts required by your school template. The bundled template falls back to common TeX fonts when macOS fonts are unavailable.

## Usage

From any report project directory:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/md-course-report-to-pdf"
python3 "$SKILL_DIR/scripts/build_course_report.py" input.md \
  --course "课程名称" \
  --student-name "姓名" \
  --student-id "学号" \
  --output-pdf "course_report.pdf"
```

Pass a logo explicitly when needed:

```bash
python3 "$SKILL_DIR/scripts/build_course_report.py" input.md \
  --course "课程名称" \
  --student-name "姓名" \
  --student-id "学号" \
  --logo "assets/school_logo.png" \
  --output-pdf "course_report.pdf"
```

If `assets/njust_logo.png` exists locally, the wrapper can use it as a default logo. That file is intentionally ignored by Git because school logos and trademarks may require separate permission to redistribute.

## Markdown Conventions

- Use the first `#` heading as the report title.
- Use `##` and below for body sections.
- Put Chinese and English abstracts in the source Markdown; the preprocessor moves them into front matter.
- Keep image paths relative to the report project root.
- Use figure captions as pure titles, for example `![方法流程图](image/figure_01.png)`.
- Use Markdown pipe tables with an adjacent Pandoc caption line:

```markdown
| 路线 | 优势 | 约束 |
|---|---|---|
| 绿色甲醇 | 便于储运 | 依赖绿氢成本 |
: 绿色甲醇路线比较
```

Do not write manual labels such as `图 1` or `表 1` in captions.

## Testing

Run the smoke tests before publishing changes:

```bash
python3 scripts/run_smoke_tests.py
```

The tests render the bundled examples, validate JSON QA output, and compile PDFs when `tectonic` or `xelatex` is available. If no LaTeX compiler is available, the tests still exercise preprocessing, Pandoc conversion, and postprocessing.

## Repository Layout

```text
SKILL.md                          Codex skill instructions
agents/openai.yaml                Skill display metadata
assets/templates/                 Pandoc/ctexart template
examples/                         Smoke-test Markdown inputs
references/format-qa.md           Detailed layout and QA rules
scripts/build_course_report.py    End-to-end wrapper
scripts/prepare_course_report.py  Markdown preprocessing and QA
scripts/postprocess_course_tex.py LaTeX postprocessing and QA
scripts/run_smoke_tests.py        Smoke-test runner
```

## License

The code, templates, examples, and documentation are released under the MIT License. User-supplied logos or other third-party assets are not covered by this license.
