# 核心 Web Vitals 阈值（2026 年 2 月）

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Updated: 2026-02-07

## 当前指标

|指标|好 |需要改进|差|
|--------|------|--------------------|------|
| LCP（Largest Contentful Paint）| ≤2.5秒| 2.5 秒–4.0 秒 | >4.0 秒 |
| INP（Interaction to Next Paint）| ≤200ms | 200 毫秒–500 毫秒 | >500 毫秒 |
| CLS（Cumulative Layout Shift）| ≤0.1 | 0.1–0.25 | >0.25 |

## 关键事实
- INP 于 **2024 年 3 月 12 日**取代了 FID（首次输入延迟）。 **2024 年 9 月 9 日**，FID 已从所有 Chrome 工具（CrUX API、PageSpeed Insights、Lighthouse）中完全删除。 INP 是唯一的交互性指标。
- 评估使用真实用户数据的 **75%**（来自 CrUX 的真实用户数据）。
- Google 在 **页面级别** 和 **origin 级别** 进行评估。
- Core Web Vitals是一个**tiebreaker**排名信号：当竞争对手之间的内容质量相似时，它们最重要。
- **自原始定义以来阈值保持不变**：忽略 SEO 博客中“收紧阈值”的声明。
- 2025 年 12 月核心更新似乎对**移动 CWV 的影响更大**。
- 截至 2025 年 10 月：**57.1%** 桌面网站和 **49.7%** 移动网站通过了所有三个 CWV。

## LCP 子部件（2025 年 2 月 CrUX 添加）

LCP 现在可以分为诊断子部分：

|子部分|它测量什么 |目标|
|---------|--------------------|--------|
| **TTFB** |首字节时间（服务器响应）| <800 毫秒 |
| **资源加载延迟** |从 TTFB 到资源请求开始的时间 |最小化 |
| **资源加载时间** |是时候下载LCP资源了|取决于尺寸 |
| **元素渲染延迟** |从资源加载到渲染的时间 |最小化 |

**总 LCP = TTFB + 资源加载延迟 + 资源加载时间 + 元素渲染延迟**

使用此细分来确定哪个阶段导致了 LCP 问题。

## 软导航 API（实验性）

**Chrome 139+ Origin 试用（2025 年 7 月）**：测量 SPA 中的 CWV 的第一步。

- 解决了长期存在的 SPA 测量盲点
- 目前处于实验阶段，**尚无排名影响**
- 检测“软导航”（URL 更改而无需完整页面加载）
- 可能影响未来 SPA CWV 测量

**检测：** 检查 SPA 框架（React、Vue、Angular、Svelte）并警告当前 CWV 测量限制。

## 测量源

## 真实用户数据（真实用户）
- Chrome 用户体验报告 (CrUX)
- PageSpeed Insights（使用 CrUX 数据）
- Search Console Core Web Vitals报告

## Lab 数据（模拟）
- Lighthouse
- WebPageTest
- Chrome 开发者工具

> 真实用户数据是 Google 用于排名的数据。Lab 数据对于调试很有用。

## 常见瓶颈

## LCP（Largest Contentful Paint）
- 未优化的hero image（压缩、使用 WebP/AVIF、添加预加载）
- 渲染阻塞 CSS/JS（延迟、异步、关键 CSS 内联）
- 服务器响应缓慢（TTFB >200ms：使用边缘 CDN、缓存）
- 第三方脚本阻止（延迟分析、聊天widget）
- Web 字体加载延迟（使用font-display：交换+预加载）

## INP（Interaction to Next Paint）
- 主线程上的长 JavaScript 任务（分成小于 50 毫秒的较小任务）
- 过重的事件处理程序（去抖，使用 requestAnimationFrame）
- DOM 大小过大（涉及 >1,500 个元素）
- 第三方脚本劫持主线程
- 同步XHR或localStorage操作
- 布局抖动（多次强制回流）

## CLS（Cumulative Layout Shift）
- 没有宽度/高度尺寸的图像/iframe
- 在现有内容之上动态注入内容
- Web 字体导致布局偏移（使用font-display：交换 + 预加载）
- 没有预留空间的广告/嵌入
- 延迟加载内容会导致页面下移

## 优化优先级

1. **LCP**：对感知性能影响最大
2. **CLS**：影响用户体验的最常见问题
3. **INP**：对于交互式应用程序最重要

## 工具

```bash
# PageSpeed Insights API
curl -H "X-Goog-Api-Key: $GOOGLE_API_KEY" \
  "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL"

# Lighthouse CLI
npx lighthouse URL --output json --output-path report.json
```

## 性能工具更新 (2025)

- **Lighthouse 13.0**（2025 年 10 月）：重大审计重组，重组绩效类别并更新评分权重。 Lighthouse 是一个实验室工具（模拟条件）：始终与 CrUX 真实用户数据交叉引用以获得实际性能。
- **CrUX Vis** 取代了 CrUX 仪表板（2025 年 11 月）。旧的 Looker Studio 仪表板已弃用。直接使用 [CrUX Vis](https://cruxvis.withgoogle.com) 或 CrUX API。
- **LCP 子部分** 添加到 CrUX（2025 年 2 月）：首字节时间 (TTFB)、资源加载延迟、资源加载时间和元素渲染延迟现在可作为 CrUX 数据中 LCP 的子组件使用。
- **Google Search Console 2025 功能**（2025 年 12 月）：用于自动分析的人工智能配置。品牌与非品牌查询过滤器。 API 中提供每小时数据。自定义图表注释。社交渠道跟踪。

> **移动优先索引** 截至 2024 年 7 月 5 日已 100% 完成。Google 现在仅使用移动 Googlebot user-agent对所有网站进行抓取和索引。确保您的移动版本包含所有关键内容、结构化数据和meta tags。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
