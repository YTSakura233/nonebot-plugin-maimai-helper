import hashlib
import json
import time
import zlib
import random
import nonebot

import urllib3
from nonebot.log import logger

from util.net.crypto import CipherAES
from util.net.SocketHttps import HttpClient
from data import network_count


config = nonebot.get_driver().config
TITLE_HOST = getattr(config, 'title_host')
CLIENT_ID = getattr(config, 'client_id')
OBFUSCATE_PARAM = getattr(config, 'obfuscate_param')


class HTTPRequest:
    def __init__(self, uid=-1):
        self._title_server_uri = TITLE_HOST
        self._obfuscate_param = OBFUSCATE_PARAM
        self._key_chip = CLIENT_ID
        self._timeout = 3
        self._max_retry = 2
        self._uid = uid
        self._mai_encoding = "1.40"

    @staticmethod
    def obfuscator(param: str) -> str:
        return hashlib.md5(str.encode(param + HTTPRequest()._obfuscate_param)).hexdigest()

    def Request(self, api: str, datas: dict):
        network_count.add_request_count()
        if not (api.endswith("MaimaiChn")):
            api += "MaimaiChn"
        unobfuscated_api = api

        api = self.obfuscator(api)
        url = self._title_server_uri + api

        final_data  = zlib.compress(CipherAES.encrypt(json.dumps(datas).encode("utf-8")))
        header = {
            "Content-Type": "application/json",
            "User-Agent": f"{api}#{self._key_chip if self._uid == -1 else self._uid}",
            "charset": "UTF-8",
            "Mai-Encoding": self._mai_encoding,
            "Content-Encoding": "deflate",
            "Content-Length": str(len(final_data)),
            "Host": urllib3.util.parse_url(self._title_server_uri).host,
        }
        print(f"Requesting {unobfuscated_api}:\nRequest URL:{url}\nRequest Data:{datas}\nRequest Header:{header}")

        result = {"status_code": 400, "headers": {}, "body": b""}
        ctime = int(round(time.time() * 1000))
        for i in range(self._max_retry):
            result = HttpClient.post(urllib3.util.parse_url(url), header, final_data.strip(), float(self._timeout))
            if result["status_code"] != 200:
                continue
            if len(result["body"]) > 0:
                break
        end = int(round(time.time() * 1000)) - ctime
        network_count.update_average_delay(end)
        if result["status_code"] != 200:
            logger.error(f"API请求失败, CODE{result['status_code']}")
            network_count.add_failed_request_count()
            raise Exception(f"Request Failed with status code {result['status_code']}")
        if not (len(result["body"]) > 0):
            logger.error("API请求失败，超过重试次数")
            network_count.add_failed_request_count()
            raise Exception("Max Retry Failed")

        print(f"{unobfuscated_api} was response in {end}ms:\nStatus Code: {result['status_code']}\nHeaders: {result['headers']}")
        try:
            try:
                decompressed_data = zlib.decompress(result["body"])
            except zlib.error:
                logger.error("ZLIB解码失败")
                network_count.add_zlib_compress_skip_count()
                decompressed_data = result["body"]
            logger.success("API请求成功")
            final_content = json.loads(CipherAES.decrypt(decompressed_data))
            print(f"{unobfuscated_api} Response data: {final_content}")
            return final_content
        except Exception as e:
            logger.error("解码失败")
            network_count.add_failed_request_count()
            print(f"{unobfuscated_api} was error in decoding with\n{result['body']}")
            raise e