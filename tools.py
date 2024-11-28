import os
import subprocess

import uuid
import re
import socket
import json

from urllib.parse import unquote
import redis



class Tools:
    def __init__(self):
        self.cash = self.connection_redis()
        self.refused = 0

    def run_v2ray(self, urls: []):

        open_ports = self.check_port()
        up_server = []
        if len(open_ports) > 0:
            for url in urls:
                for open_port in open_ports:
                    if self.convert_vless(url=url, port=open_port) == "successfully":
                        process = subprocess.Popen(["v2ray", "run", "-c", "config.json"])
                        up_server.append({"url": url, "port": open_port, "pid": process.pid})
                        open_ports.pop(open_ports.index(open_port))
                        break

            return up_server
        else:
            return "No ports are open"


    def connection_redis(self):
        return redis.Redis(host="localhost", port=6379, password="SMVlq?cp3h99kj", db=0)

    def convert_vless(self, url: str, port: int):
        try:
            result = subprocess.run(['python3', './v2ray2json/v2ray2json.py', url], stdout=subprocess.PIPE)
            output = result.stdout.decode('utf-8').strip()
            json_data = json.loads(output)
            json_data['inbounds'][0]["port"] = port
            user_uuid = self.generate_uuid_v5(re.search(r'vless://(.*?)@', url).group(1))
            if user_uuid:
                json_data["outbounds"][0]['settings']['vnext'][0]["users"][0]["id"] = user_uuid

            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        except:
            print(f"filed = {url}")

        return "successfully"

    # except AttributeError:
    #     ...

    def generate_uuid_v5(self, user_uuid: str, namespace=uuid.NAMESPACE_URL):
        try:
            uuid_obj = uuid.UUID(user_uuid)
            if uuid_obj.hex == user_uuid.replace('-', ''):
                return user_uuid
        except ValueError:
            root_namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
            return str(uuid.uuid5(root_namespace, user_uuid))



    def read_repo(self):
        with open("repository/All_Configs_Sub.txt", "r") as file:
            list_dirty = file.read().split("\n")
            for i in list_dirty:
                try:
                    if re.search(r'^([^:]+)', i).group(1) == "vless":
                        self.cash.lpush("vless_urls", unquote(i))
                except AttributeError:
                    ...

    def stop_v2ray(self, pid):
        os.system(f"kill {pid}")

    def check_port(self):
        ports = (10801, 10802, 10803, 10804, 10805, 10806, 10807, 10808, 10809, 10810)
        open_ports = []
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # تنظیم تایم‌اوت برای جلوگیری از انتظار طولانی
                s.settimeout(0.5)
                # بررسی اینکه آیا می‌توان به پورت متصل شد یا خیر
                if s.connect_ex(('localhost', port)) != 0:
                    open_ports.append(port)
        return open_ports

    def accepted(self, url: str):
        url = url.replace(url[url.find("#") + 1:], "@ZoonV | ارائه دهنده VPN پرسرعت در ایران")
        if url.find("serviceName=") != -1:
            url = re.sub(r'(serviceName=)[^&]*', rf"@ZoonV | ارائه دهنده VPN پرسرعت در ایران", url)
        if self.cash.llen("accepted") >= 100:
            self.cash.rpop("accepted")
        self.cash.lpush("accepted", url)


