# Google AI 优化指南 — 主要来源综合（2026 年 5 月）

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

Google在搜索中心发布了专门的**人工智能优化指南**
文档。它的位置是关于人工智能概述和应用的最常被引用的主要来源。
AI 模式与搜索排名互动。每一次涉及 GEO 的 seo-agents 审核
应将此文档视为规范参考并拒绝社区声明
这与它相矛盾。

**主要来源：**
https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

## 长篇大论；博士

> “针对生成式人工智能搜索进行优化**仍然是 Google 的 SEO**
> 观点。 AEO 和 GEO 是同一作品的更名标签。”
>——Google，AI优化指南

AI 概述和 AI 模式基于相同的排名和质量系统
作为经典搜索。上面有两种人工智能技术：

1. **RAG / grounding** — 检索索引页面，生成响应
   可点击的源链接。
2. **查询扇出** — 发出多个相关子查询并拉入
   回答之前的附加结果。

**资格楼层：**页面必须被**索引并有资格显示
Google 搜索中的片段**，可出现在任何 AI 功能中。没有单独的
“人工智能指数”。接下来的一切都是通过此应用的 SEO 基础知识
镜头。

## 打破神话部分（最重要）

Google明确表示您**不需要**：

|声称Google拒绝|来源 |
|---|---|
|创建 `llms.txt` 或 AI 特定标记文件 | AI优化指南§“神话”|
|将您的内容“分成”小块以供人工智能使用 |相同|
|使用特定短语或长尾关键字变体重写人工智能内容 |相同|
|在博客/论坛/视频中追踪不真实的提及|相同|
|过度投资专门针对人工智能功能的结构化数据|相同|

根据Google的说法，什么**重要**：独特的、非商品的、第一手的内容。
他们的例子将“首次购房者的 7 个提示”（商品）与
“为什么我们免除检查并节省资金：看看下水道管道内部”
（生活经验）。

> **交叉引用：** llms.txt 神话由以下机构独立证实
> [[llmstxt-evidence]]（Mueller、Illyes、SE 排名 30 万域研究，
> OtterlyAI 服务器日志审计）。两个文件必须保持对齐。

## “创建有用的内容”配套指南

AI 优化指南链接到 Google 的 E-E-A-T 指南：

**主要来源：**
https://developers.google.com/search/docs/fundamentals/creating-helpful-content

关键可操作测试 - **谁/如何/为什么**：

- **谁**创造了它 - 读者期望的署名；作者
  YMYL 所需的背景页。
- **如何**它是如何创建的——特别是对于人工智能辅助的内容；披露
  读者会合理询问的过程。
- **为什么**它存在——“为了帮助人们”，而不是“为了吸引搜索点击”。

YMYL（“你的金钱还是你的生活”）主题变得格外重要：健康、金融、
安全。 2025 年 9 月 QRG 扩展了 YMYL 以包含政治/社会主题。

Google 列出了自我审核的警告信号：

- 写入目标字数（没有目标字数）
- 进入没有专业知识的利基市场，只是为了流量
- 伪造出版日期新鲜度
- 大量内容流失以获取“新鲜度”信号

## AI 内容政策

**主要来源：**
https://developers.google.com/search/blog/2023/02/google-search-and-ai-content
（加上 Search Essentials 垃圾邮件政策）

如果人工智能生成内容符合搜索要素，那么它就很好。它跨越到
用于**扩展低价值页面**时的垃圾邮件（QRG §4.6.5 扩展内容滥用，
§4.6.6省力主要内容）。

具体执行表面的两个操作要求：

1. **Merchant Center — AI生成的产品图片：**必须携带IPTC
   `DigitalSourceType: TrainedAlgorithmicMedia` 元数据。参见
   `skills/seo-images/SKILL.md`为审核+注入模式。
2. **AI生成的产品标题和描述：**必须分开
   在商家 Feed 中指定并标记为 AI 生成。

## 前瞻性：代理友好页面和 WebMCP

人工智能优化指南接近尾声时转向**人工智能代理**——而不仅仅是
总结者。代理通过三个渠道与站点交互： 屏幕截图
加上视觉模型、原始 HTML/DOM 和浏览器可访问性树。

完整审核标准：`skills/seo-technical/references/agent-friendly-pages.md`。

该指南还提到了**WebMCP**（直接的拟议标准）
站点↔代理交互）和 **UCP**（通用商务协议 — Google +
Shopify + Etsy + 沃尔玛 + Visa/万事达卡）。 UCP审核标准：
`skills/seo-ecommerce/references/ucp-universal-commerce-protocol.md`。

## seo-agents 如何对待本指南

1. 每当出现以下情况时，`seo-geo` 审核都会引用此 URL 作为权威来源：
   用户询问 AEO/GEO 框架。
2. 上面的打破神话的列表来自社区的 AI-SEO 建议
   - 如果建议与 Google 声明的立场相矛盾，请将其标记出来。
3. 如果第三方声明与 Google 相矛盾，seo-agents 将遵循
   Google并明确指出了这一矛盾。
4. `seo-ecommerce` 和 `seo-images` 强制执行两个操作要求
   以上适用于使用人工智能生成产品内容的网站。

## 最后验证

2026年5月18日。每个季度重新检查源文档。每当出现以下情况时更新此文件：

- Google发布新的神话破灭/澄清。
- 任何链接的政策文档都会修改资格或执行语言。
- UCP / WebMCP 标准进展（目前处于早期阶段）。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
