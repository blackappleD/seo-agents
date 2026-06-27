# seo-agents 的免费地图 API

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Updated: 2026-03-23

## 源密钥

- **文档**：每个服务的官方 API 文档
- **政策**：官方使用政策和条款

---

## Overpass API（发现竞争对手的最佳免费选项）

**基本网址：** `https://overpass-api.de/api/interpreter`
**文档：** https://wiki.openstreetmap.org/wiki/Overpass_API
**许可证：** ODbL（所需归属：“来自 OpenStreetMap 的数据”）

## 速率限制

- 基于插槽：每个 IP 约 2 个并发查询
- 指南：~10,000 个请求/天，~1 GB/天下载
- 默认超时：180 秒，每个查询 512 MiB 内存
- 使用 `[timeout:25]` 进行更轻松的查询

## 查询模板

**半径5公里内的餐厅：**

```bash
curl -s "https://overpass-api.de/api/interpreter" \
  --data-urlencode 'data=[out:json][timeout:25];(node["amenity"="restaurant"](around:5000,LAT,LNG);way["amenity"="restaurant"](around:5000,LAT,LNG););out body;>;out skel qt;'
```

**街道上的所有企业：**

```bash
curl -s "https://overpass-api.de/api/interpreter" \
  --data-urlencode 'data=[out:json][timeout:25];way["name"="STREET_NAME"]["addr:city"="CITY"];(._;>;);out body;'
```

**边界框中按类别划分的竞争对手 POI：**

```bash
curl -s "https://overpass-api.de/api/interpreter" \
  --data-urlencode 'data=[out:json][timeout:25];(node["amenity"="dentist"](SOUTH,WEST,NORTH,EAST);way["amenity"="dentist"](SOUTH,WEST,NORTH,EAST););out body;>;out skel qt;'
```

## 本地 SEO 的关键 OSM 标签

|类别 | OSM 标签 |示例 |
|----------|---------|---------|
|食品与饮料 | `amenity=restaurant`、`amenity=cafe`、`amenity=fast_food` |餐厅、咖啡馆、外卖|
|医疗保健 | `amenity=dentist`、`amenity=doctors`、`amenity=pharmacy` |牙科、医疗、药房 |
|法律 | `office=lawyer`、`office=notary` |律师事务所、公证人|
|家庭服务 | `craft=plumber`、`craft=electrician`、`craft=hvac` |行业、承包商|
|零售 | `shop=supermarket`、`shop=clothes`、`shop=car` |所有零售类型 |
|汽车 | `shop=car`、`shop=car_repair`、`amenity=fuel` |经销商、维修、燃气|
|款待 | `tourism=hotel`、`tourism=motel`、`tourism=guest_house` |住宿 |
|金融| `amenity=bank`、`office=insurance`、`office=accountant` |银行、保险、会计|

## 响应字段

每个元素返回：`id`、`lat`、`lon`、`tags` 对象，其中包含 `name`、`phone`、`website`、`opening_hours`、`addr:street`、`addr:housenumber`、`addr:city`、`addr:postcode`、`cuisine`、`brand`、等等

## 限制

- 没有评论、评级或受欢迎程度数据
- 没有GBP特定信息
- 数据质量因地区而异（欧洲优秀，其他地方不一致）
- 志愿者提供的数据；可能已经过时了
- 交互式测试仪：https://overpass-turbo.eu/

---

## Geoapify Places API（结构化 POI 搜索）

**基本网址：** `https://api.geoapify.com/v2/places`
**文档：** https://apidocs.geoapify.com/docs/places/
**定价：** https://www.geoapify.com/pricing

## 免费套餐

- **3,000 credits/天**（1 credit = 返回 20 个 places）
- 5 个请求/秒
- 需要 API 密钥（免费注册，无需信用卡）
- **明确允许缓存和存储**（与 Google 不同）

## 查询模板

```bash
curl -s "https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=circle:LNG,LAT,5000&limit=20&apiKey=YOUR_KEY"
```

## 类别层次结构

使用点分隔的类别：`catering.restaurant`、`commercial.supermarket`、`healthcare.dentist`、`service.financial.accounting`、`commercial.vehicle.car_dealer`

## 响应格式

GeoJSON 特征集合。每个功能都有 `properties`：`name`、`city`、`state`、`postcode`、`country`、`street`、`housenumber`、`phone`、`website`、`categories`、`lat`、`lon`、`place_id`、 `formatted`（完整地址字符串）

## 相对于原始 Overpass 的优势

- 更清晰、结构化的响应
- 聚合数据（OSM + OpenAddresses + WhosOnFirst + GeoNames）
- 层次类别分类法
- 无利率限制意外（清晰的信用体系）

---

## Nominatim（仅限地理编码）

**基本网址：** `https://nominatim.openstreetmap.org`
**文档：** https://nominatim.org/release-docs/latest/api/Overview/
**政策：** https://operations.osmfoundation.org/policies/nominatim/

## 速率限制（严格）

- **1 个请求/秒**（绝对）
- 必须包含有效的 `User-Agent` 标头（库存库代理被拒绝）
- 自动完成查询**禁止**
- 公共实例上**禁止**批量地理编码
- 重复相同的查询会触发禁令（缓存结果）

## 正向地理编码

```bash
curl -s "https://nominatim.openstreetmap.org/search?q=123+Main+St+Austin+TX&format=json&addressdetails=1" \
  -H "User-Agent: seo-agents/1.7.0"
```

## 反向地理编码

```bash
curl -s "https://nominatim.openstreetmap.org/reverse?lat=40.7128&lon=-74.0060&format=json" \
  -H "User-Agent: seo-agents/1.7.0"
```

## 响应字段

`place_id`、`lat`、`lon`、`display_name`、`importance`、`category`、`type`、`address` 对象（门牌号、道路、城市、州、邮政编码、国家/地区）

## 最佳使用

- 地理网格中心点的地址到坐标转换
- 反向地理编码以验证公司地址
- **不适合**用于企业列表发现（使用 Overpass 或 Geoapify）

---

## 速率限制执行模式

```bash
# Nominatim: enforce 1 req/sec with sleep
for addr in "${addresses[@]}"; do
  curl -s "https://nominatim.openstreetmap.org/search?q=${addr}&format=json" \
    -H "User-Agent: seo-agents/1.7.0"
  sleep 1.1
done

# Overpass: no explicit rate limit, but use reasonable timeouts
# If HTTP 429 returned, implement exponential backoff

# Geoapify: 5 req/sec on free tier, no explicit enforcement needed
```

---

## 比较表

|功能 | Overpass | Geoapify | Nominatim |
|--------|---------|----------|-----------|
|商业发现|是（tags）|是（categories）|有限 |
|评论/评级 |否 |否 |否 |
|地理编码 |否 |是 | **最好** |
|速率限制 | ~10k/天 | 3k credits/天 | 1 请求/秒 |
|需要身份验证 |否 | API 密钥 |否 |
|允许缓存 |是 | **明确** | **必填** |
|数据质量 |区域差异明显 |聚合数据 |区域差异明显 |
|最适合 |半径内竞争对手搜索 |结构化 POI 搜索 |地址解析 |

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
