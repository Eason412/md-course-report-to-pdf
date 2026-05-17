# 引用解析回归报告

## 摘要

本示例用于检查中文标点引用、重复引用去重、代码块保护和 Markdown 链接保护。

关键词：引用；参考文献；回归测试

## Abstract

This sample checks citation normalization, deduplication, protected code blocks, and Markdown links.

Keywords: citation; references; regression

## 引用边界

正文首次引用使用中文标点［1，2］，后续只应保留尚未出现过的文献[1、3]。

再次出现的范围引用应被删除[1–3]，但 Markdown 链接 [1](https://example.com) 不应被当作引用处理。

```text
代码块里的伪引用[4]不应进入正文引用统计。

## 参考文献

[4] Fake reference in code block.

| A | B |
|---|---|
| 1 | 2 |
```

## 参考文献

[1] International Energy Agency. The role of e-fuels in decarbonising transport. 2023.

[2] IPCC. Climate Change 2022: Mitigation of Climate Change. Cambridge University Press, 2022.

[3] International Maritime Organization. 2023 IMO Strategy on Reduction of GHG Emissions from Ships. 2023.
