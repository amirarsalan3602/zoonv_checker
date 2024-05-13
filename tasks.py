import os
import time

import requests
from threading import Semaphore

from tools import Tools

application = Tools()
look = Semaphore(value=10)
# pip install requests[socks]
def calculate_download_speed(url_config, pid, port, file_url="http://cachefly.cachefly.net/10mb.test"):
    look.acquire()
    CHUNK_SIZE = 1024  # حجم هر قطعه به بایت
    DOWNLOAD_DURATION = 6  # مدت زمان دانلود به ثانیه
    total_bytes = 0
    start_time = time.time()

    proxies = {
        'http': f'socks5://127.0.0.1:{port}',
        'https': f'socks5://127.0.0.1:{port}',
    }
    print(port)
    try:
        with requests.get(file_url, stream=True, proxies=proxies, timeout=30) as response:
            for chunk in response.iter_content(CHUNK_SIZE):
                total_bytes += len(chunk)
                elapsed_time = time.time() - start_time
                if elapsed_time >= DOWNLOAD_DURATION:
                    break
        download_speed_kb = total_bytes / elapsed_time / 1024  # به کیلوبایت بر ثانیه تبدیل می‌کنیم
        download_speed_mb = download_speed_kb / 1024  # به مگابایت بر ثانیه تبدیل می‌کنیم
        application.accepted(url_config)
        print(url_config)
        application.cash.lrem("vless_urls", 1, url_config)
        os.system(f"kill {pid}")
        look.release()

        return f"{download_speed_mb} == {url_config}"
    except Exception as e:
        print(e)
        os.system(f"kill {pid}")
        application.cash.lrem("vless_urls", 1, url_config)
        application.refused += 1
        look.release()


# application.run_v2ray([
#     "vless://d8704b00-c989-480d-8cec-b87c86201a38@104.18.140.51:80?security=&type=ws&path=/Telegram:@vmessorg-Telegram:@vmessorg-Telegram:@vmessorg&host=vmessorg1.xn--54qv00ez5ar77g.co.&encryption=none#%F0%9F%9A%A9CF%20%7C%20%F0%9F%94%B4%20%7C%20vless%20%7C%20@vmessorg%20%7C%201"])
# print(calculate_download_speed(
#     url_config='vless://d8704b00-c989-480d-8cec-b87c86201a38@104.18.140.51:80?security=&type=ws&path=/Telegram:@vmessorg-Telegram:@vmessorg-Telegram:@vmessorg&host=vmessorg1.xn--54qv00ez5ar77g.co.&encryption=none#%F0%9F%9A%A9CF%20%7C%20%F0%9F%94%B4%20%7C%20vless%20%7C%20@vmessorg%20%7C%201',
#     port=10801, pid=16931))
