import requests
from typing import List, Dict

class YouTubeSearch:
    """YouTube 视频搜索"""
    
    def __init__(self):
        # 使用 yt-dlp 的搜索功能
        self.search_url = "https://www.youtube.com/results"
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        搜索 YouTube 视频
        
        Args:
            query: 搜索关键词
            max_results: 最多返回结果数
            
        Returns:
            视频列表
        """
        try:
            import yt_dlp
            
            # 使用 yt-dlp 搜索
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch',
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch{max_results}:{query}"
                result = ydl.extract_info(search_query, download=False)
            
            videos = []
            if 'entries' in result:
                for video in result['entries']:
                    videos.append({
                        'title': video.get('title', 'Unknown'),
                        'url': video.get('url', ''),
                        'duration': video.get('duration', 0),
                        'uploader': video.get('uploader', 'Unknown'),
                        'views': video.get('view_count', 0),
                    })
            
            return videos
        
        except Exception as e:
            raise Exception(f"搜索失败: {str(e)}")