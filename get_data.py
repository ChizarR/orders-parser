# TODO: Async req !!!

import os
import time
from pathlib import Path
from pprint import pprint

import requests
from fake_useragent import UserAgent

from config import Config


def send_request(order_data: list):
    ABB_URL = "https://new.abb.com/products/ru/"
    files = []
    user_agent = UserAgent()
    write_dir = _check_if_tmp_dir_exists(Path(Config.TMP_DIR))
    proxies = {
        "http": "http://103.135.102.143:80",
        "http": "http://141.98.16.38:8080",
        "http": "http://45.142.106.202:80",
        "http": "http://169.57.1.85:8123",
        "http": "http://20.210.113.32:8123",
        "http": "http://8.219.97.248:80",
    }
    index = 0
    for product in order_data:
        url = f"{ABB_URL}{product['article']}"
        print(url, end=" ")
        headers = {
            "accept": "*/*",
            "user-agent": user_agent.chrome
        }
        response = requests.get(
            url,
            headers=headers,
            proxies=proxies
        )
        if response.status_code == 500:
            while response.status_code != 200:
                response = requests.get(
                    url,
                    headers=headers,
                    proxies=proxies
                )
                time.sleep(3)
        article = order_data[index]["article"]
        path_to_file = Path(f"{write_dir}/{response.status_code}_{article}.html")
        files.append(path_to_file) 
        print(response.status_code)
        _write_file(path_to_file, response.text)
        product["path_to_file"] = path_to_file 
        time.sleep(2)
        index += 1
        if index == 3:
            break
    print("Done")
    pprint(order_data)
    return files


def _check_if_tmp_dir_exists(path: Path) -> Path:
    if os.path.exists(path):
        return path
    os.mkdir(path)
    return path


def _write_file(path_to_file: Path, text: str):
    with open(path_to_file, "w", encoding="utf-8") as file:
        file.write(text)

