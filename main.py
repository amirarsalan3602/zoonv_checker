from time import sleep
# from tasks import calculate_download_speed_task
from celery import Celery
from tools import Tools
from tasks import calculate_download_speed


def main():
    application = Tools()
    application.read_repo()
    urls = []
    total_elements = application.cash.llen("vless_urls")
    for elements in range(0, total_elements, 10):
        for url in application.cash.lrange("vless_urls", elements, elements + 9):
            if len(urls) >= 10:
                urls = []
            urls.append(url.decode("utf-8"))
        result_server = application.run_v2ray(urls=urls)
        if result_server != "No ports are open":
            for rs in result_server:
                if len(application.check_port()) != 10:
                    calculate_download_speed.apply_async(
                        kwargs={"url_config": rs["url"], "port": rs['port'], "pid": rs["pid"]}, countdown=2)
            else:
                sleep(5)
        else:
            sleep(5)
            ...
    print("="*2000)
    print(application.accepted)


if __name__ == "__main__":
    main()
    # # ایجاد نخ‌ها
    # thread_v2ray = threading.Thread(target=run_v2ray)
    # # thread_download = threading.Thread(target=download_file)
    #
    # # شروع نخ‌ها
    # thread_v2ray.start()
    # # time.sleep(5)
    # # thread_download.start()
    #
    # # انتظار برای پایان نخ‌ها
    # thread_v2ray.join()
    # # thread_download.join()
