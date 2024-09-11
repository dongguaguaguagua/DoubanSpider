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
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO books (id, title, rating, rating_count, pubdate, pages, cover_url, sharing_url, url, author, card_subtitle, book_subtitle, press, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, title, rating, rating_count, pubdate, pages, cover_url, sharing_url, url, author, card_subtitle, book_subtitle, press, now))

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
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
        INSERT OR REPLACE INTO movies (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, title, rating, rating_count, pubdate, year, genres, durations, cover_url, sharing_url, countries, url, directors, actors, now))

    conn.commit()
    conn.close()

