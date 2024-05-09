#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

import sys
import requests
import json

from requests.exceptions import RequestException, HTTPError

# from pprint import pprint


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
    for item in json_obj["sugg"]:
        print(f"{item['k']} : {item['v']}")


def main():
    if len(sys.argv) != 2:
        print("usage : tsg <word>")
        exit(-1)
    sugg(sys.argv[1])


if __name__ == "__main__":
    main()
