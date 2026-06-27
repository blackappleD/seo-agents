---
name: seo-images
description: >
  图片 SEO 检查。识别缺失 alt text、缺少 width/height 的 CLS 风险、疑似
  LCP 图片被 lazy-load，以及 srcset/sizes responsive image 信号。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Images

运行：

```bash
seo-agents images <url> --json
seo-agents images <url> --render-mode auto --json
```

## 检查范围

- 内容图片缺少 `alt`。
- 图片缺少 `width` 或 `height`，可能造成 CLS。
- 文档第一张图片带 `loading="lazy"`，作为疑似 LCP 图片延迟风险。
- 统计 `srcset` / `sizes` responsive image 信号。

## 建议规则

- 内容图片使用简洁、描述性的 alt；装饰图片可以使用空 alt。
- 首屏 hero/LCP 图片不要 lazy-load，可考虑 `fetchpriority="high"` 或 preload。
- 宽高属性和 CSS `aspect-ratio` 用于稳定布局。
- 不要承诺压缩、转码或批量改图已实现；当前 CLI 只做页面级检查。

输出中的 `images` 保留每张图片的提取字段，报告引用时优先使用 `findings[*].evidence.examples`。

## 来源能力适配

原始参考项目里的 image SERP、文件转码、IPTC/XMP 元数据注入和批量优化，在本项目里没有 CLI 实现。处理相关请求时：

- 页面图片问题用 `seo-agents images <url> --json`。
- 文件名、alt、caption、schema `image`、Open Graph image 可以给出人工建议。
- 压缩、WebP/AVIF 转换、metadata 注入只能作为后续扩展或用户另行确认的本地文件处理任务。
- AI 生成图片的 `DigitalSourceType` / IPTC 标签可作为电商和图片合规提醒，不声称已自动写入。

## 完成标准

- 输出缺 alt、缺尺寸、疑似 LCP lazy-load、responsive image 信号和样例 URL。
- 给每类图片分配建议：内容图、装饰图、hero/LCP、商品图、logo/icon、social image。
- 对影响排序：alt 和页面上下文优先，其次 filename、尺寸稳定、压缩和 metadata。

## 错误处理

| 场景 | 处理 |
|---|---|
| 页面无 `<img>` | 提示可能使用 CSS background 或 JS 图片，并建议渲染复核。 |
| 图片在 CDN/登录后 | 只报告 markup 中可见字段，不猜测文件大小或格式。 |
| 用户要求批量优化本地图片 | 说明当前无 `seo-agents images optimize`，需单独确认工具链和输出目录。 |
