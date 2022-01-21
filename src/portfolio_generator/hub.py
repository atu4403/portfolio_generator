import re
import time
import requests
import warnings
import xmltodict
import feedparser


def get_request(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    else:
        warnings.warn(f"invalid status: {r.status_code} - {url}")
        return None


def get_json(url: str) -> dict:
    r = get_request(url)
    return r.json() if r else None


def get_xml(url: str) -> dict:
    r = get_request(url)
    return xmltodict.parse(r.text) if r else None


def get_rss(url: str) -> dict:
    r = get_request(url)
    return feedparser.parse(r.text) if r else None


def hub_qiita(username: str) -> dict:
    url = f"https://qiita.com/api/v2/users/{username}/items?per_page=100"
    return get_json(url)


def hub_github(username: str) -> dict:
    def _next_link(s):
        res = {}
        li = s.split(",")
        for line in li:
            l = line.strip().split(";")
            m = re.search(r"rel=\"(\w*)\"", l[1])
            key = m.group(1)
            res[key] = l[0][1:-1]
        return res.get("next")

    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    res = []
    while url:
        r = requests.get(url)
        if r.status_code != 200:
            warnings.warn(f"invalid status: {r.status_code} - {url}")
            return None
        if link := r.headers.get("Link"):
            url = _next_link(link)
            time.sleep(1)
        else:
            url = ""
        res += r.json()

    return res


def hub_zenn(username: str) -> dict:
    url = f"https://zenn.dev/{username}/feed?all=1"
    return get_rss(url)


def hub_with_key(key: str, username: str):
    if key == "qiita":
        return hub_qiita(username)
    elif key == "github":
        return hub_github(username)
    elif key == "zenn":
        return hub_zenn(username)
    else:
        {}


def hub_with_type(
    type_: str,
    url: str,
):
    if type_ == "json":
        return get_json(url)
    elif type_ == "rss":
        return get_rss(url)
    elif type_ == "xml":
        return get_xml(url)
    else:
        {}
