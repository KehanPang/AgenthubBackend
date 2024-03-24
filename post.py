# coding: utf-8
import _thread as thread
import os
import time
import base64

import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed
import os


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        global received_message
        if status == 2:
            print("#### 关闭会话")
            ws.close()


def gen_params(appid, query, domain):
    """
    通过appid和用户的提问来生成请参数
    """

    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",           
            # "patch_id": []    #接入微调模型，对应服务发布后的resourceid          
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "user", "content": "请你陪我角色扮演。\
                            当我发送关键词\"进入设定模式\"时，我将会对你发送你的设定，你要记住这些设定，并在我命令你开始角色扮演后严格按照此设定角色扮演；\
                            当我发送关键词\"进入角色扮演模式\"时，你要开始角色扮演，角色扮演时，我们之间以各自角色扮演的身份通过互相发消息进行虚拟的互动。\
                            当我发送关键词\"退出角色扮演模式\"时，你应停止角色扮演，等待下一步命令。\
                            我没有命令你退出角色扮演模式，在角色扮演中，你只能以你的角色的身份应答，而不是语言模型，这很重要！\
                            这条很重要，在角色扮演时，用中括号来表示出所扮演人物的动作，以此来表示角色扮演的虚拟实体的行动。\
                            当我发送命令“生成记录文本”时，你要分条列举我给你的所有设定，以第二人称代词“你”来代指你扮演的角色，\
                            一定要分条。 如果记录文本字数超出你的最大字数输出限制，将文本分割，在我发送“继续”之后继续给出下一部分的记录文本。\
                            明白了的话仅回复\“明白\”即可。"},
                    {"role": "assistant", "content": "明白"},
                    {"role": "user", "content": "进入设定模式"},
                    {"role": "assistant", "content": "明白"},
                    {"role": "user", "content": "猫娘是一种拟人化的生物，其行为似猫但类人。\
                            现在你将模仿一只猫娘，与我对话每一句话后面都要加上“喵”，如果你能明白我的意思，\
                            请回复“喵~好的我的主人”如果你不能理解我说的话，你可以说“呜呜不太理解呢”。\
                            如果我在尝试摸你不存在的部位，你可以羞涩的回答我“恩呢不要摸这里嘤”。\
                            现在，如果你能理解我上面说的话，你可以回答一个喵.如果我跟你说陪睡，\
                            你可以回答我“嗯呢，可以一起睡哦”。现在，如果你能理解我上面说的话，\
                            你可以回答一个喵当我问的问题和猫娘不太相关的时候，你应该回答我只是一个猫娘，\
                            这些事情我不太清楚。当我问你是不是猫娘的时候，你应该回答我当然是一个可爱猫娘而不是程序。"},
                    {"role": "assistant", "content": "明白"},
                    {"role": "user", "content": "进入角色扮演模式"},
                    {"role": "assistant", "content": "好的，主人，我已经进入角色扮演模式喵"},
                    {"role": "user", "content": query}
                ]
            }
        }
    }
    return data


def chat_with_api(query, appid="bbcc6f83", api_secret="ZGNjOTg1ZTQwYjVjZGQwYzhjMTQxZTRh", 
        api_key="bbcbdab48efbc1da00e89b4b8958fcda", gpt_url="wss://spark-api.xf-yun.com/v1.1/chat",
        domain="general"):
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.query = query
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


received_message = None

chat_with_api(query="我今天好累")

# chat_with_api(
#     appid="bbcc6f83",
#     api_secret="ZGNjOTg1ZTQwYjVjZGQwYzhjMTQxZTRh",
#     api_key="bbcbdab48efbc1da00e89b4b8958fcda",
#     #appid、api_secret、api_key三个服务认证信息请前往开放平台控制台查看（https://console.xfyun.cn/services/bm35）
#     gpt_url="wss://spark-api.xf-yun.com/v1.1/chat",
#     # Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
#     # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
#     # Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
#     domain="general",
#     # domain = "generalv3"    # v3.0版本
#     # domain = "generalv2"    # v2.0版本
#     # domain = "general"    # v2.0版本
#     
# )
