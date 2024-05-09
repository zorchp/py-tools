#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

import sys
import requests
import json

from requests.exceptions import RequestException, HTTPError

from pprint import pprint


def en2ch(word_or_sentence):
    # for sentence
    base_url = "https://fanyi.sogou.com/api/transpc/text/result"
    # for word
    # base_url = "https://fanyi.sogou.com/api/transpc/text/transword"
    request_data = {
        "fr": "browser_pc",
        "client": "pc",
        "exchange": False,
        "needQc": 1,
        "from": "en",
        "s": "0e166f9b2a60dd8e418c80fccc931cff",
        "to": "zh-CHS",
        "text": word_or_sentence,
    }
    try:
        r = requests.post(
            base_url,
            # json=request_data,
            json={
                "from": "auto",
                "to": "zh-CHS",
                "text": "request",
                "client": "pc",
                "fr": "browser_pc",
                "needQc": 1,
                "s": "0e166f9b2a60dd8e418c80fccc931cff",
                "uuid": "121fb327-7791-41ac-9337-0b12b59b244c",
                "exchange": False,
            },
        )
        r.raise_for_status()
    except HTTPError as http_err:
        print(f"error {http_err}")
        exit(1)
    except RequestException as err:
        print(f"an error occur: {err}")
        exit(2)

    print(r.text)
    return
    json_obj = json.loads(r.text)
    for item in json_obj["sugg"]:
        print(f"{item['k']} : {item['v']}")


def main():
    # if len(sys.argv) != 2:
    #     print("usage : tsg <word>")
    #     exit(-1)
    # sugg(sys.argv[1])
    en2ch("hello")


if __name__ == "__main__":
    main()
