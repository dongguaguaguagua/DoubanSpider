import requests
import sqlite3
from datetime import datetime
import time
from utilities import *
from get_headers import *
from get_signature import *
from get_secret import *

def recommand_data(config, round):
    headers = get_headers()
    start = round * int(config['data_count'])

    base_url = 'https://frodo.douban.com/api/v2/noviciate/mark_recommendations'

    custom_params = {
        'count': config['data_count'],
        'start': str(start),
        'kind': 'movie'
    }
    base_params = {
        'apikey': get_apikey(),
        'channel': config['channel'],
        'udid': config['udid'],
        's_rom': config['os_rom'],
        'timezone': config['timezone']
    }
    base_url = add_url_params(base_url, custom_params)
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

    response = requests.get(url, headers=headers)

    data = response.json()
    save_data(data, 'latest_movie.json')

    # 连接到SQLite数据库（如果数据库不存在，则会自动创建）
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id TEXT PRIMARY KEY,
        title TEXT,
        rating REAL,
        rating_count INTEGER,
        pubdate TEXT,
        year TEXT,
        genres TEXT,
        durations TEXT,
        cover_url TEXT,
        sharing_url TEXT,
        countries TEXT,
        url TEXT,
        directors TEXT,
        actors TEXT,
        update_time TEXT
    )
    ''')

    cursor.execute('SELECT COUNT(*) FROM movies')
    total_movie_before = cursor.fetchone()[0]

    # 插入数据
    for subject in data['subjects']:
        id = subject['id']
        title = subject['title']
        rating = subject['rating']['value']
        rating_count = subject['rating']['count']
        pubdate = ', '.join(subject['pubdate']) if subject['pubdate'] else None
        year = subject['year']
        genres = ', '.join(subject['genres'])
        durations = ', '.join(subject['durations'])
        cover_url = subject['cover_url']
        sharing_url = subject['sharing_url']
        countries = ', '.join(subject['countries'])
        url = subject['url']
        directors = ', '.join([director['name'] for director in subject['directors']])
        actors = ', '.join([actor['name'] for actor in subject['actors']])
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO movies (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, now))

    received_count = len(data['subjects'])
    cursor.execute('SELECT COUNT(*) FROM movies')
    total_movie_after = cursor.fetchone()[0]
    replaced_movie_count = total_movie_before + received_count - total_movie_after

    print(f'-------- round: {round}, start: {start} --------')
    print(f'Total movie count: {total_movie_after}')
    print(f'Replaced movies count: {replaced_movie_count}')
    print(f'Response total:{data['total']}')

    conn.commit()
    conn.close()

    print(f"{received_count} Data has been inserted into the SQLite database.")

    if(start > data['total']):
        return False

    return True

config = load_config()

# for i in range(100):
#     _round = 0
#     is_continue = True
#     while(is_continue is True):
#         is_continue = recommand_data(config=config, round=_round)
#         # sys.stdout.flush()  # 强制刷新输出缓冲区
#         _round += 1
#         time.sleep(20)
recommand_data(config=config, round=0)
