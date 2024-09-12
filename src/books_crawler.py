import requests
from utilities import *
from get_headers import *
from get_signature import *
from get_secret import *
from insert_data import *
from init_tables import *

def get_related(book_id):
    headers = get_headers()
    base_url = f'https://frodo.douban.com/api/v2/book/{book_id}/related_items'
    custom_params = {
        'count': 10,
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_book_related.json')
    init_books_table('books.db')
    init_doulists_table('books.db')
    insert_small_books('books.db', data)
    insert_doulists('books.db', data)

def get_interests(book_id):
    headers = get_headers()
    base_url = f'https://frodo.douban.com/api/v2/book/{book_id}/hot_interests'
    custom_params = {
        'status': 'done',
        'following': 1
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_book_interests.json')
    init_interests_table('books.db')
    insert_interests('books.db', data)

def from_user_get_books(user_id, round):
    headers = get_headers()
    start = round * int(config['data_count'])
    base_url = f'https://frodo.douban.com/api/v2/user/{user_id}/interests'
    custom_params = {
        'type': 'book',
        'status': 'done',
        'start': str(start),
        'count': config['data_count'],
        'common_interest': 0
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    data["subjects"] = [interest["subject"] for interest in data["interests"]]
    save_data(data, 'latest_books_from_user.json')
    init_books_table('books.db')
    insert_books('books.db', data)


def get_recommendations(config, round):
    headers = get_headers()
    start = round * int(config['data_count'])
    base_url = 'https://frodo.douban.com/api/v2/noviciate/mark_recommendations'
    custom_params = {
        'count': config['data_count'],
        'start': str(start),
        'kind': 'book'
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_book.json')
    init_books_table('books.db')
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

# for i in range(100):
#     _round = 0
#     is_continue = True
#     while(is_continue is True):
#         is_continue = get_recommendations(config=config, round=_round)
#         # sys.stdout.flush()  # 强制刷新输出缓冲区
#         _round += 1
#         time.sleep(20)
# get_recommendations(config=config, round=0)
# get_recommendations(config=config, round=0)
# get_interests(35620036)
from_user_get_books(2303117, 0)
