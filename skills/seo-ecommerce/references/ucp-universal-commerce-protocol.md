# UCP — 通用商业协议（2026 年 5 月）

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

UCP 是 Google 主导的开放标准，与 Shopify 共同开发并得到以下机构的认可
Etsy、Target、沃尔玛、Wayfair 以及支付合作伙伴（Stripe、Visa、
万事达卡、Adyen、美国运通卡）。其目的：让**AI代理发现、协商、
并与商家进行交易，无需一次性集成**。

对于商业网站，UCP 位于 **Google Merchant Center feed** 旁边，
**Google 商家资料** 作为代理时代发现的第三站。领养
虽然还早，但声明profile的成本很低。

**主要来源：** Google AI优化指南参考UCP；规格
它本身是在developer.google.com/merchant.google.com上共同发布的（请参阅
Google 获取当前规范 URL — 标准正在变化）。

## UCP 是什么和不是什么

|它是什么 |它不是什么 |
|---|---|
|能力声明+协商协议|新的支付处理器 |
|与传输无关（REST、MCP、A2A）| Merchant Center Feed 的替代品 |
|与 AP2（代理支付协议）兼容，用于自主购买的加密用户同意证明 |避免成为记录商人的方法|
|今天在搜索和 Gemini 中采用 AI 模式 | “排名因素”——Google并没有这样定义|

商家在 UCP 下保持**记录商家** — 他们留住了客户
关系和购买后所有权。

## 如何声明 UCP 配置文件

在 `/.well-known/ucp` 发布配置文件，描述功能和版本。
一般形状（有关确切的字段名称，请参阅实时规范）：

```jsonc
{
  "version": "1.0",
  "capabilities": [
    {
      "id": "dev.ucp.shopping.checkout",
      "version": "1.0",
      "endpoint": "https://api.example.com/ucp/checkout"
    },
    {
      "id": "dev.ucp.shopping.fulfillment",
      "version": "1.0",
      "endpoint": "https://api.example.com/ucp/fulfillment"
    },
    {
      "id": "dev.ucp.shopping.discount",
      "version": "1.0",
      "endpoint": "https://api.example.com/ucp/discount"
    }
  ],
  "merchant": {
    "name": "Example Co.",
    "id": "merchant-center-id-here"
  }
}
```

平台（搜索中的 AI 模式、Gemini 以及最终的其他平台）自动发现
简介和谈判。 Google 已经构建了一个参考实现
支持 AI Mode 和 Gemini 的直接购买。

## 需要声明的通用能力

|能力 ID（形状）|目的|
|---|---|
| `dev.ucp.shopping.checkout` |发起结帐，返回总计+付款意向 |
| `dev.ucp.shopping.fulfillment` |报价运输选项和交货窗口 |
| `dev.ucp.shopping.discount` |在报价时应用促销代码/忠诚度折扣 |
| `dev.ucp.shopping.cart` |添加/删除/更新代理管理的购物车中的商品 |

确切的标识符由实时规范管理。模式是
`dev.ucp.<domain>.<verb>` 具有语义版本控制。

## seo-agents 审核是什么

`/seo ecommerce <url>` 应报告：

1. **存在：** `/.well-known/ucp` 是否解析为有效的 JSON 文档？
2. **能力覆盖范围：**声明了哪些能力？旗帜缺失
   结帐/履行/折扣是机会，而不是失败（
   协议还早）。
3. **端点可达性：**声明的端点是HTTPS、有效的TLS，而不是
   返回 5xx？
4. **版本一致性：**声明的协议版本是否与已知的相匹配
   释放？标记预发布或无法识别的版本。

今天的审计不应将 UCP 的缺席视为严重失败
——采用还早。将其视为一个前瞻性机会，尤其是
适用于已在 Google Merchant Center 上的商家。

## UCP 如何与现有表面交互

|现有表面|与 UCP 的关系 |
|---|---|
| Google Merchant Center Feed |上游所需 — UCP 功能按 ID 引用 Merchant Center 产品 |
|Google公司简介|独立——UCP是产品/订单；GBP是商店/地点|
|产品架构（`hasMerchantReturnPolicy`、`shippingDetails`）|互补——UCP在API层公开相同的数据； schema 在页面层公开它 |
| AP2（代理支付协议）| Pair — UCP 处理发现+结帐结构； AP2 处理用户同意的加密证明 |

已经拥有干净的 Merchant Center Feed、完整的产品的商家
schema，结账 API 可以在 sprint 中声明 UCP 配置文件。

## 审计态势

- **第 1 级（Merchant Center 上已有的电子商务网站）：** 推荐
  宣布 UCP 概况为前瞻性机会。
- **第 2 级（不在 Merchant Center 上的 DTC 网站）：** 尚不推荐 UCP —
  Merchant Center 是大多数流程的先决条件。
- **第 3 层（信息/B2B 网站）：** 完全忽略 UCP。

## 最后验证

2026年5月18日。标准正在快速发展。重新检查时间：

- 规范规范 URL 稳定（目前发布在 Google 开发者上）
  文档，但确切的路径可能会改变）。
- AP2 达到稳定版本。
- 其他平台（AI 模式 + Gemini 之外）宣布 UCP 消耗。

## 本项目适配边界

- 当前 `seo-agents ecommerce <url>` 做页面级电商 SEO 基础检查，不直接调用 Amazon、Google Merchant Center 或其他 marketplace API。
- Marketplace、UCP 或 feed 字段作为规划和人工核对参考；没有真实 feed/API 数据时必须标注缺口。
