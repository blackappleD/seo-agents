# DataForSEO 地图和业务数据 API 端点

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Updated: 2026-03-23

## 源密钥

- **文档**：docs.dataforseo.com（官方 API 文档）
- **定价**：dataforseo.com/pricing（官方定价页面）

---

## 身份验证和限制

- HTTP 基本身份验证（登录名：密码）
- 速率限制：所有端点**2,000 个 API 调用/分钟**
- 每个 POST 在单个请求中最多支持 **100 个任务**
- 最低存款：50 美元。 1 美元免费试用积分。积分永不过期。

---

## Google 地图 SERP API（地理网格主干）

**端点：** `POST https://api.dataforseo.com/v3/serp/google/maps/live/advanced`
**定价来源：** https://dataforseo.com/pricing/serp-api

## 请求参数

|参数|必填|描述 |
|------------|----------|-------------|
| `keyword` |是 |搜索查询（例如“牙医”）|
| `location_name` |否 |指定位置（例如“美国德克萨斯州奥斯汀”）|
| `location_code` |否 | DataForSEO 位置代码（例如，奥斯汀为 1026339）|
| `location_coordinate` |否 | `"latitude,longitude,zoom"`（最多 7 位小数，缩放 3z-21z）|
| `language_code` |否 |默认值：“en”|
| `device` |否 | “桌面”或“移动”|
| `depth` |否 |返回的结果数 |

**对于地理网格至关重要：** 使用 `location_coordinate` 模拟从特定 GPS 点进行的搜索。格式：`"40.7128,-74.0060,15z"`。

## 响应字段（每个业务项目）

`cid`、`place_id`、`feature_id`、`title`、`domain`、`url`、`category`、`additional_categories`、`address`、`phone`（通过 `contact_info` 阵列）、`rating.value`、`rating.votes_count`、`rating.rating_distribution` （1-5 星细分）、`price_level`、`attributes`（分组：无障碍、付款、儿童）、`work_time`（每日时间表 + `current_status`）、`popular_times`（每天每小时）、`latitude`、`longitude`、`local_business_links`（预订、菜单、订单 URL）

## 定价

|方法|每项任务的成本|周转|
|--------|--------------|------------|
|标准| $0.0006（100 个桌面/20 个移动结果）|最多 5 分钟 |
|优先| 0.0012 美元 |长达 1 分钟 |
| **直播** | **0.002 美元** |长达 6 秒 |

关键字中的搜索运算符将成本乘以 5 倍。

---

## Google 我的商家信息 API（单一商家深入研究）

**端点：** `POST https://api.dataforseo.com/v3/business_data/google/my_business_info/live`
**定价来源：** https://dataforseo.com/pricing/business-data

## 输入选项

- `keyword`：企业名称 + 位置（例如“星巴克奥斯汀德克萨斯州”）
- `"cid:XXXX"`：直接 CID 查找
- `"place_id:XXXX"`：直接地点 ID 查找

## 响应字段

完整配置文件：`title`、`description`、`category`、`additional_categories`、`category_ids`、`attributes`（可用 + 不可用，按类型分组）、`contact_info`（电话阵列）、`domain`、`url`、`work_hours`（每天的开放/关闭时间）、`popular_times`、 `cid`、`place_id`、`rating`（带配电）、`address_info`（完整故障）、`latitude`/`longitude`、`photos_count`、`main_image`

**成本：** 每个配置文件 0.0015 美元（标准队列）

**用例：** 深入研究 TARGET 业务。映射 SERP 以发现竞争对手。

---

## Google 评论 API（情绪和速度）

**端点：** `POST https://api.dataforseo.com/v3/business_data/google/reviews/task_post`
**定价来源：** https://dataforseo.com/pricing/business-data

## 参数

|参数|描述 |
|------------|-------------|
| `keyword` |公司名称 + 位置（或 CID/place_id）|
| `depth` |要检索的评论数量 |
| `sort_by` | `"highest_rating"`、`"lowest_rating"`、`"most_relevant"`、`"newest"` |

## 响应字段（每个评论）

`review_text`、`original_review_text`、`time_ago`、`timestamp`、`rating.value`、`review_id`、`profile_name`、`profile_url`、`profile_image_url`、`owner_answer`（文本 + 时间戳）、`review_images`

## 定价

|方法|输入类型 |成本|
|--------|------------|------|
|标准（每 10 条评论）|关键词| 0.003 美元 |
|扩展（每 20 条评论）|关键词| 0.003 美元 |
|扩展（每 20 条评论）|地点 ID/CID | **0.00075 美元** |

**优化：** 始终使用 `place_id` 或 `cid` 输入（比关键字便宜 4 倍）。

---

## Google问答 API

**端点：** `POST https://api.dataforseo.com/v3/business_data/google/questions_and_answers/live`

返回问题、答案、点赞、日期、答案来源。提供实时方法和标准方法。

**用例：** 识别未解答的问题，常见问题解答差距分析。

**注意：** Google 于 2025 年 12 月弃用了GBP问答（由 Ask Maps Gemini AI 取代）。该端点返回历史数据。

---

## 企业列表搜索（预索引数据库）

**端点：** `POST https://api.dataforseo.com/v3/business_data/business_listings/search/live`

查询 DataForSEO 的预索引数据库（不是实时 Google）。基于类别的批量查询速度更快。每个查询最多 700 多个结果。

**类别聚合：** `/v3/business_data/business_listings/categories_aggregation/live` 提供类别分类。

**MCP工具名称：** `business_data_business_listings_search`

---

## 跨平台审核 API

## 到到网

- 搜索：`/v3/business_data/tripadvisor/search/task_post`
- 评论：`/v3/business_data/tripadvisor/reviews/task_post`
- 每 30 条评论收费。仅标准方法。

## 信任飞行员

- 搜索：`/v3/business_data/trustpilot/search/task_post`
- 评论：`/v3/business_data/trustpilot/reviews/task_post`
- ~$0.00075/任务。仅标准方法。

---

## 成本估算表

|运营| API 调用 |预计。成本（实时）|
|------------|------------------------|-----------------|
| 7x7 地理网格，1 个关键字 | 49 | 49 0.098 美元 |
| 7x7 地理网格，3 个关键字 | 147 | 147 0.294 美元 |
| 3x3 地理网格，1 个关键字 | 9 | 0.018 美元 |
|目标企业简介| 1 | 0.0015 美元 |
| 100 条评论（通过 place_id）| 5 | 0.00375 美元 |
| 20 名竞争对手简介 | 20 | 0.03 美元 |
|GBP发布审计| 1 | ~$0.002 |
|问答检索 | 1 | ~$0.002 |
| **全面审核（1 个关键字网格）** | **~73** | **~$0.13** |
| **全面审核（3 个关键字网格）** | **~171** | **~$0.33** |

**公式：** `grid_size^2 x keywords x $0.002`（实时）或 `x $0.0006`（标准）

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
