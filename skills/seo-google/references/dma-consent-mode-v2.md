# DMA + 同意模式 v2 — 点击影响诊断

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

流经 Google 搜索的欧盟流量受到
**《数字市场法》** 自 2024 年 3 月 7 日起生效。 DMA 限制 Google
可以使用行为数据并强制同意模式 v2 合规性
欧盟的 GA4 + 广告。 SEO审核的操作效果：

- 来自 Search Console 的欧盟点击率 (CTR) 数据具有重大意义
  DMA 执行日期后噪音更大。同比点击率
  跨越这一界限的比较并不是同类比较。
- 面向欧盟用户的 GA4 自然流量报告显示系统性
  当同意模式 v2 配置为“拒绝”时报告不足
  ad_storage，授予analytics_storage”（典型的欧盟默认设置）。
  转化建模填补了空白，但原始计数较低
  比 2024 年之前。

## seo-google 技能应该做什么

1. **在针对欧盟目标酒店提取 GSC 搜索分析时**，
   注意：“2024 年 3 月 7 日之前/之后的欧盟点击率比较并非
   苹果对苹果（DMA + 同意模式 v2 生效）。”
2. **拉动 GA4 有机流量**时，显示同意模式
   配置（如果 GA4 管理 API 公开它）。如果该 GA4 property
   默认情况下有 `eu_data_collection_disabled` 或拒绝 ad_storage，
   请注意“欧盟流量计数是保守的；转化模型
   可能会提高。”
3. **不要就 cookie 同意用户体验向用户说教** — 这是合法的
   团队/工程关注点超出了 SEO 范围。只需附上
   诊断记录。

## 审核应检查的必需 GA4/同意模式设置

- GA4 4.x 同意模式 v2 已连接 (`gtag('consent', 'default', ...)`
  在任何页面浏览之前）。
- 在欧盟流量上设置 `ads_data_redaction` 标志。
- 同意转换时的服务器端标记（推荐模式；
  法律上没有要求）。

## 软化 cookieless 归因警告

Google **于 2024 年 7 月**放弃**第三方 Cookie 弃用，并且
2025 年 4 月确认 Chrome 将不会发布独立 cookie
提示。 “无cookie的未来”框架不再紧迫。

截至 2026 年 5 月的审计：

- 不建议优先考虑“切换到无 Cookie 归因”。
- 建议“实施同意模式 v2 + 服务器端标记”
  欧盟合规性 + 信号丢失恢复。
- Privacy Sandbox API 仍然可用，但可选。提及
  仅当审核主体面向消费者且具有重大意义时
  重定向依赖。

## 主要来源

- DMA 强制：https://digital-markets-act.ec.europa.eu/
- Google 的第三方 cookie 逆转：https://privacysandbox.com/news/privacy-sandbox-update-jul-2024
- 同意模式 v2 规范：https://support.google.com/google-ads/answer/14411014

最后验证时间：2026 年 5 月 17 日。

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
