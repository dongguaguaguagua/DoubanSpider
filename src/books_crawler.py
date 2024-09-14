import requests
from utilities import *
from get_headers import *
from get_signature import *
from get_secret import *
from insert_data import *
from init_tables import *

def get_related(db_path, book_id):
    headers = get_headers()
    base_url = f'https://frodo.douban.com/api/v2/book/{book_id}/related_items'
    custom_params = {
        'count': 10,
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_books_related.json')
    init_books_table(db_path)
    init_doulists_table(db_path)
    insert_small_books(db_path, data)
    insert_doulists(db_path, data)

def get_interests(db_path, book_id):
    headers = get_headers()
    base_url = f'https://frodo.douban.com/api/v2/book/{book_id}/hot_interests'
    custom_params = {
        'status': 'done',
        'following': 1
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_books_interests.json')
    init_interests_table(db_path)
    insert_interests(db_path, data)

def from_user_get_books(db_path, data_count, user_id, round):
    headers = get_headers()
    start = round * int(data_count)
    base_url = f'https://frodo.douban.com/api/v2/user/{user_id}/interests'
    custom_params = {
        'type': 'book',
        'status': 'done',
        'start': str(start),
        'count': str(data_count),
        'common_interest': 0
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    data["subjects"] = [interest["subject"] for interest in data["interests"]]
    save_data(data, 'latest_books_from_user.json')
    init_books_table(db_path)
    insert_books(db_path, data)

    if(start > data['total']):
        return False
    return True

def from_doulist_get_books(db_path, data_count, doulist_id, round):
    headers = get_headers()
    start = round * int(data_count)
    sharing_url = from_id_get_data(db_path, 'doulists', 'sharing_url', doulist_id)
    base_url = get_doulist_api_base_url(sharing_url)
    is_official = is_official_doulist(sharing_url)

    custom_params = {
        'start': str(start),
        'count': str(data_count),
        'undone': 0,
        'buyable': 0,
        'readable': 0
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_books_from_doulist.json')
    if(is_official == False):
        data["subjects"] = [item["content"]["subject"] for item in data["items"]]
    else:
        data["subjects"] = [item for item in data["subject_collection_items"]]

    init_books_table(db_path)
    insert_books(db_path, data)

    if(start > data['total']):
        return False
    return True

def crawl_entire_doulist(db_path, data_count, doulist_id):
    _round = 0
    _continue = True
    while(_continue is True):
        _continue = from_doulist_get_books(db_path, data_count, doulist_id, _round)
        print('\t\tTotal book count: ', get_total_books_count(db_path))
        _round += 1
        time.sleep(10)

def crawl_entire_user(db_path, data_count, user_id):
    _round = 0
    _continue = True
    while(_continue is True):
        _continue = from_user_get_books(db_path, data_count, user_id, _round)
        print('\t\tTotal book count: ', get_total_books_count(db_path))
        _round += 1
        time.sleep(10)

def get_recommendations(db_path, data_count, round):
    headers = get_headers()
    start = round * int(data_count)
    base_url = 'https://frodo.douban.com/api/v2/noviciate/mark_recommendations'
    custom_params = {
        'count': str(data_count),
        'start': str(start),
        'kind': 'book'
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_book.json')
    init_books_table(db_path)
    total_book_before = get_total_books_count(db_path)
    insert_books(db_path, data)
    received_count = len(data['subjects'])
    total_book_after = get_total_books_count(db_path)
    replaced_book_count = total_book_before + received_count - total_book_after
    print(f'-------- round: {round}, start: {start} --------')
    print(f'Total book count: {total_book_after}')
    print(f'Replaced books count: {replaced_book_count}')
    print(f'Response total:{data['total']}')
    print(f"{received_count} Data has been inserted into the SQLite database.")

    if(start > data['total']):
        return False
    return True

if __name__ == '__main__':
    config = load_config()
    db_path = config['db_path']
    data_count = config['data_count']
    # init database
    print("initiating database and generating seed data...")
    # get_recommendations(db_path, data_count, 0)

    book_id = get_latest_unvisited(db_path, 'books', 'id')
    book_title = from_id_get_data(db_path, 'books', 'title', book_id)
    print(f"working on book id: {book_id}, title: {book_title}")

    print("getting related books and doulists for book:", book_title)
    get_related(db_path, book_id)
    doulists = get_all_unvisited(db_path, 'doulists', 'id')
    for doulist_id in doulists:
        print("\tworking on doulist:", doulist_id)
        crawl_entire_doulist(db_path, data_count, doulist_id)
        mark_visited(db_path, 'doulists', 'id', doulist_id)

    print("getting related user comments for book:", book_title)
    get_interests(db_path, book_id)
    users = get_all_unvisited(db_path, 'interests', 'user_id')
    for user_id in users:
        print("\tworking on user:", user_id)
        crawl_entire_user(db_path, data_count, user_id)
        mark_visited(db_path, 'interests', 'user_id', user_id)



