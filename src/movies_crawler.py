import requests
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
        'kind': 'movie'
    }
    url = build_url(base_url, custom_params)
    response = requests.get(url, headers=headers)
    data = response.json()
    save_data(data, 'latest_movie.json')

    init_movie_table('movies.db')

    total_movie_before = get_total_movies_count('movies.db')

    insert_movies('movies.db', data)

    received_count = len(data['subjects'])

    total_movie_after = get_total_movies_count('movies.db')

    replaced_movie_count = total_movie_before + received_count - total_movie_after

    print(f'-------- round: {round}, start: {start} --------')
    print(f'Total movie count: {total_movie_after}')
    print(f'Replaced movies count: {replaced_movie_count}')
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
#         is_continue = recommand_data(config=config, round=_round)
#         # sys.stdout.flush()  # 强制刷新输出缓冲区
#         _round += 1
#         time.sleep(20)
recommand_data(config=config, round=0)
