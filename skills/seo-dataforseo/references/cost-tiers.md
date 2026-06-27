# DataForSEO API 成本参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 定价等级（每次调用美元，标准队列）

|类别 |端点|通话费用|笔记|
|----------|----------|------------|--------|
| **搜索结果** | `serp_*_live_advanced` | 0.002 美元 |每 100 个结果 |
| **搜索结果** | `serp_*_live_regular` | 0.001 美元 |轻量化|
| **SERP 图片** | `serp_google_images_live_*` | 0.002 美元 | 5x 站点：/文件类型：操作员 |
| **关键词** | `kw_data_google_ads_search_volume` | 0.05 美元 |每批关键词 |
| **关键词** | `kw_data_google_trends_explore` | 0.01 美元 |每个查询 |
| **实验室** | `dataforseo_labs_*_keyword_*` | 0.05 美元 |想法、建议、相关|
| **实验室** | `dataforseo_labs_bulk_*` | 0.01 美元 |难度、交通|
| **实验室** | `dataforseo_labs_*_domain_*` | 0.05 美元 |竞争对手，路口|
| **页面** | `on_page_instant_pages` | 0.01 美元 |快速分析|
| **页面** | `on_page_lighthouse` | 0.02 美元 |完整的Lighthouse|
| **外链** | `backlinks_*` | 0.02 美元 |每个子呼叫 |
| **内容** | `content_analysis_*` | 0.02 美元 |搜索、摘要、趋势 |
| **业务** | `business_data_*` | 0.05 美元 |房源搜索 |
| **人工智能/地理** | `ai_optimization_*` | 0.05 美元 | ChatGPT 抓取工具、LLM 提及 |
| **商家** | `merchant_*` | 0.02 美元 |Google购物、亚马逊 |
| **域名** | `domain_analytics_whois_*` | 0.005 美元 | WHOIS 数据 |
| **域名** | `domain_analytics_technologies_*` | 0.01 美元 |技术堆栈 |

## 预算预设

|预设|每日限额 |门槛|模式|最适合 |
|--------|------------|------------|-----|----------|
| **保守** | 2.00 美元 | 0.10 美元 |阈值|学习、测试|
| **标准** | 10.00 美元 | 0.50 美元 |阈值|定期审核|
| **激进** | 50.00 美元 | 2.00 美元 |阈值|代理批量工作|
| **无限制** | 999.00 美元 | --|无 |值得信赖的管道 |

配置：`python3 scripts/dataforseo_costs.py config --mode threshold --threshold 0.50 --daily-limit 10.00`

## 降低成本的技巧

- 当不需要完整的 SERP 功能时，使用 `live_regular` 而不是 `live_advanced`（节省 50%）
- 将关键字批量放入单个 `search_volume` 调用中，而不是单独的 SERP 查找
- 使用 `standard` 任务队列代替 `live` 进行非紧急分析（节省 60-80%）
- 避免在图像 SERP 查询中使用 `site:` 和 `filetype:` 运算符（5 倍成本乘数）
- 缓存会话结果 - 不要在会话中重新获取相同的关键字/域

## 审批流程

在任何 DataForSEO MCP 调用之前：
1.运行`python3 scripts/dataforseo_costs.py check <endpoint> [--count N]`
2. 如果 `status: "approved"` → 继续
3. 如果`status: "needs_approval"`→向用户显示费用，要求确认
4. 如果`status: "blocked"` → 通知用户每日限额将被超出
5. 调用完成后，记录：`python3 scripts/dataforseo_costs.py log <endpoint> <cost>`

## 警告端点

无论批准模式如何，这些端点始终需要用户确认：
- `backlinks_backlinks`（可以生成大型结果集）
- `backlinks_domain_intersection`（昂贵的多域比较）
- `ai_optimization_chat_gpt_scraper`（ChatGPT 网络抓取）
- `ai_opt_llm_ment_search`（法学硕士提及跟踪）
- `merchant_amazon_products_search`（亚马逊产品数据）

## 本项目适配边界

- DataForSEO 默认真实接入；`user-data` 可用于免费凭据验证。
- `serp`、`related-keywords`、`domain-rank` 等命令可能计费；只做配置检测时使用 `--offline`。
- 报告中要标明数据源、请求参数、时间和无法验证的字段。
