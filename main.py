#!/usr/bin/env python3
import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_BOT_TOKEN, DEBUG
from youtube_handler import YouTubeHandler

# 启用日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if DEBUG else logging.WARNING
)
logger = logging.getLogger(__name__)

yt_handler = YouTubeHandler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    await update.message.reply_text(
        "👋 欢迎使用 YouTube 音频下载机器人！\n\n"
        "📌 使用方法：\n"
        "只需发送任何 YouTube 链接，我会为你下载音频。\n\n"
        "⚠️ 注意：\n"
        "• 文件大小不能超过 50MB\n"
        "• 下载可能需要一些时间\n\n"
        "输入 /help 获取更多帮助"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    await update.message.reply_text(
        "🆘 帮助信息\n\n"
        "命令：\n"
        "/start - 显示欢迎信息\n"
        "/help - 显示此帮助信息\n\n"
        "用法：\n"
        "只需发送 YouTube URL，机器人会自动下载音频。\n\n"
        "示例：\n"
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理音频下载"""
    url = update.message.text.strip()
    
    # 验证 URL
    if not ("youtube.com" in url or "youtu.be" in url):
        await update.message.reply_text("❌ 请发送有效的 YouTube URL")
        return
    
    # 发送处理中消息
    status_msg = await update.message.reply_text("⏳ 正在处理，请稍候...")
    
    try:
        logger.info(f"开始下载: {url}")
        
        # 下载音频
        file_path = yt_handler.download_audio(url)
        
        # 编辑状态消息
        await status_msg.edit_text("📤 正在上传文件...")
        
        # 发送音频文件
        with open(file_path, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                caption="✅ 下载完成！"
            )
        
        # 删除状态消息
        await status_msg.delete()
        logger.info(f"下载完成: {file_path}")
        
    except Exception as e:
        logger.error(f"下载错误: {str(e)}")
        await status_msg.edit_text(f"❌ 错误: {str(e)}")
    finally:
        # 清理文件
        yt_handler.cleanup_old_files()

def main():
    """启动机器人"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ 错误: 缺少 TELEGRAM_BOT_TOKEN")
        print("请在 .env 文件中设置 TELEGRAM_BOT_TOKEN")
        sys.exit(1)
    
    # 创建应用
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # 添加处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    
    # 启动机器人
    logger.info("🚀 机器人启动中...")
    print("🚀 机器人启动中... (按 Ctrl+C 停止)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()