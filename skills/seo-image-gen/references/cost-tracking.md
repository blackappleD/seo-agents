# 成本跟踪参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

> 当用户询问成本或批量操作之前按需加载此内容。

## 定价表

| 模型 | 分辨率 | 成本/图像 | 备注 |
|--------|---------|------------|--------|
| 3.1 Flash | 512 | $0.020 | 快速草稿 |
| 3.1 Flash | 1K | $0.039 | 标准，默认 |
| 3.1 Flash | 2K | $0.078 | 高质量资产 |
| 3.1 Flash | 4K | $0.156 | 打印或 hero image |
| 2.5 Flash | 512 | $0.020 | 草稿后备 |
| 2.5 Flash | 1K | $0.039 | 标准后备 |
| Batch API | Any | 上表 50% | 异步，更高延迟 |

定价为近似值，基于每个图像约 1,290 个输出标记。
研究表明实际成本可能约为 0.067 美元/img。在 https://ai.google.dev/gemini-api/docs/pricing 处验证

## 免费套餐限制

- 每分钟约 10 个请求 (RPM)
- 每天约 500 个请求 (RPD)
- 根据 Google Cloud 项目，重置太平洋午夜

## 成本跟踪器命令

```bash
# Log a generation
cost_tracker.py log --model gemini-3.1-flash-image-preview --resolution 1K --prompt "coffee shop hero"

# View summary (total + last 7 days)
cost_tracker.py summary

# Today's usage
cost_tracker.py today

# Estimate before batch
cost_tracker.py estimate --model gemini-3.1-flash-image-preview --resolution 1K --count 10

# Reset ledger
cost_tracker.py reset --confirm
```

## 存储

账本存储在 `~/.banana/costs.json`。首次使用时自动创建。

## 本项目适配边界

- 图片生成、模型调用和后处理都可能依赖外部模型或本地工具；未配置时标注“未配置”。
- 生成商业图片时要记录 prompt、模型、成本、用途、版权/品牌约束和是否需要人工复核。
