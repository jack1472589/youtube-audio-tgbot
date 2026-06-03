# YouTube 音频下载 Telegram 机器人

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个**无需服务器**的 Telegram 机器人，可以从 YouTube 视频中提取和下载音频文件，**支持搜索功能**。

## ✨ 功能特性

- 📥 **一键下载** - 从 YouTube URL 提取音频
- 🔍 **搜索功能** - 输入关键词搜索 YouTube 视频
- 🎵 **MP3 格式** - 自动转换为高质量 MP3
- ⚡ **无需服务器** - 使用 Polling 方式，无需公网 IP
- 🐳 **Docker 支持** - 轻松部署
- ☁️ **云平台部署** - 支持 Railway、Vercel 等无服务器平台
- 🔘 **交互式界面** - 搜索结果用按钮展示

## 🚀 快速开始

### 前提条件

- Python 3.8+
- FFmpeg
- Telegram Bot Token（从 [@BotFather](https://t.me/botfather) 获取）

### 1. 获取 Telegram Bot Token

1. 在 Telegram 中找到 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot`
3. 按照提示给机器人取名字
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

复制 `.env.example` 为 `.env`：
```bash
cp .env.example .env
```

编辑 `.env`，填入你的 Token：
```
TELEGRAM_BOT_TOKEN=你的Bot_Token_这里
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

## ☁️ 云平台部署（推荐）

### Railway 部署（完全免费）

1. 访问 [Railway.app](https://railway.app)
2. 点击 **New Project** → **Deploy from GitHub repo**
3. 授权并选择 `youtube-audio-tgbot` 仓库
4. 在 **Variables** 中添加：
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: 你的 Bot Token
5. 点击 **Deploy** 完成

✅ 机器人将 24/7 自动运行

### Vercel 部署

1. Fork 此仓库
2. 访问 [Vercel.com](https://vercel.com)
3. 导入 GitHub 项目
4. 添加环境变量 `TELEGRAM_BOT_TOKEN`
5. 部署

## 📱 使用方法

### 命令列表

| 命令 | 说明 |
|------|------|
| `/start` | 显示欢迎信息 |
| `/help` | 显示帮助信息 |
| `/search 关键词` | 搜索 YouTube 视频 |

### 使用示例

#### 方式 1：直接下载

1. 在 Telegram 中找到你的机器人
2. 发送 YouTube 链接：
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
3. 等待下载完成，接收音频文件 🎵

#### 方式 2：搜索并下载

1. 发送搜索命令：
   ```
   /search 周杰伦 说好不哭
   ```
2. 机器人会显示搜索结果（最多 5 个）
3. 点击你想要的视频
4. 自动下载并发送音频 🎵

搜索结果显示：
- 视频标题
- 时长
- 观看次数
- 上传者

## ⚙️ 配置选项

在 `.env` 文件中可以配置：

| 选项 | 默认值 | 说明 |
|------|-------|------|
| `TELEGRAM_BOT_TOKEN` | - | Telegram Bot Token（必需） |
| `DOWNLOAD_DIR` | downloads | 下载文件保存目录 |
| `MAX_FILE_SIZE` | 50 | 最大文件大小（MB） |
| `DEBUG` | False | 调试模式 |

## 🔧 系统要求

### Ubuntu/Debian
```bash
sudo apt-get install ffmpeg python3-pip
```

### macOS
```bash
brew install ffmpeg python3
```

### Windows
- 从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载 FFmpeg
- 或使用 `choco install ffmpeg`
- 从 [python.org](https://www.python.org/) 下载 Python

## 📁 项目结构

```
youtube-audio-tgbot/
├── main.py                 # 机器人主程序（带搜索功能）
├── config.py               # 配置文件
├── youtube_handler.py      # YouTube 下载处理
├── youtube_search.py       # YouTube 搜索功能
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # Docker Compose
├── .env.example            # 环境变量示例
├── .gitignore              # Git 忽略文件
└── README.md               # 项目说明
```

## ❓ 常见问题

**Q: 无法找到 FFmpeg？**
A: 确保已安装 FFmpeg 并添加到系统 PATH

**Q: 文件大小超过限制？**
A: 长视频会产生大的 MP3 文件。可以在 `.env` 中增加 `MAX_FILE_SIZE`

**Q: 某些视频无法下载？**
A: 可能原因：
- YouTube 链接无效
- 视频地理位置受限
- 需要登录才能观看

**Q: 搜索不到结果？**
A: 尝试：
- 检查网络连接
- 使用简单的关键词
- 等待几秒重试

**Q: 机器人多久才能运行？**
A: 
- 本地：立即运行
- Railway：部署后 5 分钟内启动
- 云平台：通常 5-10 分钟

## 🐛 故障排除

### 机器人无响应

1. 检查 Bot Token 是否正确
2. 检查网络连接
3. 查看日志输出是否有错误

### 下载失败

1. 确保 YouTube URL 有效
2. 检查是否有网络连接
3. 试试其他视频

### 文件过大

- 减少视频长度
- 在 `.env` 中调整 `MAX_FILE_SIZE`

## 📝 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

jack1472589

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**⭐ 如果有帮助，请给个 Star！**

**📧 有问题？** 提交 Issue 或 Discussion

**🚀 想要新功能？** 欢迎提交 PR！