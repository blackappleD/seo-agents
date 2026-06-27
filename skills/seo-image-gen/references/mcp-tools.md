# MCP 工具参考：@ycse/nanobanana-mcp

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

> Package: `@ycse/nanobanana-mcp`  
> GitHub: https://github.com/YCSE/nanobanana-mcp

## 工具

### `gemini_generate_image`

根据文本 prompt 生成图片。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| `prompt` | string | 是 | 要生成的图片文本描述 |

返回：图片数据和文件路径，默认保存到 `~/Documents/nanobanana_generated/`。

示例：

```text
User: "Generate a sunset over mountains in watercolor style"
Agent: calls gemini_generate_image with prompt
Result: image path and description
```

### `gemini_edit_image`

使用文本说明编辑现有图片。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| `imagePath` | string | 是 | 要编辑的图片文件路径 |
| `prompt` | string | 是 | 编辑说明 |

返回：修改后的图片数据和文件路径。

示例：

```text
User: "Remove the background from ~/Documents/photo.png"
Agent: calls gemini_edit_image with imagePath and prompt
```

### `gemini_chat`

多轮视觉对话，保留会话上下文，适合保持角色、风格、构图和迭代修改的一致性。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| `message` | string | 是 | 聊天消息，可引用之前生成或输入的图片 |

返回：文本响应和可选图片。

### `set_aspect_ratio`

设置后续图片生成的宽高比。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| `ratio` | string | 是 | 宽高比，例如 `16:9`、`1:1`、`9:16` |

支持比例：`1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`2:3`、`3:2`、`4:5`、`5:4`、`1:4`、`4:1`、`1:8`、`8:1`、`21:9`。

### `set_model`

切换活跃 Gemini 模型。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| `model` | string | 是 | 模型标识符 |

可用模型：

- `gemini-3.1-flash-image-preview`：默认，推荐。
- `gemini-2.5-flash-image`：稳定后备。

### `get_image_history`

获取当前会话中生成的图片列表。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| 无 | - | - | 不需要参数 |

返回：包含路径和 prompt 的图片条目数组。

### `clear_conversation`

重置会话上下文和对话历史。

| 参数 | 类型 | 必填 | 描述 |
|---|---|---|---|
| 无 | - | - | 不需要参数 |

返回：重置确认。

## 环境变量

| 变量 | 必填 | 描述 |
|---|---|---|
| `GOOGLE_AI_API_KEY` | 是 | Google AI Studio API key，来源：https://aistudio.google.com/apikey |
| `NANOBANANA_MODEL` | 否 | 覆盖默认模型，例如 `gemini-3.1-flash-image-preview` |

## 输出目录

所有生成图片默认保存到 `~/Documents/nanobanana_generated/`，文件通常按时间戳命名，便于追踪生成历史。

## MCP 功能可用性

部分较新的 Gemini API 功能取决于 `@ycse/nanobanana-mcp` 的 package 版本。执行前应检查 package 版本和工具 schema。

| 功能 | API 状态 | MCP 支持 |
|---|---|---|
| `imageSize` 分辨率控制 | 可用 | 取决于 package 版本 |
| `thinkingConfig` thinking level | 可用 | 取决于 package 版本 |
| Search grounding (`googleSearch`) | 可用 | 取决于 package 版本 |
| 仅图片输出 (`responseModalities: ["IMAGE"]`) | 可用 | 取决于 package 版本 |
| 多图片输入，最多 14 张参考图 | 可用 | 通过 `gemini_chat` 和图片路径 |
| 全部 14 种宽高比 | 可用 | 通过 `set_aspect_ratio` |

如果 MCP package 尚未支持某个功能，可以通过 `curl` 或 Google AI SDK 直接调用，但要先确认用户希望使用外部模型/API。

## 本项目适配边界

- 图片生成、模型调用和后处理都可能依赖外部模型或本地工具；未配置时标注“未配置”。
- 生成商业图片时要记录 prompt、模型、成本、用途、版权/品牌约束和是否需要人工复核。
- 不声称已经生成、编辑或上传图片，除非当前任务确实调用工具并取得文件路径或输出证据。
