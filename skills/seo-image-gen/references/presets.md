# 品牌/风格预设参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

> 当用户询问预设或品牌一致性时按需加载此内容。

## 预设架构

每个预设存储为 `~/.banana/presets/NAME.json`：

```json
{
  "name": "tech-saas",
  "description": "Clean tech SaaS brand",
  "colors": ["#2563EB", "#1E40AF", "#F8FAFC"],
  "style": "clean minimal tech illustration, flat vectors, soft shadows",
  "typography": "bold geometric sans-serif",
  "lighting": "bright diffused studio, no harsh shadows",
  "mood": "professional, trustworthy, modern",
  "default_ratio": "16:9",
  "default_resolution": "2K"
}
```

## 预设示例

### 技术SaaS
- **颜色：** #2563EB、#1E40AF、#F8FAFC（蓝色 + 白色）
- **风格：**干净的最小技术插图、平面矢量、柔和的阴影
- **排版：** 粗体几何无衬线字体
- **心情：**专业、值得信赖、现代

### 奢侈品牌
- **颜色：** #1A1A1A、#C9A96E、#FAFAF5（黑色 + 金色 + 奶油色）
- **风格：** 优雅高端摄影，纹理丰富，对比度深
- **版式：** 纤细优雅的衬线，宽大的字母间距
- **心情：** 独特、精致、有抱负

### 社论杂志
- **颜色：** #000000、#FFFFFF、#FF3B30（黑色 + 白色 + 强调红色）
- **风格：** 大胆的编辑摄影，强烈的几何构图
- **排版：** 压缩全大写无衬线标题
- **情绪：** 大胆、挑衅、现代

## 预设如何合并到推理摘要中

当预设处于活动状态时，当前 Agent 使用其值作为推理摘要的默认值：
1. **颜色** → 通知上下文和样式组件中的调色板描述
2. **Style** → 成为 Style 组件的基础
3. **排版** → 用于任何文本渲染
4. **Lighting** → 成为Lighting组件的基础
5. **情绪** → 影响动作和情境成分

用户指令总是覆盖预设值。如果用户说“将其变暗”
但预设有明亮的灯光，请遵循用户的指示。

## 管理预设

```bash
# List presets
presets.py list

# Show details
presets.py show tech-saas

# Create interactively (当前 Agent fills in details from conversation)
presets.py create NAME --colors "#hex,#hex" --style "..." --mood "..."

# Delete
presets.py delete NAME --confirm
```

## 本项目适配边界

- 图片生成、模型调用和后处理都可能依赖外部模型或本地工具；未配置时标注“未配置”。
- 生成商业图片时要记录 prompt、模型、成本、用途、版权/品牌约束和是否需要人工复核。
