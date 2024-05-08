#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python3

import sys
import requests
import json

# from pprint import pprint


def post_request(keyword):
    base_url = "https://fanyi.sogou.com/reventondc/suggV3"
    request_data = {
        "from": "auto",
        "to": "zh-CHS",
        "text": keyword,
        "pid": "sogou-dict-vr",
        "addSugg": "on",
    }
    r = requests.post(base_url, request_data)
    return r.text


def main():
    if len(sys.argv) != 2:
        print("usage : tsg <word>")
        exit(-1)
    json_obj = json.loads(post_request(sys.argv[1]))
    # pprint(json_obj["sugg"])
    for item in json_obj["sugg"]:
        print(f"{item['k']} : {item['v']}")


if __name__ == "__main__":
    main()
