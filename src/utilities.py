from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import json

def add_url_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qs(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query, doseq=True)

    return urlunparse(url_parts)

def load_config():
    with open('config.json','r',encoding='utf8') as file:
        config = json.load(file)
    return config

def save_data(data, fileName):
    with open(fileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
