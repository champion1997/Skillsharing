---
name: agnes-ai-integration
description: "一键集成 Agnes AI 三大免费模型：文本(agnes-2.0-flash)、生图(agnes-image-2.1-flash)、生视频(agnes-video-v2.0)。提供完整配置脚本和 CLI 工具，任何 agent 框架加载此 skill 后输入 API Key 即可使用。"
version: 2.0.0
author: "champion1997"
tags: [agnes, sapiens, api, image-generation, video-generation, multi-modal, free]
---

# Agnes AI 一键集成技能

Agnes AI 提供三个免费模型，全部 OpenAI 兼容，零 Token 消耗：
- **文本+视觉**：`agnes-2.0-flash` — 多模态，支持图片输入（聊天+看图）
- **图片生成**：`agnes-image-2.1-flash` — 文生图 + 图生图
- **视频生成**：`agnes-video-v2.0` — 文生视频 + 图生视频

## 一键部署（3 步搞定）

### 第 1 步：安装依赖

```bash
pip install requests pyyaml
```

### 第 2 步：保存 API Key

把 Agnes API Key 保存到 `~/.agnes_api_key`：

```bash
echo "sk-你的密钥" > ~/.agnes_api_key
chmod 600 ~/.agnes_api_key
```

去 https://platform.agnes-ai.com 注册/登录获取。

### 第 3 步：配置模型

根据你的 Agent 框架，在配置文件中添加：

#### Hermes Agent
```yaml
model:
  default: agnes-2.0-flash
  provider: custom
  base_url: https://apihub.agnes-ai.com/v1
  api_key: sk-xxx

auxiliary:
  vision:
    provider: custom
    model: agnes-2.0-flash
    base_url: https://apihub.agnes-ai.com/v1
```

#### Claude Code / Codex / 其他 OpenAI 兼容客户端
```
OPENAI_BASE_URL=https://apihub.agnes-ai.com/v1
OPENAI_API_KEY=***
MODEL=agnes-2.0-flash
```

## 生图示例

### 示例 1：高端服务式公寓

- **Prompt：** `一个高端服务式公寓的豪华客厅，现代简约风格，落地窗可以看到城市天际线，暖色调灯光，摄影级质量`
- **尺寸：** 1024x768
- **结果：** https://platform-outputs.agnes-ai.space/images/text-to-image/2026/06/17ee7677fd7e4a199ce109def824ec8e.png

### 示例 2：房地产投资报告封面

- **Prompt：** `中国房地产投资分析报告封面，金色建筑剪影，深蓝色背景，专业商务风格，包含数据图表元素`
- **尺寸：** 1024x768
- **结果：** https://platform-outputs.agnes-ai.space/images/text-to-image/2026/06/460d62a15f9f4f85a89de379a58395e5.png

## 视频示例

### 示例：橘猫窗台

- **Prompt：** `一只橘猫坐在阳光下的窗台上，镜头缓慢推进，金色光线，电影质感`
- **参数：** 241 帧 / 24fps = 约 10 秒
- **结果：** https://storage.googleapis.com/agnes-aigc/aigc/videos/2026/06/12/video_1601b17e0d6961188c26eb6841719e763003e3a2bab9d2f5.mp4

## 生图 CLI 工具

脚本：`scripts/agnes_image.py`

```bash
# 基本用法
python3 agnes_image.py '<prompt>' [size] [model]

# 示例
python3 agnes_image.py "一只猫在键盘上"
python3 agnes_image.py "现代售楼处大厅" 1024x768
python3 agnes_image.py "产品图" 512x512 agnes-image-2.0-flash
```

输出：JSON 格式的图片 URL，不下载到本地。

**生图 API 注意事项：**
- `response_format` 必须放在 `extra_body` 里，放顶层会 400 错误
- 图生图：输入图片放在 `extra_body.image` 数组里，可以是 URL 或 Data URI

## 生视频 CLI 工具

脚本：`scripts/agnes_video.py`

```bash
# 基本用法
python3 agnes_video.py '<prompt>' [width] [height] [frames] [fps]

# 示例
python3 agnes_video.py "一只猫在海滩散步"
python3 agnes_video.py "日落海边" 1152 768 121 24
```

输出：JSON 格式的视频 URL，不下载到本地。

**生视频注意事项：**
- `num_frames` 必须 = 8n+1 且 ≤ 441
- 默认 121 帧 24fps = 5秒视频
- 要更长的视频：用 241 帧（10秒）或 441 帧（18秒）
- 异步任务：提交→轮询→返回 URL
- 提交请求 timeout 要设 120 秒（API 可能慢）
- 轮询接口是 `/agnesapi`（不带 `/v1` 前缀）
- 提交接口是 `/v1/videos`（带 `/v1` 前缀）

## 视频时长对照表

| num_frames | frame_rate | 时长 |
|-----------|-----------|------|
| 121       | 24        | 5秒  |
| 161       | 24        | 6.7秒|
| 241       | 24        | 10秒 |
| 321       | 24        | 13.4秒|
| 441       | 24        | 18.4秒|

## 视觉（图片识别）— ⚠️ 重要

**关键：必须用 agnes-2.0-flash（chat 模型）做视觉，不能用 agnes-image-2.1-flash！**

agnes-image-2.1-flash 是一个图片**生成**模型，不是聊天视觉接口。切到它做视觉识别只能看到颜色分布，完全看不出内容。

正确配置：
```yaml
auxiliary:
  vision:
    provider: custom
    model: agnes-2.0-flash  # ← 必须是 chat 模型！
    base_url: https://apihub.agnes-ai.com/v1
```

`agnes-2.0-flash` 支持图片输入，格式同 OpenAI 多模态：

```python
import requests

r = requests.post(
    "https://apihub.agnes-ai.com/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_KEY", "Content-Type": "application/json"},
    json={
        "model": "agnes-2.0-flash",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图里有什么？"},
                {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}}
            ]
        }]
    }
)
```

## 图生视频

给视频 API 传一张图片的 URL：

```python
r = requests.post(
    "https://apihub.agnes-ai.com/v1/videos",
    headers={"Authorization": "Bearer YOUR_KEY", "Content-Type": "application/json"},
    json={
        "model": "agnes-video-v2.0",
        "prompt": "让这个图片动起来，镜头缓缓推进",
        "image": "https://example.com/photo.jpg",
        "mode": "ti2vid",
        "num_frames": 121,
        "frame_rate": 24
    }
)
```

## 视频 Prompt 写法

格式：`[主体] + [动作] + [场景] + [运镜] + [光线] + [风格]`

示例：`"一只橘猫(主体)慢慢走着(动作)在夕阳下的海滩(场景)镜头缓缓推进(运镜)金色光线(光线)电影质感(风格)"`

## 常见问题

1. **401**：API Key 无效/过期，去 platform.agnes-ai.com 重新生成
2. **503**：模型通道繁忙，稍后重试
3. **视频生成慢**：异步任务，通常 2-3 分钟，脚本自动轮询
4. **图片 URL 打不开**：用浏览器直接访问，微信内不支持预览
5. **视频 URL 打不开**：Google Storage 链接，复制链接到浏览器播放
