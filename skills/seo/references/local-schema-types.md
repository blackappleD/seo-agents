# 本地架构类型和行业特定模式（2026 年 3 月）

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Updated: 2026-03-23

模式不是直接的排名因素（已确认：John Mueller、Gary Illyes）。它通过丰富的结果（点击率提高 43%，Webstix 案例研究）、更良好实体理解和人工智能搜索功能间接影响可见性。

---

## Google 支持的 LocalBusiness 子类型

## 食品与餐饮

|架构类型 |用于 |
|-------------|---------|
| `Restaurant` |全方位服务餐厅|
| `CafeOrCoffeeShop` |咖啡店、咖啡馆|
| `BarOrPub` |酒吧、酒馆、酒馆 |
| `Bakery` |面包店|
| `FastFoodRestaurant` |快餐，快捷服务|
| `IceCreamShop` |冰淇淋、冷冻酸奶|
| `FoodEstablishment` |普通食品（如果存在特定亚型则避免）|

## 卫生保健

|架构类型 |用于 |
|-------------|---------|
| `MedicalClinic` |诊所、紧急护理（有资格获得丰富结果）|
| `Hospital` |医院（有资格获得丰富结果）|
| `Dentist` |牙科诊所（有资格获得丰富结果）|
| `Physician` |个人医生页面（与 Person 一起使用）|
| `Optician` |眼睛护理、眼镜店|
| `Pharmacy` |药房 |
| `MedicalBusiness` |通用医疗（如果存在特定亚型则避免）|

## 合法的

|架构类型 |用于 |笔记|
|------------|---------|--------|
| `LegalService` |律师事务所、法律实践| **正确类型** |
| ~~`Attorney`~~ | ~~个人律师~~ | **已被 Schema.org 弃用。使用 `LegalService` + `Person`** |

## 家庭服务

|架构类型 |用于 |
|-------------|---------|
| `Plumber` |管道服务|
| `Electrician` |电力服务|
| `HVACBusiness` |供暖、通风、空调 |
| `RoofingContractor` |屋顶|
| `GeneralContractor` |总承包|
| `HousePainter` |喷漆服务|
| `Locksmith` |锁匠服务|
| `MovingCompany` |搬家服务|
| `HomeAndConstructionBusiness` |通用（如果存在特定子类型则避免）|

## 房地产

|架构类型 |用于 |笔记|
|------------|---------|--------|
| `RealEstateAgent` |代理和经纪|不存在 `RealEstateBrokerage` 类型 |

## 汽车

|架构类型 |用于 |
|-------------|---------|
| `AutoDealer` |销售部门|
| `AutoRepair` |服务部门 |
| `AutoPartsStore` |零件部门 |

## 其他常见本地类型

`AnimalShelter`、`BeautySalon`、`ChildCare`、`DaySpa`、`DryCleaningOrLaundry`、`EmergencyService`、`EmploymentAgency`、`EntertainmentBusiness`、`FinancialService`、`FireStation`、`FurnitureStore`、`GasStation`、`GolfCourse`、`GovernmentOffice`、 `HealthClub`、`Hotel`、`InsuranceAgency`、`Library`、`LodgingBusiness`、`NightClub`、`PetStore`、`PoliceStation`、`PostOffice`、`RecyclingCenter`、`ShoppingCenter`、`SkiResort`、`SportsActivityLocation`、`Store`、 `TouristInformationCenter`、`TravelAgency`、`VeterinaryCare`

---

## 必需属性与推荐属性

根据 Google Developers 文档（2025 年 12 月 10 日更新，已确认）。

## 必需（最少）

|属性 |类型 |备注|
|----------|------|--------|
| `name` |文字|公司名称必须与GBP完全匹配 |
| `address` |邮政地址 |包含街道地址、地址地点、地址区域、邮政编码 |

## 受到推崇的

|属性 |类型 |备注|
|----------|------|--------|
| `aggregateRating` |综合评级 |带有 reviewCount 的评级摘要 |
| `geo` |地理坐标| **最少 5 位小数**（已确认，~1.1m 精度）|
| `openingHoursSpecification` |开放时间规格 |标准、深夜、24 小时、季节性 |
| `telephone` |文字|必须与 GBP 和 NAP 页相匹配 |
| `url` |网址 |此位置的规范 URL |
| `priceRange` |文字| 100 个字符以下 |
| `image` |网址 |商业照片|
| `review` |评论 |个人评论 |
| `department` |本地企业 |对于嵌套部门（汽车经销商）|
| `menu` | URL 或菜单 |仅限餐厅 |
| `servesCuisine` |文字|仅限餐厅 |

## SAB 特定

|属性 |类型 |备注|
|----------|------|--------|
| `areaServed` |地点/地理形状 |不在 Google 官方推荐列表中，但受 Schema.org 支持。行业推荐用于 SAB。使用带有 `sameAs` 维基百科/维基数据链接的命名城市。 |

---

## 行业特定的架构模式

## 餐厅

```
Restaurant (or specific subtype)
  + Menu > MenuSection > MenuItem (name, price, nutrition, suitableForDiet)
  + ReserveAction (booking capabilities)
  + OrderAction (takeout/delivery)
  + servesCuisine, acceptsReservations
```

