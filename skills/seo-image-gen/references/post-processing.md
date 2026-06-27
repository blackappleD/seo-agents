# 后处理管道参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

> 当用户在生成后需要进行图像处理时，按需加载此内容。

## 先决条件

使用前检查可用性：

```bash
which magick    # ImageMagick 7 (preferred)
which convert   # ImageMagick 6 (fallback)
which ffmpeg    # For video/animation
```

如果不存在，请安装 ImageMagick：`sudo apt install imagemagick` (Debian/Ubuntu) 或 `brew install imagemagick` (macOS)。

## 常用操作

### 调整平台大小

```bash
# Instagram post (1080x1080)
magick input.png -resize 1080x1080^ -gravity center -extent 1080x1080 instagram.png

# Twitter/X header (1500x500)
magick input.png -resize 1500x500^ -gravity center -extent 1500x500 twitter-header.png

# YouTube thumbnail (1280x720)
magick input.png -resize 1280x720^ -gravity center -extent 1280x720 youtube-thumb.png

# LinkedIn banner (1584x396)
magick input.png -resize 1584x396^ -gravity center -extent 1584x396 linkedin-banner.png

# Favicon (multi-size ICO)
magick input.png -resize 32x32 favicon.ico
```

### 背景去除（透明度）

```bash
# Remove solid white background
magick input.png -fuzz 10% -transparent white output.png

# Remove solid color background (specify color)
magick input.png -fuzz 15% -transparent "#F0F0F0" output.png

# Clean edges after transparency (anti-alias)
magick input.png -fuzz 10% -transparent white -channel A -blur 0x1 -level 50%,100% output.png

# Auto-crop transparent padding
magick input.png -trim +repage output.png
```

### 格式转换

```bash
# PNG to WebP (web-optimized, smaller file)
magick input.png -quality 85 output.webp

# PNG to JPEG (with white background for transparency)
magick input.png -background white -flatten -quality 90 output.jpg

# PNG to AVIF (modern, smallest size)
magick input.png -quality 80 output.avif

# SVG trace (for logos; requires potrace)
potrace input.pbm -s -o output.svg
```

### 颜色调整

```bash
# Increase contrast
magick input.png -contrast-stretch 2%x1% output.png

# Warm color temperature
magick input.png -modulate 100,110,105 output.png

# Cool color temperature
magick input.png -modulate 100,90,95 output.png

# Desaturate (muted colors)
magick input.png -modulate 100,70,100 output.png

# Convert to grayscale
magick input.png -colorspace Gray output.png

# Sepia tone
magick input.png -sepia-tone 80% output.png
```

### 合成

```bash
# Overlay watermark (bottom-right, 20% opacity)
magick base.png watermark.png -gravity southeast -geometry +20+20 \
  -compose dissolve -define compose:args=20 -composite output.png

# Side-by-side comparison
magick input1.png input2.png +append comparison.png

# Vertical stack
magick input1.png input2.png -append stack.png

# Add padding/border
magick input.png -bordercolor white -border 40 output.png

# Add rounded corners
magick input.png \( +clone -alpha extract -draw \
  "roundrectangle 0,0,%[fx:w-1],%[fx:h-1],20,20" \) \
  -alpha off -compose CopyOpacity -composite rounded.png
```

### 批处理

```bash
# Resize all PNGs in directory
for f in ~/Documents/nanobanana_generated/*.png; do
  magick "$f" -resize 800x800 "${f%.png}_thumb.png"
done

# Convert all to WebP
for f in ~/Documents/nanobanana_generated/*.png; do
  magick "$f" -quality 85 "${f%.png}.webp"
done
```

## 动画（来自多个帧的 GIF/视频）

```bash
# Create GIF from multiple images
magick -delay 100 frame1.png frame2.png frame3.png animation.gif

# Create MP4 from image sequence
ffmpeg -framerate 1 -pattern_type glob -i '*.png' \
  -c:v libx264 -pix_fmt yuv420p slideshow.mp4
```

## 4K 输出注意事项

借助 Gemini 3.1 Flash 的 `imageSize: "4K"` 选项（高达 4096×4096），许多传统
不再需要升级后处理步骤。如果您的目标平台接受
4K 分辨率或低于 4K 分辨率的图像，以原生 4K 生成，而不是以 1K 生成
和升级。这会产生更良好细节并避免放大伪像。

## 绿屏透明度管道

Gemini 无法生成透明背景。使用此解决方法：

### 1.生成，绿屏提示

附加到任何提示：

```
on a solid bright green (#00FF00) chroma key background
with a thin white outline separating the subject from the background
```

### 2. 删除绿屏 (ImageMagick)

```bash
magick input.png -fuzz 20% -transparent "#00FF00" output.png
```

### 3.清理边缘+修剪(ImageMagick)

```bash
magick output.png -channel A -blur 0x1 -level 50%,100% -trim +repage final.png
```

### 4.替代方案（FFmpeg，更适合批量）

```bash
ffmpeg -i input.png -vf "colorkey=0x00FF00:0.3:0.1,despill=type=green" -pix_fmt rgba output.png
```

### 提示
- `-fuzz 20%` 处理边缘的轻微颜色变化；对于较软的边缘，增加至 25%
- 提示中的白色轮廓有助于防止颜色溢出到主题边缘
- 对于批处理，FFmpeg 方法速度更快并自动处理溢出
- 转换后始终验证边缘；可能需要手动修饰头发/毛皮

## 质量评估

```bash
# Get image dimensions and info
magick identify -verbose input.png | head -20

# Check file size
ls -lh input.png

# Get exact pixel dimensions
magick identify -format "%wx%h" input.png
```

## 本项目适配边界

- 图片生成、模型调用和后处理都可能依赖外部模型或本地工具；未配置时标注“未配置”。
- 生成商业图片时要记录 prompt、模型、成本、用途、版权/品牌约束和是否需要人工复核。
