# YouTube 音频下载机器人 - 安装指南

## 前置要求

### 1. Python 依赖
```bash
pip install -r requirements.txt
```

### 2. **重要**: 安装 JavaScript 运行时（必需）

YouTube 现在需要 JavaScript 运行时来解析视频信息。建议安装 **deno**：

#### Linux/Mac:
```bash
curl -fsSL https://deno.land/install.sh | sh
# 添加 deno 到 PATH
export PATH="$HOME/.deno/bin:$PATH"
```

#### Windows (PowerShell):
```powershell
irm https://deno.land/install.ps1 | iex
```

#### 或使用 Docker（推荐用于生产环境）

Dockerfile 已配置好，直接运行：
```bash
docker-compose up -d
```

### 3. 验证安装

```bash
# 检查 yt-dlp 版本
yt-dlp --version

# 检查 deno 是否安装
deno --version
```

## 配置

1. 复制 `.env.example` 到 `.env`：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，设置你的 Telegram Bot Token：
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
DEBUG=true
```

## 运行

### 本地运行：
```bash
python main.py
```

### Docker 运行：
```bash
docker-compose up -d
```

## 常见问题

### 错误：HTTP Error 429: Too Many Requests
- 这是 YouTube 的速率限制
- 解决方案：等待几分钟后重试，或使用 cookies 进行身份验证

### 错误：No supported JavaScript runtime
- 需要安装 deno（见上面的安装步骤）
- 验证：`deno --version`

### 错误：Sign in to confirm you're not a bot
- YouTube 需要验证你的身份
- 解决方案：稍后重试，或提供浏览器 cookies

## 性能优化

当前配置包含：
- **速率限制**: 100,000 字节/秒（防止 429 错误）
- **重试机制**: 3 次重试
- **超时**: 300 秒
- **Socket 超时**: 30 秒

这些设置在 `youtube_handler.py` 中配置。

## 支持

如有问题，请查看 yt-dlp 官方文档：
- https://github.com/yt-dlp/yt-dlp
- https://github.com/yt-dlp/yt-dlp/wiki/FAQ
