# Google Ads API - 关键字规划师参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

关键字搜索量的黄金标准来源。 DataForSEO 从 Google Ads 获取流量数据——这省去了中间商。

## 先决条件（比其他 Google API 更复杂）

1. **Google Ads Manager 帐户** -- 在 ads.google.com 上创建（免费创建）
2. **开发者令牌** -- 在 Google Ads API 中心申请（需要基本访问批准）
3. **OAuth 2.0 凭证** -- 重用 seo-google 配置中的现有 OAuth 客户端
4. **对于确切的数量**：运行最低限度的活动（约 5-10 美元/天）。如果没有支出，交易量是分桶范围（“1K-10K”）

## 关键方法

## 生成关键字创意
从种子术语生成关键字建议。

**每个关键词的回报：**
- `text`：关键字字符串
- `avg_monthly_searches`：平均每月交易量（如果支出则精确，如果没有则分桶）
- `competition`：低/中/高（用于广告，非有机）
- `competition_index`：0-100 比赛分数
- `low_top_of_page_bid_micros`：〜第 20 个百分位每次点击费用（以微为单位）
- `high_top_of_page_bid_micros`：约第 80 个百分位数的 CPC（以微为单位）
- `monthly_search_volumes[]`：过去 12 个月的每月交易量

## 生成关键字历史指标
获取特定关键字的数量数据。

与上面相同的返回字段，但用于精确的关键字列表而不是建议。

## 生成关键字预测指标
预测关键字的点击次数、展示次数和费用。

## 配置

添加到 `~/.config/seo-agents/google-api.json`：

```json
{
  "ads_developer_token": "YOUR_DEV_TOKEN",
  "ads_customer_id": "123-456-7890",
  "ads_login_customer_id": "123-456-7890"
}
```

## 速率限制

- 与其他广告 API 服务相比，关键字规划请求受到更严格的速率限制
- 确切的 QPM/QPS 未公开记录
- Google 建议缓存结果

## Python 库

```bash
pip install google-ads
```

使用 `google-ads` 库（与 `google-api-python-client` 分开）。

## 重要提示

- **数量准确性**：如果没有活跃的广告支出，Google 将返回存储范围（“1K-10K”、“10K-100K”），而不是“14,800”等精确数字
- **竞争分数**：衡量广告商对广告的竞争，而不是自然排名难度
- **每次点击费用出价**：反映广告商支付的费用，有助于估算关键字商业价值
- **位置定位**：使用位置 ID（2840 = 美国，2826 = 英国）
- **语言定位**：使用语言 ID（1000 = 英语，1003 = 西班牙语）

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
