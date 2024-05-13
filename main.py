from concurrent.futures import ThreadPoolExecutor

from time import sleep, perf_counter
from celery import Celery

from repository.Files.app import repo_main
from tools import Tools
from tasks import calculate_download_speed
from threading import Thread

start = perf_counter()


def main():
    application = Tools()
    application.read_repo()
    total_elements = application.cash.llen("vless_urls")

    with ThreadPoolExecutor(max_workers=10) as executor:
        for elements in range(0, total_elements, 10):
            urls = [url.decode("utf-8") for url in application.cash.lrange("vless_urls", elements, elements + 9)]
            result_server = application.run_v2ray(urls=urls)
            futures = [executor.submit(calculate_download_speed, rs["url"], rs['pid'], rs["port"]) for rs in
                       result_server]

            # اگر می‌خواهید منتظر بمانید تا تمام تردها کار خود را تمام کنند
            for future in futures:
                future.result()

    # این قسمت از کد برای اجرای کد پس از اتمام تمام تردها است
    end = perf_counter()
    print(f"finish time : {round(end - start)}")
    repo_main()
    main()

    # application = Tools()
    # application.read_repo()
    # urls = []
    #
    # total_elements = application.cash.llen("vless_urls")
    # for elements in range(0, total_elements, 10):
    #     for url in application.cash.lrange("vless_urls", elements, elements + 9):
    #         if len(urls) >= 10:
    #             urls = []
    #         urls.append(url.decode("utf-8"))
    #     result_server = application.run_v2ray(urls=urls)
    #     for rs in result_server:
    #             t = Thread(target=calculate_download_speed,
    #                        kwargs={'url_config': rs["url"], 'pid': rs['pid'], 'port': rs[
    #                            "port"]})
    #             t.start()
    #             t.join()
    #             # calculate_download_speed(url_config=rs["url"], pid=rs['pid'], port=rs["port"])
    # else:
    #     sleep(5)
    #     ...


if __name__ == "__main__":
    repo_main()
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
