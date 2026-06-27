---
name: seo-image-gen
description: >
  SEO 图片生成规划 playbook。用于规划 OG 图、文章配图、商品图、实体图和
  AI image prompt；当前无 `seo-agents image-gen` CLI，也不直接调用外部生图 API。
user-invocable: true
argument-hint: "<use-case> <description>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Image Gen

当前保留为 Agent playbook，尚无 `seo-agents image-gen` CLI。

## 推荐流程

1. 明确图片用途：OG/social、文章首图、步骤图、商品图、local 实景、schema image。
2. 从页面运行 `seo-agents images/page/content <url> --json` 获取已有图片和内容信号。
3. 输出 prompt、尺寸、文件名、alt text、caption、结构化数据 image 字段建议。
4. 标注生成图片需要人工审核事实准确性、品牌一致性和版权风险。
5. 不要声称 Gemini、MCP 或后处理脚本已接入当前 CLI。

## 用途预设

- OG/social preview：16:9，适合 1200x630，文本留白清晰。
- Blog hero：16:9 或 4:3，强调主题和情绪，但避免 stock-like。
- Product photo：4:3 或 1:1，白底/场景图需和真实商品一致。
- Infographic：2:3，适合流程、数据和对比。
- Schema image：4:3 或 16:9，必须能代表页面实体。
- Local image：真实门店/团队/服务场景优先；AI 图必须标注不可替代实拍证据。

## 输出结构

- Creative brief：受众、用途、品牌语气、不可出现元素。
- Prompt：主体、环境、构图、风格、光线、文字限制、负面约束。
- SEO package：filename、alt、caption、OG/Twitter image、schema `image` 建议。
- QA：事实准确性、版权/商标、可访问性、压缩尺寸和人工审核项。

## 可结合命令

```bash
seo-agents images <url> --json
seo-agents page <url> --json
```

## 按需引用

- `references/seo-image-presets.md`
- `references/prompt-engineering.md`
- `references/post-processing.md`
- `references/cost-tracking.md`
- `references/gemini-models.md` 和 `references/mcp-tools.md` 仅作未来接入背景。

## 完成标准

- 不直接调用外部生图 API；只输出可用于生图工具或设计师的 brief/prompt。
- prompt 必须和 SEO 目的绑定，避免只追求好看。
- 对商品、医疗、法律、本地服务等高信任场景，要求人工核验或优先使用真实素材。

## 错误处理

| 场景 | 处理 |
|---|---|
| 用户要求直接生成图片 | 说明当前 `seo-agents image-gen` CLI 未实现；如当前 harness 有生图能力，需另按用户明确需求处理。 |
| 品牌资料不足 | 输出通用 prompt 并列出需要的品牌色、logo、禁用词和风格参考。 |
| 涉及真实商品/地点 | 标注必须人工确认外观和版权。 |
