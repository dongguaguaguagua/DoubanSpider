from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import json
import time
import sqlite3
from get_headers import *
from get_signature import *
from get_secret import *

def add_url_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qs(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query, doseq=True)

    return urlunparse(url_parts)

def build_url(base_url, params):
    config = load_config()

    base_params = {
        'apikey': get_apikey(),
        'channel': config['channel'],
        'udid': config['udid'],
        's_rom': config['os_rom'],
        'timezone': config['timezone']
    }
    base_url = add_url_params(base_url, params)
    base_url = add_url_params(base_url, base_params)

    timestamp = int(time.time())
    secret_key = get_secret_key()
    auth_params = {
        '_ts': str(timestamp),
        '_sig': get_signature(
            base_url,
            config['access_token'],
            secret_key,
            timestamp
        )
    }
    url = add_url_params(base_url, auth_params)
    return url

def load_config():
    with open('config.json','r',encoding='utf8') as file:
        config = json.load(file)
    return config

def save_data(data, fileName):
    with open(fileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_total_movies_count(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM movies')
    total_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return total_count

def get_total_books_count(db_path):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    total_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return total_count

