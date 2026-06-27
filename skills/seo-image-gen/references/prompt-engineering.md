# 提示工程参考：seo-image-gen

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

> 在构造复杂提示或用户时按需加载此内容
> 询问提示技巧。不要在启动时加载。
>
> 与 Google 2026 年 3 月发布的 Gemini 图像生成“终极提示指南”保持一致。

## 目录

- [The 6-Component Reasoning Brief](#the-6-component-reasoning-brief) -- 主题、动作、背景、构图、风格、技术
- [Domain Mode Modifier Libraries](#domain-mode-modifier-libraries) -- 摄影、产品、社论、信息图表修饰符
- [Advanced Techniques](#advanced-techniques) -- 负面提示、迭代细化、批次变异
- [Prompt Adaptation Rules](#prompt-adaptation-rules) -- 特定于型号的调整
- [Common Prompt Mistakes](#common-prompt-mistakes) -- 要避免的反模式
- [Proven Prompt Templates](#proven-prompt-templates) -- 按用例列出的即用型模板
- [Safety Filter Rephrase Strategies](#safety-filter-rephrase-strategies) -- 阻止提示的解决方法

## 六部分推理简介

每个图像提示都应该包含这些组件，写得自然
叙述性段落，切勿作为逗号分隔的关键字列表。

### 1. 主题
图像的主要焦点。用物理特性进行描述。

**好：** “一位70多岁、饱经风霜的日本陶艺家，深深的阳光蚀刻
皱纹映射了数十年的窑炉工作，长满老茧的双手抱着
新扔的茶碗，带有不规则的有机边缘”

**坏：**“老人、陶瓷、碗”

### 2.行动
发生了什么。动作、姿势、手势、存在状态。

**好：**“全神贯注地向前倾，轻轻抚平
拇指沾湿了边缘，一条细细的滑痕顺着他的手腕流下来”

**坏：**“制作陶器”

### 3. 背景
环境、设置、时间和空间细节。

**好：** “在传统的燃木阿那迦窑作坊内，
晚间，柔和的背景中可见堆放的干燥罐架子
午后的光线透过宣纸屏风”

**不好：**“研讨会，下午”

### 4. 组成
摄像机角度、镜头类型、取景、空间关系。

**好：**“从略低于视线水平的亲密特写镜头，
浅景深将手和碗与物体隔离
后面车间的柔和散景”

**不好：**“特写”

### 5. 照明
光源、质量、方向、温度、阴影。

**好：**“来自左侧高窗摄像机的温暖定向光，
用柔和的三角形在脸上创造出柔和的伦勃朗光线
阴影侧脸颊上的光线，车间里深沉温暖的阴影”

**不好：**“自然采光”

### 6.风格
艺术媒介、美学参考、技术摄影细节。

**好：**“使用 Sony A7R IV、85mm f/1.4 GM 镜头、Kodak Portra 拍摄
400 种颜色分级，带有提升的阴影和柔和的大地色调，令人怀念
多萝西娅·兰格的纪实肖像”

**不好：**“逼真，8K，杰作”

## 域模式修饰符库

### 影院模式
**相机规格：** RED V-Raptor、ARRI Alexa 65、Sony Venice 2、Blackmagic URSA
**镜头：** Cooke S7/i、Zeiss Supreme Prime、Atlas Orion anamorphic
**胶片库存：** Kodak Vision3 500T（钨丝灯）、Kodak Vision3 250D（日光）、Fuji Eterna Vivid
**灯光设置：** 三点、明暗、伦勃朗、分体、蝴蝶、边缘/背光
**镜头类型：**建立广角、中特写、极特写、荷兰角、吊车、斯坦尼康跟踪
**颜色分级：** 青色和橙色、去饱和冷色、暖复古色、高对比度黑色

### 产品模式
**表面：** 抛光大理石、拉丝混凝土、原亚麻、丙烯酸立管、渐变扫面
**照明：** 柔光箱漫射、带填充卡的硬键、边缘分离、帐篷照明、光绘
**角度：** 45 度英雄、平躺、四分之三、直视、虫眼
**风格参考：** Apple 产品摄影、Aesop mini、Bang & Olufsen clean、奢华化妆品

### 肖像模式
**焦距：** 85mm（经典）、105mm（压缩）、135mm（长焦）、50mm（环境）
**光圈：** f/1.4（梦幻散景）、f/2.8（拍摄对象清晰）、f/5.6（环境背景）
**姿势语言：**坦率的中间姿势、直接对着镜头的对抗、侧面轮廓、过肩扫视
**皮肤/纹理：** 雀斑可见，宏观距离毛孔，眼睛捕捉光线，次表面散射

### 编辑/时尚模式
**出版物参考：** 《Vogue》意大利版、《Harper's Bazaar》、《GQ》、《国家地理》、《Kinfolk》
**造型注意事项：**分层纹理、个性配饰、单色调色板、对比图案
**地点：**大理石楼梯、黄金时段的屋顶、工业阁楼、沙漠沙丘、霓虹灯照亮的小巷
**姿势：**力量姿势、轻松的编辑精益、运动模糊、风中的织物

### UI/网页模式
**风格：**平面矢量、等距 3D、线条艺术、玻璃形态、同态、材料设计
**颜色：**指定精确的十六进制或描述性调色板（例如，“酷蓝#2563EB到#1E40AF”）
**尺寸：** 视网膜设计为 2 倍，指定所需的精确像素尺寸
**背景：** 透明（要求纯白色然后后期处理）、渐变、纯色

### 标志模式
**构造：**几何基元、黄金比例、基于网格、负空间
**排版：** 粗体无衬线、优雅衬线、自定义字母标记、字母组合
**颜色：** 最多 2-3 种颜色，适用于单色、高对比度
**输出：**纯白色背景上的请求，后处理为透明

### 风景模式
**深度层：**前景兴趣、中景主题、背景氛围
**大气：** 雾、薄雾、薄雾、体积光线、灰尘颗粒
**一天中的时间：** 蓝色时刻（黎明前）、黄金时刻、神奇时刻（日落后）、午夜蓝色
**天气：** 剧烈的暴风云、雨后放晴、冰雪覆盖、阳光斑驳

### 信息图模式
**布局：** 模块化部分、清晰的视觉层次、便当网格、从上到下的流程
**文本：** 使用引号表示准确的文本、描述性字体样式、指定大小层次结构
**数据即：**条形图、饼图、流程图、时间线、比较表
**颜色：** 高对比度、易于使用的调色板、一致的品牌颜色

### 抽象模式
**几何：** 分形、泰森镶嵌、螺旋、斐波那契、有机流、晶体
**纹理：** 大理石纹理、流体动力学、烟雾、墨水扩散、水彩渗色
**调色板：** 相似和谐、互补冲突、单色渐变、霓虹黑
**风格：**生成艺术、数据可视化艺术、故障、程序、材料的宏观摄影

## 先进技术

### 字符一致性（多轮）
使用 `gemini_chat` 并维护描述性锚点：
- 第一回合：生成具有详尽物理描述的角色
- 后续轮流：参考“相同字符”+重复2-3个关键标识符
- 关键标识符：头发颜色/风格、独特的服装、面部特征

**多图像参考技术**（3.1 Flash）：
- 在对话中提供最多 4-5 个角色参考图像
- 为每个角色分配不同的名称（“角色A：红发骑士”）
- 模型保留不同角度、动作和环境的特征
- 当参考图像从多个角度显示角色时效果最佳

### 没有参考图像的风格转移
详尽地描述目标风格而不是引用图像：

```
Render this scene in the style of a 1950s travel poster: flat areas of
color in a limited palette of teal, coral, and cream. Bold geometric
shapes with visible paper texture. Hand-lettered title text with a
mid-century modern typeface feel.
```

### 文本渲染技巧
- 引用确切文本：`with the text "OPEN DAILY" in bold condensed sans-serif`
- **25 个字符或更少**：这是可靠渲染的实际限制
- **最多 2-3 个不同的短语**：更多文本片段会降低质量
- 描述字体特征，而不是字体名称
- 指定位置：“在顶部三分之一处居中”、“沿着底部边缘”
- 高对比度：深色文本浅色，反之亦然
- **文本优先黑客：** 首先通过对话建立文本概念（“我需要一个标有新鲜面包的标志”），然后生成。该模型锚定前面提到的文本
- 期待创造性的字体解释，而不是所描述样式的精确复制

### 积极框架（无消极提示）
Gemini 不支持负面提示。重新表述排除：
- 而不是“无模糊”→“清晰、对焦、清晰的细节”
- 而不是“无人”→“空旷、荒凉、无人居住”
- 而不是“没有文字”→“干净、整洁、无文字”
- 代替“不暗”→“明亮、高调的照明”

### 以搜索为基础的一代
对于基于真实世界数据（天气、事件、统计数据）的图像，
Gemini 可以使用 Google Search grounding 整合实时信息。
对于包含当前数据的信息图表很有用。

**基于搜索的提示的三部分公式：**
1. `[Source/Search request`：查找什么
2. `[Analytical task`：要分析或提取什么
3. `[Visual translation`：如何将其渲染为图像

**示例：**“按 2026 年 GitHub 使用情况搜索当前排名前 5 的编程语言，分析它们的相对受欢迎程度百分比，然后生成一个干净的信息图表条形图，其中包含现代深色主题中的语言徽标和百分比。”

## 提示适配规则

当改编来自 claude-prompts 数据库的提示时（Midjourney/DALL-E/等）
Gemini 的自然语言格式：

|源语法 | Gemini 等价写法 |
|--------------|--------------------|
| `--ar 16:9` |单独致电 `set_aspect_ratio("16:9")` |
| `--v 6`、`--style raw` |删除 - Gemini 没有版本/样式标志 |
| `--chaos 50` |描述多样性：“意想不到的、超现实的构图” |
| `--no trees` |正面框架：“没有植被的开阔空地”|
| `(word:1.5)` 重量 |描述性强调：“突出[词]”|
| `8K, masterpiece, ultra-detailed` |只保留“超写实、高分辨率”；删除其余的 |
|逗号分隔的标签 |扩展为描述性叙述段落 |
| `shot on Hasselblad` | Keep - 相机规格在 Gemini 中运行良好 |

## 常见提示错误

1. **关键词堆砌**：堆叠通用质量术语（“8K、杰作、最佳质量”）不会增加任何内容。最后仅使用“超现实、高分辨率”
2. **标签列表**：Gemini 更适合自然语言段落，而不是“红车、日落、山峰、电影”
3. **缺少照明**：最大的质量差异化因素
4. **无构图方向**：导致通用居中框架
5. **模糊的风格**：“让它看起来很酷”与特定的艺术方向
6. **忽略宽高比**：始终在生成前设置
7. **超长提示**：递减返回超过~200字；准确而不冗长
8. **文本长度超过约 25 个字符**：超过此限制后，渲染速度会迅速下降
9. **将关键细节埋在最后**：在长提示中，放在最后的细节可能会被降低优先级；将关键细节（确切的文本、关键约束）放在提示的前三分之一中
10. **不进行后续提示迭代**：使用 `gemini_chat` 进行渐进式细化，而不是试图在一代内把所有事情都做好

## 经过验证的提示模板

> 从 2,500 多个经过测试的提示中提取。这些模式始终如一地产生
> 高质量的结果。使用它们作为起点并适应要求。

### 获胜公式（重量分布）

|组件|重量 |包括什么 |
|------------|--------------------|-----------------|
| **主题** | 40% |年龄、肤色、发色/发型、眼睛颜色、体型、表情 |
| **造型** | 25% |品牌名称、质地、版型、配饰、颜色 |
| **环境** | 15% |位置+一天中的时间+上下文详细信息|
| **相机** | 10% |相机型号+镜头+焦距+拍摄类型 |
| **照明** | 10% |质量、方向、色温、阴影 |

### Instagram 广告/社交媒体

**图案：** `[Subject with age/appearance] + [outfit with brand/texture] + [action verb] + [setting] + [camera spec] + [lighting] + [platform aesthetic]`

**示例（产品植入）：**

```
Hyper-realistic gym selfie of athletic 24yo influencer with glowing olive
skin, wearing crinkle-textured athleisure set in mauve. iPhone 16 Pro Max
front-facing portrait mode capturing sweat droplets on collarbones, hazel
eyes enhanced by gym LED lighting. Mirror reflection shows perfect form,
golden morning light through floor-to-ceiling windows. Frayed chestnut
ponytail with baby hairs, ultra-detailed skin texture, trending aesthetic.
```

**示例（生活方式广告）：**

```
A 24-year-old blonde fitness model in a high-energy sports drink
advertisement. Mid-run on a beach, wearing a vibrant orange sports bra
and black shorts, playful smile and sparkling blue eyes exuding vitality.
Bottle of the drink held in hand, waves crashing in background. Shot on
Nikon D850 with 70-200mm f/2.8 lens, natural light, fast shutter speed
capturing motion. Ultra-realistic skin texture, water droplets, product
label clearly visible.
```

**示例（奢华生活方式）：**

```
Gorgeous Instagram model wearing a designer silk gown, luxury rooftop
restaurant, golden hour lighting, champagne in hand, luxurious aspirational
lifestyle. Captured with Sony A7R IV, 85mm f/1.4 lens, shallow depth of
field, warm color grading.
```

### 产品/商业摄影

**图案：** `[Product with brand/detail] + [dynamic elements] + [surface/setting] + "commercial photography for advertising campaign" + [lighting] + "high resolution"`

**示例（饮料）：**

```
Gatorade bottle with condensation dripping down the sides, surrounded by
lightning bolts and a burst of vibrant blue and orange light rays. The
Gatorade logo is prominently displayed on the bottle, with splashes of
water frozen in mid-air. Commercial food photography for an advertising
campaign, high resolution, high level of detail, vibrant complementary
colors.
```

**示例（食物）：**

```
In and Out burger with layers of fresh lettuce, melted cheese, and pretzel
bun, placed on a white surface with the In and Out logo subtly glowing in
the background. Falling french fries and golden light, warm scene.
Commercial food photography for an advertising campaign, high resolution,
high level of detail, vibrant complementary colors.
```

### 时尚/社论

**图案：** `[Subject with ethnicity/age/features] + [outfit with texture/brand/cut] + [location] + [pose/action] + [camera + lens] + [lighting quality]`

**示例（街头风格）：**

```
A 24-year-old female AI influencer posing confidently in an urban cityscape
during golden hour. Flawless sun-kissed skin, long wavy brown hair, deep
green eyes. Wearing a chic streetwear outfit: oversized beige blazer,
white top, high-waisted jeans. Captured with Sony A7R IV at 85mm f/1.4,
shallow depth of field with warm golden bokeh.
```

**示例（高级时装）：**

```
Stunning 24-year-old woman, long platinum blonde hair, radiant skin,
piercing blue eyes, dressed in a chic pastel blazer with a modern
minimalist aesthetic, soft sunlight glow, high-end fashion appeal.
Shot on Canon EOS R5, 85mm f/1.2 lens.
```

**示例（前卫）：**

```
A blonde fitness model transformed into a runway-ready fashion icon,
wearing a bold avant-garde outfit: cropped leather jacket with neon pink
accents, paired with high-waisted athletic shorts and knee-high boots.
Captured mid-stride on a minimalist white runway, playful twinkle in her
eye, dramatic studio lighting from above.
```

### SaaS/技术营销

**图案：** `[UI mockup or abstract visual] + "on [dark/light] background" + [specific colors with hex] + [typography description] + "clean, premium SaaS aesthetic" + [glassmorphism/gradient/glow effects]`

**示例（仪表板英雄）：**

```
A floating glassmorphism UI card on a deep charcoal background showing a
content analytics dashboard with a rising line graph in teal (#14B8A6),
bar charts in coral (#F97316), and a circular progress indicator at 94%.
Subtle grid lines, frosted glass effect with 20% opacity, teal glow
bleeding from the card edges. Clean premium SaaS aesthetic, no text
smaller than headline size.
```

**示例（功能亮点）：**

```
An isometric 3D illustration of interconnected data nodes on a dark navy
background. Each node is a glowing teal sphere connected by thin luminous
lines, forming a constellation pattern. One central node pulses brighter
with radiating rings. Modern tech illustration style with subtle depth
of field, volumetric lighting from below.
```

**示例（比较/前后）：**

```
Split-screen image: left side shows a cluttered, dim workspace with
scattered papers, red error indicators, and a frustrated expression
conveyed through a cracked coffee mug and tangled cables. Right side
shows a clean, organized dashboard interface glowing in teal and white
on a dark background, with smooth flowing lines and checkmarks. A sharp
vertical dividing line separates chaos from clarity.
```

### 标志/品牌

**图案：** `[Product/bottle/item] + "with [brand element] prominently displayed" + [dynamic visual elements] + "commercial photography" + [lighting style] + "high resolution, vibrant complementary colors"`

**例子：**

```
A sleek matte black bottle with a minimal white logo mark centered on the
label, surrounded by swirling gradient ribbons of teal and coral light.
The bottle sits on a reflective dark surface, sharp studio rim lighting
separating it from the background. Product photography for luxury
branding, high resolution, dramatic contrast.
```

### 使提示发挥作用的关键策略

1. **真实相机命名**：“索尼A7R IV”、“佳能EOS R5”、“iPhone 16 Pro Max”主播真实感
2. **指定精确的镜头**：“85mm f/1.4”为模型提供精确的景深信息
3. **使用年龄+种族+特征**：“24岁，橄榄色皮肤，淡褐色眼睛”胜过“一个人”
4. **造型名牌**：“Lululemon 垫子”、“Tom Ford 套装”触发特定的视觉联想
5. **包括微观细节**：“锁骨上的汗滴”，“婴儿的毛发粘在脖子上”
6. **添加平台上下文**：“Instagram美学”、“广告商业摄影”
7. **描述纹理**：“皱纹纹理”、“金属银”、“磨砂玻璃”
8. **使用动作动词**：“奔跑中”、“自信地摆姿势”、“跨步中捕捉”
9. **以“超现实、高分辨率”结尾**：这两个特定锚点对 Gemini 有帮助。避免诸如“8K、杰作、最佳质量”之类的通用堆叠，这不会增加任何价值
10. **对于产品，说“突出显示”**：确保产品/徽标不被隐藏

### 反模式（不该做什么）

- **“黑暗主题的 Instagram 广告显示......”**：太元，描述的是概念而不是图像
- **“时尚的 SaaS 仪表板可视化...”**：抽象，没有视觉锚点
- **“现代、干净、专业...”**：对模型来说毫无意义的模糊形容词
- **“大胆采取行动......”**：描述营销意图，而不是视觉内容
- **描述观众应该感受到什么**：相反，描述是什么创造了这种感觉

## 安全过滤器改写策略

Gemini 的安全过滤器（第 2 层：服务器端输出过滤器）无法禁用。
当提示被阻止时，唯一的出路就是重新措辞。

### 常见触发器类别

|类别 |触发 |改写方法|
|----------|------------|--------------------|
|暴力/武器 |战斗、血腥、伤害、枪械|使用比喻或后果：“久经沙场”→“饱经风霜的老兵” |
|医疗/血腥 |手术、伤口、解剖细节 |抽象或临床：“开放性伤口”→“医学插图”|
|真实的公众人物|名人、政治家|使用原型：“埃隆·马斯克”→“​​极简办公室里的科技企业家”|
|儿童+风险|任何模棱两可的情况下的未成年人 |添加安全背景：指定教育、家庭或有趣的框架 |
| NSFW/暗示 |暴露的服装、亲密的姿势|使用艺术框架：“时尚社论，全衣，社论姿势”|

### 改写模式

1. **抽象**：用抽象概念代替具体的危险元素
2. **艺术框架**：将内容框架为艺术、社论或纪录片
3. **隐喻**：使用符号语言代替字面描述
4. **积极强调**：描述存在的内容，而不是危险的内容
5. **环境转变**：从威胁环境转向教育/专业环境

### 改写示例

|阻止提示 |成功改写 |
|----------------|---------------------|
| “一名士兵在战斗中用步枪射击”| “一名坚定的士兵在黎明时站岗，步枪挎在肩上，晨雾笼罩着前哨”|
| “一个可怕的恐怖怪物”| “来自黑暗童话故事的奇幻生物，错综复杂的有机纹理，生物发光的口音，概念艺术风格”|
| “狗在打架”| “一只友良好金毛猎犬在阳光明媚的公园里精力充沛地玩耍，动作镜头，欢乐的表情”|
| “医疗手术场景”| “从观察廊看到干净的现代化手术室，柔和的蓝色手术灯，专业的纪实风格”|
| “[名字]的名人肖像”| “一位尊贵的中年男子，穿着定制的海军蓝西装，温暖的工作室灯光，社论肖像风格”|

### 关键原则

第 2 层（输出过滤器）分析生成的图像，而不仅仅是提示。
如果模型的解释触发过滤器，即使是措辞良好的提示也可能被阻止
输出滤波器。发生这种情况时，请尝试进一步转变视觉概念
从触发器而不仅仅是改变词语。

## 本项目适配边界

- 图片生成、模型调用和后处理都可能依赖外部模型或本地工具；未配置时标注“未配置”。
- 生成商业图片时要记录 prompt、模型、成本、用途、版权/品牌约束和是否需要人工复核。
