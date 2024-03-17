#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

import re
import sys
from urllib.parse import quote

import requests
from requests.exceptions import RequestException, HTTPError

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
        r.raise_for_status() # get status code
    except HTTPError as http_err:
        print(f"error {http_err}")
        exit()
    except RequestException as err:
        print(f"an error occur: {err}")
        exit()
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


def main():
    argv = sys.argv
    if len(argv) != 2:
        print("Usage: trans <kwd>")
        exit(-1)
    word = argv[1]
    word = quote(word)
    if word[0].isalnum():
        eng2chn(argv[1])
    else:
        chn2eng(word)


if __name__ == "__main__":
    main()
