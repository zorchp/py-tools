#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

import os
import json
import requests
import argparse
from requests.exceptions import RequestException, HTTPError
from urllib.parse import quote
from fake_useragent import UserAgent
from lxml import etree


def get_tree(kwd: str, isEng=True) -> str:
    ua = UserAgent()
    user_agent = ua.random
    headers = {"User-Agent": user_agent}
    pattern = "&transto=zh-CHS"
    try:
        r = requests.get(
            f"https://fanyi.sogou.com/text?keyword={kwd}&transfrom=auto{pattern}&model=general",
            headers=headers,
        )
        r.raise_for_status()  # get status code
    except HTTPError as http_err:
        print(f"error {http_err}")
        exit(1)
    except RequestException as err:
        print(f"an error occur: {err}")
        exit(2)
    # print(r.text)
    parser = etree.HTMLParser()
    tree = etree.fromstring(r.text, parser)
    return tree


def eng2chn(kwd):
    tree = get_tree(kwd)
    ans = tree.xpath('//p[@class="output-val"]/text()')
    if ans == []:
        print("no result...")
        return
    print(ans[0])
    print()

    item_wrap = tree.xpath('//div[@class="item-wrap"]')
    if item_wrap == []:
        print("no other info...")
        return

    pronounce = item_wrap[0].xpath('./div[@class="pronounce"]')
    if pronounce == []:
        return
    syms = pronounce[0].xpath('./div[@class="item"]/span/text()')
    if len(syms) == 1:
        print(syms[0])
        return
    print(f"{syms[0]}, {syms[1]}")
    print()

    symbols = item_wrap[0].xpath('./div[@class="item"]/span/text()')
    means = item_wrap[0].xpath('./div[@class="item"]/p/text()')
    for a, b in zip(symbols, means):
        print(f"{a} {b}")


def chn2eng(kwd: str):
    tree = get_tree(kwd)
    t1 = tree.xpath('//*[@class="output"]')
    t2 = t1[0].xpath('./p[@id="trans-result"]')
    ans = t2[0].xpath('./span[@class="trans-sentence"]/text()')
    if ans != []:
        print(ans[0])  # may not work sometimes
    print()
    # get word list :
    t3 = tree.xpath('//*[@class="word-list"]/li')
    for itm in t3:
        word, trans = itm.xpath("./a/text()"), itm.xpath("./span/text()")
        if word != []:
            print(word[0], end="  ")
            if trans != []:
                print(trans[0], end="")
            print()


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
        "-s",
        "--suggestion",
        help="get suggestion for a worf",
        action="store_true",
    )
    args = parser.parse_args()
    sentence = " ".join(args.word_or_sentence)
    if args.suggestion:
        sugg(sentence)
    else:
        sentence = quote(sentence)
        if sentence[0].isalnum():
            eng2chn(sentence)
        else:
            chn2eng(sentence)

# TODO : use post request when trans long sentence

def close_proxy():
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    if "https_proxy" in os.environ:
        del os.environ["https_proxy"]
    if "all_proxy" in os.environ:
        del os.environ["all_proxy"]


if __name__ == "__main__":
    close_proxy()
    main()
