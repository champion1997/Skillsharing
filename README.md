# skill-sharing

分享一些好玩的 skill

## 可用 Skills

### [Agnes AI 一键集成](agnes-ai-integration/)

一键集成 Agnes AI 三大免费模型：文本（agnes-2.0-flash）、生图（agnes-image-2.1-flash）、生视频（agnes-video-v2.0）。

**特点：**
- 全部免费，零 Token 消耗
- OpenAI 兼容接口，零学习成本
- 提供生图 + 生视频 CLI 脚本
- 支持图片识别（多模态输入）
- 支持图生视频

---

## 生图效果示例

### 示例 1：高端服务式公寓

**Prompt：** 一个高端服务式公寓的豪华客厅，现代简约风格，落地窗可以看到城市天际线，暖色调灯光，摄影级质量

![高端服务式公寓](https://platform-outputs.agnes-ai.space/images/text-to-image/2026/06/17ee7677fd7e4a199ce109def824ec8e.png)

### 示例 2：房地产投资报告封面

**Prompt：** 中国房地产投资分析报告封面，金色建筑剪影，深蓝色背景，专业商务风格，包含数据图表元素

![报告封面](https://platform-outputs.agnes-ai.space/images/text-to-image/2026/06/460d62a15f9f4f85a89de379a58395e5.png)

---

## 视频效果示例

### 示例：橘猫窗台

**Prompt：** 一只橘猫坐在阳光下的窗台上，镜头缓慢推进，金色光线，电影质感

**参数：** 241 帧 / 24fps = 约 10 秒

[![橘猫视频](https://storage.googleapis.com/agnes-aigc/aigc/videos/2026/06/12/video_1601b17e0d6961188c26eb6841719e763003e3a2bab9d2f5.mp4)](https://storage.googleapis.com/agnes-aigc/aigc/videos/2026/06/12/video_1601b17e0d6961188c26eb6841719e763003e3a2bab9d2f5.mp4)

> 点击链接查看视频，或复制链接到浏览器播放。

---

## 快速开始

1. 去 [platform.agnes-ai.com](https://platform.agnes-ai.com) 注册获取 API Key
2. 安装 `pip install requests pyyaml`
3. 把 API Key 写入 `~/.agnes_api_key`
4. 加载此 skill 即可使用

**完整文档见：** [agnes-ai-integration/SKILL.md](agnes-ai-integration/SKILL.md)
