import os
import subprocess
import time
from pathlib import Path
from config import DOWNLOAD_DIR, MAX_FILE_SIZE

class YouTubeHandler:
    """处理 YouTube 音频下载"""
    
    def __init__(self):
        self.download_dir = DOWNLOAD_DIR
        Path(self.download_dir).mkdir(exist_ok=True)
    
    def download_audio(self, url: str) -> str:
        """下载 YouTube 视频的音频"""
        try:
            output_template = os.path.join(
                self.download_dir, 
                "%(title)s.%(ext)s"
            )
            
            cmd = [
                "yt-dlp",
                "-x",  # 仅提取音频
                "--audio-format", "mp3",
                "--audio-quality", "192",
                "-o", output_template,
                # 添加以下选项以解决 YouTube 限制
                "--socket-timeout", "30",
                "--hls-prefer-ffmpeg",
                "--no-part",
                # 添加延迟以避免速率限制 (字节/秒)
                "--ratelimit", "100000",
                # 重试设置
                "--retries", "3",
                "--fragment-retries", "3",
                url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                error_msg = result.stderr
                # 检查常见的 YouTube 错误
                if "429" in error_msg:
                    raise Exception("❌ 错误: YouTube 请求过多，请稍后再试")
                elif "Sign in to confirm" in error_msg:
                    raise Exception("❌ 错误: YouTube 需要验证，请稍后再试")
                elif "No supported JavaScript runtime" in error_msg:
                    raise Exception("❌ 错误: 需要安装 JavaScript 运行时。请运行: pip install deno")
                else:
                    raise Exception(f"下载失败: {error_msg}")
            
            # 查找下载的文件
            mp3_files = list(Path(self.download_dir).glob("*.mp3"))
            if not mp3_files:
                raise Exception("找不到下载的文件")
            
            file_path = max(mp3_files, key=os.path.getctime)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            if file_size_mb > MAX_FILE_SIZE:
                os.remove(file_path)
                raise Exception(f"文件过大 ({file_size_mb:.1f}MB > {MAX_FILE_SIZE}MB)")
            
            return str(file_path)
            
        except subprocess.TimeoutExpired:
            raise Exception("下载超时 - 视频过长或网络不稳定")
        except Exception as e:
            raise Exception(f"错误: {str(e)}")
    
    def cleanup_old_files(self):
        """清理旧文件"""
        for file in Path(self.download_dir).glob("*.mp3"):
            try:
                os.remove(file)
            except:
                pass
