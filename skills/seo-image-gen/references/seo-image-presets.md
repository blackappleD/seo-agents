# SEO 图像预设

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

针对常见 SEO 图像用例的预配置预设。这些映射到香蕉的
预设格式（有关架构详细信息，请参阅 `references/presets.md`）。

## 预设模板

### og-default:标准 OG/社交预览

```json
{
  "name": "og-default",
  "description": "Clean, professional OG image for social sharing",
  "aspect_ratio": "16:9",
  "resolution": "1K",
  "domain_mode": "Product",
  "style": {
    "colors": ["#FFFFFF", "#F5F5F5"],
    "mood": "Professional, clean, trustworthy",
    "lighting": "Bright, even studio lighting with soft shadows",
    "typography": "Modern sans-serif if text needed"
  },
  "post_processing": "magick output.png -resize 1200x630^ -gravity center -extent 1200x630 output-og.webp"
}
```

### blog-hero：宽屏博客hero image

```json
{
  "name": "blog-hero",
  "description": "Dramatic widescreen hero for blog posts",
  "aspect_ratio": "16:9",
  "resolution": "2K",
  "domain_mode": "Cinema",
  "style": {
    "colors": ["contextual"],
    "mood": "Dramatic, atmospheric, editorial",
    "lighting": "Golden hour or moody blue hour, directional",
    "typography": "None:image only"
  },
  "post_processing": "magick output.png -quality 85 output-hero.webp"
}
```

### 产品白色：电子商务产品拍摄

```json
{
  "name": "product-white",
  "description": "Clean white background product photography",
  "aspect_ratio": "4:3",
  "resolution": "2K",
  "domain_mode": "Product",
  "style": {
    "colors": ["#FFFFFF"],
    "mood": "Clean, professional, catalog-ready",
    "lighting": "360-degree soft studio lighting, minimal shadows",
    "typography": "None"
  },
  "prompt_suffix": "Studio product photography, clean white background, professional catalog shot, high resolution",
  "post_processing": "magick output.png -fuzz 5% -transparent white output-transparent.png"
}
```

### 社交广场：社交媒体广场

```json
{
  "name": "social-square",
  "description": "1:1 square image for social media platforms",
  "aspect_ratio": "1:1",
  "resolution": "1K",
  "domain_mode": "UI/Web",
  "style": {
    "colors": ["brand-contextual"],
    "mood": "Engaging, scroll-stopping, platform-native",
    "lighting": "Bright, even, high-contrast",
    "typography": "Bold sans-serif if text needed, under 25 characters"
  }
}
```

### infographic-vertical：数据密集型信息图

```json
{
  "name": "infographic-vertical",
  "description": "Tall vertical infographic for data visualization",
  "aspect_ratio": "2:3",
  "resolution": "4K",
  "domain_mode": "Infographic",
  "style": {
    "colors": ["brand-contextual", "data-visualization palette"],
    "mood": "Informative, structured, authoritative",
    "lighting": "Flat, even, no dramatic shadows",
    "typography": "Clear hierarchy:headline, subheads, body, captions"
  },
  "notes": "Use thinking: high for better text rendering accuracy"
}
```

### favicon-mark：网站图标/应用程序图标

```json
{
  "name": "favicon-mark",
  "description": "Minimal iconic mark for favicon or app icon",
  "aspect_ratio": "1:1",
  "resolution": "512",
  "domain_mode": "Logo",
  "style": {
    "colors": ["2-3 brand colors max"],
    "mood": "Minimal, recognizable, scalable",
    "lighting": "Flat, no shadows",
    "typography": "Single letter or symbol only"
  },
  "post_processing": "magick output.png -resize 32x32 favicon.ico && magick output.png -resize 180x180 apple-touch-icon.png"
}
```

## 创建自定义预设

用户可以创建自己的预设：

```bash
python3 ~/.claude/skills/seo-image-gen/scripts/presets.py create my-brand
```

这将创建具有完整架构的 `~/.banana/presets/my-brand.json`。
指定时，自定义预设会覆盖 SEO 默认值。

## 预设选择逻辑

1. 如果用户指定用例命令（og、hero、product），则加载匹配的预设
2. 如果用户提到品牌预设名称，则从 `~/.banana/presets/` 加载
3.品牌预设覆盖颜色、情绪和版式的SEO预设
4. SEO预设始终提供宽高比和分辨率默认值

## 本项目适配边界

- 图片生成、模型调用和后处理都可能依赖外部模型或本地工具；未配置时标注“未配置”。
- 生成商业图片时要记录 prompt、模型、成本、用途、版权/品牌约束和是否需要人工复核。
