from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import json
import time
import sqlite3
from get_headers import *
from get_signature import *
from get_secret import *
import random

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

def get_all_unvisited(db_path, table_name, column):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    query = f"""
        SELECT {column}
        FROM {table_name}
        WHERE is_visited = 0
        ORDER BY update_time ASC, id ASC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in result]

def get_latest_unvisited(db_path, table_name, column):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    query = f"""
        SELECT {column}
        FROM {table_name}
        WHERE is_visited = 0
        ORDER BY update_time ASC, id ASC
        LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result

def get_random_unvisited(db_path, table_name, column):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    query = f"""
        SELECT {column}
        FROM {table_name}
        WHERE is_visited = 0
        ORDER BY RANDOM()
        LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result

def mark_visited(db_path, table_name, column, target_id):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    query = f"""
        UPDATE {table_name}
        SET is_visited = 1
        WHERE {column} = '{target_id}';
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def from_id_get_data(db_path, table_name, column, target_id):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    query = f"""
        SELECT {column}
        FROM {table_name}
        WHERE id = '{target_id}'
        LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return result

def get_doulist_api_base_url(sharing_url):
    if sharing_url.startswith("https://m.douban.com/subject_collection/"):
        doulist_id = sharing_url.split("/subject_collection/")[1]
        return f"https://frodo.douban.com/api/v2/subject_collection/{doulist_id}/items"

    elif sharing_url.startswith("https://www.douban.com/doulist/"):
        doulist_id = sharing_url.split("/doulist/")[1]
        return f"https://frodo.douban.com/api/v2/doulist/{doulist_id}/posts"

    else:
        return None

def is_official_doulist(sharing_url):
    if sharing_url.startswith("https://m.douban.com/subject_collection/"):
        return True

    elif sharing_url.startswith("https://www.douban.com/doulist/"):
        return False

    else:
        return None

def log_message(message):
    print(message)
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def random_break():
    rand = random.randint(5, 20)
    time.sleep(rand)
