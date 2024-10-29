#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

"""
ref to https://blog.csdn.net/m0_53342945/article/details/130240344
1. get cookies contains FQV 
2. post with FQV 
3. parse result
"""

import os
import sys
import requests
import json
import argparse
import shutil
from requests.exceptions import RequestException, HTTPError

# from concurrent.futures import ThreadPoolExecutor  # for async play audio
# from urllib.parse import quote
# from pprint import pprint
# from fake_useragent import UserAgent

# requests.packages.urllib3.disable_warnings(
#     requests.packages.urllib3.exceptions.InsecureRequestWarning
# )

session = requests.Session()


def get_FQV():
    headers = {
        "Content-Type": "application/json",
        "Host": "fanyi.sogou.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not-A.Brand";v="24", "Chromium";v="14"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    try:
        r = session.get(
            "https://fanyi.sogou.com/",
            headers=headers,
        )
        r.raise_for_status()
    except HTTPError as http_err:
        print(f"error {http_err}")
        exit(1)
    except RequestException as err:
        print(f"an error occur: {err}")
        exit(2)
    # print(type(r.headers))
    # pprint(r.headers)
    cookies = r.headers["Set-Cookie"]
    # print(cookies)
    FQV = ""
    for item in cookies.split(";"):
        if "FQV" in item:
            FQV = item.strip().split("FQV=")[1]
            break
    # return cookies
    return FQV


def trans(word, fqv, to, audio_type):
    base_url = "https://fanyi.sogou.com/api/transpc/text/transword"
    request_data = {
        "from": "auto",
        "to": to,
        "query": word,
    }
    # ua = UserAgent()
    headers = {
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36",
        # ua.random,
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://fanyi.sogou.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": f"FQV={fqv}",
    }

    try:
        r = session.post(
            base_url,
            json=request_data,
            headers=headers,
            timeout=30,
            # verify=False,
        )
        r.raise_for_status()
    except HTTPError as http_err:
        print(f"error {http_err}")
        exit(1)
    except RequestException as err:
        print(f"an error occur: {err}")
        exit(2)

    # print(r.text)
    json_obj = json.loads(r.text)["data"]
    flg = True
    has_phonetic = False
    if "phonetic" in json_obj:
        has_phonetic = True
        flg = False
        # dict for audio
        audio_list = {}
        for item in json_obj["phonetic"]:
            if "type" in item and "filename" in item:
                audio_list[item["type"]] = item["filename"]
                print(f"{item['type']} [{item['text']}]")

    print("=" * 50)
    if "paraphrase" in json_obj:
        flg = False
        for item in json_obj["paraphrase"]:
            print(
                f"{item['pos']} {item['value']}  {item['text'] if 'text' in item else ''}"
            )
    if flg and "translation" in json_obj:
        print(f"{json_obj['translation']['trans_text']}")
    if has_phonetic and audio_type is not None:
        play_word_audio(audio_list[audio_type])


def sugg(keyword):
    base_url = "https://fanyi.sogou.com/reventondc/suggV3"
    request_data = {
        "from": "auto",
        "to": "zh-CHS",
        "text": keyword,
        "pid": "sogou-dict-vr",
        "addSugg": "on",
    }
    try:
        r = requests.post(base_url, request_data)
        r.raise_for_status()
    except HTTPError as http_err:
        print(f"error {http_err}")
        exit(1)
    except RequestException as err:
        print(f"an error occur: {err}")
        exit(2)

    json_obj = json.loads(r.text)
    if json_obj is None:
        print("error: empty json object")
        return
    for item in json_obj["sugg"]:
        print(f"{item['k']} : {item['v']}")


def play_word_audio(url):
    if shutil.which("ffplay") is None:
        print("You need to install ffmpeg and ffplay")
        exit(-1)
    os.system(f"ffplay -i {url} -nodisp -autoexit > /dev/null 2>&1")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "word_or_sentence",
        help="word(s) or sentence where you want to query",
        nargs="*",  # limit may not out of 5000
    )
    parser.add_argument(
        "-l",
        "--language",
        help="""
which language you want to translate, default: Chinese, available language: \n
1. ko Korean \n
2. ja Japanese \n
3. de German \n
4. ar Arabic \n
5. ru Russian \n
6. fr French \n
        """,
        default="zh-CHS",
    )
    parser.add_argument(
        "-s",
        "--suggestion",
        help="get suggestion for a word",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--play_audio",
        help="play word audio by ffplay, default: usa",
        nargs="?",  # optional argument
        choices=["usa", "uk"],
        const="usa",
    )
    args = parser.parse_args()
    sentence = " ".join(args.word_or_sentence)
    # print(args.audio_address)
    if args.suggestion:
        sugg(sentence)
    else:
        # sentence = quote(sentence)
        trans(sentence, get_FQV(), args.language, args.play_audio)


def remove_proxy():
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    if "https_proxy" in os.environ:
        del os.environ["https_proxy"]
    if "all_proxy" in os.environ:
        del os.environ["all_proxy"]


if __name__ == "__main__":
    remove_proxy()
    main()
