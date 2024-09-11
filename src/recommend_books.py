import requests
import sqlite3
import time
from utilities import *
from get_headers import *
from get_signature import *
from get_secret import *
from insert_data import *

def recommand_data(config, round):
    headers = get_headers()
    start = round * int(config['data_count'])

    base_url = 'https://frodo.douban.com/api/v2/noviciate/mark_recommendations'

    custom_params = {
        'count': config['data_count'],
        'start': str(start),
        'kind': 'book'
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
    save_data(data, 'latest_book.json')

    init_book_table('books.db')

    total_book_before = get_total_books_count('books.db')

    insert_books('books.db', data)

    received_count = len(data['subjects'])

    total_book_after = get_total_books_count('books.db')

    replaced_book_count = total_book_before + received_count - total_book_after

    print(f'-------- round: {round}, start: {start} --------')
    print(f'Total book count: {total_book_after}')
    print(f'Replaced books count: {replaced_book_count}')
    print(f'Response total:{data['total']}')

    print(f"{received_count} Data has been inserted into the SQLite database.")

    if(start > data['total']):
        return False

    return True

config = load_config()

for i in range(100):
    _round = 0
    is_continue = True
    while(is_continue is True):
        is_continue = recommand_data(config=config, round=_round)
        # sys.stdout.flush()  # 强制刷新输出缓冲区
        _round += 1
        time.sleep(20)
# recommand_data(config=config, round=0)
# recommand_data(config=config, round=0)
