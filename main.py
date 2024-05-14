from concurrent.futures import ThreadPoolExecutor

from time import perf_counter

from repository.Files.app import repo_main
from tools import Tools
from tasks import calculate_download_speed

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




if __name__ == "__main__":
    repo_main()
    main()
