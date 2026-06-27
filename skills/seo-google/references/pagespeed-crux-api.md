# PageSpeed Insights v5 + CrUX API 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 目录
1.[PageSpeed Insights v5](#pagespeed-insights-v5)
2.[CrUX API (Daily)](#crux-api-daily)
3.[CrUX History API (Weekly)](#crux-history-api-weekly)
4.[Core Web Vitals Thresholds](#core-web-vitals-thresholds)

---

## PageSpeed Insights v5

**端点：** `GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed`

## 参数

|参数|类型 |描述 |
|--------|------|-------------|
| `url` |字符串|必需的。要分析的网址。 |
| `category` |字符串| `ACCESSIBILITY`、`BEST_PRACTICES`、`PERFORMANCE`、`SEO`。可以指定多个。 |
| `strategy` |字符串| `DESKTOP` 或 `MOBILE`（默认）。 |
| `locale` |字符串|文本区域设置（例如 `en`）。 |
| `key` |字符串| API 密钥。可选，但建议用于配额。 |

## 响应结构

```
{
  "id": "https://example.com/",
  "loadingExperience": { ... },        // URL-level CrUX data
  "originLoadingExperience": { ... },  // Origin-level CrUX data
  "lighthouseResult": {
    "categories": {
      "performance": { "score": 0.85 },
      "accessibility": { "score": 0.92 },
      "best-practices": { "score": 0.88 },
      "seo": { "score": 0.95 }
    },
    "audits": { ... }                  // Individual audit results
  },
  "analysisUTCTimestamp": "2026-03-27T..."
}
```

## 真实用户数据指标（在loadingExperience中）

| PSI 密钥 | CrUX 指标 |单位|
|---------|-------------|------|
| `LARGEST_CONTENTFUL_PAINT_MS` | LCP | ms |
| `INTERACTION_TO_NEXT_PAINT` | INP | ms |
| `CUMULATIVE_LAYOUT_SHIFT_SCORE` | CLS |无单位|
| `FIRST_CONTENTFUL_PAINT_MS` | FCP | ms |
| `EXPERIMENTAL_TIME_TO_FIRST_BYTE` | TTFB | ms |

每个指标包含：`percentile` (p75)、`distributions[]` ({最小值、最大值、比例})、`category` (快/平均/慢/无)。

## 关键 Lighthouse 审核 ID

`first-contentful-paint`、`largest-contentful-paint`、`total-blocking-time`、`cumulative-layout-shift`、`speed-index`、`interactive`

## 速率限制
- 25,000 QPD（含 API 密钥）
- 240 QPM
- 免费，无需计费

## 真实用户数据迁移注意事项
Google 正在将 CrUX 真实用户数据从 PSI 中迁移出来。对于真实用户数据，更喜欢直接使用 CrUX API。主要将 PSI 用于 Lighthouse Lab 数据。

---

## CrUX API（每日）

**端点：** `POST https://chromeuxreport.googleapis.com/v1/records:queryRecord`

在 `X-Goog-Api-Key` 标头中发送 API 密钥，而不是在 URL 中。

## 要求

```json
{
  "origin": "https://example.com",
  "formFactor": "PHONE",
  "metrics": ["largest_contentful_paint", "interaction_to_next_paint", "cumulative_layout_shift"]
}
```

|领域|描述 |
|--------|-------------|
| `origin` |原始 URL（与 `url` 互斥）|
| `url` |具体页面URL（与`origin`互斥）|
| `formFactor` | `DESKTOP`、`PHONE`、`TABLET`（可选，全部省略）|
| `metrics` |指标名称数组（可选，全部省略）|

## 可用指标

|指标|类型 |笔记|
|--------|------|--------|
| `largest_contentful_paint` |整数（毫秒）|Core Web Vital |
| `interaction_to_next_paint` |整数（毫秒）| Core Web Vital（取代 FID）|
| `cumulative_layout_shift` | **字符串** |Core Web Vital。 **字符串编码！** 仔细解析。 |
| `first_contentful_paint` |整数（毫秒）| |
| `experimental_time_to_first_byte` |整数（毫秒）| |
| `round_trip_time` |整数（毫秒）|替换 effectiveConnectionType（2025 年 2 月）|
| `navigation_types` |分数 | | 导航、navigate_cache、重新加载等
| `form_factors` |分数 |桌面/手机/平板电脑分发|

## 回复

```json
{
  "record": {
    "key": { "origin": "https://example.com" },
    "metrics": {
      "largest_contentful_paint": {
        "histogram": [
          { "start": 0, "end": 2500, "density": 0.72 },
          { "start": 2500, "end": 4000, "density": 0.18 },
          { "start": 4000, "density": 0.10 }
        ],
        "percentiles": { "p75": 2100 }
      },
      "cumulative_layout_shift": {
        "percentiles": { "p75": "0.05" }
      }
    },
    "collectionPeriod": {
      "firstDate": { "year": 2026, "month": 2, "day": 27 },
      "lastDate": { "year": 2026, "month": 3, "day": 26 }
    }
  }
}
```

## 重要
- **CLS p75 是一个字符串**（例如，`"0.05"` 而不是 `0.05`）。始终从字符串解析为浮点数。
- 最后一个直方图箱**没有 `end`**（延伸到无穷大）。
- 密度总和约为 1.0。
- **404** = 无数据（Chrome 流量不足）。不是身份验证错误。
- 每日更新约 04:00 UTC，有约 2 天的延迟。

## 速率限制
- CrUX 和 CrUX 历史 API 之间共享 150 QPM
- 免费，无需付费升级

---

## CrUX 历史 API（每周）

**端点：** `POST https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord`

在 `X-Goog-Api-Key` 标头中发送 API 密钥，而不是在 URL 中。

与 CrUX API 相同的请求格式。返回最多 **25 个每周收集周期**。

## 与 CrUX API 的响应差异

返回时间序列而不是单个值：

```json
{
  "record": {
    "metrics": {
      "largest_contentful_paint": {
        "histogramTimeseries": [
          { "start": 0, "end": 2500, "densities": [0.70, 0.71, 0.72, ...] },
          { "start": 2500, "end": 4000, "densities": [0.19, 0.18, 0.18, ...] },
          { "start": 4000, "densities": [0.11, 0.11, 0.10, ...] }
        ],
        "percentilesTimeseries": {
          "p75s": [2200, 2150, 2100, ...]
        }
      }
    },
    "collectionPeriods": [
      {
        "firstDate": { "year": 2025, "month": 9, "day": 29 },
        "lastDate": { "year": 2025, "month": 10, "day": 26 }
      },
      ...
    ]
  }
}
```

## NaN 处理
- `"NaN"` 字符串表示不合格期间的密度
- `null` 用于不合格期间的百分位数
- 在数字运算之前始终检查这些

## 更新时间表
- 更新**周一** ~04:00 UTC
- 每个周期 = 28 天滚动平均值，于周日结束

---

## 核心 Web Vitals 阈值

目前截至 2026 年 3 月。INP 于 2024 年 3 月 12 日取代 FID。

|指标|好 |需要改进|差|
|--------|------|--------------------|------|
| **LCP** | ≤ 2,500 毫秒 | 2,500–4,000 毫秒 | > 4,000 毫秒 |
| **INP** | ≤ 200 毫秒 | 200–500 毫秒 | > 500 毫秒 |
| **CLS** | ≤ 0.1 | 0.1–0.25 | > 0.25 |
| **FCP** | ≤ 1,800 毫秒 | 1,800–3,000 毫秒 | > 3,000 毫秒 |
| **TTFB** | ≤ 800 毫秒 | 800–1,800 毫秒 | > 1,800 毫秒 |

FID 已于 2024 年 9 月 9 日从 Chrome 工具（CrUX、PSI、Lighthouse）中完全删除。切勿在输出中引用 FID。

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
