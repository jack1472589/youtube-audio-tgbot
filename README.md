# YouTube 音频下载 Telegram 机器人

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个**无需服务器**的 Telegram 机器人，可以从 YouTube 视频中提取和下载音频文件。

## ✨ 功能特性

- 📥 **一键下载** - 只需发送 YouTube 链接
- 🔊 **MP3 格式** - 自动转换为高质量 MP3
- ⚡ **无需服务器** - 使用 Polling 方式，无需公网 IP
- 🐳 **Docker 支持** - 轻松部署
- ☁️ **云平台部署** - 支持 Railway、Vercel 等
- 🔒 **安全可靠** - 开源代码，隐私有保障

## 🚀 快速开始

### 前提条件

- Python 3.8+
- FFmpeg
- Telegram Bot Token

### 1. 获取 Telegram Bot Token

1. 在 Telegram 中找到 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot`
3. 按照提示输入机器人名称
4. 复制得到的 Token

### 2. 本地运行

**克隆仓库：**
```bash
git clone https://github.com/jack1472589/youtube-audio-tgbot.git
cd youtube-audio-tgbot
```

**安装依赖：**
```bash
pip install -r requirements.txt
```

**配置环境变量：**

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Token：
```
TELEGRAM_BOT_TOKEN=你的Token
DOWNLOAD_DIR=downloads
MAX_FILE_SIZE=50
```

**启动机器人：**
```bash
python main.py
```

### 3. Docker 运行

**构建镜像：**
```bash
docker build -t youtube-audio-bot .
```

**运行容器：**
```bash
docker run -e TELEGRAM_BOT_TOKEN=你的Token youtube-audio-bot
```

**使用 docker-compose：**
```bash
docker-compose up -d
```

## ☁️ 云平台部署

### Railway 部署（推荐）

1. 访问 [Railway.app](https://railway.app)
2. 点击 **New Project**
3. 选择 **Deploy from GitHub repo**
4. 授权并选择 `youtube-audio-tgbot` 仓库
5. 在 **Variables** 中添加 `TELEGRAM_BOT_TOKEN`
6. 点击 **Deploy**

### Vercel 部署

1. Fork 此仓库
2. 访问 [Vercel.com](https://vercel.com)
3. 导入 GitHub 项目
4. 添加环境变量 `TELEGRAM_BOT_TOKEN`
5. 部署

## 📱 使用方法

1. 在 Telegram 中找到你的机器人
2. 点击 **START** 按钮
3. 发送任何 YouTube 链接，例如：
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
4. 等待机器人下载完成
5. 接收音频文件 🎵

## 🎮 命令列表

| 命令 | 说明 |
|------|------|
| `/start` | 显示欢迎信息 |
| `/help` | 显示帮助信息 |

## ⚙️ 配置选项

在 `.env` 文件中可以配置：

| 选项 | 默认值 | 说明 |
|------|-------|------|
| `TELEGRAM_BOT_TOKEN` | - | Telegram Bot Token |
| `DOWNLOAD_DIR` | downloads | 下载保存目录 |
| `MAX_FILE_SIZE` | 50 | 最大文件大小（MB） |
| `DEBUG` | False | 调试模式 |

## 🔧 系统需求

**Ubuntu/Debian：**
```bash
sudo apt-get install ffmpeg
```

**macOS：**
```bash
brew install ffmpeg
```

**Windows：**
- 从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
- 或使用 `choco install ffmpeg`

## ❓ 常见问题

**Q: 无法找到 FFmpeg？**
A: 确保已安装 FFmpeg 并添加到系统 PATH。

**Q: 文件大小超过限制？**
A: 长视频可能会产生大于 50MB 的 MP3 文件。可以在 `.env` 中增加 `MAX_FILE_SIZE`。

**Q: 某些视频无法下载？**
A: 可能原因：
- YouTube 链接不合法
- 视频地理位置受限
- 需要登录才能观看

**Q: Bot 运行在哪里？**
A: 
- 本地：你的电脑
- 云平台：Railway/Vercel 服务器（24/7 运行）

## 📝 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

jack1472589

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**⭐ 如果有帮助，请给个 Star！**