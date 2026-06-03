#!/usr/bin/env python3
import logging
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_BOT_TOKEN, DEBUG
from youtube_handler import YouTubeHandler
from youtube_search import YouTubeSearch

# 启用日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if DEBUG else logging.WARNING
)
logger = logging.getLogger(__name__)

yt_handler = YouTubeHandler()
yt_search = YouTubeSearch()

# 存储用户搜索结果
user_search_results = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    await update.message.reply_text(
        "👋 欢迎使用 YouTube 音频下载机器人！\n\n"
        "📌 使用方法：\n"
        "1️⃣ 发送 YouTube 链接直接下载\n"
        "2️⃣ 使用 /search 关键词 搜索视频\n\n"
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
        "/help - 显示此帮助信息\n"
        "/search <关键词> - 搜索 YouTube 视频\n\n"
        "使用方法：\n"
        "1️⃣ 直接发送 YouTube URL\n"
        "2️⃣ 或输入: /search 关键词\n\n"
        "示例：\n"
        "/search 周杰伦 (搜索相关视频)"
    )

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /search 命令 - 搜索视频"""
    
    # 获取搜索关键词
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供搜索关键词\n\n"
            "使用方法：/search 关键词\n"
            "示例：/search 周杰伦"
        )
        return
    
    query = ' '.join(context.args)
    user_id = update.effective_user.id
    
    # 发送搜索中消息
    status_msg = await update.message.reply_text(f"🔍 正在搜索: {query}...")
    
    try:
        logger.info(f"用户 {user_id} 搜索: {query}")
        
        # 执行搜索
        results = yt_search.search(query, max_results=5)
        
        if not results:
            await status_msg.edit_text("❌ 没有找到相关视频")
            return
        
        # 存储搜索结果
        user_search_results[user_id] = results
        
        # 构建按钮
        buttons = []
        for idx, video in enumerate(results, 1):
            # 格式化标题和信息
            title = video['title'][:30] + "..." if len(video['title']) > 30 else video['title']
            duration_min = video['duration'] // 60 if video['duration'] else 0
            
            button_text = f"{idx}. {title} ({duration_min}分钟)"
            buttons.append([
                InlineKeyboardButton(
                    button_text, 
                    callback_data=f"download_{idx-1}"
                )
            ])
        
        # 创建键盘
        keyboard = InlineKeyboardMarkup(buttons)
        
        # 删除搜索中消息
        await status_msg.delete()
        
        # 发送结果
        result_text = f"🎬 找到 {len(results)} 个结果，请选择：\n\n"
        for idx, video in enumerate(results, 1):
            duration_min = video['duration'] // 60 if video['duration'] else 0
            views = format_views(video['views'])
            result_text += f"{idx}. {video['title']}\n"
            result_text += f"   ⏱️ {duration_min}分钟 | 👁️ {views}次观看\n"
            result_text += f"   📤 {video['uploader']}\n\n"
        
        await update.message.reply_text(
            result_text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"搜索错误: {str(e)}")
        await status_msg.edit_text(f"❌ 搜索失败: {str(e)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮点击"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    # 获取用户的搜索结果
    if user_id not in user_search_results:
        await query.edit_message_text("❌ 搜索结果已过期，请重新搜索")
        return
    
    try:
        # 解析回调数据
        action, video_idx = query.data.split('_')
        video_idx = int(video_idx)
        
        video = user_search_results[user_id][video_idx]
        url = video['url']
        
        logger.info(f"用户 {user_id} 选择下载: {url}")
        
        # 编辑消息为下载中
        await query.edit_message_text(
            f"📥 正在下载：{video['title']}\n⏳ 请稍候..."
        )
        
        # 下载音频
        file_path = yt_handler.download_audio(url)
        
        # 编辑消息为上传中
        await query.edit_message_text(
            f"📤 正在上传：{video['title']}\n⏳ 请稍候..."
        )
        
        # 发送音频文件
        with open(file_path, 'rb') as audio_file:
            await query.message.reply_audio(
                audio=audio_file,
                caption=f"✅ {video['title']}\n\n🎵 已下载完成！"
            )
        
        # 删除下载中消息
        await query.edit_message_text("✅ 下载并上传完成！")
        
    except Exception as e:
        logger.error(f"下载错误: {str(e)}")
        await query.edit_message_text(f"❌ 错误: {str(e)}")
    finally:
        # 清理文件
        yt_handler.cleanup_old_files()

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理音频下载 - 直接链接"""
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

def format_views(views):
    """格式化观看次数"""
    if views is None:
        return "N/A"
    if views >= 1000000:
        return f"{views / 1000000:.1f}M"
    elif views >= 1000:
        return f"{views / 1000:.1f}K"
    else:
        return str(views)

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
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    
    # 启动机器人
    logger.info("🚀 机器人启动中...")
    print("🚀 机器人启动中... (按 Ctrl+C 停止)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()