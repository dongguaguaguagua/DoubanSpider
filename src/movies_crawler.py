import requests
from utilities import *
from get_headers import *
from get_signature import *
from get_secret import *
from insert_data import *
from init_tables import *

def get_related(db_path, movie_id):
    headers = get_headers()
    base_url = f'https://frodo.douban.com/api/v2/movie/{movie_id}/related_items'
    custom_params = {
        'count': 10,
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_movies_related.json')
    init_movies_table(db_path)
    init_doulists_table(db_path)
    # insert_small_movies(db_path, data)
    insert_doulists(db_path, data)

def get_interests(db_path, movie_id):
    headers = get_headers()
    base_url = f'https://frodo.douban.com/api/v2/movie/{movie_id}/hot_interests'
    custom_params = {
        'status': 'done',
        'following': 1
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_movies_interests.json')
    init_interests_table(db_path)
    insert_interests(db_path, data)

def from_user_get_movies(db_path, data_count, user_id, round):
    headers = get_headers()
    start = round * int(data_count)
    base_url = f'https://frodo.douban.com/api/v2/user/{user_id}/interests'
    custom_params = {
        'type': 'movie',
        'status': 'done',
        'start': str(start),
        'count': str(data_count),
        'common_interest': 0
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    data["subjects"] = [interest.get("subject") for interest in data.get("interests", {})]
    save_data(data, 'latest_movies_from_user.json')
    init_movies_table(db_path)
    insert_movies(db_path, data)

    if(start > data.get('total', start)):
        return False
    return True

def from_doulist_get_movies(db_path, data_count, doulist_id, round):
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
    save_data(data, 'latest_movies_from_doulist.json')
    if(is_official == False):
        data["subjects"] = [item.get("content").get("subject") for item in data.get("items", {})]
    else:
        data["subjects"] = [item for item in data.get("subject_collection_items", {})]

    init_movies_table(db_path)
    insert_movies(db_path, data)

    if(start > data.get('total', start)):
        return False
    return True

def crawl_entire_doulist(db_path, data_count, doulist_id):
    _round = 0
    _continue = True
    while(_continue is True):
        _continue = from_doulist_get_movies(db_path, data_count, doulist_id, _round)
        log_message(f'\t\tTotal movie count: {get_total_movies_count(db_path)}','movie_log.txt')
        _round += 1
        random_break()

def crawl_entire_user(db_path, data_count, user_id):
    _round = 0
    _continue = True
    while(_continue is True):
        _continue = from_user_get_movies(db_path, data_count, user_id, _round)
        log_message(f'\t\tTotal movie count: {get_total_movies_count(db_path)}','movie_log.txt')
        _round += 1
        random_break()

def get_recommendations(db_path, data_count, round):
    headers = get_headers()
    start = round * int(data_count)
    base_url = 'https://frodo.douban.com/api/v2/noviciate/mark_recommendations'
    custom_params = {
        'count': str(data_count),
        'start': str(start),
        'kind': 'movie'
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_movies_recommendations.json')
    init_movies_table(db_path)
    total_movie_before = get_total_movies_count(db_path)
    insert_movies(db_path, data)
    received_count = len(data.get('subjects'))
    total_movie_after = get_total_movies_count(db_path)
    replaced_movie_count = total_movie_before + received_count - total_movie_after
    log_message(f'-------- round: {round}, start: {start} --------','movie_log.txt')
    log_message(f'Total movie count: {total_movie_after}','movie_log.txt')
    log_message(f'Replaced movies count: {replaced_movie_count}','movie_log.txt')
    log_message(f'Response total:{data.get('total', start)}','movie_log.txt')
    log_message(f"{received_count} Data has been inserted into the SQLite database.",'movie_log.txt')

    if(start > data.get('total', start)):
        return False
    return True

if __name__ == '__main__':
    config = load_config()
    db_path = 'movies.db'
    data_count = config['data_count']
    # init database
    log_message("initiating database and generating seed data...",'movie_log.txt')
    get_recommendations(db_path, data_count, 0)

    while(get_random_unvisited(db_path, 'movies', 'id') is not None):
        movie_id = get_random_unvisited(db_path, 'movies', 'id')
        movie_title = from_id_get_data(db_path, 'movies', 'title', movie_id)
        log_message(f"working on movie id: {movie_id}, title: {movie_title}",'movie_log.txt')

        log_message(f"getting related movies and doulists for movie: {movie_title}",'movie_log.txt')
        get_related(db_path, movie_id)
        doulists = get_all_unvisited(db_path, 'doulists', 'id')
        for doulist_id in doulists:
            log_message(f"\tworking on doulist: {doulist_id}",'movie_log.txt')
            crawl_entire_doulist(db_path, data_count, doulist_id)
            mark_visited(db_path, 'doulists', 'id', doulist_id)

        log_message(f"getting related user comments for movie: {movie_title}",'movie_log.txt')
        get_interests(db_path, movie_id)
        users = get_all_unvisited(db_path, 'interests', 'user_id')
        for user_id in users:
            log_message(f"\tworking on user:{user_id}",'movie_log.txt')
            crawl_entire_user(db_path, data_count, user_id)
            mark_visited(db_path, 'interests', 'user_id', user_id)

        mark_visited(db_path, 'movies', 'id', movie_id)

