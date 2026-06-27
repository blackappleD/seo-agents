# 线框模板：IST/SOLL 模式

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

生成之前 (IST) 和之后 (SOLL) 线框图，显示页面当前的内容
看起来像与基于 SERP 预期的应该是什么样子。

## 核心原则

1. **超具体占位符**：不是“添加 CTA”，而是“添加年度定价 CTA”
   英雄下方的储蓄徽章，链接到/pricing#enterprise”
2. **移动优先**：首先假设375px视口；首屏 (~600px) 必须
   包含页面类型最关键的元素
3. **语义 HTML**：使用 HTML5 元素输出为部分大纲

## IST 一代

解析当前页面并映射到此结构：

```
IST: [URL]
├── ABOVE FOLD
│   ├── [element]: "[actual content]"
│   └── [element]: "[actual content]"
├── MAIN CONTENT
│   ├── [section]: "[summary]" (~XXX words)
│   └── [section]: "[summary]" (~XXX words)
├── SUPPORTING
│   └── [element]: "[description]"
└── FOOTER — [elements present]

Missing from SERP expectations:
- [element]: [why it matters]
```

## SOLL 模板（按页面类型）

### 1. 登陆页面

```
<header> Nav: logo + 3-4 links max + primary CTA button </header>
<section class="hero">
  H1: [value proposition matching target keyword]
  Subhead: [supporting benefit] | CTA: [primary action]
  Trust line: "Trusted by [X] companies including [logos]"
</section>
<section class="social-proof"> 3-5 logo badges + key metric </section>
<section class="features"> 3 blocks: icon + H3 + 2-line desc (address PAA) </section>
<section class="how-it-works"> 3-step process with numbered icons </section>
<section class="testimonial"> Quote + photo + name + title + company </section>
<section class="pricing"> 2-3 tiers, recommended highlighted, annual toggle </section>
<section class="faq"> 5-7 PAA questions, FAQPage schema </section>
<section class="final-cta"> Repeat hero CTA with urgency </section>
```

### 2. 博客文章

```
<article>
  <header> H1 | Author + photo + credentials | Date + Updated | Reading time </header>
  <nav class="toc"> Jump links to H2 sections </nav>
  <section class="intro"> Hook + thesis + TL;DR box (above fold) </section>
  <section> H2: [cluster 1] — address PAA #1 </section>
  <section> H2: [cluster 2] — address PAA #2 </section>
  <section> H2: [cluster 3] — comparison table if SERP warrants </section>
  <section> H2: [cluster 4] — image/diagram </section>
  <section class="expert-quote"> Blockquote from SME (E-E-A-T) </section>
  <section> H2: FAQ — remaining PAA questions </section>
  <footer> Author bio | Related posts (3) | CTA: newsletter </footer>
</article>
```

### 3.产品页面

```
<section class="product-hero">
  H1: [product + benefit keyword] | Gallery: 4-6 images
  Price + savings indicator | CTA: "Add to Cart" (above fold)
  Trust: stars + review count + shipping
</section>
<section class="key-features"> 4-6 bullets: feature + benefit </section>
<section class="specifications"> Table: specs, dimensions, compatibility </section>
<section class="reviews"> aggregateRating + 5 reviews, filterable </section>
<section class="comparison"> "Why choose this" table (if SERP shows intent) </section>
<section class="faq"> Product PAA questions </section>
<section class="related"> 4 complementary products </section>
```

### 4.比较页面

```
<header>
  H1: "[A] vs [B]: [year] Comparison"
  Quick verdict: "Best for [use case]: [winner]"
</header>
<section class="matrix"> Feature table: check/cross/partial icons </section>
<section class="reviews">
  H2: [A] — pros, cons, best for, pricing
  H2: [B] — pros, cons, best for, pricing
</section>
<section class="verdict"> Persona recs: "Choose A if...", "Choose B if..." </section>
<section class="faq"> Comparison PAA questions </section>
```

### 5.服务页面

```
<section class="hero"> H1: [service + location] | CTA: "Free Consultation" </section>
<section class="problem"> Empathy-driven problem statement </section>
<section class="process"> 3-5 numbered steps </section>
<section class="results"> 2-3 case studies with before/after metrics </section>
<section class="credentials"> Certs, experience, team </section>
<section class="pricing"> Packages or "starting at" </section>
<section class="faq"> PAA questions </section>
<section class="cta"> Repeat CTA + contact form </section>
```

### 6.本地页面

```
<section class="hero">
  H1: [service] in [city] — [business name]
  CTA: "Call Now" + "Get Directions" | NAP displayed
</section>
<section class="map"> Google Map embed + landmark directions </section>
<section class="services"> Location-specific services (unique content) </section>
<section class="reviews"> Review widget with reviewer locations </section>
<section class="hours"> openingHoursSpecification + "open now" </section>
<section class="about"> Team, history, community (location-specific) </section>
```

### 7. 工具/交互

```
<section class="tool" id="tool">
  H1: Free [Tool Name] — [purpose]
  Input: [fields/dropdowns/upload] (ABOVE FOLD)
  CTA: "Calculate" / "Generate" / "Check" | Output zone
</section>
<section class="instructions"> How to Use — 3 steps max </section>
<section class="explanation"> Educational depth for SEO </section>
<section class="faq"> Tool-specific PAA </section>
<section class="related-tools"> 3-4 related tools </section>
```

### 8.混合（教育+产品）

```
<section class="hero">
  H1: [education + product keyword] | Dual CTA: "Learn More" + "Try Free"
</section>
<section class="education"> Address awareness-stage PAA </section>
<section class="solution"> Bridge: how [Product] solves this </section>
<section class="features"> 3-4 benefit-framed features </section>
<section class="proof"> Case study or testimonial </section>
<section class="cta"> Match journey stage from SERP analysis </section>
<section class="faq"> Mix of educational + product PAA </section>
```

## 占位符规则

填充 SOLL 占位符时，请始终具体：

|不好（含糊）|好（具体）|
|----------|------------------|
| “添加 CTA”| “在英雄下面添加‘开始免费试用’按钮，绿色#2d6a4f，链接到/signup” |
| “包括社会证明”| “添加 3 个徽标（G2、Capterra、TrustRadius）+‘4.8/5，来自 2,300 条评论’”|
| “添加常见问题解答部分” | “添加 PAA 的 5 个常见问题解答：‘X 安全吗？’、‘X 需要多少钱？’……”|
| “增进信任” | “添加 SSL 徽章 +‘SOC 2 认证’横幅 + 客户数量”|
| “更多内容” | “在 H2 '[功能] 如何工作'下添加 400 字的部分并附有图表”|

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
