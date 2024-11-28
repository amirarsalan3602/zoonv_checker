# import subprocess
# pid = subprocess.run(["pgrep", '-a', "v2ray"], capture_output=True, text=True, check=True)
# print(pid)
import re

# import requests
# import time
#
# import requests
# import time
#
#
# def calculate_download_speed(file_url="http://cachefly.cachefly.net/10mb.test"):
#     CHUNK_SIZE = 1024  # حجم هر قطعه به بایت
#     DOWNLOAD_DURATION = 10  # مدت زمان دانلود به ثانیه
#     total_bytes = 0
#     start_time = time.time()
#
#     with requests.get(file_url, stream=True) as response:
#         for chunk in response.iter_content(CHUNK_SIZE):
#             total_bytes += len(chunk)
#             elapsed_time = time.time() - start_time
#             if elapsed_time >= DOWNLOAD_DURATION:
#                 break
#
#     download_speed_kb = total_bytes / elapsed_time / 1024  # به کیلوبایت بر ثانیه تبدیل می‌کنیم
#     download_speed_mb = download_speed_kb / 1024  # به مگابایت بر ثانیه تبدیل می‌کنیم
#     return download_speed_mb
#
#
# file_url = "http://cachefly.cachefly.net/10mb.test"
# avg_speed = calculate_download_speed(file_url)
# print(f"میانگین سرعت دانلود: {avg_speed:.2f} مگابایت بر ثانیه")



