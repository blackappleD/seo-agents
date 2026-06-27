# DataForSEO 商家 API 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

Google Shopping 和 Amazon 市场数据的端点详细信息。

## 端点

## Google购物产品

|领域|价值|
|--------|--------|
|端点| `merchant_google_products_search` |
|方法| POST（任务）/ GET（结果）|
|成本|每次通话 0.02 美元 |
|队列|标准（与实时相比节省 60-80%）|

**参数：**
- `keyword`（必填）——搜索查询
- `location_code`（默认：2840 = 美国）--DataForSEO 位置 ID
- `language_code`（默认：“en”）--语言
- `price_min` / `price_max`（可选）——按价格范围过滤
- `sort_by`（可选）--“相关性”、“price_low_to_high”、“price_high_to_low”、“评级”
- `depth`（可选，默认：100）--结果数

**响应字段：**
- `title` -- 产品列表标题
- `price` -- 数字价格值
- `currency` -- 货币代码（美元、欧元等）
- `seller` -- 商户名称
- `rating` -- 产品评级（浮点数，0-5）
- `reviews_count` -- 评论数量
- `url` -- 产品列表 URL
- `image_url` -- 产品图片 URL
- `availability` --“库存”、“库存不足”、“预订”
- `delivery_info` -- 运输详细信息文本
- `product_id` -- Google 购物产品 ID

## Google购物卖家

|领域|价值|
|--------|--------|
|端点| `merchant_google_sellers_search` |
|方法| POST（任务）/ GET（结果）|
|成本|每次通话 0.02 美元 |

**参数：** 与产品搜索相同。

**响应字段：**
- `seller_name` -- 商户名称
- `seller_rating` -- 商户评级（浮动）
- `seller_reviews_count` -- 商户评论计数
- `price` -- 该卖家提供的价格
- `delivery_info` -- 运输和交货文本
- `url` -- 卖家列表 URL

## 亚马逊产品

|领域|价值|
|--------|--------|
|端点| `merchant_amazon_products_search` |
|方法| POST（任务）/ GET（结果）|
|成本|每次通话 0.02 美元 |
|注意|在 `warn_endpoints` 中——始终需要用户批准 |

**参数：**
- `keyword`（必填）——搜索查询
- `location_code`（默认：2840 = 美国）
- `language_code`（默认值：“en”）
- `depth`（可选，默认：100）
- `sort_by`（可选）--“相关性”、“price_low_to_high”、“price_high_to_low”、“avg_customer_review”

**响应字段：**
- `title` -- 产品标题
- `price` -- 数字价格
- `currency` -- 货币代码
- `seller` -- 卖家/品牌名称
- `rating` -- 星级（浮点数，0-5）
- `reviews_count` -- 评论计数
- `url` -- 亚马逊产品 URL
- `image_url` -- 产品图片
- `availability` -- 库存状态
- `asin` -- 亚马逊标准识别号
- `is_prime` -- Prime 资格（布尔值）
- `is_best_seller` -- 畅销书徽章（布尔值）

## 任务/投票模式

所有商家端点都使用标准 DataForSEO 队列模式：

1. **POST** 带有参数的任务来创建端点
2. **轮询**以指数退避（2s、4s、8s、最长 60s）的结果
3. 通过任务ID**GET**完成的结果

与实时端点相比，这可以节省 60-80%。

## 速率限制

- 每分钟最多 2000 个任务（跨所有端点）
- 标准计划每天最多执行 30,000 个任务
- HTTP 429 上的退避：等待 60 秒，然后重试

## 数据标准化

当使用响应时，标准化：

|领域|原料|标准化|
|--------|-----|------------|
|价格|字符串“$29.99”或浮点数 |浮球 `29.99` |
|货币 |混合格式| ISO 4217 代码（美元、欧元、GBP）|
|可用性 |各种琴弦|枚举：`in_stock`、`out_of_stock`、`preorder`、`unknown` |
|评级 |整数或浮点数 |浮点数四舍五入到小数点后 1 位 |
|评论 |字符串或整数 |整数 |

使用 `scripts/dataforseo_normalize.py --module merchant` 进行自动归一化。

## 费用参考

请参阅 `skills/seo-dataforseo/references/cost-tiers.md` 了解完整定价表，
预算预设和降低成本的技巧。所有商家端点的价格为 0.02 美元/次
在标准队列上。

## 本项目适配边界

- 当前 `seo-agents ecommerce <url>` 做页面级电商 SEO 基础检查，不直接调用 Amazon、Google Merchant Center 或其他 marketplace API。
- Marketplace、UCP 或 feed 字段作为规划和人工核对参考；没有真实 feed/API 数据时必须标注缺口。
