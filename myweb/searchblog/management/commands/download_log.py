from django.core.management.base import BaseCommand
from searchblog.models import SearchQueryLog, ClickLog 
import os
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = 'Download Logs'
    def handle(self, *args, **kwargs):
        def export_logs():
            # 确保输出目录存在
            output_dir = '/Users/liuvivian/Blog_Search_Engine/logs'
            os.makedirs(output_dir, exist_ok=True)

            # 生成包含当前时间戳的文件名
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"logs_{current_time}.txt"

            # 导出搜索查询日志和点击日志到同一个文件
            with open(os.path.join(output_dir, file_name), 'w') as file:
                # 写入搜索查询日志
                search_logs = SearchQueryLog.objects.all()
                file.write("Search Query Logs:\n")
                for log in search_logs:
                    file.write(f"{log.user} searched for '{log.query}' on {log.timestamp}\n")
                
                file.write("\nClick Logs:\n")
                # 写入点击日志
                click_logs = ClickLog.objects.all()
                for log in click_logs:
                    file.write(f"{log.user} clicked on '{log.url}' at {log.timestamp}\n")
        
        export_logs()
