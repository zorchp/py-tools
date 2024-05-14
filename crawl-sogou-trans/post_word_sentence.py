#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

"""
ref to https://blog.csdn.net/m0_53342945/article/details/130240344
1. get cookies contains FQV 
2. post with FQV 
3. parse result
"""

import sys
import requests
import json
import argparse
from fake_useragent import UserAgent
from requests.exceptions import RequestException, HTTPError
from urllib.parse import quote
from pprint import pprint

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


def trans(word, fqv, to):
    base_url = "https://fanyi.sogou.com/api/transpc/text/transword"
    request_data = {
        "from": "auto",
        "to": to,
        "query": word,
    }
    ua = UserAgent()
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
    if "phonetic" in json_obj:
        flg = False
        for item in json_obj["phonetic"]:
            print(
                f"{item['type'] if 'type' in item else ''} [{item['text']}]{', https:'+item['filename'] if 'filename' in item else ''}"
            )
    print("=" * 50)
    if "paraphrase" in json_obj:
        flg = False
        for item in json_obj["paraphrase"]:
            print(
                f"{item['pos']} {item['value']}  {item['text'] if 'text' in item else ''}"
            )
    if flg and "translation" in json_obj:
        print(f"{json_obj['translation']['trans_text']}")


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
which language you want to translate, default: Chinese, available language:
1. ko Korean
2. ja Japanese
3. de German
4. ar Arabic
5. ru Russian
6. fr French
        """,
        default="zh-CHS",
    )
    parser.add_argument(
        "-s",
        "--suggestion",
        help="get suggestion for a word",
        action="store_true",
    )
    args = parser.parse_args()
    sentence = " ".join(args.word_or_sentence)
    if args.suggestion:
        sugg(sentence)
    else:
        # sentence = quote(sentence)
        trans(sentence, get_FQV(), args.language)


if __name__ == "__main__":
    main()
