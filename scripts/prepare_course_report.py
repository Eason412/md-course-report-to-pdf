#!/usr/bin/env python3
"""Prepare a Chinese Markdown course report for the ctexart template."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUM_PREFIX_RE = re.compile(r"^(#{2,6})\s+(?:\d+(?:\.\d+)+\s+|\d+(?:\.\d+)*[.、]\s*)(.+?)\s*$")
LEADING_NUMBER_RE = re.compile(r"^(?:\d+(?:\.\d+)+\s+|\d+(?:\.\d+)*[.、]\s*)")
KEYWORDS_ZH_RE = re.compile(r"^\s*(?:\*\*)?\s*关键词\s*(?:\*\*)?\s*[：:]\s*(.+?)\s*$", re.I)
KEYWORDS_EN_RE = re.compile(r"^\s*(?:\*\*)?\s*Keywords\s*(?:\*\*)?\s*[：:]\s*(.+?)\s*$", re.I)
PIPE_TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
CITATION_RE = re.compile(r"(?<!\{)[\[［]([\d,\-\s，、–—]+)[\]］]")
REFERENCE_LABEL_RE = re.compile(r"(?m)^\s*(?:[\[［](\d+)[\]］]|(\d+)[.、])\s+")
INVALID_TABLE_CAPTION_RE = re.compile(r"^\s*(?:表|图|Table|Figure)\s*[：:]\s+\S+", re.I)
LINK_DEFINITION_RE = re.compile(r"^\s*\[[^\]]+\]:")
SLIDE_PAGE_HEADING_RE = re.compile(r"^##\s*第\s*\d+\s*页\s*[｜|:：]")
SLIDE_FIELD_RE = re.compile(r"^(?:屏幕|讲|图|手工反应式)\s*[：:]")


def normalize_heading(text: str) -> str:
    text = re.sub(r"[*_`#]", "", text)
    text = LEADING_NUMBER_RE.sub("", text)
    return re.sub(r"\s+", "", text).strip("：:")


def clean_keyword_value(value: str) -> str:
    return value.strip().strip("*").strip()


def is_url_path(path: str) -> bool:
    parsed = urlparse(path)
    return parsed.scheme in {"http", "https"}


def resolve_project_asset(path: str, source_dir: Path, allow_absolute: bool = False) -> tuple[str, bool, bool]:
    cleaned = path.strip().strip("<>")
    if not cleaned or is_url_path(cleaned):
        return cleaned, False, False
    candidate = Path(cleaned)
    if candidate.is_absolute():
        return cleaned, candidate.exists(), allow_absolute
    resolved = candidate if candidate.is_absolute() else source_dir / candidate
    try:
        resolved_path = resolved.resolve()
        inside_project = resolved_path.relative_to(source_dir.resolve()) is not None
    except ValueError:
        inside_project = False
    return cleaned, resolved.exists(), inside_project


def is_reference_heading(line: str) -> bool:
    match = HEADING_RE.match(line)
    if not match:
        return False
    kind = normalize_heading(match.group(2)).lower()
    return kind in {"参考文献", "references", "reference"}


def protected_line_indexes(lines: list[str]) -> set[int]:
    protected: set[int] = set()
    in_fence = False
    fence_marker = ""
    in_html_code = False
    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        lowered = stripped.lower()
        if in_html_code:
            protected.add(idx)
            if "</pre>" in lowered or "</code>" in lowered:
                in_html_code = False
            continue
        if lowered.startswith("<pre") or lowered.startswith("<code"):
            protected.add(idx)
            if "</pre>" not in lowered and "</code>" not in lowered:
                in_html_code = True
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            protected.add(idx)
            if in_fence and marker == fence_marker:
                in_fence = False
                fence_marker = ""
            elif not in_fence:
                in_fence = True
                fence_marker = marker
            continue
        if in_fence or line.startswith("    ") or line.startswith("\t"):
            protected.add(idx)
    return protected


def extract_reference_numbers(text: str) -> list[int]:
    numbers: set[int] = set()
    lines = text.splitlines()
    protected = protected_line_indexes(lines)
    for idx, line in enumerate(lines):
        if idx in protected or LINK_DEFINITION_RE.match(line):
            continue
        match = REFERENCE_LABEL_RE.match(line)
        if match:
            number = match.group(1) or match.group(2)
            if number:
                numbers.add(int(number))
    return sorted(numbers)


def split_reference_section(body: str) -> tuple[str, str]:
    lines = body.splitlines()
    protected = protected_line_indexes(lines)
    candidates = [idx for idx, line in enumerate(lines) if idx not in protected and is_reference_heading(line)]
    for idx in reversed(candidates):
        tail = "\n".join(lines[idx + 1 :])
        if extract_reference_numbers(tail):
            return "\n".join(lines[:idx]), "\n".join(lines[idx:])
    for idx in reversed(candidates):
        if idx >= max(0, int(len(lines) * 0.75)):
            return "\n".join(lines[:idx]), "\n".join(lines[idx:])
    return body, ""


def detect_slide_draft(lines: list[str]) -> dict[str, object]:
    """Detect page-by-page PPT drafts that are not course-report sources."""
    page_heading_count = sum(1 for line in lines if SLIDE_PAGE_HEADING_RE.match(line.strip()))
    slide_field_count = sum(1 for line in lines if SLIDE_FIELD_RE.match(line.strip()))
    text_fence_count = sum(1 for line in lines if line.strip() == "```text")
    detected = page_heading_count >= 3 and slide_field_count >= 6
    return {
        "detected": detected,
        "page_heading_count": page_heading_count,
        "slide_field_count": slide_field_count,
        "text_fence_count": text_fence_count,
    }


def expand_numeric_markers(markers: list[str]) -> list[int]:
    numbers: set[int] = set()
    for marker in markers:
        normalized = marker.replace("，", ",").replace("、", ",").replace("–", "-").replace("—", "-")
        for part in re.split(r"\s*,\s*", normalized):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                start_text, end_text = [item.strip() for item in part.split("-", 1)]
                if start_text.isdigit() and end_text.isdigit():
                    start, end = int(start_text), int(end_text)
                    if 0 < start <= end <= start + 50:
                        numbers.update(range(start, end + 1))
                continue
            if part.isdigit():
                numbers.add(int(part))
    return sorted(numbers)


def format_citation_marker(numbers: list[int]) -> str:
    if not numbers:
        return ""
    unique_numbers = sorted(set(numbers))
    ranges: list[str] = []
    start = prev = unique_numbers[0]
    for number in unique_numbers[1:]:
        if number == prev + 1:
            prev = number
            continue
        ranges.append(f"{start}-{prev}" if start != prev else str(start))
        start = prev = number
    ranges.append(f"{start}-{prev}" if start != prev else str(start))
    return "[" + ",".join(ranges) + "]"


def pipe_cell_count(line: str) -> int:
    if "|" not in line:
        return 0
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells = [cell.strip() for cell in stripped.split("|")]
    return len(cells) if len(cells) >= 2 else 0


def is_pipe_row(line: str, expected_cells: int | None = None) -> bool:
    count = pipe_cell_count(line)
    if count < 2:
        return False
    return expected_cells is None or count == expected_cells


def is_pipe_separator(line: str, expected_cells: int | None = None) -> bool:
    if not PIPE_TABLE_SEPARATOR_RE.match(line):
        return False
    return is_pipe_row(line, expected_cells)


def find_pipe_tables(lines: list[str], protected: set[int] | None = None) -> list[dict[str, object]]:
    protected = protected or set()
    tables: list[dict[str, object]] = []
    idx = 1
    while idx < len(lines):
        if idx in protected or not is_pipe_separator(lines[idx]):
            idx += 1
            continue
        column_count = pipe_cell_count(lines[idx])
        header_idx = idx - 1
        if header_idx < 0 or header_idx in protected or not is_pipe_row(lines[header_idx], column_count):
            idx += 1
            continue
        end = idx
        while end + 1 < len(lines) and end + 1 not in protected and is_pipe_row(lines[end + 1], column_count):
            end += 1
        tables.append(
            {
                "start_line": header_idx + 1,
                "end_line": end + 1,
                "separator_line": idx + 1,
                "column_count": column_count,
            }
        )
        idx = end + 1
    return tables


def build_table_line_set(lines: list[str]) -> set[int]:
    protected = protected_line_indexes(lines)
    table_lines: set[int] = set()
    for table in find_pipe_tables(lines, protected):
        start = int(table["start_line"]) - 1
        end = int(table["end_line"]) - 1
        table_lines.update(range(start, end + 1))
        caption_idx = end + 1
        if caption_idx < len(lines) and (is_table_caption(lines[caption_idx]) or INVALID_TABLE_CAPTION_RE.match(lines[caption_idx])):
            table_lines.add(caption_idx)
    return table_lines


def mask_span(match: re.Match[str]) -> str:
    return " " * (match.end() - match.start())


def mask_inline_context(line: str) -> str:
    masked = re.sub(r"`[^`]*`", mask_span, line)
    masked = re.sub(r"!?\[[^\]]*\]\([^)]+\)", mask_span, masked)
    def mask_reference_link(match: re.Match[str]) -> str:
        label = match.group(1).strip()
        if re.fullmatch(r"[\d,\-\s，、–—]+", label):
            return match.group(0)
        return " " * (match.end() - match.start())

    masked = re.sub(r"!?\[([^\]]+)\]\[[^\]]*\]", mask_reference_link, masked)
    return masked


def replace_citations_in_line(line: str, replace_match) -> str:
    if LINK_DEFINITION_RE.match(line):
        return line
    masked = mask_inline_context(line)
    pieces: list[str] = []
    pos = 0
    for match in CITATION_RE.finditer(masked):
        pieces.append(line[pos : match.start()])
        original = re.match(CITATION_RE, line[match.start() : match.end()])
        if original:
            pieces.append(replace_match(original))
        else:
            pieces.append(line[match.start() : match.end()])
        pos = match.end()
    pieces.append(line[pos:])
    return "".join(pieces)


def collect_body_citations(body_before_refs: str) -> list[int]:
    lines = body_before_refs.splitlines()
    protected = protected_line_indexes(lines)
    table_lines = build_table_line_set(lines)
    markers: list[str] = []
    for idx, line in enumerate(lines):
        if idx in protected or idx in table_lines or LINK_DEFINITION_RE.match(line):
            continue
        markers.extend(CITATION_RE.findall(mask_inline_context(line)))
    return expand_numeric_markers(markers)


def dedupe_repeated_citations(body: str) -> tuple[str, dict[str, object]]:
    body_before_refs, reference_section = split_reference_section(body)
    lines = body_before_refs.splitlines()
    protected = protected_line_indexes(lines)
    table_lines = build_table_line_set(lines)
    seen: set[int] = set()
    events: list[dict[str, object]] = []
    removed_marker_count = 0
    rewritten_marker_count = 0
    normalized_marker_count = 0
    removed_numbers: list[int] = []

    def repl(match: re.Match[str], line_number: int) -> str:
        nonlocal removed_marker_count, rewritten_marker_count, normalized_marker_count
        marker = match.group(0)
        numbers = expand_numeric_markers([match.group(1)])
        if not numbers:
            return marker
        new_numbers = [number for number in numbers if number not in seen]
        repeated_numbers = [number for number in numbers if number in seen]
        seen.update(numbers)
        if not repeated_numbers:
            return marker

        removed_numbers.extend(repeated_numbers)
        events.append(
            {
                "line": line_number,
                "marker": marker,
                "removed_numbers": repeated_numbers,
                "kept_numbers": new_numbers,
            }
        )
        if not new_numbers:
            removed_marker_count += 1
            return ""
        rewritten_marker_count += 1
        return format_citation_marker(new_numbers)

    out_lines: list[str] = []
    for idx, line in enumerate(lines):
        if idx in protected or idx in table_lines or LINK_DEFINITION_RE.match(line):
            out_lines.append(line)
            continue

        def line_repl(match: re.Match[str]) -> str:
            nonlocal normalized_marker_count
            marker = match.group(0)
            numbers = expand_numeric_markers([match.group(1)])
            normalized = format_citation_marker(numbers)
            replaced = repl(match, idx + 1)
            if replaced == marker and normalized and marker != normalized:
                normalized_marker_count += 1
                return normalized
            return replaced

        replaced_line = replace_citations_in_line(line, line_repl)
        if replaced_line != line:
            replaced_line = re.sub(r"[ \t]+([，。；：、,.!?;:])", r"\1", replaced_line)
            replaced_line = re.sub(r"[ \t]{2,}", " ", replaced_line)
        out_lines.append(replaced_line)

    deduped_body = "\n".join(out_lines)
    if reference_section:
        deduped_body = deduped_body.rstrip() + "\n\n" + reference_section.lstrip()

    return deduped_body, {
        "removed_marker_count": removed_marker_count,
        "rewritten_marker_count": rewritten_marker_count,
        "normalized_marker_count": normalized_marker_count,
        "removed_numbers": removed_numbers,
        "events": events,
    }


def strip_outer_title_marks(text: str) -> str:
    text = text.strip()
    if text.startswith("《") and text.endswith("》"):
        return text[1:-1].strip()
    return text


def yaml_block(key: str, value: str) -> str:
    value = value.rstrip()
    if not value:
        return f"{key}: ''\n"
    lines = value.splitlines()
    indented = "\n".join(f"  {line}" if line else "" for line in lines)
    return f"{key}: |-\n{indented}\n"


def extract_abstract(lines: list[str]) -> tuple[list[str], dict[str, str], list[str]]:
    metadata: dict[str, str] = {}
    warnings: list[str] = []
    output: list[str] = []
    i = 0

    while i < len(lines):
        match = HEADING_RE.match(lines[i])
        if not match:
            output.append(lines[i])
            i += 1
            continue

        level, heading = match.groups()
        kind = normalize_heading(heading)
        is_zh_abs = level == "##" and kind == "摘要"
        is_en_abs = level == "##" and kind.lower() == "abstract"
        if not (is_zh_abs or is_en_abs):
            output.append(lines[i])
            i += 1
            continue

        section_lines: list[str] = []
        i += 1
        while i < len(lines):
            next_heading = HEADING_RE.match(lines[i])
            if next_heading and next_heading.group(1) == "##":
                break
            section_lines.append(lines[i])
            i += 1

        body_lines: list[str] = []
        for line in section_lines:
            if line.strip() in {r"\newpage", r"\clearpage"}:
                continue
            zh_kw = KEYWORDS_ZH_RE.match(line)
            en_kw = KEYWORDS_EN_RE.match(line)
            if zh_kw:
                metadata["keywords_zh"] = clean_keyword_value(zh_kw.group(1))
                continue
            if en_kw:
                metadata["keywords_en"] = clean_keyword_value(en_kw.group(1))
                continue
            body_lines.append(line)

        body = "\n".join(body_lines).strip()
        if is_zh_abs:
            metadata["abstract_zh"] = body
        else:
            metadata["abstract_en"] = body

    if "abstract_zh" not in metadata:
        warnings.append("未找到中文摘要，前置摘要页将为空。")
    if "abstract_en" not in metadata:
        warnings.append("未找到英文 Abstract，英文摘要页将为空。")

    return output, metadata, warnings


def prepare_body(lines: list[str]) -> tuple[list[str], str | None, list[str]]:
    title: str | None = None
    output: list[str] = []
    warnings: list[str] = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match and match.group(1) == "#" and title is None:
            title = strip_outer_title_marks(match.group(2))
            continue

        num_match = NUM_PREFIX_RE.match(line)
        if num_match:
            output.append(f"{num_match.group(1)} {num_match.group(2).strip()}")
            continue

        output.append(line)

    if title is None:
        warnings.append("未找到一级标题，将使用输入文件名作为封面题目。")
    return output, title, warnings


def keyword_count(value: str) -> int:
    if not value:
        return 0
    parts = re.split(r"[；;,，]", value)
    return len([p for p in parts if p.strip()])


def is_table_caption(line: str) -> bool:
    return bool(re.match(r"^\s*:\s+\S+", line))


def table_caption_has_manual_number(line: str) -> bool:
    return bool(re.match(r"^\s*(?::|Table:)\s*(表|Table)?\s*\d+(?:\.\d+)?", line, re.I))


def scan_pipe_tables(lines: list[str]) -> dict[str, object]:
    tables = []
    manual_captions = []
    separated_captions = []
    invalid_captions = []
    protected = protected_line_indexes(lines)
    for found in find_pipe_tables(lines, protected):
        start = int(found["start_line"]) - 1
        end = int(found["end_line"]) - 1
        caption_idx = end + 1
        caption = lines[caption_idx].strip() if caption_idx < len(lines) else ""
        has_caption = is_table_caption(caption)
        if caption and INVALID_TABLE_CAPTION_RE.match(caption):
            invalid_captions.append(caption)
        if not has_caption:
            loose_idx = caption_idx
            blank_lines = 0
            while loose_idx < len(lines) and not lines[loose_idx].strip():
                blank_lines += 1
                loose_idx += 1
            if blank_lines and loose_idx < len(lines) and is_table_caption(lines[loose_idx].strip()):
                separated_captions.append(
                    {
                        "table_start_line": start + 1,
                        "caption_line": loose_idx + 1,
                        "blank_lines_before_caption": blank_lines,
                    }
                )
        if has_caption and table_caption_has_manual_number(caption):
            manual_captions.append(caption)
        tables.append(
            {
                "start_line": start + 1,
                "end_line": end + 1,
                "caption_line": caption_idx + 1 if has_caption else None,
                "caption": caption if has_caption else "",
                "column_count": found["column_count"],
            }
        )
    return {
        "pipe_table_count": len(tables),
        "table_caption_count": sum(1 for table in tables if table["caption"]),
        "tables_without_adjacent_caption": [
            {"start_line": table["start_line"], "end_line": table["end_line"]}
            for table in tables
            if not table["caption"]
        ],
        "invalid_table_captions": invalid_captions,
        "table_captions_with_manual_numbers": manual_captions,
        "table_captions_separated_by_blank_line": separated_captions,
        "tables": tables,
    }


def scan_body(body: str, source_dir: Path) -> dict[str, object]:
    lines = body.splitlines()
    markdown_images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)
    html_images = re.findall(r"<img\b[^>]*\bsrc=['\"]([^'\"]+)['\"]", body, flags=re.I)
    images = markdown_images + html_images
    image_items = []
    for image in images:
        path, exists, inside_project = resolve_project_asset(image, source_dir)
        image_items.append({"path": path, "exists": exists, "inside_project": inside_project})

    captions_with_numbers = [
        caption
        for caption in re.findall(r"!\[([^\]]+)\]\([^)]+\)", body)
        if re.match(r"\s*[图表]\s*\d+", caption)
    ]
    table_qa = scan_pipe_tables(lines)
    body_before_refs, reference_section = split_reference_section(body)
    citations = collect_body_citations(body_before_refs)
    references = extract_reference_numbers(reference_section)

    return {
        "image_count": len(image_items),
        "images": image_items,
        "markdown_image_count": len(markdown_images),
        "html_image_count": len(html_images),
        "missing_images": [item["path"] for item in image_items if not item["exists"]],
        "unsafe_image_paths": [item["path"] for item in image_items if not item["inside_project"]],
        "captions_with_manual_numbers": captions_with_numbers,
        **table_qa,
        "references_section_found": bool(reference_section),
        "citation_numbers": citations,
        "reference_numbers": references,
        "missing_reference_entries": [n for n in citations if n not in references],
        "unused_reference_entries": [n for n in references if n not in citations],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("latex"))
    parser.add_argument("--course", default="")
    parser.add_argument("--student-name", default="")
    parser.add_argument("--student-id", default="")
    parser.add_argument("--logo", default="")
    parser.add_argument("--no-cover", action="store_true")
    parser.add_argument("--allow-slide-draft", action="store_true")
    args = parser.parse_args()

    source = args.source
    lines = source.read_text(encoding="utf-8").splitlines()
    slide_draft = detect_slide_draft(lines)
    no_abs_lines, metadata, warnings = extract_abstract(lines)
    body_lines, title, body_warnings = prepare_body(no_abs_lines)
    warnings.extend(body_warnings)

    if not title:
        title = source.stem

    metadata.update(
        {
            "title": title,
            "course": args.course,
            "studentname": args.student_name,
            "studentid": args.student_id,
            "logo": args.logo,
            "cover_disabled": "yes" if args.no_cover else "",
        }
    )

    for key in ("keywords_zh", "keywords_en"):
        count = keyword_count(metadata.get(key, ""))
        if count > 5:
            warnings.append(f"{key} 有 {count} 个关键词，超过最多 5 个的默认限制。")

    prepared_body = "\n".join(body_lines).strip() + "\n"
    prepared_body, citation_dedup = dedupe_repeated_citations(prepared_body)
    prepared_body = prepared_body.strip() + "\n"
    qa = scan_body(prepared_body, source.parent)
    qa["citation_dedup"] = citation_dedup
    qa["probable_slide_draft"] = {
        **slide_draft,
        "allowed": args.allow_slide_draft,
    }
    if slide_draft["detected"] and not args.allow_slide_draft:
        warnings.append(
            "输入看起来是逐页讲稿或幻灯片内容稿（如“第 X 页”“屏幕：”“讲：”“图：”），"
            "不是正式课程报告 Markdown；请先改写成摘要、章节正文和参考文献结构，"
            "或确认后使用 --allow-slide-draft 强制转换。"
        )
    if qa["missing_images"]:
        warnings.append("存在缺失图片：" + ", ".join(qa["missing_images"]))
    if qa["captions_with_manual_numbers"]:
        warnings.append("图片或表格 caption 含手写编号，可能与 LaTeX 自动编号重复。")
    if qa["missing_reference_entries"]:
        warnings.append("正文引用缺少参考文献条目：" + ", ".join(map(str, qa["missing_reference_entries"])))
    if qa["unused_reference_entries"]:
        warnings.append("存在未被正文引用的参考文献条目，请确认是否保留：" + ", ".join(map(str, qa["unused_reference_entries"])))
    if qa["tables_without_adjacent_caption"]:
        warnings.append("存在 Markdown 表格但未发现紧邻表题；三线表可能无法自动编号。")
    if qa["invalid_table_captions"]:
        warnings.append("存在不支持的表题写法；请使用紧邻表格的 ': 标题'，不要使用 '表:' 或 'Table:'。")
    if qa["table_captions_separated_by_blank_line"]:
        warnings.append("表题与 Markdown 表格之间存在空行；Pandoc 可能不会把它识别为表题。")
    if qa["table_captions_with_manual_numbers"]:
        warnings.append("表题含手写编号，可能与 LaTeX 自动编号重复。")
    logo_path, logo_exists, logo_inside_project = (
        resolve_project_asset(args.logo, source.parent, allow_absolute=True)
        if args.logo
        else ("", False, False)
    )
    if args.logo and not logo_exists:
        warnings.append(f"logo 文件不存在：{args.logo}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    body_path = args.out_dir / "report_body.md"
    metadata_path = args.out_dir / "metadata.yaml"
    report_path = args.out_dir / "prepare_report.json"

    body_path.write_text(prepared_body, encoding="utf-8")
    metadata_text = "---\n" + "".join(yaml_block(k, metadata.get(k, "")) for k in sorted(metadata)) + "---\n"
    metadata_path.write_text(metadata_text, encoding="utf-8")
    report_path.write_text(
        json.dumps(
            {
                "body": str(body_path),
                "metadata": str(metadata_path),
                "title": title,
                "cover": {
                    "enabled": not args.no_cover,
                    "course": args.course,
                    "studentname": args.student_name,
                    "studentid": args.student_id,
                    "logo_path": args.logo,
                    "logo_exists": logo_exists,
                    "logo_inside_project": logo_inside_project,
                },
                "qa": qa,
                "warnings": warnings,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "body": str(body_path),
                "metadata": str(metadata_path),
                "report": str(report_path),
                "warning_count": len(warnings),
                "warnings": warnings,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
