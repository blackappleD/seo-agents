# 代理友好页面 — 审核参考（2026 年 5 月）

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

人工智能搜索的下一波浪潮不是总结——而是**代理**作用于
代表用户（搜索、比较、购买、预订）。 Google 的 AI 优化指南和
链接的 web.dev 文章描述了代理的三个渠道
解释您的网站：

1. **截图+视觉模型**——解读视觉层次、按钮
   突出，布局。缓慢且昂贵。
2. **原始 HTML / DOM** — 嵌套、ID、类、数据属性。
3. **可访问性树**——浏览器原生语义蒸馏
   （角色、名称、状态）。三者中最干净的信号。

现代代理将这三者结合起来。针对**可访问性树**进行优化是
单一最高杠杆举措；如果您的可访问性树已损坏，则不会
大量的视觉修饰可以节省你的时间。

**主要来源：**
- GoogleAI优化指南：
  https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- web.dev（参考上面的指南）：关于构建的文章
  适合代理商的网站

## 审核清单

### 1.使用真实的交互元素

|通行证 |失败|
|---|---|
| `<button>` 行动 | `<div onclick="...">` |
| `<a href="...">` 导航 | `<div onclick="window.location...">` |
| `<input>` / `<select>` / `<textarea>` |定制 `contenteditable` widget |

如果您无法使用真正的交互式标签，请提供 ARIA：`role="button"`，
`role="link"`、`tabindex="0"`，以及 `Enter` 和 `Space` 的密钥处理程序。

**为什么重要：** 可访问性树公开了真正的交互元素
和他们的角色。自定义 div widget通常出现在树中，但没有任何作用
所有——特工都会跳过它们。

### 2. 标签关联

每个表单输入都必须有一个关联的标签：

```html
<label for="email">Email</label>
<input id="email" type="email" name="email">
```

或者在无法看到标签的地方使用 `aria-label` / `aria-labelledby`。
读取可访问性树的代理直接从
相关标签——没有它，输入就是空的。

### 3.交互目标尺寸

可视化分析管道过滤掉小于 **~8 的交互元素
未遮挡区域的方形像素**。点击目标可访问性最小值（24×24
WCAG AA、44×44 Apple HIG）比较严格，默认通过代理门。

审核：任何低于 24×24px 的可点击元素都是代理的候选者
隐形，除了 WCAG 失败之外。

### 4. 不要用透明覆盖层覆盖交互节点

视觉模型在计算“此时交互的内容”时会丢弃覆盖的节点
的立场”。常见违法者：

- 覆盖每个子链接的全卡点击处理程序。
- 透明的cookie同意层在超出同意的情况下持续存在。
- 关闭后，带有 `pointer-events: auto` 的模态门户仍保持打开状态。
- 使用 `position: absolute; inset: 0` 的“幽灵”跟踪像素。

### 5.布局稳定性

如果“添加到购物车”在 `/category/shoes` 与
`/category/bags`，基于屏幕截图的代理必须重新学习每个页面
访问。在同一屏幕象限中保持功能相同的操作
模板。

交叉引用：这与 Core 中的 **CLS**（Cumulative Layout Shift）重叠
Web Vitals，但代理用户体验的关注范围更广——它涵盖了页面到页面
稳定性，而不仅仅是页内移动。

### 6. `cursor: pointer` 作为合法信号

视觉型号读取 `cursor: pointer`（在 `<a>` / `<button>` 上默认设置）为
元素可操作的提示。不要将其覆盖为 `cursor: default`
真正的互动元素，只为视觉极简主义。

反向：不要将 `cursor: pointer` 应用于非交互式元素 - 即
使代理点击不执行任何操作的内容。

### 7. 稳定、有意义的选择器

回退到 DOM 解析的代理依赖于：

- 真实语义标签（`<nav>`、`<main>`、`<article>`、`<section>`、`<aside>`）
- 顶级布局容器上稳定的 `id` 属性
- `data-*` 描述目的而非实现的属性

避免将自动生成的类名（如 `__sc_a4b7d9e2`）作为唯一的句柄
关键的交互元素——代理可以瞄准他们，但无法分辨出什么
他们的意思是。

## 前瞻性：WebMCP

Google的人工智能优化指南提到了**WebMCP**，这是一项拟议的标准
直接的站点到代理交互（类似于 当前 Agent / Anthropic 中的 MCP）
生态系统，但在页面级别运行）。有一个早期预览
计划；预计 2027 年之前不会得到广泛采用。

**审计立场：** 在报告中提及 WebMCP 作为前瞻性信号值得
跟踪。不要将缺乏 WebMCP 支持标记为结果 —
标准尚未稳定。

## 快速审核一行

要进行快速烟雾检查，请通过 Lighthouse 捕获可访问性树或
Chrome DevTools 并查找：

- 任何带有 `role="generic"` 的交互元素 → 语义错误。
- 任何没有 `accessible name` 的输入 → 缺少标签。
- 任何带有 `onclick` 且没有 `role` / `tabindex` 的 `<div>` → 自定义widget
  代理不会看到。

`scripts/render_page.py --mode auto` 已经无头加载页面；延伸
它带有可访问性树转储（`page.accessibility.snapshot()` in
Playwright）是进行自动化代理用户体验检查的自然场所
未来的迭代。

## 最后验证

2026年5月18日。更新时间：

- WebMCP 从预览版升级到稳定版。
- Google 发布了单独的 Agent-UX 评分框架。
- web.dev 发布了一篇带有修订标准的后续文章。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
