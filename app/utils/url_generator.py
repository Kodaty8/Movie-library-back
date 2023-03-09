import json


def create_url(path: str, lang: str):
    with open('app/config.json', 'r') as f:
        cfg = json.load(f)
        base_url = cfg['base-url'] + path
        api_key = "?api_key=" + cfg['api-key']
    lang_param = "&language=" + lang
    url = base_url + api_key + lang_param
    return url


def create_image_url(path: str, size: str = "original"):
    if path is None:
        return None
    with open('app/config.json', 'r') as f:
        cfg = json.load(f)
        base_url = cfg['image-url'] + "/"

    url = base_url + size + path
    return url
