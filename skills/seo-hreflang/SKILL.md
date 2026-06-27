---
name: seo-hreflang
description: >
  hreflang / 国际化 SEO 检查。检测 hreflang 标签、语言地区格式、自引用、
  x-default、canonical host 一致性、内容 parity 与机器翻译 QA 背景。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Hreflang

运行：

```bash
seo-agents hreflang <url> --json
```

## 当前检查

- 未发现 hreflang 时输出 Info，除非站点确实有多语言/多地区版本。
- 校验 `en`、`en-US`、`zh-CN`、`x-default` 等格式。
- 有 hreflang 时要求自引用。
- 建议添加 `x-default` 到默认落地页或语言选择页。
- 当 canonical 与 hreflang URL host 不一致时提示跨域策略风险。
- return tags、内容 parity 和翻译质量需要抓取 alternates 或人工材料；当前 CLI 只做页面级基础检测。

## 按需引用

- `references/locale-formats.md`：语言地区代码格式。
- `references/content-parity.md`：多语言内容等价性检查。
- `references/cultural-profiles.md`：地区化内容差异。
- `references/machine-translation-qa.md`：机器翻译 QA 清单。

不要自动生成大规模 hreflang 文件；当前 CLI 只做页面级检测。

## 完成标准

- 输出 hreflang 数量、无效代码、自引用、x-default、canonical host 风险和样例。
- 对国际化站点要说明语言、地区、货币、联系方式、法律页和内容 parity 的人工检查点。
- 如用户要生成标签，基于已确认 URL 映射生成片段，并标注需要在每个 alternate 上互相返回。

## 错误处理

| 场景 | 处理 |
|---|---|
| 没有 hreflang | 如果站点单语言，作为 Info；若用户确认多语言，则给实现方案。 |
| 代码格式异常 | 指向 ISO 639-1 / ISO 3166-1 Alpha-2 或 `x-default`。 |
| canonical 与 alternate 冲突 | 优先建议 canonical/hreflang 架构一致化。 |
| 用户提供 URL 映射不完整 | 不生成完整网络，先列缺失语言/地区。 |
