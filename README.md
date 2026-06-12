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

**适用场景：**
- Hermes Agent 加载此 skill 后可直接使用
- 任何 OpenAI 兼容框架（Claude Code、Codex 等）配置环境变量即可
- 需要快速搭建 AI 生图/生视频能力的开发者

**快速开始：**
1. 去 [platform.agnes-ai.com](https://platform.agnes-ai.com) 注册获取 API Key
2. 安装 `pip install requests pyyaml`
3. 把 API Key 写入 `~/.agnes_api_key`
4. 加载此 skill 即可使用