注意：Google Food Ordering (GFO) 直接结帐已于 2024 年 6 月停止。“在线订购”按钮现在重定向到第三方平台。

## 卫生保健

```
MedicalClinic (or Hospital, Dentist)
  + Physician pages: Person + medicalSpecialty + hospitalAffiliation + hasCredential
  + MedicalSpecialty (helps match "hip replacement surgery" to relevant pages)
  + sameAs: link to NPI Registry entry and medical board page
```

**HIPAA 限制**：无法确认/否认审阅者是审阅回复中的患者。良好先例：30,000 美元（马纳萨健康中心，2023 年）。

## 合法的

```
LegalService (NOT Attorney -- deprecated)
  + Person on attorney bio pages: jobTitle, worksFor, alumniOf, hasCredential (bar admissions)
  + makesOffer > Service (one per practice area)
  + Practitioner GBP: unique phone per attorney, not sole lawyer at firm
```

注意：当律师更换公司时，审查将遵循从业者列表。

## 家庭服务

```
Specific subtype (Plumber, Electrician, etc.)
  + areaServed: named cities with sameAs to Wikipedia/Wikidata
  + Service on individual service pages, linked via provider
  + hasOfferCatalog for service listings
```

**SAB 注意**：GBP的服务区域目前不会影响排名 - 排名基于验证地址（Sterling Sky，2025 年 3 月）。

## 房地产

```
RealEstateAgent (for both agent and brokerage)
  + Person on agent pages: memberOf (brokerage), credentials
  + RealEstateListing + SingleFamilyResidence/Apartment + Offer (pricing)
  + Event for open houses with organizing agent
```

注意：Schema.org 上不存在 `RealEstateBrokerage` 类型。

## 汽车

```
AutoDealer (sales)
  + Car/Vehicle: VIN, mileage, fuelType, vehicleTransmission
  + Offer: price, priceCurrency, availability
  + Separate GBP: AutoRepair (service), AutoPartsStore (parts)
```

**VehicleListing 已于 2025 年 6 月 12 日弃用**（已确认）。请改用汽车 + 优惠。通过 Google Merchant Center 基于 Feed 的车辆列表仍然有效。

---

## 特定行业的引文来源

## 餐厅
Yelp、TripAdvisor（1B+ 评论）、OpenTable（DA + 预订）、DoorDash、UberEats、Grubhub、Foursquare（为 Apple 地图、Uber 提供支持）

## 医疗保健
Healthgrades（50% 的就诊美国人）、Zocdoc（预约 + 潜在客户生成）、WebMD 医生目录（高 DA）、Vitals、Doximity（80% 的美国医生）、NPI 注册中心（实体验证真实来源）、州医疗委员会目录

## 法律
FindLaw（DA~91，dofollow）、Martindale-Hubbell（DA~84，自 1868 年以来的同行评审）、Avvo（1-10 评级，根据律师数据自动创建）、Justia（DA~70，免费配置文件）、Super Lawyers（前 5%，基于选择）、州律师目录（实体验证）

注：Internet Brands (KKR) 拥有 Avvo + Martindale + Lawyers.com + Nolo。汤森路透拥有 FindLaw + Super Lawyers + LawInfo。

## 家庭服务
Thumbtack（2024 年收入 4 亿美元，与 ChatGPT/Alexa/Zillow 集成）、BBB、Nextdoor、Yelp。 **下降**：Angi（收入较 2022 年峰值-30%）、Porch（转向保险）、Houzz（转向 SaaS）

## 房地产
Zillow（占所有 RE 搜索流量的 44%，于 2025 年 10 月整合到 ChatGPT）、Homes.com（排名第二，超过 Realtor.com，每月访问量达 1 亿）、Realtor.com、Redfin（2025 年 3 月被 Rocket Companies 收购）、本地 MLS 网站

## 汽车
Cars.com、AutoTrader、CarGurus、DealerRater（Cars.com + OEM 网站的评论集团，支持销售人员评级）、Edmunds、Kelley Blue Book（定价权威）、OEM 制造商经销商定位器（实体验证）

---

## 多位置架构模式

```json
// Homepage: Organization with branchOf references
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#org",
  "name": "Brand Name",
  "url": "https://example.com"
}

// Each location page: individual LocalBusiness
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "@id": "https://example.com/locations/downtown/#location",
  "name": "Brand Name - Downtown",
  "branchOf": { "@id": "https://example.com/#org" },
  "address": { ... },
  "geo": { "latitude": "40.71234", "longitude": "-74.00567" },
  "telephone": "+1-555-123-4567",
  "openingHoursSpecification": [ ... ]
}
```

使用 `@id` 作为每个位置的唯一标识符。建议的子目录结构：`domain.com/locations/city-name/`（子目录比子域更好地巩固链接资产，Bruce Clay 研究：50%+ 流量提升）。

---

## 已弃用/无效的本地架构

|类型 |状态 |日期 |使用替代 |
|------|--------|------|------------|
| `Attorney` |已被 Schema.org 弃用 | --| `LegalService` + `Person` |
| `VehicleListing` |丰富的结果已删除 | 2025 年 6 月 12 日 | `Car` + `Offer` |
| `HowTo` |丰富的结果已删除 | 2023 年 9 月 |无 |
| `SpecialAnnouncement` |已弃用 | 2025 年 7 月 31 日 |无 |

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
