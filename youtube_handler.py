import os
import subprocess
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
                url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"下载失败: {result.stderr}")
            
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
            raise Exception("下载超时")
        except Exception as e:
            raise Exception(f"错误: {str(e)}")
    
    def cleanup_old_files(self):
        """清理旧文件"""
        for file in Path(self.download_dir).glob("*.mp3"):
            try:
                os.remove(file)
            except:
                pass