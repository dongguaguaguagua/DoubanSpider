import sqlite3
from datetime import datetime

def insert_books(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 插入数据
    for subject in data['subjects']:
        id = subject['id']
        title = subject['title']
        rating = subject['rating']['value']
        rating_count = subject['rating']['count']
        pubdate = ', '.join(subject['pubdate']) if subject['pubdate'] else None
        pages = ', '.join(subject['pages'])
        cover_url = subject['cover_url']
        sharing_url = subject['sharing_url']
        url = subject['url']
        author = ', '.join(subject['author']) if subject['author'] else None
        card_subtitle = subject['card_subtitle']
        book_subtitle = subject['book_subtitle']
        press = ', '.join(subject['press'])
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO books (id, title, rating, rating_count, pubdate, pages, cover_url, sharing_url, url, author, card_subtitle, book_subtitle, press, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, title, rating, rating_count, pubdate, pages, cover_url, sharing_url, url, author, card_subtitle, book_subtitle, press, update_time))

    conn.commit()
    conn.close()


def insert_small_books(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    for subject in data['subjects']:
        id = subject['id']
        title = subject['title']
        rating = subject['rating']['value']
        rating_count = subject['rating']['count']
        url = subject['url']
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO books (id, title, rating, rating_count, url, update_time)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, title, rating, rating_count, url, update_time))

    conn.commit()
    conn.close()

def insert_movies(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

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
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO movies (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, update_time))

    conn.commit()
    conn.close()

def insert_doulists(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    for subject in data['doulists']:
        id = subject['id']
        title = subject['title']
        cover_url = subject['cover_url']
        sharing_url = subject['sharing_url']
        url = subject['url']
        items_count = subject['items_count']
        followers_count = subject['followers_count']
        owner_id = subject['owner']['id']
        owner_uid = subject['owner']['uid']
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO doulists (id, title, cover_url, sharing_url, url, items_count, followers_count, owner_id, owner_uid, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, title, cover_url, sharing_url, url, items_count, followers_count, owner_id, owner_uid, update_time))

    conn.commit()
    conn.close()


def insert_interests(db_path, data):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    for subject in data['interests']:
        id = subject['id']
        comment = subject['comment']
        rating = subject['rating']['value'] if subject['rating'] != None else None
        sharing_url = subject['sharing_url']
        create_time = subject['create_time']
        user_id = subject['user']['id']
        user_gender = subject['user']['gender']
        user_name = subject['user']['name']
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO interests (id, comment, rating, sharing_url, create_time, user_id, user_gender, user_name, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, comment, rating, sharing_url, create_time, user_id, user_gender, user_name, update_time))

    conn.commit()
    conn.close()
