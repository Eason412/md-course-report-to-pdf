local title_seen = false

local function normalize(text)
  return text:gsub("%s+", ""):gsub("：$", ""):gsub(":$", "")
end

local function metadata_title()
  if PANDOC_STATE and PANDOC_STATE.meta and PANDOC_STATE.meta.title then
    return normalize(pandoc.utils.stringify(PANDOC_STATE.meta.title))
  end
  return ""
end

function Header(el)
  local heading_text = normalize(pandoc.utils.stringify(el.content))
  local heading_key = heading_text:lower()

  if heading_text == "参考文献" or heading_key == "references" or heading_key == "reference" then
    return pandoc.RawBlock(
      "latex",
      "% COURSE_REPORT_REFERENCES_BEGIN\n\\phantomsection\n\\section*{\\centering\\zihao{3}\\songti\\bfseries 参考文献}\n\\addcontentsline{toc}{section}{参考文献}"
    )
  end

  if not title_seen and el.level == 1 then
    title_seen = true
    if heading_text == metadata_title() then
      return {}
    end
  end

  if el.level > 1 then
    el.level = el.level - 1
  end

  return el
end
