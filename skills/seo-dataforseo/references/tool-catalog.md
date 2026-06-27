# DataForSEO MCP 工具目录

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

> 当您需要查找特定的 DataForSEO MCP 工具时加载此参考
> 主要 SKILL.md 命令未涵盖。这些都是实用工具
> 可供内部使用，但没有专用的 `/seo dataforseo` 命令。

## SERP 实用程序

- `serp_locations`：SERP 查询的位置代码查找
- `serp_youtube_locations`：YouTube 查询的位置代码查找

## 关键字数据实用程序

- `kw_data_google_ads_locations`：关键字数据的位置查找
- `kw_data_dfs_trends_demography`：用于趋势分析的人口统计数据
- `kw_data_dfs_trends_subregion_interests`：次区域趋势兴趣数据
- `kw_data_dfs_trends_explore`：DFS专有趋势数据
- `kw_data_google_trends_categories`：Google 趋势类别查找

## DataForSEO 实验室实用程序

- `dataforseo_labs_google_keyword_overview`：关键字指标快速概述
- `dataforseo_labs_google_historical_serp`：关键字的历史 SERP 结果
- `dataforseo_labs_google_serp_competitors`：特定 SERP 的竞争对手
- `dataforseo_labs_google_keywords_for_site`：网站排名的关键字（排名的替代方案）
- `dataforseo_labs_google_page_intersection`：页面级交叉分析
- `dataforseo_labs_google_historical_rank_overview`：历史域名排名数据
- `dataforseo_labs_google_historical_keyword_data`：历史关键字指标
- `dataforseo_labs_available_filters`：实验室端点的可用过滤器选项

## 外链实用程序

- `backlinks_competitors`：查找具有相似外链配置文件的域
- `backlinks_bulk_backlinks`：多个目标的批量外链计数
- `backlinks_bulk_new_lost_referring_domains`：批量新的/丢失的引用域
- `backlinks_bulk_new_lost_backlinks`：批量新的/丢失的外链
- `backlinks_bulk_ranks`：多个目标的批量排名概述
- `backlinks_bulk_referring_domains`：批量引用域计数
- `backlinks_domain_pages_summary`：域上页面的摘要
- `backlinks_domain_pages`：列出具有外链数据的域上的页面
- `backlinks_page_intersection`：页面级别共享外链源
- `backlinks_referring_networks`：参考网络分析
- `backlinks_timeseries_new_lost_summary`：随着时间的推移跟踪新的/丢失的外链
- `backlinks_bulk_pages_summary`：批量页面摘要
- `backlinks_available_filters`：外链端点的可用过滤器选项

## 域分析实用程序

- `domain_analytics_whois_available_filters`：WHOIS 过滤器选项
- `domain_analytics_technologies_available_filters`：技术检测过滤器选项

## AI 优化实用程序

- `ai_opt_kw_data_loc_and_lang`：AI优化关键词数据位置/语言
- `ai_optimization_keyword_data_search_volume`：AI特定关键词量数据
- `ai_optimization_llm_response`：直接法学硕士响应分析
- `ai_optimization_llm_mentions_filters`：LLM提及的可用过滤器
- `ai_optimization_chat_gpt_scraper_locations`：ChatGPT 抓取工具的可用位置

## 本项目适配边界

- DataForSEO 默认真实接入；`user-data` 可用于免费凭据验证。
- `serp`、`related-keywords`、`domain-rank` 等命令可能计费；只做配置检测时使用 `--offline`。
- 报告中要标明数据源、请求参数、时间和无法验证的字段。
