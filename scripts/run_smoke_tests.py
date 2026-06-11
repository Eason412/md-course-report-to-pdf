#!/usr/bin/env python3
"""Run smoke tests for the Markdown course-report PDF workflow."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
SCRIPTS = ROOT / "scripts"
BUILD = SCRIPTS / "build_course_report.py"
PREPARE = SCRIPTS / "prepare_course_report.py"
LOCAL_DEFAULT_LOGO = ROOT / "assets" / "njust_logo.png"

COURSE = "示例课程"
STUDENT_NAME = "示例学生"
STUDENT_ID = "0000000000"


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def first_longtable(tex: str) -> str:
    match = re.search(r"\\begin\{longtable\}.*?\\end\{longtable\}", tex, flags=re.S)
    return match.group(0) if match else ""


def fail(message: str, details: object | None = None) -> dict[str, object]:
    result: dict[str, object] = {"ok": False, "error": message}
    if details is not None:
        result["details"] = details
    return result


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def render_case(source: Path, work_root: Path, compiler_available: bool) -> dict[str, object]:
    case_dir = work_root / source.stem
    case_dir.mkdir(parents=True)
    copied_source = case_dir / source.name
    shutil.copy2(source, copied_source)

    latex_dir = case_dir / "latex"
    tex = case_dir / "report.tex"
    pdf_path = case_dir / "report.pdf"
    build_cmd = [
        sys.executable,
        str(BUILD),
        str(copied_source),
        "--work-dir",
        str(latex_dir),
        "--course",
        COURSE,
        "--student-name",
        STUDENT_NAME,
        "--student-id",
        STUDENT_ID,
        "--tex",
        str(tex),
        "--pdf",
        str(pdf_path),
    ]
    if not compiler_available:
        build_cmd.append("--skip-compile")
    else:
        build_cmd.extend(["--output-pdf", str(pdf_path)])

    built = run(build_cmd, case_dir)
    if built.returncode != 0:
        return fail("build failed", {"stdout": built.stdout, "stderr": built.stderr})

    try:
        build_summary = json.loads(built.stdout)
    except json.JSONDecodeError:
        return fail("build summary is not JSON", {"stdout": built.stdout, "stderr": built.stderr})

    if not tex.exists():
        return fail("expected TeX output missing", str(tex))
    report = load_json(latex_dir / "prepare_report.json")
    post_qa = load_json(latex_dir / "postprocess_qa.json")

    errors: list[str] = []
    warnings = report.get("warnings", [])
    qa = report.get("qa", {})
    if not isinstance(qa, dict):
        return fail("prepare QA is not an object", report)

    check(warnings == [], "prepare warnings must be empty", errors)
    check(post_qa.get("remaining_raw_citations_before_references") == [], "raw citations remain", errors)
    check(post_qa.get("remaining_unnumbered_display_math") == 0, "unnumbered display math remains", errors)
    font_sizes = post_qa.get("toc_entry_font_sizes", [])
    check(font_sizes == ["-4", "4"], "toc_entry_font_sizes must be ['-4', '4'] (sub 小4号, level-1 4号)", errors)
    check(post_qa.get("toc_section_font_size") == "4", "TOC level-1 entries must be four-size", errors)
    check(post_qa.get("toc_section_is_bold") is True, "TOC level-1 entries must be bold", errors)
    check(post_qa.get("toc_sub_font_size") == "-4", "TOC sub-level entries must be small-four", errors)
    check(post_qa.get("toc_uses_shared_numwidth") is True, "TOC entries must use shared number width", errors)
    check(post_qa.get("toc_page_width_configured") is True, "TOC page number width/right margin must be configured", errors)
    check(post_qa.get("cover_fields_use_makebox_centering") is True, "cover fields must use centered makebox layout", errors)
    check(post_qa.get("cover_fields_have_underlines") is True, "cover value boxes must use equal-width underlines", errors)
    cover = report.get("cover", {})
    if not isinstance(cover, dict):
        return fail("cover QA is not an object", report)
    check(
        cover.get("logo_exists") is LOCAL_DEFAULT_LOGO.exists(),
        "default logo QA must match local asset availability",
        errors,
    )

    citation_dedup = qa.get("citation_dedup", {})
    if source.name == "minimal_report.md":
        check(isinstance(citation_dedup, dict), "citation_dedup must be an object", errors)
        check(citation_dedup.get("removed_marker_count") == 1, "minimal duplicate citation marker must be removed", errors)
        check(citation_dedup.get("rewritten_marker_count") == 0, "minimal duplicate citation marker should not be rewritten", errors)

    if source.name == "citation_report.md":
        check(qa.get("citation_numbers") == [1, 2, 3], "citation case must collect only real body citations", errors)
        check(qa.get("reference_numbers") == [1, 2, 3], "citation case must collect only real reference labels", errors)
        check(qa.get("pipe_table_count") == 0, "pipe table inside code block must be ignored", errors)
        check(isinstance(citation_dedup, dict), "citation_dedup must be an object", errors)
        check(
            citation_dedup.get("normalized_marker_count", 0) >= 1,
            "citation case must normalize Chinese/full-width citation markers",
            errors,
        )
        check(
            citation_dedup.get("rewritten_marker_count", 0) >= 1,
            "citation case must rewrite mixed repeated/new markers",
            errors,
        )
        check(
            citation_dedup.get("removed_marker_count", 0) >= 1,
            "citation case must remove fully repeated markers",
            errors,
        )

    if source.name == "no_reference_report.md":
        check(qa.get("citation_numbers") == [], "no-reference case must have no citations", errors)
        check(qa.get("reference_numbers") == [], "no-reference case must have no reference labels", errors)
        check(post_qa.get("references_section_found") is False, "no-reference case should not invent references", errors)

    if source.name == "table_report.md":
        tex_text = tex.read_text(encoding="utf-8")
        table_block = first_longtable(tex_text)
        check(qa.get("pipe_table_count") == 1, "table pipe_table_count must be 1", errors)
        check(qa.get("table_caption_count") == 1, "table table_caption_count must be 1", errors)
        check(post_qa.get("longtable_count") == 1, "table longtable_count must be 1", errors)
        check(post_qa.get("booktabs_longtable_count") == 1, "table booktabs_longtable_count must be 1", errors)
        check(post_qa.get("longtables_missing_caption") == 0, "table longtables_missing_caption must be 0", errors)
        check(post_qa.get("longtables_missing_endfoot") == 0, "table longtables_missing_endfoot must be 0", errors)
        check(
            post_qa.get("longtables_missing_continued_caption") == 0,
            "table longtables_missing_continued_caption must be 0",
            errors,
        )
        check(post_qa.get("longtable_headers_centered") is True, "table headers must be centered", errors)
        check("（续表）" in table_block, "longtable must include continued caption text", errors)
        check(r"\endfirsthead" in table_block and r"\endhead" in table_block, "longtable must keep repeated heads", errors)
        check(r"\endfoot" in table_block and r"\endlastfoot" in table_block, "longtable must define foot and lastfoot", errors)
        check(r"\multicolumn{1}{c}{方案}" in table_block, "plain longtable header cells must be centered", errors)

    if compiler_available:
        check(pdf_path.exists(), "compiled PDF must exist", errors)
        check(pdf_path.exists() and pdf_path.stat().st_size > 0, "compiled PDF must be nonempty", errors)

    if source.name == "标准课程报告模板.md":
        check(qa.get("image_count") == 0, "standard template must not reference a missing live image", errors)
        check(qa.get("pipe_table_count") == 1, "standard template pipe_table_count must be 1", errors)
        check(qa.get("table_caption_count") == 1, "standard template table_caption_count must be 1", errors)
        check(qa.get("citation_numbers") == [1, 2, 3], "standard template citations must be [1, 2, 3]", errors)
        check(qa.get("reference_numbers") == [1, 2, 3], "standard template references must be [1, 2, 3]", errors)

    return {
        "ok": not errors,
        "errors": errors,
        "prepare": {
            "warning_count": len(warnings) if isinstance(warnings, list) else None,
            "pipe_table_count": qa.get("pipe_table_count"),
            "table_caption_count": qa.get("table_caption_count"),
            "citation_dedup": qa.get("citation_dedup"),
        },
        "postprocess": {
            "remaining_raw_citations_before_references": post_qa.get(
                "remaining_raw_citations_before_references"
            ),
            "remaining_unnumbered_display_math": post_qa.get("remaining_unnumbered_display_math"),
            "toc_entry_font_sizes": post_qa.get("toc_entry_font_sizes"),
            "toc_section_font_size": post_qa.get("toc_section_font_size"),
            "toc_section_is_bold": post_qa.get("toc_section_is_bold"),
            "toc_sub_font_size": post_qa.get("toc_sub_font_size"),
            "toc_uses_shared_numwidth": post_qa.get("toc_uses_shared_numwidth"),
            "toc_page_width_configured": post_qa.get("toc_page_width_configured"),
            "cover_fields_use_makebox_centering": post_qa.get("cover_fields_use_makebox_centering"),
            "cover_fields_have_underlines": post_qa.get("cover_fields_have_underlines"),
            "longtable_count": post_qa.get("longtable_count"),
            "booktabs_longtable_count": post_qa.get("booktabs_longtable_count"),
            "longtables_missing_caption": post_qa.get("longtables_missing_caption"),
            "longtables_missing_endfoot": post_qa.get("longtables_missing_endfoot"),
            "longtables_missing_continued_caption": post_qa.get("longtables_missing_continued_caption"),
            "longtable_headers_centered": post_qa.get("longtable_headers_centered"),
        },
        "pdf": {
            "attempted": compiler_available,
            "exists": pdf_path.exists() if compiler_available else None,
            "nonempty": pdf_path.stat().st_size > 0 if compiler_available and pdf_path.exists() else None,
        },
        "build": build_summary,
    }


def render_no_cover_case(source: Path, work_root: Path, compiler_available: bool) -> dict[str, object]:
    case_dir = work_root / "no_cover"
    case_dir.mkdir(parents=True)
    copied_source = case_dir / source.name
    shutil.copy2(source, copied_source)

    latex_dir = case_dir / "latex"
    tex = case_dir / "report.tex"
    pdf_path = case_dir / "report.pdf"
    build_cmd = [
        sys.executable,
        str(BUILD),
        str(copied_source),
        "--no-cover",
        "--work-dir",
        str(latex_dir),
        "--tex",
        str(tex),
        "--pdf",
        str(pdf_path),
    ]
    if not compiler_available:
        build_cmd.append("--skip-compile")
    built = run(build_cmd, case_dir)
    if built.returncode != 0:
        return fail("no-cover build failed", {"stdout": built.stdout, "stderr": built.stderr})

    try:
        build_summary = json.loads(built.stdout)
    except json.JSONDecodeError:
        return fail("no-cover build summary is not JSON", {"stdout": built.stdout, "stderr": built.stderr})

    report = load_json(latex_dir / "prepare_report.json")
    tex_text = tex.read_text(encoding="utf-8") if tex.exists() else ""
    cover = report.get("cover", {})

    errors: list[str] = []
    check(tex.exists(), "no-cover TeX output must exist", errors)
    check(isinstance(cover, dict), "no-cover QA must include cover object", errors)
    if isinstance(cover, dict):
        check(cover.get("enabled") is False, "cover.enabled must be false when --no-cover is used", errors)
    check(r"\begin{titlepage}" not in tex_text, "no-cover output must not contain a titlepage", errors)
    if compiler_available:
        check(pdf_path.exists(), "no-cover compiled PDF must exist", errors)
        check(pdf_path.exists() and pdf_path.stat().st_size > 0, "no-cover compiled PDF must be nonempty", errors)
    return {"ok": not errors, "errors": errors, "build": build_summary}


def render_negative_case(
    name: str,
    markdown: str,
    expected_error: str,
    work_root: Path,
    extra_args: list[str] | None = None,
    expect_prepare_failure: bool = True,
) -> dict[str, object]:
    case_dir = work_root / name
    case_dir.mkdir(parents=True)
    source = case_dir / f"{name}.md"
    source.write_text(markdown, encoding="utf-8")

    latex_dir = case_dir / "latex"
    tex = case_dir / "report.tex"
    pdf_path = case_dir / "report.pdf"
    build_cmd = [
        sys.executable,
        str(BUILD),
        str(source),
        "--work-dir",
        str(latex_dir),
        "--course",
        COURSE,
        "--student-name",
        STUDENT_NAME,
        "--student-id",
        STUDENT_ID,
        "--tex",
        str(tex),
        "--pdf",
        str(pdf_path),
        "--skip-compile",
    ]
    if extra_args:
        build_cmd.extend(extra_args)
    built = run(build_cmd, case_dir)

    errors: list[str] = []
    check(built.returncode != 0, "negative case should fail", errors)
    if expect_prepare_failure:
        check("Prepare QA failed" in built.stderr, "missing prepare QA failure message", errors)
    check(expected_error in built.stderr, f"missing expected error: {expected_error}", errors)
    check(not tex.exists(), "negative case should fail before Pandoc emits TeX", errors)
    return {
        "ok": not errors,
        "errors": errors,
        "stdout": built.stdout,
        "stderr": built.stderr,
    }


def render_absolute_logo_case(work_root: Path, compiler_available: bool) -> dict[str, object]:
    case_dir = work_root / "absolute_logo_path"
    case_dir.mkdir(parents=True)
    source = case_dir / "absolute_logo_path.md"
    shutil.copy2(EXAMPLES / "minimal_report.md", source)

    latex_dir = case_dir / "latex"
    tex = case_dir / "report.tex"
    pdf_path = case_dir / "report.pdf"
    build_cmd = [
        sys.executable,
        str(BUILD),
        str(source),
        "--work-dir",
        str(latex_dir),
        "--course",
        COURSE,
        "--student-name",
        STUDENT_NAME,
        "--student-id",
        STUDENT_ID,
        "--logo",
        str(LOCAL_DEFAULT_LOGO.resolve()),
        "--tex",
        str(tex),
        "--pdf",
        str(pdf_path),
    ]
    if not compiler_available:
        build_cmd.append("--skip-compile")
    built = run(build_cmd, case_dir)
    if built.returncode != 0:
        return fail("absolute logo build failed", {"stdout": built.stdout, "stderr": built.stderr})

    report = load_json(latex_dir / "prepare_report.json")
    cover = report.get("cover", {})
    errors: list[str] = []
    check(isinstance(cover, dict), "absolute logo QA must include cover object", errors)
    if isinstance(cover, dict):
        logo_path = str(cover.get("logo_path", ""))
        check(cover.get("logo_exists") is True, "absolute logo copy must exist", errors)
        check(cover.get("logo_inside_project") is True, "absolute logo copy must be inside project", errors)
        check(not Path(logo_path).is_absolute(), "absolute logo must be converted to a relative project path", errors)
    if compiler_available:
        check(pdf_path.exists(), "absolute logo compiled PDF must exist", errors)
        check(pdf_path.exists() and pdf_path.stat().st_size > 0, "absolute logo compiled PDF must be nonempty", errors)
    return {"ok": not errors, "errors": errors}


def render_prepare_absolute_logo_warning(work_root: Path) -> dict[str, object]:
    case_dir = work_root / "prepare_absolute_logo_warning"
    case_dir.mkdir(parents=True)
    source = case_dir / "prepare_absolute_logo_warning.md"
    shutil.copy2(EXAMPLES / "minimal_report.md", source)

    out_dir = case_dir / "latex"
    prepared = run(
        [
            sys.executable,
            str(PREPARE),
            str(source),
            "--out-dir",
            str(out_dir),
            "--course",
            COURSE,
            "--student-name",
            STUDENT_NAME,
            "--student-id",
            STUDENT_ID,
            "--logo",
            str(LOCAL_DEFAULT_LOGO.resolve()),
        ],
        case_dir,
    )
    if prepared.returncode != 0:
        return fail("prepare with absolute logo should warn, not crash", {"stdout": prepared.stdout, "stderr": prepared.stderr})

    report = load_json(out_dir / "prepare_report.json")
    cover = report.get("cover", {})
    warnings = report.get("warnings", [])
    errors: list[str] = []
    check(isinstance(cover, dict), "prepare absolute logo QA must include cover object", errors)
    check(isinstance(warnings, list), "prepare absolute logo warnings must be a list", errors)
    if isinstance(cover, dict):
        check(cover.get("logo_exists") is True, "prepare absolute logo must exist", errors)
        check(cover.get("logo_inside_project") is False, "prepare absolute logo must be marked outside project", errors)
    if isinstance(warnings, list):
        check(
            any("logo 路径不是项目内相对路径" in str(item) for item in warnings),
            "prepare absolute logo must emit a path warning",
            errors,
        )
    return {"ok": not errors, "errors": errors}


def main() -> int:
    required = [BUILD, PREPARE]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print(json.dumps({"ok": False, "error": "required files missing", "missing": missing}, ensure_ascii=False))
        return 1

    sources = [
        EXAMPLES / "minimal_report.md",
        EXAMPLES / "table_report.md",
        EXAMPLES / "citation_report.md",
        EXAMPLES / "no_reference_report.md",
        EXAMPLES / "标准课程报告模板.md",
    ]
    missing_sources = [str(path) for path in sources if not path.exists()]
    if missing_sources:
        print(
            json.dumps(
                {"ok": False, "error": "example files missing", "missing": missing_sources},
                ensure_ascii=False,
            )
        )
        return 1

    if shutil.which("pandoc") is None:
        print(json.dumps({"ok": False, "error": "pandoc not found"}, ensure_ascii=False))
        return 1

    compiler_available = shutil.which("tectonic") is not None or shutil.which("xelatex") is not None
    require_compiler = os.environ.get("MD_COURSE_REPORT_REQUIRE_COMPILER") == "1"
    if require_compiler and not compiler_available:
        print(json.dumps({"ok": False, "error": "compiler required but tectonic/xelatex not found"}, ensure_ascii=False))
        return 1
    with tempfile.TemporaryDirectory(prefix="md-course-report-smoke-") as tmp:
        work_root = Path(tmp)
        cases = {source.name: render_case(source, work_root, compiler_available) for source in sources}
        no_cover_case = render_no_cover_case(EXAMPLES / "minimal_report.md", work_root, compiler_available)
        negative_cases = {
            "table_missing_caption": render_negative_case(
                "table_missing_caption",
                "# 表格缺表题\n\n| A | B |\n|---|---|\n| 1 | 2 |\n",
                "missing adjacent Pandoc captions",
                work_root,
            ),
            "table_caption_blank_line": render_negative_case(
                "table_caption_blank_line",
                "# 表题空行\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n: 路线比较\n",
                "captions are separated by blank lines",
                work_root,
            ),
            "table_manual_number_caption": render_negative_case(
                "table_manual_number_caption",
                "# 手写表号\n\n| A | B |\n|---|---|\n| 1 | 2 |\n: 表 1 路线比较\n",
                "table captions contain manual numbers",
                work_root,
            ),
            "table_colon_prefix_caption": render_negative_case(
                "table_colon_prefix_caption",
                "# 错误表题语法\n\n| A | B |\n|---|---|\n| 1 | 2 |\n表: 路线比较\n",
                "unsupported syntax",
                work_root,
            ),
            "absolute_image_path": render_negative_case(
                "absolute_image_path",
                "# 绝对图片路径\n\n![系统文件](/etc/hosts)\n",
                "absolute, remote, or outside",
                work_root,
            ),
            "missing_logo": render_negative_case(
                "missing_logo",
                "# 缺失 logo\n\n正文。\n",
                "logo file is missing",
                work_root,
                extra_args=["--logo", "assets/missing_logo.png"],
            ),
            "absolute_logo_path": render_absolute_logo_case(work_root, compiler_available),
            "prepare_absolute_logo_warning": render_prepare_absolute_logo_warning(work_root),
            "outside_work_dir": render_negative_case(
                "outside_work_dir",
                "# 项目外工作目录\n\n正文。\n",
                "--work-dir must be inside",
                work_root,
                extra_args=["--work-dir", str(work_root / "outside_latex")],
                expect_prepare_failure=False,
            ),
            "skip_compile_output_pdf": render_negative_case(
                "skip_compile_output_pdf",
                "# 跳过编译\n\n正文。\n",
                "--output-pdf requires compilation",
                work_root,
                extra_args=["--output-pdf", str(work_root / "skip_compile_output_pdf" / "out.pdf")],
                expect_prepare_failure=False,
            ),
            "bad_pdf_suffix": render_negative_case(
                "bad_pdf_suffix",
                "# 错误 PDF 后缀\n\n正文。\n",
                "--pdf must end with .pdf",
                work_root,
                extra_args=["--pdf", str(work_root / "bad_pdf_suffix" / "out.md")],
                expect_prepare_failure=False,
            ),
            "tex_overwrites_source": render_negative_case(
                "tex_overwrites_source",
                "# 输出覆盖源文件\n\n正文。\n",
                "--tex must end with .tex",
                work_root,
                extra_args=["--tex", str(work_root / "tex_overwrites_source" / "tex_overwrites_source.md")],
                expect_prepare_failure=False,
            ),
            "slide_draft_input": render_negative_case(
                "slide_draft_input",
                "# 逐页内容稿\n\n"
                "## 第 1 页｜标题\n\n屏幕：一句话。\n\n讲：讲稿。\n\n图：图片提示。\n\n"
                "## 第 2 页｜标题\n\n屏幕：一句话。\n\n讲：讲稿。\n\n图：图片提示。\n\n"
                "## 第 3 页｜标题\n\n屏幕：一句话。\n\n讲：讲稿。\n\n图：图片提示。\n",
                "page-by-page lecture notes or a slide draft",
                work_root,
            ),
        }

    ok = (
        all(bool(result.get("ok")) for result in cases.values())
        and bool(no_cover_case.get("ok"))
        and all(bool(result.get("ok")) for result in negative_cases.values())
    )
    summary = {
        "ok": ok,
        "compiler_available": compiler_available,
        "cases": cases,
        "no_cover_case": no_cover_case,
        "negative_cases": negative_cases,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
