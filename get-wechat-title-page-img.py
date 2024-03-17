import re
import sys

import requests


def main():
    argv = sys.argv
    n = len(argv)
    if n != 2:
        print("need url to get img")
        exit(-1)
    url = argv[1]
    content = requests.get(url).text

    if content.find("msg_cdn_url") == -1:
        print("img url not found, exit..")
        exit(-1)
    img_url = re.findall(r"msg_cdn_url\s=\s\"(http.*?)\"", content)[0]
    fmt = img_url[img_url.rfind("fmt=") + 4 :]
    # print(fmt)
    img_filename = f"img.{fmt}"
    # print(img_url)
    with open(img_filename, "wb") as img:
        img.write(requests.get(img_url).content)
    print(f"{img_url} => {img_filename}")


if __name__ == "__main__":
    main()
